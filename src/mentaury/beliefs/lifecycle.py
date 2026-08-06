"""Pure P0-014 command evaluation for one belief stream."""

from __future__ import annotations

from collections.abc import Mapping

from mentaury.contracts import CommandEnvelope, PendingEvent

from .contracts import (
    ATTACH_EVIDENCE,
    BELIEF_CREATED,
    BELIEF_CREATED_SCHEMA,
    BELIEF_DECISION_SCHEMA,
    BELIEF_REVISED,
    BELIEF_REVISED_SCHEMA,
    BELIEF_REVISION_REJECTED,
    COMMAND_REJECTED,
    CONTRADICTION_REGISTERED,
    CONTRADICTION_REGISTERED_SCHEMA,
    CREATE_BELIEF,
    EVIDENCE_ATTACHED,
    EVIDENCE_ATTACHED_SCHEMA,
    REGISTER_CONTRADICTION,
    REVISE_BELIEF,
    BeliefDecision,
    BeliefRejectionCode,
    BeliefStatus,
    ClaimType,
    EvidenceSide,
    belief_stream_id,
)


_ALLOWED_TRANSITIONS: dict[BeliefStatus, frozenset[BeliefStatus]] = {
    BeliefStatus.HYPOTHESIS: frozenset(
        {
            BeliefStatus.PROVISIONAL,
            BeliefStatus.SUPPORTED,
            BeliefStatus.CONTESTED,
            BeliefStatus.CONTRADICTED,
            BeliefStatus.UNRESOLVED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.PROVISIONAL: frozenset(
        {
            BeliefStatus.SUPPORTED,
            BeliefStatus.CONTESTED,
            BeliefStatus.CONTRADICTED,
            BeliefStatus.UNRESOLVED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.SUPPORTED: frozenset(
        {
            BeliefStatus.PROVISIONAL,
            BeliefStatus.CONTESTED,
            BeliefStatus.CONTRADICTED,
            BeliefStatus.UNRESOLVED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.CONTESTED: frozenset(
        {
            BeliefStatus.PROVISIONAL,
            BeliefStatus.SUPPORTED,
            BeliefStatus.CONTRADICTED,
            BeliefStatus.UNRESOLVED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.CONTRADICTED: frozenset(
        {
            BeliefStatus.PROVISIONAL,
            BeliefStatus.UNRESOLVED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.UNRESOLVED: frozenset(
        {
            BeliefStatus.HYPOTHESIS,
            BeliefStatus.PROVISIONAL,
            BeliefStatus.SUPPORTED,
            BeliefStatus.CONTESTED,
            BeliefStatus.CONTRADICTED,
            BeliefStatus.SUPERSEDED,
        }
    ),
    BeliefStatus.SUPERSEDED: frozenset(),
}


class BeliefLifecycle:
    """Evaluate one command without persistence, clocks or authority lookup."""

    def decide(
        self,
        command: CommandEnvelope,
        state: Mapping[str, object],
    ) -> BeliefDecision:
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
                BeliefRejectionCode.INVALID_COMMAND,
                "command payload requires belief_id",
            )
        if command.target_stream != belief_stream_id(belief_id):
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.TARGET_STREAM_MISMATCH,
                "target_stream must equal belief:<belief_id>",
            )
        if command.command_type == CREATE_BELIEF:
            return self._create(command, state, belief_id)
        if command.command_type == ATTACH_EVIDENCE:
            return self._attach(command, state, belief_id)
        if command.command_type == REGISTER_CONTRADICTION:
            return self._contradiction(command, state, belief_id)
        if command.command_type == REVISE_BELIEF:
            return self._revise(command, state, belief_id)
        return self._reject(
            command,
            belief_id,
            state,
            BeliefRejectionCode.INVALID_COMMAND,
            f"unsupported command_type: {command.command_type}",
        )

    def _create(
        self,
        command: CommandEnvelope,
        state: Mapping[str, object],
        belief_id: str,
    ) -> BeliefDecision:
        if _revision(state) != 0 or state.get("belief_id") is not None:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.BELIEF_ALREADY_EXISTS,
                "belief stream already contains a belief",
            )
        statement = _optional_string(command.payload, "statement")
        claim_type = _parse_enum(ClaimType, command.payload.get("claim_type"))
        if statement is None or claim_type is None:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "CREATE_BELIEF requires statement and supported claim_type",
            )
        return _accepted(
            PendingEvent(
                BELIEF_CREATED,
                BELIEF_CREATED_SCHEMA,
                True,
                {
                    "belief_id": belief_id,
                    "statement": statement,
                    "claim_type": claim_type.value,
                    "status": BeliefStatus.HYPOTHESIS.value,
                    "revision": 1,
                },
            )
        )

    def _attach(
        self,
        command: CommandEnvelope,
        state: Mapping[str, object],
        belief_id: str,
    ) -> BeliefDecision:
        missing = self._require_mutable(command, state, belief_id)
        if missing is not None:
            return missing
        evidence_ref = _optional_string(command.payload, "evidence_ref")
        side = _parse_enum(EvidenceSide, command.payload.get("side"))
        note = _optional_string(command.payload, "note")
        if evidence_ref is None or side is None:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "ATTACH_EVIDENCE requires evidence_ref and supported side",
            )
        attached = _attached_evidence(state)
        if evidence_ref in attached:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.DUPLICATE_EVIDENCE,
                "evidence reference is already attached",
            )
        payload: dict[str, object] = {
            "belief_id": belief_id,
            "evidence_ref": evidence_ref,
            "side": side.value,
        }
        if note is not None:
            payload["note"] = note
        return _accepted(
            PendingEvent(
                EVIDENCE_ATTACHED,
                EVIDENCE_ATTACHED_SCHEMA,
                True,
                payload,
            )
        )

    def _contradiction(
        self,
        command: CommandEnvelope,
        state: Mapping[str, object],
        belief_id: str,
    ) -> BeliefDecision:
        missing = self._require_mutable(command, state, belief_id)
        if missing is not None:
            return missing
        contradiction_id = _optional_string(command.payload, "contradiction_id")
        statement = _optional_string(command.payload, "statement")
        evidence_refs = _string_sequence(command.payload.get("evidence_refs"))
        if contradiction_id is None or statement is None or not evidence_refs:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "REGISTER_CONTRADICTION requires id, statement and evidence_refs",
            )
        known_ids = {
            str(item["contradiction_id"])
            for item in _object_sequence(state.get("contradictions"))
        }
        if contradiction_id in known_ids:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.DUPLICATE_CONTRADICTION,
                "contradiction_id is already registered",
            )
        unknown = set(evidence_refs).difference(_attached_evidence(state))
        if unknown:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.UNKNOWN_EVIDENCE_REF,
                f"contradiction references unattached evidence: {sorted(unknown)!r}",
            )
        current = _status(state)
        resulting = (
            BeliefStatus.CONTRADICTED
            if current is BeliefStatus.CONTRADICTED
            else BeliefStatus.CONTESTED
        )
        return _accepted(
            PendingEvent(
                CONTRADICTION_REGISTERED,
                CONTRADICTION_REGISTERED_SCHEMA,
                True,
                {
                    "belief_id": belief_id,
                    "contradiction_id": contradiction_id,
                    "statement": statement,
                    "evidence_refs": list(evidence_refs),
                    "resulting_status": resulting.value,
                },
            )
        )

    def _revise(
        self,
        command: CommandEnvelope,
        state: Mapping[str, object],
        belief_id: str,
    ) -> BeliefDecision:
        missing = self._require_mutable(command, state, belief_id)
        if missing is not None:
            return missing
        expected_revision = command.payload.get("expected_revision")
        if isinstance(expected_revision, bool) or not isinstance(expected_revision, int):
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "REVISE_BELIEF requires integer expected_revision",
            )
        current_revision = _revision(state)
        if expected_revision != current_revision:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.REVISION_CONFLICT,
                "expected_revision does not match current belief revision",
            )
        new_statement = _optional_string(command.payload, "new_statement")
        new_status = _parse_enum(BeliefStatus, command.payload.get("new_status"))
        reason = _optional_string(command.payload, "reason")
        evidence_refs = _string_sequence(command.payload.get("evidence_refs"))
        contradiction_ids = _string_sequence(
            command.payload.get("addressed_contradiction_ids", ())
        )
        if new_statement is None or new_status is None or reason is None or not evidence_refs:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "REVISE_BELIEF requires statement, status, reason and evidence_refs",
            )
        unknown_evidence = set(evidence_refs).difference(_attached_evidence(state))
        if unknown_evidence:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.UNKNOWN_EVIDENCE_REF,
                f"revision references unattached evidence: {sorted(unknown_evidence)!r}",
            )
        known_contradictions = {
            str(item["contradiction_id"])
            for item in _object_sequence(state.get("contradictions"))
        }
        unknown_contradictions = set(contradiction_ids).difference(
            known_contradictions
        )
        if unknown_contradictions:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.UNKNOWN_CONTRADICTION,
                "revision references unknown contradiction: "
                f"{sorted(unknown_contradictions)!r}",
            )
        current_status = _status(state)
        if new_status != current_status and new_status not in _ALLOWED_TRANSITIONS[current_status]:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_STATUS_TRANSITION,
                f"transition {current_status.value} → {new_status.value} is not allowed",
            )
        if (
            new_statement == state.get("statement")
            and new_status is current_status
            and not contradiction_ids
        ):
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.NO_EFFECT,
                "revision must change statement/status or address a contradiction",
            )
        return _accepted(
            PendingEvent(
                BELIEF_REVISED,
                BELIEF_REVISED_SCHEMA,
                True,
                {
                    "belief_id": belief_id,
                    "previous_revision": current_revision,
                    "new_revision": current_revision + 1,
                    "previous_statement": state["statement"],
                    "new_statement": new_statement,
                    "previous_status": current_status.value,
                    "new_status": new_status.value,
                    "reason": reason,
                    "evidence_refs": list(evidence_refs),
                    "addressed_contradiction_ids": list(contradiction_ids),
                },
            )
        )

    def _require_mutable(
        self,
        command: CommandEnvelope,
        state: Mapping[str, object],
        belief_id: str,
    ) -> BeliefDecision | None:
        if _revision(state) == 0 or state.get("belief_id") is None:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.BELIEF_NOT_FOUND,
                "belief does not exist",
            )
        if state.get("belief_id") != belief_id:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.INVALID_COMMAND,
                "state belief_id does not match command",
            )
        if _status(state) is BeliefStatus.SUPERSEDED:
            return self._reject(
                command,
                belief_id,
                state,
                BeliefRejectionCode.TERMINAL_BELIEF,
                "superseded belief is terminal",
            )
        return None

    def _reject(
        self,
        command: CommandEnvelope,
        belief_id: str,
        state: Mapping[str, object],
        code: BeliefRejectionCode,
        message: str,
    ) -> BeliefDecision:
        current_revision = _revision(state)
        event_type = (
            BELIEF_REVISION_REJECTED
            if command.command_type == REVISE_BELIEF
            else COMMAND_REJECTED
        )
        audit = PendingEvent(
            event_type,
            BELIEF_DECISION_SCHEMA,
            False,
            {
                "command_id": command.command_id,
                "command_type": command.command_type,
                "belief_id": belief_id,
                "rejection_code": code.value,
                "message": message,
                "expected_revision": command.expected_stream_version,
                "current_revision": current_revision,
            },
        )
        return BeliefDecision(False, (), audit, code, message)


def _accepted(event: PendingEvent) -> BeliefDecision:
    return BeliefDecision(True, (event,))


def _optional_string(mapping: Mapping[str, object], key: str) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        return None
    return value


def _parse_enum(enum_type, value):
    if not isinstance(value, str):
        return None
    try:
        return enum_type(value)
    except ValueError:
        return None


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


def _string_sequence(value: object) -> tuple[str, ...]:
    if not isinstance(value, (tuple, list)):
        return ()
    if any(not isinstance(item, str) or not item for item in value):
        return ()
    result = tuple(value)
    return result if len(set(result)) == len(result) else ()


def _object_sequence(value: object) -> tuple[Mapping[str, object], ...]:
    if not isinstance(value, (tuple, list)):
        return ()
    if any(not isinstance(item, Mapping) for item in value):
        return ()
    return tuple(value)


def _attached_evidence(state: Mapping[str, object]) -> frozenset[str]:
    return frozenset(
        (*_string_sequence(state.get("evidence_for")), *_string_sequence(state.get("evidence_against")))
    )
