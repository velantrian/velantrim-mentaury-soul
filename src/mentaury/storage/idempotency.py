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
from .sealing import compute_payload_digest
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


class IdempotencyReceiptIntegrityError(RuntimeError):
    """Raised when a stored ALREADY_APPLIED receipt is not ledger-backed."""

    def __init__(self, idempotency_key: str, detail: str) -> None:
        self.idempotency_key = idempotency_key
        self.detail = detail
        super().__init__(
            f"invalid stored idempotency receipt for key "
            f"{idempotency_key}: {detail}"
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
                receipt = _receipt_from_row(
                    existing,
                    request.command.idempotency_key,
                )
                _verify_stored_receipt(
                    connection,
                    receipt,
                    request,
                )
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


def _receipt_from_row(
    row: sqlite3.Row,
    idempotency_key: str,
) -> BatchAppendReceipt:
    try:
        encoded_event_ids = bytes(row["event_ids_json"])
        decoded_event_ids = json.loads(encoded_event_ids.decode("utf-8"))
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json is not valid UTF-8 JSON",
        ) from exc

    if not isinstance(decoded_event_ids, list) or not decoded_event_ids:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json must be a non-empty list",
        )
    if any(
        not isinstance(event_id, str) or not event_id
        for event_id in decoded_event_ids
    ):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json must contain non-empty strings",
        )
    if len(set(decoded_event_ids)) != len(decoded_event_ids):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json must not contain duplicate event IDs",
        )
    if canonical_json_bytes(decoded_event_ids) != encoded_event_ids:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event_ids_json must use canonical JSON encoding",
        )

    batch_id = row["batch_id"]
    stream_id = row["stream_id"]
    first_stream_version = row["first_stream_version"]
    last_stream_version = row["last_stream_version"]
    if not isinstance(batch_id, str) or not batch_id:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "batch_id must be a non-empty string",
        )
    if not isinstance(stream_id, str) or not stream_id:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "stream_id must be a non-empty string",
        )
    if (
        isinstance(first_stream_version, bool)
        or not isinstance(first_stream_version, int)
        or first_stream_version <= 0
    ):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "first_stream_version must be a positive integer",
        )
    if (
        isinstance(last_stream_version, bool)
        or not isinstance(last_stream_version, int)
        or last_stream_version < first_stream_version
    ):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "last_stream_version must not precede first_stream_version",
        )

    receipt = BatchAppendReceipt(
        batch_id=batch_id,
        stream_id=stream_id,
        event_ids=tuple(decoded_event_ids),
        first_stream_version=first_stream_version,
        last_stream_version=last_stream_version,
    )
    expected_count = (
        receipt.last_stream_version - receipt.first_stream_version + 1
    )
    if len(receipt.event_ids) != expected_count:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "event ID count does not match the stored version span",
        )
    return receipt


def _verify_stored_receipt(
    connection: sqlite3.Connection,
    receipt: BatchAppendReceipt,
    request: IdempotentBatchRequest,
) -> None:
    idempotency_key = request.command.idempotency_key
    expected_first_version = request.command.expected_stream_version + 1
    if receipt.stream_id != request.command.target_stream:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "stored stream_id does not match command target_stream",
        )
    if receipt.first_stream_version != expected_first_version:
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "stored first_stream_version does not follow the command expectation",
        )
    if len(receipt.event_ids) != len(request.pending_events):
        raise IdempotencyReceiptIntegrityError(
            idempotency_key,
            "stored event count does not match the fingerprinted pending batch",
        )

    expected_batch_size = len(receipt.event_ids)
    for offset, (event_id, proposed) in enumerate(
        zip(receipt.event_ids, request.pending_events, strict=True)
    ):
        row = connection.execute(
            """
            SELECT event_id, batch_id, batch_index, batch_size,
                   stream_id, stream_version, event_type, payload_schema,
                   affects_domain_state, payload_digest,
                   initiator_type, initiator_id,
                   capability_lease_id, capability_revision
            FROM events
            WHERE event_id = ?
            """,
            (event_id,),
        ).fetchone()
        if row is None:
            raise IdempotencyReceiptIntegrityError(
                idempotency_key,
                f"referenced event {event_id} does not exist",
            )

        expected_version = receipt.first_stream_version + offset
        checks = (
            (row["batch_id"] == receipt.batch_id, "batch_id"),
            (row["batch_index"] == offset, "batch_index"),
            (row["batch_size"] == expected_batch_size, "batch_size"),
            (row["stream_id"] == receipt.stream_id, "stream_id"),
            (row["stream_version"] == expected_version, "stream_version"),
            (row["event_type"] == proposed.event_type, "event_type"),
            (row["payload_schema"] == proposed.payload_schema, "payload_schema"),
            (
                bool(row["affects_domain_state"])
                is proposed.affects_domain_state,
                "affects_domain_state",
            ),
            (
                row["payload_digest"]
                == compute_payload_digest(canonical_json_bytes(proposed.payload)),
                "payload_digest",
            ),
            (
                row["initiator_type"] == request.command.issuer.actor_type
                and row["initiator_id"] == request.command.issuer.actor_id,
                "initiator",
            ),
            (
                row["capability_lease_id"]
                == request.command.authority.capability_lease_id
                and row["capability_revision"]
                == request.command.authority.capability_revision,
                "authority",
            ),
        )
        for matches, field in checks:
            if not matches:
                raise IdempotencyReceiptIntegrityError(
                    idempotency_key,
                    f"event {event_id} {field} does not match the fingerprinted request",
                )
