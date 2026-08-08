"""P0-010 atomic same-stream redaction: governed external-payload removal.

Redaction never touches the immutable ``events`` row. It removes external
payload material for exactly one target event and appends a
``REDACTION_RECORDED`` audit event to the *same* stream, atomically, under
one write lock. The ``redactions`` table is the authoritative record R0 uses
to distinguish governed redaction from payload corruption; it is itself
append-only and immutable, mirroring ``idempotency_records``.
"""

from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    EventEnvelope,
    ProducerRef,
    canonical_json_bytes,
    canonical_timestamp,
)
from mentaury.contracts.canonical_json import authority_ref_value
from mentaury.contracts.primitives import require_non_empty
from mentaury.validation import SchemaRegistry

from ._event_rows import insert_event_row
from .concurrency import (
    DEFAULT_BUSY_RETRY_POLICY,
    BusyRetryPolicy,
    VersionConflictError,
    begin_immediate,
    commit_with_retry,
    is_stream_version_conflict,
)
from .sealing import seal_event_bytes, validate_event_for_commit
from .sqlite_store import SQLiteEventPayloadStore
from .stream_meta import require_expected_stream_version, update_stream_meta

REDACTION_EVENT_TYPE: Final[str] = "REDACTION_RECORDED"
REDACTION_PAYLOAD_SCHEMA: Final[str] = "redaction-recorded/v1"
REDACTION_IDEMPOTENCY_PROFILE: Final[str] = "MENTAURY_REDACTION_V1"


class RedactionError(RuntimeError):
    """Base error for controlled P0-010 redaction failures."""


class TargetEventNotFoundError(RedactionError):
    def __init__(self, target_event_id: str) -> None:
        self.target_event_id = target_event_id
        super().__init__(f"target event not found: {target_event_id}")


class CrossStreamRedactionError(RedactionError):
    def __init__(self, target_stream: str, actual_stream: str) -> None:
        self.target_stream = target_stream
        self.actual_stream = actual_stream
        super().__init__(
            "cross-stream redaction rejected: requested "
            f"{target_stream}, target event belongs to {actual_stream}"
        )


class TargetAlreadyRedactedError(RedactionError):
    def __init__(self, target_event_id: str) -> None:
        self.target_event_id = target_event_id
        super().__init__(f"target event already redacted: {target_event_id}")


class TargetPayloadMissingError(RedactionError):
    def __init__(self, payload_ref: str) -> None:
        self.payload_ref = payload_ref
        super().__init__(f"target payload material already absent: {payload_ref}")


class RedactionConflictError(RedactionError):
    """Raised when one idempotency key is reused for a different redaction."""

    def __init__(
        self,
        idempotency_key: str,
        stored_fingerprint: str,
        attempted_fingerprint: str,
    ) -> None:
        self.idempotency_key = idempotency_key
        self.stored_fingerprint = stored_fingerprint
        self.attempted_fingerprint = attempted_fingerprint
        super().__init__(
            f"redaction conflict for key {idempotency_key}: "
            f"stored {stored_fingerprint}, attempted {attempted_fingerprint}"
        )


class RedactionStatus(StrEnum):
    REDACTED = "REDACTED"
    ALREADY_REDACTED = "ALREADY_REDACTED"


@dataclass(frozen=True, slots=True)
class RedactionRequest:
    """One governed intent to remove external payload material from one event.

    ``expected_stream_version`` is the caller-observed current tail version of
    ``target_stream`` before the audit event is appended; it is unrelated to
    the target event's own (immutable) stream position.
    """

    idempotency_key: str
    command_id: str
    target_event_id: str
    target_stream: str
    expected_stream_version: int
    reason: str
    issuer: ActorRef
    authority: AuthorityRef
    correlation_id: str
    audit_event_id: str
    producer: ProducerRef
    occurred_at: str
    recorded_at: str

    def __post_init__(self) -> None:
        for field_name in (
            "idempotency_key",
            "command_id",
            "target_event_id",
            "target_stream",
            "reason",
            "correlation_id",
            "audit_event_id",
            "occurred_at",
            "recorded_at",
        ):
            require_non_empty(getattr(self, field_name), field_name)
        if (
            isinstance(self.expected_stream_version, bool)
            or not isinstance(self.expected_stream_version, int)
            or self.expected_stream_version < 0
        ):
            raise ValueError(
                "expected_stream_version must be a non-negative integer"
            )
        if not isinstance(self.issuer, ActorRef):
            raise TypeError("issuer must be an ActorRef")
        if not isinstance(self.authority, AuthorityRef):
            raise TypeError("authority must be an AuthorityRef")
        if not isinstance(self.producer, ProducerRef):
            raise TypeError("producer must be a ProducerRef")


@dataclass(frozen=True, slots=True)
class RedactionResult:
    status: RedactionStatus
    fingerprint: str
    audit_event_id: str
    audit_stream_version: int


def redaction_fingerprint(request: RedactionRequest) -> str:
    """Fingerprint semantic redaction intent, excluding volatile identifiers.

    ``audit_event_id``, ``command_id``, ``correlation_id``, and timestamps may
    change between a first attempt and a semantic retry; the target, stream,
    reason, and authority reference must not.
    """

    if not isinstance(request, RedactionRequest):
        raise TypeError("request must be a RedactionRequest")
    semantic_value = {
        "profile": REDACTION_IDEMPOTENCY_PROFILE,
        "target_event_id": request.target_event_id,
        "target_stream": request.target_stream,
        "reason": request.reason,
        "authority": authority_ref_value(request.authority),
    }
    digest = hashlib.sha256(canonical_json_bytes(semantic_value)).hexdigest()
    return f"sha256:{digest}"


def redaction_payload_value(
    *,
    target_event_id: str,
    target_stream_id: str,
    target_payload_ref: str,
    reason: str,
    authority: AuthorityRef,
) -> dict[str, object]:
    """Build the canonical ``REDACTION_RECORDED`` evidence payload."""

    return {
        "target_event_id": target_event_id,
        "target_stream_id": target_stream_id,
        "target_payload_ref": target_payload_ref,
        "reason": reason,
        "authority": authority_ref_value(authority),
    }


class SQLiteRedactionExecutor:
    """Atomically remove one event's external payload under one write lock."""

    def __init__(
        self,
        store: SQLiteEventPayloadStore,
        registry: SchemaRegistry,
        busy_policy: BusyRetryPolicy = DEFAULT_BUSY_RETRY_POLICY,
    ) -> None:
        if not isinstance(store, SQLiteEventPayloadStore):
            raise TypeError("store must be a SQLiteEventPayloadStore")
        if not isinstance(registry, SchemaRegistry):
            raise TypeError("registry must be a SchemaRegistry")
        if not isinstance(busy_policy, BusyRetryPolicy):
            raise TypeError("busy_policy must be a BusyRetryPolicy")
        self._store = store
        self._registry = registry
        self._busy_policy = busy_policy

    def redact(self, request: RedactionRequest) -> RedactionResult:
        """Validate, then atomically delete payload and append audit evidence.

        Order matters: the expected-version and schema checks run before any
        payload material is touched, so a stale version or invalid audit
        payload leaves the target payload untouched. Any failure after that
        point (including the audit-event insert) rolls back the whole
        transaction, so payload deletion is never observed without evidence.
        """

        if not isinstance(request, RedactionRequest):
            raise TypeError("request must be a RedactionRequest")
        self._store._require_initialized()
        connection = self._store._connection
        fingerprint = redaction_fingerprint(request)
        sealed_audit: EventEnvelope | None = None

        try:
            begin_immediate(connection, self._busy_policy)

            existing_by_key = connection.execute(
                """
                SELECT fingerprint, audit_event_id
                FROM redactions WHERE idempotency_key = ?
                """,
                (request.idempotency_key,),
            ).fetchone()
            if existing_by_key is not None:
                if existing_by_key["fingerprint"] != fingerprint:
                    raise RedactionConflictError(
                        request.idempotency_key,
                        existing_by_key["fingerprint"],
                        fingerprint,
                    )
                audit_event = self._store.load_event(
                    existing_by_key["audit_event_id"]
                )
                if audit_event is None:  # pragma: no cover - defensive guard
                    raise AssertionError("recorded audit event is missing")
                commit_with_retry(connection, self._busy_policy)
                return RedactionResult(
                    RedactionStatus.ALREADY_REDACTED,
                    fingerprint,
                    audit_event.event_id,
                    audit_event.stream_version,
                )

            already_redacted = connection.execute(
                "SELECT 1 FROM redactions WHERE target_event_id = ?",
                (request.target_event_id,),
            ).fetchone()
            if already_redacted is not None:
                raise TargetAlreadyRedactedError(request.target_event_id)

            target = self._store.load_event(request.target_event_id)
            if target is None:
                raise TargetEventNotFoundError(request.target_event_id)
            if target.stream_id != request.target_stream:
                raise CrossStreamRedactionError(
                    request.target_stream, target.stream_id
                )

            unsealed_audit = EventEnvelope(
                event_id=request.audit_event_id,
                event_type=REDACTION_EVENT_TYPE,
                envelope_schema_version=1,
                payload_schema=REDACTION_PAYLOAD_SCHEMA,
                stream_id=request.target_stream,
                stream_version=request.expected_stream_version + 1,
                batch_id=request.audit_event_id,
                batch_index=0,
                batch_size=1,
                occurred_at=request.occurred_at,
                recorded_at=request.recorded_at,
                producer=request.producer,
                initiator=request.issuer,
                authority=request.authority,
                causation_id=request.command_id,
                correlation_id=request.correlation_id,
                affects_domain_state=True,
                payload_digest="sha256:pending",
                payload_ref=f"PAYLOAD-REDACTION-{request.audit_event_id}",
                previous_hash="sha256:pending",
                event_hash="sha256:pending",
            )

            # Version check before any mutation: a stale caller-observed tail
            # leaves the target payload untouched.
            previous_meta = require_expected_stream_version(
                connection, unsealed_audit
            )

            payload = redaction_payload_value(
                target_event_id=target.event_id,
                target_stream_id=target.stream_id,
                target_payload_ref=target.payload_ref,
                reason=request.reason,
                authority=request.authority,
            )
            # Schema/identity validation before any mutation, for the same
            # reason: an invalid audit payload must not delete anything.
            payload_bytes = validate_event_for_commit(
                unsealed_audit, payload, self._registry
            )

            if self._store.load_payload(target.payload_ref) is None:
                raise TargetPayloadMissingError(target.payload_ref)

            connection.execute(
                "DELETE FROM event_payloads WHERE payload_ref = ?",
                (target.payload_ref,),
            )

            sealed_audit = seal_event_bytes(
                unsealed_audit,
                payload_bytes,
                previous_hash=previous_meta.last_event_hash,
            )
            created_at = canonical_timestamp(sealed_audit.recorded_at)
            connection.execute(
                """
                INSERT INTO event_payloads(payload_ref, payload_bytes, created_at)
                VALUES (?, ?, ?)
                """,
                (sealed_audit.payload_ref, payload_bytes, created_at),
            )
            _insert_audit_event(connection, sealed_audit)
            update_stream_meta(connection, (sealed_audit,), previous_meta)

            connection.execute(
                """
                INSERT INTO redactions(
                    target_event_id, idempotency_key, fingerprint,
                    target_stream_id, target_payload_ref, audit_event_id,
                    reason, capability_lease_id, capability_revision, redacted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    target.event_id,
                    request.idempotency_key,
                    fingerprint,
                    target.stream_id,
                    target.payload_ref,
                    sealed_audit.event_id,
                    request.reason,
                    request.authority.capability_lease_id,
                    request.authority.capability_revision,
                    created_at,
                ),
            )
        except sqlite3.IntegrityError as exc:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            if is_stream_version_conflict(exc):
                raise VersionConflictError(
                    request.target_stream, request.expected_stream_version + 1
                ) from exc
            raise
        except Exception:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            raise
        else:
            commit_with_retry(connection, self._busy_policy)

        if sealed_audit is None:  # pragma: no cover - defensive guard
            raise AssertionError("redaction audit event was not allocated")
        return RedactionResult(
            RedactionStatus.REDACTED,
            fingerprint,
            sealed_audit.event_id,
            sealed_audit.stream_version,
        )


def redacted_targets_for_stream(
    connection: sqlite3.Connection, stream_id: str
) -> dict[str, str]:
    """Return ``{target_event_id: target_payload_ref}`` for one stream.

    This is the authoritative evidence R0 uses to distinguish a governed
    redaction from missing-payload corruption.
    """

    rows = connection.execute(
        """
        SELECT target_event_id, target_payload_ref
        FROM redactions WHERE target_stream_id = ?
        """,
        (stream_id,),
    ).fetchall()
    return {row["target_event_id"]: row["target_payload_ref"] for row in rows}


def _insert_audit_event(connection: sqlite3.Connection, event: EventEnvelope) -> None:
    insert_event_row(connection, event)
