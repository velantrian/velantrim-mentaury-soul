"""P0-009 R0 integrity verification and first-failure diagnostics."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from enum import StrEnum

from mentaury.contracts import EventEnvelope, canonical_json_bytes
from mentaury.validation import SchemaRegistry

from .budget import ResourceBudgetExceeded, VerificationBudget
from .redaction import REDACTION_EVENT_TYPE, REDACTION_PAYLOAD_SCHEMA
from .sealing import compute_event_hash, compute_payload_digest
from .sqlite_store import SQLiteEventPayloadStore
from .stream_meta import GENESIS_HASH, read_stream_meta


class IntegrityCode(StrEnum):
    RESOURCE_BUDGET_EXCEEDED = "RESOURCE_BUDGET_EXCEEDED"
    STREAM_VERSION_GAP = "STREAM_VERSION_GAP"
    BATCH_INCOMPLETE = "BATCH_INCOMPLETE"
    BATCH_ORDER_MISMATCH = "BATCH_ORDER_MISMATCH"
    SCHEMA_INVALID = "SCHEMA_INVALID"
    PAYLOAD_MISSING = "PAYLOAD_MISSING"
    PAYLOAD_DECODE_ERROR = "PAYLOAD_DECODE_ERROR"
    PAYLOAD_NOT_CANONICAL = "PAYLOAD_NOT_CANONICAL"
    PAYLOAD_DIGEST_MISMATCH = "PAYLOAD_DIGEST_MISMATCH"
    PREVIOUS_HASH_MISMATCH = "PREVIOUS_HASH_MISMATCH"
    EVENT_HASH_MISMATCH = "EVENT_HASH_MISMATCH"
    STREAM_META_VERSION_MISMATCH = "STREAM_META_VERSION_MISMATCH"
    STREAM_META_HASH_MISMATCH = "STREAM_META_HASH_MISMATCH"
    STREAM_META_COUNT_MISMATCH = "STREAM_META_COUNT_MISMATCH"
    REDACTED_PAYLOAD_STILL_PRESENT = "REDACTED_PAYLOAD_STILL_PRESENT"
    REDACTION_PAYLOAD_REF_MISMATCH = "REDACTION_PAYLOAD_REF_MISMATCH"
    REDACTION_TARGET_EVENT_MISSING = "REDACTION_TARGET_EVENT_MISSING"
    REDACTION_TARGET_STREAM_MISMATCH = "REDACTION_TARGET_STREAM_MISMATCH"
    REDACTION_AUDIT_EVENT_MISSING = "REDACTION_AUDIT_EVENT_MISSING"
    REDACTION_AUDIT_TYPE_MISMATCH = "REDACTION_AUDIT_TYPE_MISMATCH"
    REDACTION_AUDIT_SCHEMA_MISMATCH = "REDACTION_AUDIT_SCHEMA_MISMATCH"
    REDACTION_AUDIT_STREAM_MISMATCH = "REDACTION_AUDIT_STREAM_MISMATCH"
    REDACTION_AUDIT_ORDER_MISMATCH = "REDACTION_AUDIT_ORDER_MISMATCH"
    REDACTION_AUTHORITY_MISMATCH = "REDACTION_AUTHORITY_MISMATCH"
    REDACTION_AUDIT_PAYLOAD_MISSING = "REDACTION_AUDIT_PAYLOAD_MISSING"
    REDACTION_AUDIT_PAYLOAD_DECODE_ERROR = (
        "REDACTION_AUDIT_PAYLOAD_DECODE_ERROR"
    )
    REDACTION_AUDIT_PAYLOAD_NOT_CANONICAL = (
        "REDACTION_AUDIT_PAYLOAD_NOT_CANONICAL"
    )
    REDACTION_AUDIT_PAYLOAD_MISMATCH = "REDACTION_AUDIT_PAYLOAD_MISMATCH"
    REDACTION_AUDIT_PAYLOAD_DIGEST_MISMATCH = (
        "REDACTION_AUDIT_PAYLOAD_DIGEST_MISMATCH"
    )


@dataclass(frozen=True, slots=True)
class IntegrityFailure:
    code: IntegrityCode
    stream_id: str
    message: str
    event_id: str | None = None
    stream_version: int | None = None


@dataclass(frozen=True, slots=True)
class R0IntegrityReport:
    stream_id: str
    ok: bool
    checked_events: int
    failure: IntegrityFailure | None


@dataclass(frozen=True, slots=True)
class _RedactionEvidence:
    target_event_id: str
    target_stream_id: str
    target_payload_ref: str
    audit_event_id: str
    reason: str
    capability_lease_id: str
    capability_revision: int


class R0IntegrityVerifier:
    """Verify one stream under an explicit caller-supplied resource budget."""

    def __init__(
        self,
        store: SQLiteEventPayloadStore,
        registry: SchemaRegistry,
        budget: VerificationBudget,
    ) -> None:
        if not isinstance(store, SQLiteEventPayloadStore):
            raise TypeError("store must be a SQLiteEventPayloadStore")
        if not isinstance(registry, SchemaRegistry):
            raise TypeError("registry must be a SchemaRegistry")
        if not isinstance(budget, VerificationBudget):
            raise TypeError("budget must be a VerificationBudget")
        self._store = store
        self._registry = registry
        self._budget = budget

    def verify_stream(self, stream_id: str) -> R0IntegrityReport:
        self._store._require_initialized()
        event_count = self._store._connection.execute(
            "SELECT COUNT(*) FROM events WHERE stream_id = ?",
            (stream_id,),
        ).fetchone()[0]
        try:
            self._budget.require_event_count(event_count)
        except ResourceBudgetExceeded as exc:
            return self._budget_fail(stream_id, 0, exc)

        events = self._store.list_stream(stream_id)
        meta = read_stream_meta(self._store._connection, stream_id)
        redactions = self._redaction_evidence_for_stream(stream_id)

        if not events:
            if redactions:
                return self._fail(
                    stream_id,
                    0,
                    IntegrityCode.REDACTION_TARGET_EVENT_MISSING,
                    "redaction evidence exists for an empty stream",
                )
            if meta.current_version != 0:
                return self._fail(
                    stream_id,
                    0,
                    IntegrityCode.STREAM_META_VERSION_MISMATCH,
                    "empty stream must have current_version 0",
                )
            if meta.last_event_hash != GENESIS_HASH:
                return self._fail(
                    stream_id,
                    0,
                    IntegrityCode.STREAM_META_HASH_MISMATCH,
                    "empty stream must use GENESIS_HASH",
                )
            if meta.event_count != 0:
                return self._fail(
                    stream_id,
                    0,
                    IntegrityCode.STREAM_META_COUNT_MISMATCH,
                    "empty stream must have event_count 0",
                )
            return R0IntegrityReport(stream_id, True, 0, None)

        event_ids = {event.event_id for event in events}
        for evidence in redactions.values():
            if evidence.target_event_id not in event_ids:
                return self._fail(
                    stream_id,
                    0,
                    IntegrityCode.REDACTION_TARGET_EVENT_MISSING,
                    "redaction target event does not exist in the declared stream",
                )

        expected_previous_hash = GENESIS_HASH
        checked = 0
        batch_start = 0
        total_payload_bytes = 0
        for index, event in enumerate(events):
            expected_version = index + 1
            if event.stream_version != expected_version:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.STREAM_VERSION_GAP,
                    f"expected stream version {expected_version}",
                )
            if index == batch_start:
                if event.batch_index != 0:
                    return self._event_fail(
                        event,
                        checked,
                        IntegrityCode.BATCH_ORDER_MISMATCH,
                        "batch must start at index 0",
                    )
                batch_end = batch_start + event.batch_size
                if batch_end > len(events):
                    return self._event_fail(
                        event,
                        checked,
                        IntegrityCode.BATCH_INCOMPLETE,
                        "batch extends beyond available stream events",
                    )
                for expected_index, member in enumerate(
                    events[batch_start:batch_end]
                ):
                    if (
                        member.batch_id != event.batch_id
                        or member.batch_size != event.batch_size
                        or member.batch_index != expected_index
                    ):
                        return self._event_fail(
                            member,
                            checked,
                            IntegrityCode.BATCH_ORDER_MISMATCH,
                            "batch identifiers, size, or order are inconsistent",
                        )
                batch_start = batch_end

            envelope_issues = self._registry.validate_event_envelope(event)
            if envelope_issues:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.SCHEMA_INVALID,
                    str(envelope_issues[0]),
                )

            evidence = redactions.get(event.event_id)
            if evidence is not None:
                if event.stream_id != evidence.target_stream_id:
                    return self._event_fail(
                        event,
                        checked,
                        IntegrityCode.REDACTION_TARGET_STREAM_MISMATCH,
                        "redaction record stream differs from target event stream",
                    )
                if event.payload_ref != evidence.target_payload_ref:
                    return self._event_fail(
                        event,
                        checked,
                        IntegrityCode.REDACTION_PAYLOAD_REF_MISMATCH,
                        "redaction record payload_ref differs from event payload_ref",
                    )
                if self._store.load_payload(event.payload_ref) is not None:
                    return self._event_fail(
                        event,
                        checked,
                        IntegrityCode.REDACTED_PAYLOAD_STILL_PRESENT,
                        "payload material must be absent after governed redaction",
                    )
                linkage_failure = self._verify_redaction_linkage(
                    event,
                    evidence,
                    checked,
                )
                if linkage_failure is not None:
                    return linkage_failure
                if event.previous_hash != expected_previous_hash:
                    return self._event_fail(
                        event,
                        checked,
                        IntegrityCode.PREVIOUS_HASH_MISMATCH,
                        "previous_hash does not match the prior event hash",
                    )
                if event.event_hash != compute_event_hash(event):
                    return self._event_fail(
                        event,
                        checked,
                        IntegrityCode.EVENT_HASH_MISMATCH,
                        "stored event hash differs from recomputed hash",
                    )
                expected_previous_hash = event.event_hash
                checked += 1
                continue

            payload = self._store.load_payload(event.payload_ref)
            if payload is None:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.PAYLOAD_MISSING,
                    "payload material is missing",
                )
            try:
                self._budget.require_payload_size(len(payload.payload_bytes))
                total_payload_bytes += len(payload.payload_bytes)
                self._budget.require_total_payload_size(total_payload_bytes)
            except ResourceBudgetExceeded as exc:
                return self._event_budget_fail(event, checked, exc)
            try:
                decoded = json.loads(payload.payload_bytes.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.PAYLOAD_DECODE_ERROR,
                    f"payload cannot be decoded: {exc}",
                )
            if not isinstance(decoded, dict):
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.SCHEMA_INVALID,
                    "event payload must decode to an object",
                )
            try:
                canonical_payload = canonical_json_bytes(decoded)
            except (TypeError, ValueError) as exc:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.SCHEMA_INVALID,
                    f"payload is not canonically representable: {exc}",
                )
            if canonical_payload != payload.payload_bytes:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.PAYLOAD_NOT_CANONICAL,
                    "stored payload bytes differ from canonical encoding",
                )
            payload_issues = self._registry.validate_event_payload(event, decoded)
            if payload_issues:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.SCHEMA_INVALID,
                    str(payload_issues[0]),
                )
            if event.payload_digest != compute_payload_digest(
                payload.payload_bytes
            ):
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.PAYLOAD_DIGEST_MISMATCH,
                    "stored payload digest differs from recomputed digest",
                )
            if event.previous_hash != expected_previous_hash:
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.PREVIOUS_HASH_MISMATCH,
                    "previous_hash does not match the prior event hash",
                )
            if event.event_hash != compute_event_hash(event):
                return self._event_fail(
                    event,
                    checked,
                    IntegrityCode.EVENT_HASH_MISMATCH,
                    "stored event hash differs from recomputed hash",
                )
            expected_previous_hash = event.event_hash
            checked += 1

        tail = events[-1]
        if meta.current_version != tail.stream_version:
            return self._fail(
                stream_id,
                checked,
                IntegrityCode.STREAM_META_VERSION_MISMATCH,
                "stream_meta current_version differs from ledger tail",
            )
        if meta.last_event_hash != tail.event_hash:
            return self._fail(
                stream_id,
                checked,
                IntegrityCode.STREAM_META_HASH_MISMATCH,
                "stream_meta last_event_hash differs from ledger tail",
            )
        if meta.event_count != len(events):
            return self._fail(
                stream_id,
                checked,
                IntegrityCode.STREAM_META_COUNT_MISMATCH,
                "stream_meta event_count differs from ledger count",
            )
        return R0IntegrityReport(stream_id, True, checked, None)

    def _redaction_evidence_for_stream(
        self,
        stream_id: str,
    ) -> dict[str, _RedactionEvidence]:
        rows = self._store._connection.execute(
            """
            SELECT target_event_id, target_stream_id, target_payload_ref,
                   audit_event_id, reason, capability_lease_id,
                   capability_revision
            FROM redactions
            WHERE target_stream_id = ?
            """,
            (stream_id,),
        ).fetchall()
        return {
            row["target_event_id"]: _RedactionEvidence(
                target_event_id=row["target_event_id"],
                target_stream_id=row["target_stream_id"],
                target_payload_ref=row["target_payload_ref"],
                audit_event_id=row["audit_event_id"],
                reason=row["reason"],
                capability_lease_id=row["capability_lease_id"],
                capability_revision=row["capability_revision"],
            )
            for row in rows
        }

    def _verify_redaction_linkage(
        self,
        target_event: EventEnvelope,
        evidence: _RedactionEvidence,
        checked: int,
    ) -> R0IntegrityReport | None:
        audit_event = self._store.load_event(evidence.audit_event_id)
        if audit_event is None:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_EVENT_MISSING,
                "redaction audit event does not exist",
            )
        if audit_event.event_type != REDACTION_EVENT_TYPE:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_TYPE_MISMATCH,
                "linked audit event has the wrong event_type",
            )
        if audit_event.payload_schema != REDACTION_PAYLOAD_SCHEMA:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_SCHEMA_MISMATCH,
                "linked audit event has the wrong payload_schema",
            )
        if audit_event.stream_id != evidence.target_stream_id:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_STREAM_MISMATCH,
                "linked audit event is not in the target stream",
            )
        if audit_event.stream_version <= target_event.stream_version:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_ORDER_MISMATCH,
                "redaction audit event must follow its target event",
            )
        if (
            audit_event.authority.capability_lease_id
            != evidence.capability_lease_id
            or audit_event.authority.capability_revision
            != evidence.capability_revision
        ):
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUTHORITY_MISMATCH,
                "audit envelope authority differs from redaction evidence",
            )
        envelope_issues = self._registry.validate_event_envelope(audit_event)
        if envelope_issues:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_SCHEMA_MISMATCH,
                str(envelope_issues[0]),
            )

        audit_payload = self._store.load_payload(audit_event.payload_ref)
        if audit_payload is None:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_PAYLOAD_MISSING,
                "redaction audit payload material is missing",
            )
        try:
            decoded = json.loads(audit_payload.payload_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_PAYLOAD_DECODE_ERROR,
                f"redaction audit payload cannot be decoded: {exc}",
            )
        if not isinstance(decoded, dict):
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_PAYLOAD_MISMATCH,
                "redaction audit payload must decode to an object",
            )
        try:
            canonical_payload = canonical_json_bytes(decoded)
        except (TypeError, ValueError) as exc:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_PAYLOAD_NOT_CANONICAL,
                f"redaction audit payload is not representable: {exc}",
            )
        if canonical_payload != audit_payload.payload_bytes:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_PAYLOAD_NOT_CANONICAL,
                "redaction audit payload bytes are not canonical",
            )

        expected_payload: dict[str, object] = {
            "target_event_id": evidence.target_event_id,
            "target_stream_id": evidence.target_stream_id,
            "target_payload_ref": evidence.target_payload_ref,
            "reason": evidence.reason,
            "authority": {
                "capability_lease_id": evidence.capability_lease_id,
                "capability_revision": evidence.capability_revision,
            },
        }
        if decoded != expected_payload:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_PAYLOAD_MISMATCH,
                "redaction row and audit payload are not mutually consistent",
            )
        payload_issues = self._registry.validate_event_payload(
            audit_event,
            decoded,
        )
        if payload_issues:
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_PAYLOAD_MISMATCH,
                str(payload_issues[0]),
            )
        if audit_event.payload_digest != compute_payload_digest(
            audit_payload.payload_bytes
        ):
            return self._event_fail(
                target_event,
                checked,
                IntegrityCode.REDACTION_AUDIT_PAYLOAD_DIGEST_MISMATCH,
                "redaction audit payload digest differs from the event",
            )
        return None

    @staticmethod
    def _event_budget_fail(
        event: EventEnvelope,
        checked: int,
        error: ResourceBudgetExceeded,
    ) -> R0IntegrityReport:
        return R0IntegrityReport(
            event.stream_id,
            False,
            checked,
            IntegrityFailure(
                IntegrityCode.RESOURCE_BUDGET_EXCEEDED,
                event.stream_id,
                str(error),
                event.event_id,
                event.stream_version,
            ),
        )

    @staticmethod
    def _budget_fail(
        stream_id: str,
        checked: int,
        error: ResourceBudgetExceeded,
    ) -> R0IntegrityReport:
        return R0IntegrityReport(
            stream_id,
            False,
            checked,
            IntegrityFailure(
                IntegrityCode.RESOURCE_BUDGET_EXCEEDED,
                stream_id,
                str(error),
            ),
        )

    @staticmethod
    def _event_fail(
        event: EventEnvelope,
        checked: int,
        code: IntegrityCode,
        message: str,
    ) -> R0IntegrityReport:
        return R0IntegrityReport(
            event.stream_id,
            False,
            checked,
            IntegrityFailure(
                code,
                event.stream_id,
                message,
                event.event_id,
                event.stream_version,
            ),
        )

    @staticmethod
    def _fail(
        stream_id: str,
        checked: int,
        code: IntegrityCode,
        message: str,
    ) -> R0IntegrityReport:
        return R0IntegrityReport(
            stream_id,
            False,
            checked,
            IntegrityFailure(code, stream_id, message),
        )
