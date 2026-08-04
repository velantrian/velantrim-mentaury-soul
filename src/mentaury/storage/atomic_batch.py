"""P0-006 real ordered atomic multi-event batch append."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from mentaury.contracts import EventEnvelope, canonical_json_bytes, canonical_timestamp
from mentaury.contracts.primitives import FrozenPayload, freeze_payload

from .concurrency import (
    DEFAULT_BUSY_RETRY_POLICY,
    BusyRetryPolicy,
    VersionConflictError,
    begin_immediate,
    commit_with_retry,
    is_stream_version_conflict,
)
from .sqlite_store import SQLiteEventPayloadStore
from .stream_meta import require_expected_stream_version, update_stream_meta


class BatchInvariantError(ValueError):
    """Raised before storage when batch metadata is incoherent."""


@dataclass(frozen=True, slots=True)
class BatchEntry:
    event: EventEnvelope
    payload: FrozenPayload

    def __post_init__(self) -> None:
        if not isinstance(self.event, EventEnvelope):
            raise TypeError("event must be an EventEnvelope")
        if not isinstance(self.payload, Mapping):
            raise TypeError("payload must be a mapping")
        object.__setattr__(self, "payload", freeze_payload(self.payload))


@dataclass(frozen=True, slots=True)
class BatchAppendReceipt:
    batch_id: str
    stream_id: str
    event_ids: tuple[str, ...]
    first_stream_version: int
    last_stream_version: int


@dataclass(frozen=True, slots=True)
class _PreparedEntry:
    event: EventEnvelope
    payload_bytes: bytes
    created_at: str


class SQLiteAtomicBatchAppender:
    """Append one coherent ordered event batch in a single SQL transaction."""

    def __init__(
        self,
        store: SQLiteEventPayloadStore,
        busy_policy: BusyRetryPolicy = DEFAULT_BUSY_RETRY_POLICY,
    ) -> None:
        if not isinstance(store, SQLiteEventPayloadStore):
            raise TypeError("store must be a SQLiteEventPayloadStore")
        if not isinstance(busy_policy, BusyRetryPolicy):
            raise TypeError("busy_policy must be a BusyRetryPolicy")
        self._store = store
        self._busy_policy = busy_policy

    def append(self, entries: Iterable[BatchEntry]) -> BatchAppendReceipt:
        prepared = _prepare_batch(tuple(entries))
        self._store._require_initialized()
        connection = self._store._connection

        try:
            begin_immediate(connection, self._busy_policy)
            _insert_prepared_batch(connection, prepared)
        except sqlite3.IntegrityError as exc:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            if is_stream_version_conflict(exc):
                raise VersionConflictError(
                    prepared[0].event.stream_id,
                    prepared[0].event.stream_version,
                ) from exc
            raise
        except Exception:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            raise
        else:
            commit_with_retry(connection, self._busy_policy)

        return _receipt_from_prepared(prepared)


def _prepare_batch(entries: tuple[BatchEntry, ...]) -> tuple[_PreparedEntry, ...]:
    if not entries:
        raise BatchInvariantError("batch cannot be empty")
    if any(not isinstance(entry, BatchEntry) for entry in entries):
        raise TypeError("all entries must be BatchEntry")
    events = tuple(entry.event for entry in entries)
    expected_size = len(events)
    first = events[0]
    event_ids: set[str] = set()
    payload_refs: set[str] = set()
    for index, event in enumerate(events):
        if event.batch_id != first.batch_id:
            raise BatchInvariantError("all events must share one batch_id")
        if event.stream_id != first.stream_id:
            raise BatchInvariantError("P0-006 batch must target one stream")
        if event.batch_size != expected_size:
            raise BatchInvariantError("event batch_size must equal entry count")
        if event.batch_index != index:
            raise BatchInvariantError("batch_index must match input order")
        if event.stream_version != first.stream_version + index:
            raise BatchInvariantError("stream versions must be contiguous")
        if event.causation_id != first.causation_id:
            raise BatchInvariantError("all events must share one causation_id")
        if event.correlation_id != first.correlation_id:
            raise BatchInvariantError("all events must share one correlation_id")
        if event.initiator != first.initiator or event.authority != first.authority:
            raise BatchInvariantError("all events must share initiator and authority refs")
        if event.event_id in event_ids:
            raise BatchInvariantError("event_id must be unique inside batch")
        if event.payload_ref in payload_refs:
            raise BatchInvariantError("payload_ref must be unique inside batch")
        event_ids.add(event.event_id)
        payload_refs.add(event.payload_ref)
    return tuple(
        _PreparedEntry(
            event=entry.event,
            payload_bytes=canonical_json_bytes(entry.payload),
            created_at=canonical_timestamp(entry.event.recorded_at),
        )
        for entry in entries
    )


def _insert_prepared_batch(
    connection: sqlite3.Connection,
    prepared: tuple[_PreparedEntry, ...],
) -> None:
    previous_meta = require_expected_stream_version(connection, prepared[0].event)
    for item in prepared:
        _insert_payload(connection, item)
        _insert_event(connection, item.event)
    update_stream_meta(
        connection,
        tuple(item.event for item in prepared),
        previous_meta,
    )


def _receipt_from_prepared(prepared: tuple[_PreparedEntry, ...]) -> BatchAppendReceipt:
    events = tuple(item.event for item in prepared)
    return BatchAppendReceipt(
        batch_id=events[0].batch_id,
        stream_id=events[0].stream_id,
        event_ids=tuple(event.event_id for event in events),
        first_stream_version=events[0].stream_version,
        last_stream_version=events[-1].stream_version,
    )


def _insert_payload(connection: sqlite3.Connection, item: _PreparedEntry) -> None:
    connection.execute(
        "INSERT INTO event_payloads(payload_ref, payload_bytes, created_at) VALUES (?, ?, ?)",
        (item.event.payload_ref, item.payload_bytes, item.created_at),
    )


def _insert_event(connection: sqlite3.Connection, event: EventEnvelope) -> None:
    connection.execute(
        """
        INSERT INTO events(
            event_id, event_type, envelope_schema_version, payload_schema,
            stream_id, stream_version, batch_id, batch_index, batch_size,
            occurred_at, recorded_at, producer_component, producer_version,
            initiator_type, initiator_id, capability_lease_id,
            capability_revision, causation_id, correlation_id,
            affects_domain_state, payload_digest, payload_ref,
            previous_hash, event_hash
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            event.event_id, event.event_type, event.envelope_schema_version,
            event.payload_schema, event.stream_id, event.stream_version,
            event.batch_id, event.batch_index, event.batch_size,
            canonical_timestamp(event.occurred_at), canonical_timestamp(event.recorded_at),
            event.producer.component, event.producer.version,
            event.initiator.actor_type, event.initiator.actor_id,
            event.authority.capability_lease_id, event.authority.capability_revision,
            event.causation_id, event.correlation_id, int(event.affects_domain_state),
            event.payload_digest, event.payload_ref, event.previous_hash, event.event_hash,
        ),
    )
