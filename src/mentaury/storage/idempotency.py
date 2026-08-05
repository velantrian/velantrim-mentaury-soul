"""P0-007/P0-009 event-aware idempotency and trusted batch commit."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from mentaury.contracts import (
    CommandEnvelope,
    PendingEvent,
    canonical_json_bytes,
    canonical_timestamp,
    snapshot_pending_batch,
)
from mentaury.contracts.canonical_json import (
    actor_ref_value,
    authority_ref_value,
    pending_batch_value,
)
from mentaury.validation import SchemaRegistry

from .atomic_batch import (
    BatchAppendReceipt,
    BatchEntry,
    _insert_prepared_batch,
    _prepare_batch,
    _receipt_from_prepared,
)
from .concurrency import (
    DEFAULT_BUSY_RETRY_POLICY,
    BusyRetryPolicy,
    VersionConflictError,
    begin_immediate,
    commit_with_retry,
    is_stream_version_conflict,
)
from .sqlite_store import SQLiteEventPayloadStore

IDEMPOTENCY_PROFILE: Final[str] = "MENTAURY_IDEMPOTENCY_V1"


class IdempotencyStatus(StrEnum):
    APPLIED = "APPLIED"
    ALREADY_APPLIED = "ALREADY_APPLIED"


class IdempotencyInvariantError(ValueError):
    """Raised when command, pending events, and committed entries disagree."""


class IdempotencyConflictError(RuntimeError):
    """Raised when one key is reused for a different semantic mutation."""

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
            f"idempotency conflict for key {idempotency_key}: "
            f"stored {stored_fingerprint}, attempted {attempted_fingerprint}"
        )


@dataclass(frozen=True, slots=True)
class IdempotentBatchRequest:
    command: CommandEnvelope
    pending_events: tuple[PendingEvent, ...]
    entries: tuple[BatchEntry, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.command, CommandEnvelope):
            raise TypeError("command must be a CommandEnvelope")
        pending = snapshot_pending_batch(self.pending_events)
        entries = tuple(self.entries)
        if not entries or any(not isinstance(entry, BatchEntry) for entry in entries):
            raise TypeError("entries must contain BatchEntry values")
        object.__setattr__(self, "pending_events", pending)
        object.__setattr__(self, "entries", entries)
        _validate_request_alignment(self.command, pending, entries)


@dataclass(frozen=True, slots=True)
class IdempotentAppendResult:
    status: IdempotencyStatus
    fingerprint: str
    receipt: BatchAppendReceipt


class SQLiteIdempotentBatchAppender:
    """Apply or replay one validated semantic command/batch result."""

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

    def append(self, request: IdempotentBatchRequest) -> IdempotentAppendResult:
        if not isinstance(request, IdempotentBatchRequest):
            raise TypeError("request must be an IdempotentBatchRequest")
        fingerprint = idempotency_fingerprint(
            request.command, request.pending_events
        )
        connection = self._store._connection
        self._store._require_initialized()
        receipt: BatchAppendReceipt | None = None

        try:
            begin_immediate(connection, self._busy_policy)
            existing = connection.execute(
                """
                SELECT fingerprint_profile, fingerprint, batch_id, stream_id,
                       event_ids_json, first_stream_version, last_stream_version
                FROM idempotency_records
                WHERE idempotency_key = ?
                """,
                (request.command.idempotency_key,),
            ).fetchone()
            if existing is not None:
                if (
                    existing["fingerprint_profile"] != IDEMPOTENCY_PROFILE
                    or existing["fingerprint"] != fingerprint
                ):
                    raise IdempotencyConflictError(
                        request.command.idempotency_key,
                        existing["fingerprint"],
                        fingerprint,
                    )
                receipt = _receipt_from_row(existing)
                commit_with_retry(connection, self._busy_policy)
                return IdempotentAppendResult(
                    IdempotencyStatus.ALREADY_APPLIED,
                    fingerprint,
                    receipt,
                )

            prepared = _prepare_batch(request.entries, self._registry)
            committed = _insert_prepared_batch(connection, prepared)
            receipt = _receipt_from_prepared(committed)
            connection.execute(
                """
                INSERT INTO idempotency_records(
                    idempotency_key, fingerprint_profile, fingerprint,
                    batch_id, stream_id, event_ids_json,
                    first_stream_version, last_stream_version, applied_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request.command.idempotency_key,
                    IDEMPOTENCY_PROFILE,
                    fingerprint,
                    receipt.batch_id,
                    receipt.stream_id,
                    canonical_json_bytes(list(receipt.event_ids)),
                    receipt.first_stream_version,
                    receipt.last_stream_version,
                    canonical_timestamp(committed[0].event.recorded_at),
                ),
            )
        except sqlite3.IntegrityError as exc:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            if is_stream_version_conflict(exc):
                first = request.entries[0].event
                raise VersionConflictError(
                    first.stream_id,
                    first.stream_version,
                ) from exc
            raise
        except Exception:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            raise
        else:
            commit_with_retry(connection, self._busy_policy)

        if receipt is None:  # pragma: no cover - defensive control-flow guard
            raise AssertionError("idempotent receipt was not allocated")
        return IdempotentAppendResult(
            IdempotencyStatus.APPLIED,
            fingerprint,
            receipt,
        )


def idempotency_fingerprint(
    command: CommandEnvelope,
    pending_events: Iterable[PendingEvent],
) -> str:
    """Fingerprint semantic command intent plus the ordered proposed batch.

    Volatile command/event identifiers and timestamps are deliberately excluded.
    """

    if not isinstance(command, CommandEnvelope):
        raise TypeError("command must be a CommandEnvelope")
    pending = snapshot_pending_batch(pending_events)
    semantic_value = {
        "profile": IDEMPOTENCY_PROFILE,
        "command": {
            "command_type": command.command_type,
            "command_schema": command.command_schema,
            "target_stream": command.target_stream,
            "expected_stream_version": command.expected_stream_version,
            "issuer": actor_ref_value(command.issuer),
            "authority": authority_ref_value(command.authority),
            "payload": command.payload,
        },
        "pending_events": pending_batch_value(pending),
    }
    digest = hashlib.sha256(canonical_json_bytes(semantic_value)).hexdigest()
    return f"sha256:{digest}"


def _validate_request_alignment(
    command: CommandEnvelope,
    pending: tuple[PendingEvent, ...],
    entries: tuple[BatchEntry, ...],
) -> None:
    if len(pending) != len(entries):
        raise IdempotencyInvariantError(
            "pending event count must equal committed entry count"
        )
    first_event = entries[0].event
    if first_event.stream_id != command.target_stream:
        raise IdempotencyInvariantError(
            "command target_stream must match batch stream"
        )
    if first_event.stream_version != command.expected_stream_version + 1:
        raise IdempotencyInvariantError(
            "first stream version must follow expected_stream_version"
        )
    if first_event.initiator != command.issuer:
        raise IdempotencyInvariantError(
            "command issuer must match event initiator"
        )
    if first_event.authority != command.authority:
        raise IdempotencyInvariantError(
            "command authority must match event authority"
        )
    if first_event.correlation_id != command.correlation_id:
        raise IdempotencyInvariantError(
            "command correlation_id must match event correlation_id"
        )
    if first_event.causation_id != command.command_id:
        raise IdempotencyInvariantError(
            "event causation_id must match command_id"
        )

    for index, (proposed, entry) in enumerate(zip(pending, entries, strict=True)):
        committed = entry.event
        if committed.event_type != proposed.event_type:
            raise IdempotencyInvariantError(
                f"event_type mismatch at batch index {index}"
            )
        if committed.payload_schema != proposed.payload_schema:
            raise IdempotencyInvariantError(
                f"payload_schema mismatch at batch index {index}"
            )
        if committed.affects_domain_state is not proposed.affects_domain_state:
            raise IdempotencyInvariantError(
                f"affects_domain_state mismatch at batch index {index}"
            )
        if canonical_json_bytes(entry.payload) != canonical_json_bytes(proposed.payload):
            raise IdempotencyInvariantError(
                f"payload mismatch at batch index {index}"
            )


def _receipt_from_row(row: sqlite3.Row) -> BatchAppendReceipt:
    raw_event_ids = json.loads(bytes(row["event_ids_json"]).decode("utf-8"))
    if not isinstance(raw_event_ids, list) or any(
        not isinstance(item, str) for item in raw_event_ids
    ):
        raise RuntimeError("invalid stored idempotency receipt")
    return BatchAppendReceipt(
        batch_id=row["batch_id"],
        stream_id=row["stream_id"],
        event_ids=tuple(raw_event_ids),
        first_stream_version=row["first_stream_version"],
        last_stream_version=row["last_stream_version"],
    )
