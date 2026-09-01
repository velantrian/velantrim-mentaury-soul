"""CBP-v0.1 creation-time adapter over the existing P0-014 belief owner."""

from __future__ import annotations

from collections.abc import Mapping
from hashlib import sha256

from mentaury.beliefs import (
    CREATE_BELIEF,
    BeliefDecision,
    BeliefLifecycle,
    BeliefRejectionCode,
)
from mentaury.claims import ProvenanceClaimRecord
from mentaury.contracts import CommandEnvelope, PendingEvent, canonical_json

from .contracts import (
    BELIEF_CLAIM_BOUND,
    BELIEF_CLAIM_BOUND_SCHEMA,
    CANONICAL_PROFILE,
    CLAIM_BELIEF_BINDING_CONTRACT_VERSION,
    CREATE_BELIEF_FROM_CLAIM,
    CREATE_BELIEF_FROM_CLAIM_SCHEMA,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    INPUT_FINGERPRINT_DOMAIN,
    ClaimBeliefBinding,
    ClaimBeliefBindingBudget,
    ClaimBeliefBindingBudgetExceeded,
    ClaimBeliefBindingContractError,
    StatementEquivalence,
)

_COMMAND_KEYS = frozenset(
    {
        "belief_id",
        "statement",
        "claim_id",
        "claim_record_fingerprint",
        "claim_type",
    }
)


class ClaimBoundBeliefLifecycle:
    """Bind exact PCR identity while delegating belief creation to P0-014.

    This is deliberately an adapter, not a BeliefLifecycle subtype: claim-bound
    creation requires an exact PCR record and a bounded evaluation budget, so it
    cannot satisfy the base two-argument lifecycle contract.
    """

    def __init__(self, belief_lifecycle: BeliefLifecycle | None = None) -> None:
        self._belief_lifecycle = belief_lifecycle or BeliefLifecycle()

    def decide(
        self,
        command: CommandEnvelope,
        state: Mapping[str, object],
        *,
        record: ProvenanceClaimRecord,
        budget: ClaimBeliefBindingBudget,
    ) -> BeliefDecision:
        if not isinstance(command, CommandEnvelope):
            raise TypeError("command must be a CommandEnvelope")
        if not isinstance(state, Mapping):
            raise TypeError("state must be a mapping")
        if type(record) is not ProvenanceClaimRecord:
            raise TypeError("record must be exact ProvenanceClaimRecord")
        if type(budget) is not ClaimBeliefBindingBudget:
            raise TypeError("budget must be exact ClaimBeliefBindingBudget")

        belief_id = _payload_string(command.payload, "belief_id")
        if belief_id is None:
            return self._belief_lifecycle._reject(  # noqa: SLF001
                command,
                command.target_stream,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "CREATE_BELIEF_FROM_CLAIM requires belief_id",
            )
        if command.command_type != CREATE_BELIEF_FROM_CLAIM:
            return self._belief_lifecycle._reject(  # noqa: SLF001
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                f"unsupported command_type: {command.command_type}",
            )
        if command.command_schema != CREATE_BELIEF_FROM_CLAIM_SCHEMA:
            return self._belief_lifecycle._reject(  # noqa: SLF001
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "CREATE_BELIEF_FROM_CLAIM command_schema must be exact",
            )
        if frozenset(command.payload) != _COMMAND_KEYS:
            return self._belief_lifecycle._reject(  # noqa: SLF001
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "CREATE_BELIEF_FROM_CLAIM payload keys must be exact",
            )

        statement = _payload_string(command.payload, "statement")
        claim_id = _payload_string(command.payload, "claim_id")
        record_fingerprint = _payload_string(
            command.payload,
            "claim_record_fingerprint",
        )
        claim_type = _payload_string(command.payload, "claim_type")
        if None in (statement, claim_id, record_fingerprint, claim_type):
            return self._belief_lifecycle._reject(  # noqa: SLF001
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "CREATE_BELIEF_FROM_CLAIM requires exact non-empty string fields",
            )
        assert statement is not None
        assert claim_id is not None
        assert record_fingerprint is not None
        assert claim_type is not None

        if claim_id != record.claim.claim_id:
            return self._belief_lifecycle._reject(  # noqa: SLF001
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "claim_id does not match the exact PCR record",
            )
        if record_fingerprint != record.input_fingerprint:
            return self._belief_lifecycle._reject(  # noqa: SLF001
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "claim_record_fingerprint does not match the exact PCR record",
            )
        if claim_type != record.claim.claim_type.value:
            return self._belief_lifecycle._reject(  # noqa: SLF001
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "claim_type does not match the exact PCR record",
            )

        _check_local_string_budget(statement, "statement", budget)
        _check_local_string_budget(belief_id, "belief_id", budget)
        _check_local_string_budget(claim_id, "claim_id", budget)
        _check_local_string_budget(record_fingerprint, "claim_record_fingerprint", budget)
        _check_local_string_budget(record.claim.statement_ref, "statement_ref", budget)

        binding_fingerprint = _binding_input_fingerprint(
            command=command,
            record=record,
            budget=budget,
        )
        binding = ClaimBeliefBinding(
            contract_version=CLAIM_BELIEF_BINDING_CONTRACT_VERSION,
            belief_id=belief_id,
            belief_revision=1,
            claim_id=claim_id,
            claim_record_fingerprint=record_fingerprint,
            claim_type=record.claim.claim_type,
            statement_ref=record.claim.statement_ref,
            statement_equivalence=StatementEquivalence.NOT_ESTABLISHED,
            binding_input_fingerprint=binding_fingerprint,
        )

        delegated = CommandEnvelope(
            command_id=command.command_id,
            command_type=CREATE_BELIEF,
            command_schema="create-belief/v1",
            target_stream=command.target_stream,
            expected_stream_version=command.expected_stream_version,
            issued_at=command.issued_at,
            issuer=command.issuer,
            authority=command.authority,
            correlation_id=command.correlation_id,
            idempotency_key=command.idempotency_key,
            payload={
                "belief_id": belief_id,
                "statement": statement,
                "claim_type": claim_type,
            },
        )
        base_decision = self._belief_lifecycle.decide(delegated, state)
        if not base_decision.accepted:
            if base_decision.rejection_code is None or base_decision.message is None:
                raise AssertionError("P0-014 rejection must carry code and message")
            return self._belief_lifecycle._reject(  # noqa: SLF001
                command,
                belief_id,
                state,
                base_decision.rejection_code,
                base_decision.message,
            )
        if len(base_decision.domain_events) != 1:
            raise AssertionError("P0-014 CREATE_BELIEF must emit exactly one event")

        binding_event = PendingEvent(
            BELIEF_CLAIM_BOUND,
            BELIEF_CLAIM_BOUND_SCHEMA,
            True,
            binding.to_value(),
        )
        return BeliefDecision(
            accepted=True,
            domain_events=(base_decision.domain_events[0], binding_event),
        )


def _payload_string(mapping: Mapping[str, object], key: str) -> str | None:
    value = mapping.get(key)
    if type(value) is not str or not value or value != value.strip():
        return None
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return None
    return value


def _check_local_string_budget(
    value: str,
    name: str,
    budget: ClaimBeliefBindingBudget,
) -> None:
    if len(value.encode("utf-8")) > budget.max_string_bytes:
        raise ClaimBeliefBindingBudgetExceeded(
            f"{name} exceeds local max_string_bytes"
        )


def _binding_input_fingerprint(
    *,
    command: CommandEnvelope,
    record: ProvenanceClaimRecord,
    budget: ClaimBeliefBindingBudget,
) -> str:
    if canonical_json.PROFILE_NAME != CANONICAL_PROFILE:
        raise ClaimBeliefBindingContractError(
            "STOP_AND_RECONCILE: canonical JSON profile drift"
        )
    try:
        encoded = canonical_json.canonical_json_bytes(
            {
                "contract_version": CLAIM_BELIEF_BINDING_CONTRACT_VERSION,
                "command": {
                    "command_id": command.command_id,
                    "command_type": command.command_type,
                    "command_schema": command.command_schema,
                    "target_stream": command.target_stream,
                    "expected_stream_version": command.expected_stream_version,
                    "payload": dict(command.payload),
                },
                "record": record.to_value(),
                "statement_equivalence": StatementEquivalence.NOT_ESTABLISHED.value,
                "budget": budget.to_value(),
            }
        )
    except (TypeError, ValueError) as exc:
        raise ClaimBeliefBindingContractError(
            "canonicalization failed for admitted CBP-v0.1 input"
        ) from exc
    if len(encoded) > HARD_MAX_CANONICAL_INPUT_BYTES:
        raise ClaimBeliefBindingContractError(
            "canonical input exceeds HARD_MAX_CANONICAL_INPUT_BYTES"
        )
    if len(encoded) > budget.max_canonical_input_bytes:
        raise ClaimBeliefBindingBudgetExceeded(
            "canonical input exceeds local max_canonical_input_bytes"
        )
    return sha256(
        INPUT_FINGERPRINT_DOMAIN.encode("ascii") + b"\x00" + encoded
    ).hexdigest()
