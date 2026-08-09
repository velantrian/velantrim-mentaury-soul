"""P0-015 pure belief decision layer backed by deterministic evidence receipts."""

from __future__ import annotations

from collections.abc import Mapping

from mentaury.contracts import CommandEnvelope, PendingEvent, canonical_timestamp
from mentaury.evidence import (
    APPLY_EVIDENCE_GATE,
    BELIEF_EVIDENCE_GATED,
    BELIEF_EVIDENCE_GATED_SCHEMA,
    DEFAULT_EVIDENCE_GATE_POLICIES,
    EVIDENCE_GATE_DECISION_SCHEMA,
    EVIDENCE_GATE_REJECTED,
    EvidenceGate,
    EvidenceGateDecision,
    EvidenceGateError,
    EvidenceGateOutcome,
    EvidenceGatePolicyRegistry,
    EvidenceGateReceipt,
    EvidenceGateRejectionCode,
    records_from_value,
)

from .contracts import BeliefStatus, ClaimType, belief_stream_id

_COMMAND_KEYS = frozenset({"belief_id", "expected_revision", "policy_id", "records"})


class EvidenceGatedBeliefLifecycle:
    """Evaluate one P0-015 gate command without persistence or authority lookup."""

    def __init__(
        self,
        gate: EvidenceGate | None = None,
        policies: EvidenceGatePolicyRegistry = DEFAULT_EVIDENCE_GATE_POLICIES,
    ) -> None:
        if gate is not None and not isinstance(gate, EvidenceGate):
            raise TypeError("gate must be an EvidenceGate or None")
        if not isinstance(policies, EvidenceGatePolicyRegistry):
            raise TypeError("policies must be an EvidenceGatePolicyRegistry")
        self._gate = gate or EvidenceGate()
        self._policies = policies

    def decide(
        self,
        command: CommandEnvelope,
        state: Mapping[str, object],
    ) -> EvidenceGateDecision:
        if not isinstance(command, CommandEnvelope):
            raise TypeError("command must be a CommandEnvelope")
        if not isinstance(state, Mapping):
            raise TypeError("state must be a mapping")
        belief_id = _optional_string(command.payload, "belief_id")
        if belief_id is None:
            return self._reject(
                command,
                command.target_stream,
                state,
                EvidenceGateRejectionCode.INVALID_COMMAND,
                "command payload requires belief_id",
            )
        if command.target_stream != belief_stream_id(belief_id):
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.TARGET_STREAM_MISMATCH,
                "target_stream must equal belief:<belief_id>",
            )
        if command.command_type != APPLY_EVIDENCE_GATE:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.INVALID_COMMAND,
                f"unsupported command_type: {command.command_type}",
            )
        payload_keys = frozenset(command.payload)
        if payload_keys != _COMMAND_KEYS:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.INVALID_COMMAND,
                "gate command payload keys must be exact",
            )
        if state.get("belief_id") is None or _revision(state) == 0:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.BELIEF_NOT_FOUND,
                "belief does not exist",
            )
        if state.get("belief_id") != belief_id:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.INVALID_COMMAND,
                "state belief_id does not match command",
            )
        current_status = _status(state)
        if current_status in {
            BeliefStatus.SUPPORTED,
            BeliefStatus.CONTRADICTED,
            BeliefStatus.SUPERSEDED,
        }:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.TERMINAL_BELIEF,
                f"{current_status.value} belief is terminal for P0-015",
            )
        requested_revision = command.payload.get("expected_revision")
        if (
            isinstance(requested_revision, bool)
            or not isinstance(requested_revision, int)
            or requested_revision <= 0
        ):
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.INVALID_COMMAND,
                "APPLY_EVIDENCE_GATE requires positive expected_revision",
            )
        current_revision = _revision(state)
        if requested_revision != current_revision:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.REVISION_CONFLICT,
                "expected_revision does not match current belief revision",
            )
        policy_id = _optional_string(command.payload, "policy_id")
        policy = self._policies.get(policy_id or "")
        if policy is None:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.POLICY_NOT_APPROVED,
                "command references an unapproved evidence-gate policy",
            )
        try:
            claim_type = ClaimType(_required_state_string(state, "claim_type"))
        except ValueError:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.INVALID_COMMAND,
                "belief projection contains an unsupported claim type",
            )
        if claim_type not in policy.allowed_claim_types:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.CLAIM_TYPE_NOT_ALLOWED,
                f"policy {policy.policy_id} does not allow {claim_type.value} claims",
            )
        try:
            evaluated_at = canonical_timestamp(command.issued_at)
            records = records_from_value(command.payload.get("records"))
            receipt = self._gate.evaluate(
                belief_id=belief_id,
                belief_revision=current_revision,
                claim_type=claim_type,
                statement=_required_state_string(state, "statement"),
                evidence_for=_state_strings(state, "evidence_for"),
                evidence_against=_state_strings(state, "evidence_against"),
                records=records,
                policy=policy,
                evaluated_at=evaluated_at,
            )
        except (EvidenceGateError, TypeError, ValueError) as exc:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.INVALID_EVIDENCE_SET,
                str(exc),
            )

        if receipt.outcome is EvidenceGateOutcome.CONFLICT:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.CONFLICT,
                "qualifying evidence exists on both sides; fail-closed conflict",
                receipt=receipt,
            )
        if receipt.outcome is EvidenceGateOutcome.INCONCLUSIVE:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.INCONCLUSIVE,
                "neither evidence side satisfies the approved policy",
                receipt=receipt,
            )

        contradictions = _state_objects(state, "contradictions")
        open_contradictions = tuple(
            item for item in contradictions if item.get("addressed_in_revision") is None
        )
        if receipt.outcome is EvidenceGateOutcome.SUPPORTED and open_contradictions:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.OPEN_CONTRADICTIONS,
                "supported status requires no open contradictions",
                receipt=receipt,
            )
        if receipt.outcome is EvidenceGateOutcome.CONTRADICTED and not open_contradictions:
            return self._reject(
                command,
                belief_id,
                state,
                EvidenceGateRejectionCode.CONTRADICTION_REQUIRED,
                "contradicted status requires an open registered contradiction",
                receipt=receipt,
            )

        new_status = BeliefStatus(receipt.outcome.value)
        sorted_records = sorted(records, key=lambda item: item.evidence_ref)
        event = PendingEvent(
            BELIEF_EVIDENCE_GATED,
            BELIEF_EVIDENCE_GATED_SCHEMA,
            True,
            {
                "belief_id": belief_id,
                "previous_revision": current_revision,
                "new_revision": current_revision + 1,
                "claim_type": claim_type.value,
                "statement": _required_state_string(state, "statement"),
                "previous_status": current_status.value,
                "new_status": new_status.value,
                "evaluated_at": receipt.evaluated_at,
                "policy": policy.to_value(),
                "records": [record.to_value() for record in sorted_records],
                "receipt": receipt.to_value(),
            },
        )
        return EvidenceGateDecision(True, (event,), receipt=receipt)

    def _reject(
        self,
        command: CommandEnvelope,
        belief_id: str,
        state: Mapping[str, object],
        code: EvidenceGateRejectionCode,
        message: str,
        *,
        receipt: EvidenceGateReceipt | None = None,
    ) -> EvidenceGateDecision:
        current_revision = _revision(state)
        requested_revision = command.payload.get("expected_revision", 0)
        if (
            isinstance(requested_revision, bool)
            or not isinstance(requested_revision, int)
            or requested_revision < 0
        ):
            requested_revision = 0
        payload: dict[str, object] = {
            "command_id": command.command_id,
            "command_type": command.command_type,
            "belief_id": belief_id,
            "rejection_code": code.value,
            "message": message or code.value,
            "expected_stream_version": command.expected_stream_version,
            "current_belief_revision": current_revision,
            "requested_belief_revision": requested_revision,
        }
        if receipt is not None:
            payload["receipt"] = receipt.to_value()
        audit = PendingEvent(
            EVIDENCE_GATE_REJECTED,
            EVIDENCE_GATE_DECISION_SCHEMA,
            False,
            payload,
        )
        return EvidenceGateDecision(
            False,
            (),
            receipt=receipt,
            audit_event=audit,
            rejection_code=code,
            message=message,
        )


def _optional_string(mapping: Mapping[str, object], key: str) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        return None
    return value


def _revision(state: Mapping[str, object]) -> int:
    value = state.get("revision", 0)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("state revision must be a non-negative integer")
    return value


def _status(state: Mapping[str, object]) -> BeliefStatus:
    value = state.get("status")
    if not isinstance(value, str):
        raise ValueError("existing belief state requires status")
    return BeliefStatus(value)


def _required_state_string(state: Mapping[str, object], key: str) -> str:
    value = state.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"state {key} must be a non-empty string")
    return value


def _state_strings(state: Mapping[str, object], key: str) -> tuple[str, ...]:
    value = state.get(key)
    if not isinstance(value, (tuple, list)) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise ValueError(f"state {key} must be a string sequence")
    result = tuple(value)
    if len(set(result)) != len(result):
        raise ValueError(f"state {key} must not contain duplicates")
    return result


def _state_objects(
    state: Mapping[str, object],
    key: str,
) -> tuple[Mapping[str, object], ...]:
    value = state.get(key)
    if not isinstance(value, (tuple, list)) or any(
        not isinstance(item, Mapping) for item in value
    ):
        raise ValueError(f"state {key} must be an object sequence")
    return tuple(value)
