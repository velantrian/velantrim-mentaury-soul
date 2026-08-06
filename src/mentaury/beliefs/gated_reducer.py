"""P0-015 reducer that re-computes Evidence Gate receipts during replay."""

from __future__ import annotations

from collections.abc import Mapping

from mentaury.contracts import EventEnvelope, canonical_json_bytes, canonical_timestamp
from mentaury.contracts.primitives import FrozenPayload
from mentaury.evidence import (
    BELIEF_EVIDENCE_GATED,
    BELIEF_EVIDENCE_GATED_SCHEMA,
    DEFAULT_EVIDENCE_GATE_POLICIES,
    EvidenceGate,
    EvidenceGateError,
    EvidenceGateOutcome,
    EvidenceGatePolicyRegistry,
    policy_from_value,
    records_from_value,
)

from .contracts import BeliefStatus, ClaimType
from .reducer import BeliefReducer, BeliefReducerError


class EvidenceGatedBeliefReducer(BeliefReducer):
    """Version 2 projection with replay-verifiable gated terminal statuses."""

    reducer_id = "mentaury-belief-projection"
    reducer_version = "2"
    supported_event_schemas = BeliefReducer.supported_event_schemas | frozenset(
        {(BELIEF_EVIDENCE_GATED, BELIEF_EVIDENCE_GATED_SCHEMA)}
    )

    def __init__(
        self,
        gate: EvidenceGate | None = None,
        policies: EvidenceGatePolicyRegistry = DEFAULT_EVIDENCE_GATE_POLICIES,
    ) -> None:
        if not isinstance(policies, EvidenceGatePolicyRegistry):
            raise TypeError("policies must be an EvidenceGatePolicyRegistry")
        self._gate = gate or EvidenceGate()
        self._policies = policies

    def apply(
        self,
        state: FrozenPayload,
        event: EventEnvelope,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        if (
            event.event_type,
            event.payload_schema,
        ) != (BELIEF_EVIDENCE_GATED, BELIEF_EVIDENCE_GATED_SCHEMA):
            return super().apply(state, event, payload)
        return self._evidence_gated(state, event, payload)

    def _evidence_gated(
        self,
        state: FrozenPayload,
        event: EventEnvelope,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        belief_id = _state_string(state, "belief_id")
        if _payload_string(payload, "belief_id") != belief_id:
            raise BeliefReducerError("gate event belief_id does not match projection")
        current_revision = _state_integer(state, "revision")
        previous_revision = _payload_integer(payload, "previous_revision")
        new_revision = _payload_integer(payload, "new_revision")
        if previous_revision != current_revision or new_revision != current_revision + 1:
            raise BeliefReducerError("gate event revision sequence is invalid")
        statement = _state_string(state, "statement")
        if _payload_string(payload, "statement") != statement:
            raise BeliefReducerError("gate event statement does not match projection")
        claim_type = _state_claim_type(state)
        if _payload_string(payload, "claim_type") != claim_type.value:
            raise BeliefReducerError("gate event claim_type does not match projection")
        previous_status = BeliefStatus(_state_string(state, "status"))
        if _payload_string(payload, "previous_status") != previous_status.value:
            raise BeliefReducerError("gate event previous_status does not match projection")
        if previous_status in {
            BeliefStatus.SUPPORTED,
            BeliefStatus.CONTRADICTED,
            BeliefStatus.SUPERSEDED,
        }:
            raise BeliefReducerError("terminal belief cannot be evidence-gated again")
        try:
            event_evaluated_at = canonical_timestamp(event.occurred_at)
            payload_evaluated_at = canonical_timestamp(
                _payload_string(payload, "evaluated_at")
            )
        except (TypeError, ValueError) as exc:
            raise BeliefReducerError("invalid gate evaluation timestamp") from exc
        if payload_evaluated_at != event_evaluated_at:
            raise BeliefReducerError(
                "gate evaluated_at must equal immutable event occurred_at"
            )

        try:
            policy = policy_from_value(payload.get("policy"))
            approved_policy = self._policies.require(policy.policy_id)
            if canonical_json_bytes(policy.to_value()) != canonical_json_bytes(
                approved_policy.to_value()
            ):
                raise EvidenceGateError(
                    "event policy does not match the approved policy registry"
                )
            if claim_type not in approved_policy.allowed_claim_types:
                raise EvidenceGateError(
                    f"approved policy does not allow claim type {claim_type.value}"
                )
            records = records_from_value(payload.get("records"))
            normalized_records = [
                record.to_value()
                for record in sorted(records, key=lambda item: item.evidence_ref)
            ]
            if canonical_json_bytes(payload.get("records")) != canonical_json_bytes(
                normalized_records
            ):
                raise EvidenceGateError(
                    "event records must be sorted and use exact canonical fields"
                )
            receipt_value = payload.get("receipt")
            if not isinstance(receipt_value, Mapping):
                raise EvidenceGateError("receipt must be an object")
            receipt = self._gate.verify_receipt(
                receipt_value,
                belief_id=belief_id,
                belief_revision=current_revision,
                claim_type=claim_type,
                statement=statement,
                evidence_for=_state_strings(state, "evidence_for"),
                evidence_against=_state_strings(state, "evidence_against"),
                records=records,
                policy=approved_policy,
                evaluated_at=payload_evaluated_at,
            )
        except (EvidenceGateError, KeyError, TypeError, ValueError) as exc:
            raise BeliefReducerError(f"invalid evidence-gate receipt: {exc}") from exc
        if receipt.outcome not in {
            EvidenceGateOutcome.SUPPORTED,
            EvidenceGateOutcome.CONTRADICTED,
        }:
            raise BeliefReducerError("non-terminal gate outcome cannot mutate belief")
        new_status = BeliefStatus(_payload_string(payload, "new_status"))
        if new_status.value != receipt.outcome.value:
            raise BeliefReducerError("new_status does not match gate outcome")

        contradictions = [dict(item) for item in _state_objects(state, "contradictions")]
        open_contradictions = [
            item for item in contradictions if item.get("addressed_in_revision") is None
        ]
        if new_status is BeliefStatus.SUPPORTED and open_contradictions:
            raise BeliefReducerError("supported status requires no open contradictions")
        if new_status is BeliefStatus.CONTRADICTED and not open_contradictions:
            raise BeliefReducerError(
                "contradicted status requires an open registered contradiction"
            )

        history = [dict(item) for item in _state_objects(state, "history")]
        history.append(
            {
                "revision": new_revision,
                "event_id": event.event_id,
                "statement": statement,
                "status": new_status.value,
                "reason": "P0-015 approved evidence gate",
                "evidence_refs": sorted(
                    set(_state_strings(state, "evidence_for")).union(
                        _state_strings(state, "evidence_against")
                    )
                ),
                "addressed_contradiction_ids": [],
                "gate_receipt_digest": receipt.receipt_digest,
                "gate_policy_id": receipt.policy_id,
                "gate_policy_digest": receipt.policy_digest,
                "gate_evidence_set_digest": receipt.evidence_set_digest,
                "gate_evaluated_at": receipt.evaluated_at,
            }
        )
        copied = {
            "belief_id": state["belief_id"],
            "statement": state["statement"],
            "claim_type": state["claim_type"],
            "status": new_status.value,
            "revision": new_revision,
            "origin_event_id": state["origin_event_id"],
            "evidence_for": list(_state_strings(state, "evidence_for")),
            "evidence_against": list(_state_strings(state, "evidence_against")),
            "contradictions": contradictions,
            "history": history,
        }
        if canonical_json_bytes(receipt.to_value()) != canonical_json_bytes(
            dict(payload["receipt"])
        ):
            raise BeliefReducerError("receipt changed after successful verification")
        return copied


def _state_string(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise BeliefReducerError(f"state {key} must be a non-empty string")
    return value


def _payload_string(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise BeliefReducerError(f"payload {key} must be a non-empty string")
    return value


def _state_integer(mapping: Mapping[str, object], key: str) -> int:
    value = mapping.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise BeliefReducerError(f"state {key} must be an integer")
    return value


def _payload_integer(mapping: Mapping[str, object], key: str) -> int:
    value = mapping.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise BeliefReducerError(f"payload {key} must be an integer")
    return value


def _state_claim_type(mapping: Mapping[str, object]) -> ClaimType:
    try:
        return ClaimType(_state_string(mapping, "claim_type"))
    except ValueError as exc:
        raise BeliefReducerError("state claim_type is unsupported") from exc


def _state_strings(mapping: Mapping[str, object], key: str) -> tuple[str, ...]:
    value = mapping.get(key)
    if not isinstance(value, tuple) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise BeliefReducerError(f"state {key} must be an immutable string sequence")
    if len(set(value)) != len(value):
        raise BeliefReducerError(f"state {key} must not contain duplicates")
    return value


def _state_objects(
    mapping: Mapping[str, object],
    key: str,
) -> tuple[Mapping[str, object], ...]:
    value = mapping.get(key)
    if not isinstance(value, tuple) or any(
        not isinstance(item, Mapping) for item in value
    ):
        raise BeliefReducerError(f"state {key} must be an immutable object sequence")
    return value
