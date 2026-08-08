"""Pure versioned reducer for the P0-014 belief projection."""

from __future__ import annotations

from collections.abc import Mapping

from mentaury.contracts import EventEnvelope
from mentaury.contracts.primitives import FrozenPayload

from .contracts import (
    BELIEF_CREATED,
    BELIEF_CREATED_SCHEMA,
    BELIEF_REVISED,
    BELIEF_REVISED_SCHEMA,
    CONTRADICTION_REGISTERED,
    CONTRADICTION_REGISTERED_SCHEMA,
    EVIDENCE_ATTACHED,
    EVIDENCE_ATTACHED_SCHEMA,
    BeliefStatus,
    ClaimType,
    EvidenceSide,
    belief_status_requires_evidence_gate,
    belief_status_transition_allowed,
)


class BeliefReducerError(ValueError):
    """Raised when committed belief history violates lifecycle invariants."""


class BeliefReducer:
    reducer_id = "mentaury-belief-projection"
    reducer_version = "1"
    supported_event_schemas = frozenset(
        {
            (BELIEF_CREATED, BELIEF_CREATED_SCHEMA),
            (EVIDENCE_ATTACHED, EVIDENCE_ATTACHED_SCHEMA),
            (CONTRADICTION_REGISTERED, CONTRADICTION_REGISTERED_SCHEMA),
            (BELIEF_REVISED, BELIEF_REVISED_SCHEMA),
        }
    )

    def initial_state(self) -> Mapping[str, object]:
        return {
            "belief_id": None,
            "statement": None,
            "claim_type": None,
            "status": None,
            "revision": 0,
            "origin_event_id": None,
            "evidence_for": [],
            "evidence_against": [],
            "contradictions": [],
            "history": [],
        }

    def apply(
        self,
        state: FrozenPayload,
        event: EventEnvelope,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        pair = (event.event_type, event.payload_schema)
        if pair not in self.supported_event_schemas:
            raise BeliefReducerError(f"unsupported belief event/schema: {pair!r}")
        if event.event_type == BELIEF_CREATED:
            return self._created(state, event, payload)
        if event.event_type == EVIDENCE_ATTACHED:
            return self._evidence(state, payload)
        if event.event_type == CONTRADICTION_REGISTERED:
            return self._contradiction(state, payload)
        if event.event_type == BELIEF_REVISED:
            return self._revised(state, event, payload)
        raise BeliefReducerError(f"unsupported belief event: {event.event_type}")

    def _created(
        self,
        state: FrozenPayload,
        event: EventEnvelope,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        if state["revision"] != 0 or state["belief_id"] is not None:
            raise BeliefReducerError("BELIEF_CREATED requires an empty projection")
        belief_id = _string(payload, "belief_id")
        statement = _string(payload, "statement")
        claim_type = _enum_value(ClaimType, payload, "claim_type")
        status = _enum_value(BeliefStatus, payload, "status")
        revision = _integer(payload, "revision")
        if status is not BeliefStatus.HYPOTHESIS or revision != 1:
            raise BeliefReducerError(
                "BELIEF_CREATED must start at hypothesis revision 1"
            )
        return {
            "belief_id": belief_id,
            "statement": statement,
            "claim_type": claim_type.value,
            "status": status.value,
            "revision": revision,
            "origin_event_id": event.event_id,
            "evidence_for": [],
            "evidence_against": [],
            "contradictions": [],
            "history": [
                {
                    "revision": 1,
                    "event_id": event.event_id,
                    "statement": statement,
                    "status": status.value,
                    "reason": "belief created",
                    "evidence_refs": [],
                    "addressed_contradiction_ids": [],
                }
            ],
        }

    def _evidence(
        self,
        state: FrozenPayload,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        _require_existing(state, payload)
        _require_non_terminal(state)
        evidence_ref = _string(payload, "evidence_ref")
        side = _enum_value(EvidenceSide, payload, "side")
        evidence_for = list(_strings(state, "evidence_for"))
        evidence_against = list(_strings(state, "evidence_against"))
        if evidence_ref in evidence_for or evidence_ref in evidence_against:
            raise BeliefReducerError("evidence reference is already attached")
        if side is EvidenceSide.FOR:
            evidence_for.append(evidence_ref)
        else:
            evidence_against.append(evidence_ref)
        return _copy_state(
            state,
            evidence_for=evidence_for,
            evidence_against=evidence_against,
        )

    def _contradiction(
        self,
        state: FrozenPayload,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        _require_existing(state, payload)
        _require_non_terminal(state)
        contradiction_id = _string(payload, "contradiction_id")
        evidence_refs = list(_strings(payload, "evidence_refs"))
        attached = set(_strings(state, "evidence_for")) | set(
            _strings(state, "evidence_against")
        )
        if not evidence_refs or not set(evidence_refs).issubset(attached):
            raise BeliefReducerError(
                "contradiction evidence must already be attached to belief"
            )
        contradictions = [dict(item) for item in _objects(state, "contradictions")]
        if any(item["contradiction_id"] == contradiction_id for item in contradictions):
            raise BeliefReducerError("contradiction_id must be unique")
        resulting_status = _enum_value(
            BeliefStatus,
            payload,
            "resulting_status",
        )
        # После _require_non_terminal() CONTRADICTED недоступен; ожидаем
        # только детерминированный CONTESTED.
        if resulting_status is not BeliefStatus.CONTESTED:
            raise BeliefReducerError("invalid contradiction resulting_status")
        contradictions.append(
            {
                "contradiction_id": contradiction_id,
                "statement": _string(payload, "statement"),
                "evidence_refs": evidence_refs,
                "addressed_in_revision": None,
            }
        )
        return _copy_state(
            state,
            status=resulting_status.value,
            contradictions=contradictions,
        )

    def _revised(
        self,
        state: FrozenPayload,
        event: EventEnvelope,
        payload: FrozenPayload,
    ) -> Mapping[str, object]:
        _require_existing(state, payload)
        previous_revision = _integer(payload, "previous_revision")
        new_revision = _integer(payload, "new_revision")
        current_revision = _integer(state, "revision")
        if previous_revision != current_revision or new_revision != current_revision + 1:
            raise BeliefReducerError("belief revision sequence is invalid")
        previous_statement = _string(payload, "previous_statement")
        previous_status = _enum_value(BeliefStatus, payload, "previous_status")
        if previous_statement != _string(state, "statement"):
            raise BeliefReducerError("previous_statement does not match projection")
        if previous_status.value != _string(state, "status"):
            raise BeliefReducerError("previous_status does not match projection")
        _require_non_terminal(state)

        evidence_refs = list(_strings(payload, "evidence_refs"))
        attached = set(_strings(state, "evidence_for")) | set(
            _strings(state, "evidence_against")
        )
        if not evidence_refs or not set(evidence_refs).issubset(attached):
            raise BeliefReducerError(
                "revision evidence must already be attached to belief"
            )
        addressed = set(_strings(payload, "addressed_contradiction_ids"))
        contradictions = [dict(item) for item in _objects(state, "contradictions")]
        known = {str(item["contradiction_id"]) for item in contradictions}
        open_contradictions = {
            str(item["contradiction_id"])
            for item in contradictions
            if item["addressed_in_revision"] is None
        }
        if not addressed.issubset(known):
            raise BeliefReducerError("revision references unknown contradiction")
        for item in contradictions:
            if item["contradiction_id"] in addressed:
                item["addressed_in_revision"] = new_revision

        new_statement = _string(payload, "new_statement")
        new_status = _enum_value(BeliefStatus, payload, "new_status")
        if belief_status_requires_evidence_gate(new_status):
            raise BeliefReducerError(
                f"{new_status.value} status requires a future Evidence Gate receipt"
            )
        if not belief_status_transition_allowed(previous_status, new_status):
            raise BeliefReducerError(
                f"transition {previous_status.value} → {new_status.value} is not allowed"
            )
        if (
            previous_status is BeliefStatus.CONTESTED
            and new_status not in {BeliefStatus.CONTESTED, BeliefStatus.UNRESOLVED}
            and not open_contradictions.issubset(addressed)
        ):
            raise BeliefReducerError(
                "leaving contested status requires addressing every open contradiction"
            )
        if (
            new_statement == previous_statement
            and new_status is previous_status
            and not addressed
        ):
            raise BeliefReducerError("belief revision has no effect")
        history = [dict(item) for item in _objects(state, "history")]
        history.append(
            {
                "revision": new_revision,
                "event_id": event.event_id,
                "statement": new_statement,
                "status": new_status.value,
                "reason": _string(payload, "reason"),
                "evidence_refs": evidence_refs,
                "addressed_contradiction_ids": sorted(addressed),
            }
        )
        return _copy_state(
            state,
            statement=new_statement,
            status=new_status.value,
            revision=new_revision,
            contradictions=contradictions,
            history=history,
        )


def _require_non_terminal(state: FrozenPayload) -> None:
    status = BeliefStatus(_string(state, "status"))
    if status is BeliefStatus.SUPERSEDED:
        raise BeliefReducerError("superseded belief is terminal")
    if belief_status_requires_evidence_gate(status):
        raise BeliefReducerError(
            "P0-014 cannot continue from an Evidence Gate-owned status"
        )


def _require_existing(state: FrozenPayload, payload: FrozenPayload) -> None:
    belief_id = state["belief_id"]
    if not isinstance(belief_id, str) or not belief_id:
        raise BeliefReducerError("belief does not exist")
    if belief_id != _string(payload, "belief_id"):
        raise BeliefReducerError("event belief_id does not match projection")


def _copy_state(state: FrozenPayload, **changes: object) -> dict[str, object]:
    copied = {
        "belief_id": state["belief_id"],
        "statement": state["statement"],
        "claim_type": state["claim_type"],
        "status": state["status"],
        "revision": state["revision"],
        "origin_event_id": state["origin_event_id"],
        "evidence_for": list(_strings(state, "evidence_for")),
        "evidence_against": list(_strings(state, "evidence_against")),
        "contradictions": [dict(item) for item in _objects(state, "contradictions")],
        "history": [dict(item) for item in _objects(state, "history")],
    }
    copied.update(changes)
    return copied


def _string(mapping: Mapping[str, object], key: str) -> str:
    value = mapping[key]
    if not isinstance(value, str) or not value:
        raise BeliefReducerError(f"{key} must be a non-empty string")
    return value


def _integer(mapping: Mapping[str, object], key: str) -> int:
    value = mapping[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise BeliefReducerError(f"{key} must be an integer")
    return value


def _strings(mapping: Mapping[str, object], key: str) -> tuple[str, ...]:
    value = mapping[key]
    if not isinstance(value, tuple) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise BeliefReducerError(f"{key} must be an immutable string sequence")
    return value


def _objects(
    mapping: Mapping[str, object],
    key: str,
) -> tuple[Mapping[str, object], ...]:
    value = mapping[key]
    if not isinstance(value, tuple) or any(not isinstance(item, Mapping) for item in value):
        raise BeliefReducerError(f"{key} must be an immutable object sequence")
    return value


def _enum_value(enum_type, mapping: Mapping[str, object], key: str):
    try:
        return enum_type(_string(mapping, key))
    except ValueError as exc:
        raise BeliefReducerError(f"unsupported {key}") from exc
