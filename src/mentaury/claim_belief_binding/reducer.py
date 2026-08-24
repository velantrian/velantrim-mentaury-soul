"""CBP-v0.1 replay projection layered over P0-014/P0-015 belief reducers."""

from __future__ import annotations

from collections.abc import Mapping

from mentaury.beliefs import BeliefReducerError, ClaimType, belief_stream_id
from mentaury.beliefs.gated_reducer import EvidenceGatedBeliefReducer
from mentaury.contracts import EventEnvelope
from mentaury.contracts.primitives import FrozenPayload

from .contracts import (
    BELIEF_CLAIM_BOUND,
    BELIEF_CLAIM_BOUND_SCHEMA,
    CLAIM_BELIEF_BINDING_CONTRACT_VERSION,
    StatementEquivalence,
)

_BINDING_KEYS = frozenset(
    {
        "contract_version",
        "belief_id",
        "belief_revision",
        "claim_id",
        "claim_record_fingerprint",
        "claim_type",
        "statement_ref",
        "statement_equivalence",
        "binding_input_fingerprint",
    }
)


class ClaimBoundBeliefReducer(EvidenceGatedBeliefReducer):
    """Version 3 projection that retains optional PCR genesis binding."""

    reducer_id = "mentaury-belief-projection"
    reducer_version = "3"
    supported_event_schemas = (
        EvidenceGatedBeliefReducer.supported_event_schemas
        | frozenset({(BELIEF_CLAIM_BOUND, BELIEF_CLAIM_BOUND_SCHEMA)})
    )

    def initial_state(self) -> Mapping[str, object]:
        state = dict(super().initial_state())
        state["claim_binding"] = None
        return state

    def apply(
        self,
        state: FrozenPayload,
        event: EventEnvelope,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        if (event.event_type, event.payload_schema) == (
            BELIEF_CLAIM_BOUND,
            BELIEF_CLAIM_BOUND_SCHEMA,
        ):
            return self._claim_bound(state, event, payload)
        result = dict(super().apply(state, event, payload))
        result["claim_binding"] = state.get("claim_binding")
        return result

    def _claim_bound(
        self,
        state: FrozenPayload,
        event: EventEnvelope,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        if frozenset(payload) != _BINDING_KEYS:
            raise BeliefReducerError("binding event payload keys must be exact")
        belief_id = _state_string(state, "belief_id")
        if event.stream_id != belief_stream_id(belief_id):
            raise BeliefReducerError("binding event stream_id does not match belief")
        if not event.affects_domain_state:
            raise BeliefReducerError("binding event must affect domain state")
        if _payload_string(payload, "belief_id") != belief_id:
            raise BeliefReducerError(
                "binding event belief_id does not match projection"
            )
        if _state_integer(state, "revision") != 1:
            raise BeliefReducerError(
                "claim binding is allowed only at belief genesis revision 1"
            )
        if state.get("claim_binding") is not None:
            raise BeliefReducerError("belief already has a claim binding")
        if _payload_integer(payload, "belief_revision") != 1:
            raise BeliefReducerError("binding belief_revision must equal 1")
        if (
            _payload_string(payload, "contract_version")
            != CLAIM_BELIEF_BINDING_CONTRACT_VERSION
        ):
            raise BeliefReducerError("unsupported claim-binding contract version")
        if (
            _payload_string(payload, "statement_equivalence")
            != StatementEquivalence.NOT_ESTABLISHED.value
        ):
            raise BeliefReducerError(
                "CBP-v0.1 cannot claim concrete statement equivalence"
            )

        claim_type = _payload_claim_type(payload)
        if claim_type.value != _state_string(state, "claim_type"):
            raise BeliefReducerError(
                "binding claim_type does not match belief projection"
            )
        _payload_string(payload, "claim_id")
        _payload_string(payload, "statement_ref")
        _payload_sha256(payload, "claim_record_fingerprint")
        _payload_sha256(payload, "binding_input_fingerprint")

        copied = dict(state)
        copied["claim_binding"] = {
            "contract_version": CLAIM_BELIEF_BINDING_CONTRACT_VERSION,
            "belief_id": belief_id,
            "belief_revision": 1,
            "claim_id": _payload_string(payload, "claim_id"),
            "claim_record_fingerprint": _payload_sha256(
                payload,
                "claim_record_fingerprint",
            ),
            "claim_type": claim_type.value,
            "statement_ref": _payload_string(payload, "statement_ref"),
            "statement_equivalence": StatementEquivalence.NOT_ESTABLISHED.value,
            "binding_input_fingerprint": _payload_sha256(
                payload,
                "binding_input_fingerprint",
            ),
            "binding_event_id": event.event_id,
        }
        return copied


def _state_string(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise BeliefReducerError(f"state {key} must be a non-empty string")
    return value


def _state_integer(mapping: Mapping[str, object], key: str) -> int:
    value = mapping.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise BeliefReducerError(f"state {key} must be an integer")
    return value


def _payload_string(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value or value != value.strip():
        raise BeliefReducerError(
            f"payload {key} must be a non-empty unpadded string"
        )
    return value


def _payload_integer(mapping: Mapping[str, object], key: str) -> int:
    value = mapping.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise BeliefReducerError(f"payload {key} must be an integer")
    return value


def _payload_sha256(mapping: Mapping[str, object], key: str) -> str:
    value = _payload_string(mapping, key)
    if len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise BeliefReducerError(f"payload {key} must be lowercase sha256 hex")
    return value


def _payload_claim_type(mapping: Mapping[str, object]) -> ClaimType:
    try:
        return ClaimType(_payload_string(mapping, "claim_type"))
    except ValueError as exc:
        raise BeliefReducerError("binding claim_type is unsupported") from exc
