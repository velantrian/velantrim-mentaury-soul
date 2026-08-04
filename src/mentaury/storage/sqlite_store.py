"""P0-004 SQLite adapter for immutable event rows and external payloads.

The adapter is explicit: importing this module opens no database. P0-004 stores
one already-formed EventEnvelope together with canonical payload bytes in one
transaction. It does not allocate versions, validate domain schemas, resolve
authority, compute hashes, append multi-event batches, or implement redaction.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Self

from .concurrency import (
    DEFAULT_BUSY_RETRY_POLICY,
    BusyRetryPolicy,
    VersionConflictError,
    begin_immediate,
    commit_with_retry,
    is_stream_version_conflict,
)
from .stream_meta import (
    StreamMeta,
    read_stream_meta,
    require_expected_stream_version,
    update_stream_meta,
)

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    EventEnvelope,
    ProducerRef,
    canonical_json_bytes,
    canonical_timestamp,
)

SCHEMA_VERSION: Final[int] = 3
MINIMUM_SQLITE_VERSION: Final[tuple[int, int, int]] = (3, 37, 0)


class StorageError(RuntimeError):
    """Base error for controlled P0-004 storage failures."""


class StoreNotInitializedError(StorageError):
    """Raised when operations are attempted before explicit schema setup."""


@dataclass(frozen=True, slots=True)
class StoredPayload:
    """External payload material detached from the immutable event row."""

    payload_ref: str
    payload_bytes: bytes
    created_at: str


_SCHEMA_SQL: Final[str] = """
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS p0_schema_meta (
    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
    schema_version INTEGER NOT NULL CHECK (schema_version > 0)
);

INSERT INTO p0_schema_meta(singleton, schema_version)
VALUES (1, 1)
ON CONFLICT(singleton) DO NOTHING;

CREATE TABLE IF NOT EXISTS event_payloads (
    payload_ref TEXT PRIMARY KEY NOT NULL,
    payload_bytes BLOB NOT NULL,
    created_at TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY NOT NULL,
    event_type TEXT NOT NULL,
    envelope_schema_version INTEGER NOT NULL CHECK (envelope_schema_version > 0),
    payload_schema TEXT NOT NULL,
    stream_id TEXT NOT NULL,
    stream_version INTEGER NOT NULL CHECK (stream_version > 0),
    batch_id TEXT NOT NULL,
    batch_index INTEGER NOT NULL CHECK (batch_index >= 0),
    batch_size INTEGER NOT NULL CHECK (batch_size > 0),
    occurred_at TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    producer_component TEXT NOT NULL,
    producer_version TEXT NOT NULL,
    initiator_type TEXT NOT NULL,
    initiator_id TEXT NOT NULL,
    capability_lease_id TEXT NOT NULL,
    capability_revision INTEGER NOT NULL CHECK (capability_revision >= 0),
    causation_id TEXT NOT NULL,
    correlation_id TEXT NOT NULL,
    affects_domain_state INTEGER NOT NULL CHECK (affects_domain_state IN (0, 1)),
    payload_digest TEXT NOT NULL,
    payload_ref TEXT NOT NULL,
    previous_hash TEXT NOT NULL,
    event_hash TEXT NOT NULL,
    UNIQUE(stream_id, stream_version),
    CHECK (batch_index < batch_size)
) STRICT;

CREATE INDEX IF NOT EXISTS events_stream_order
ON events(stream_id, stream_version);

CREATE TRIGGER IF NOT EXISTS events_are_immutable_on_update
BEFORE UPDATE ON events
BEGIN
    SELECT RAISE(ABORT, 'immutable event rows cannot be updated');
END;

CREATE TRIGGER IF NOT EXISTS events_are_immutable_on_delete
BEFORE DELETE ON events
BEGIN
    SELECT RAISE(ABORT, 'immutable event rows cannot be deleted');
END;

CREATE TRIGGER IF NOT EXISTS payload_material_cannot_be_rewritten
BEFORE UPDATE OF payload_ref, payload_bytes, created_at ON event_payloads
BEGIN
    SELECT RAISE(ABORT, 'payload material cannot be rewritten');
END;
"""

_MIGRATE_1_TO_2_SQL: Final[str] = """
BEGIN IMMEDIATE;

CREATE TABLE idempotency_records (
    idempotency_key TEXT PRIMARY KEY NOT NULL,
    fingerprint_profile TEXT NOT NULL,
    fingerprint TEXT NOT NULL,
    batch_id TEXT NOT NULL,
    stream_id TEXT NOT NULL,
    event_ids_json BLOB NOT NULL,
    first_stream_version INTEGER NOT NULL CHECK (first_stream_version > 0),
    last_stream_version INTEGER NOT NULL CHECK (last_stream_version >= first_stream_version),
    applied_at TEXT NOT NULL
) STRICT;

CREATE TRIGGER idempotency_records_are_immutable_on_update
BEFORE UPDATE ON idempotency_records
BEGIN
    SELECT RAISE(ABORT, 'idempotency records cannot be updated');
END;

CREATE TRIGGER idempotency_records_are_immutable_on_delete
BEFORE DELETE ON idempotency_records
BEGIN
    SELECT RAISE(ABORT, 'idempotency records cannot be deleted');
END;

UPDATE p0_schema_meta SET schema_version = 2 WHERE singleton = 1;
COMMIT;
"""

_MIGRATE_2_TO_3_SQL: Final[str] = """
BEGIN IMMEDIATE;

CREATE TABLE stream_meta (
    stream_id TEXT PRIMARY KEY NOT NULL,
    current_version INTEGER NOT NULL CHECK (current_version >= 0),
    last_event_hash TEXT NOT NULL,
    event_count INTEGER NOT NULL CHECK (event_count >= 0)
) STRICT;

INSERT INTO stream_meta(stream_id, current_version, last_event_hash, event_count)
SELECT
    e.stream_id,
    MAX(e.stream_version),
    (
        SELECT tail.event_hash
        FROM events AS tail
        WHERE tail.stream_id = e.stream_id
        ORDER BY tail.stream_version DESC
        LIMIT 1
    ),
    COUNT(*)
FROM events AS e
GROUP BY e.stream_id;

UPDATE p0_schema_meta SET schema_version = 3 WHERE singleton = 1;
COMMIT;
"""


class SQLiteEventPayloadStore:
    """Replaceable first-profile adapter for P0-004 storage primitives."""

    def __init__(
        self,
        connection: sqlite3.Connection,
        busy_policy: BusyRetryPolicy = DEFAULT_BUSY_RETRY_POLICY,
    ) -> None:
        ensure_supported_sqlite_runtime()
        if not isinstance(busy_policy, BusyRetryPolicy):
            raise TypeError("busy_policy must be a BusyRetryPolicy")
        self._connection = connection
        self._busy_policy = busy_policy
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")

    @classmethod
    def connect(
        cls,
        path: str | Path,
        *,
        busy_timeout_ms: int = 0,
        busy_policy: BusyRetryPolicy = DEFAULT_BUSY_RETRY_POLICY,
    ) -> Self:
        """Open a database explicitly with bounded application-level retries."""

        if isinstance(busy_timeout_ms, bool) or busy_timeout_ms < 0:
            raise ValueError("busy_timeout_ms must be a non-negative integer")
        connection = sqlite3.connect(
            path,
            isolation_level=None,
            timeout=busy_timeout_ms / 1000,
        )
        connection.execute(f"PRAGMA busy_timeout = {busy_timeout_ms}")
        return cls(connection, busy_policy)

    @classmethod
    def in_memory(
        cls,
        *,
        busy_policy: BusyRetryPolicy = DEFAULT_BUSY_RETRY_POLICY,
    ) -> Self:
        """Open an explicit isolated in-memory database for deterministic tests."""

        return cls.connect(":memory:", busy_policy=busy_policy)

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def initialize_schema(self) -> None:
        """Create or migrate the explicit P0 storage schema."""

        self._connection.executescript(_SCHEMA_SQL)
        version = self._connection.execute(
            "SELECT schema_version FROM p0_schema_meta WHERE singleton = 1"
        ).fetchone()
        if version is None:
            raise StorageError("missing P0 storage schema version")
        current = version["schema_version"]
        if current == 1:
            try:
                self._connection.executescript(_MIGRATE_1_TO_2_SQL)
            except Exception:
                if self._connection.in_transaction:
                    self._connection.execute("ROLLBACK")
                raise
            current = 2
        if current == 2:
            try:
                self._connection.executescript(_MIGRATE_2_TO_3_SQL)
            except Exception:
                if self._connection.in_transaction:
                    self._connection.execute("ROLLBACK")
                raise
            current = 3
        if current != SCHEMA_VERSION:
            raise StorageError("unsupported P0 storage schema version")
        try:
            self._connection.execute(
                "SELECT idempotency_key FROM idempotency_records LIMIT 0"
            )
            self._connection.execute(
                "SELECT stream_id FROM stream_meta LIMIT 0"
            )
        except sqlite3.OperationalError as exc:
            raise StorageError("incomplete P0 storage schema") from exc

    def _require_initialized(self) -> None:
        try:
            row = self._connection.execute(
                "SELECT schema_version FROM p0_schema_meta WHERE singleton = 1"
            ).fetchone()
        except sqlite3.OperationalError as exc:
            raise StoreNotInitializedError(
                "storage schema must be initialized explicitly"
            ) from exc
        if row is None or row["schema_version"] != SCHEMA_VERSION:
            raise StoreNotInitializedError("unsupported or missing storage schema")

    def append_one(
        self,
        event: EventEnvelope,
        payload: Mapping[str, object],
    ) -> None:
        """Atomically store one external payload and one immutable event row."""

        if not isinstance(event, EventEnvelope):
            raise TypeError("event must be an EventEnvelope")
        self._require_initialized()
        payload_bytes = canonical_json_bytes(payload)
        created_at = canonical_timestamp(event.recorded_at)

        try:
            begin_immediate(self._connection, self._busy_policy)
            previous_meta = require_expected_stream_version(
                self._connection, event
            )
            self._connection.execute(
                """
                INSERT INTO event_payloads(payload_ref, payload_bytes, created_at)
                VALUES (?, ?, ?)
                """,
                (event.payload_ref, payload_bytes, created_at),
            )
            self._connection.execute(
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
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?
                )
                """,
                (
                    event.event_id,
                    event.event_type,
                    event.envelope_schema_version,
                    event.payload_schema,
                    event.stream_id,
                    event.stream_version,
                    event.batch_id,
                    event.batch_index,
                    event.batch_size,
                    canonical_timestamp(event.occurred_at),
                    canonical_timestamp(event.recorded_at),
                    event.producer.component,
                    event.producer.version,
                    event.initiator.actor_type,
                    event.initiator.actor_id,
                    event.authority.capability_lease_id,
                    event.authority.capability_revision,
                    event.causation_id,
                    event.correlation_id,
                    int(event.affects_domain_state),
                    event.payload_digest,
                    event.payload_ref,
                    event.previous_hash,
                    event.event_hash,
                ),
            )
            update_stream_meta(self._connection, (event,), previous_meta)
        except sqlite3.IntegrityError as exc:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            if is_stream_version_conflict(exc):
                raise VersionConflictError(
                    event.stream_id,
                    event.stream_version,
                ) from exc
            raise
        except Exception:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise
        else:
            commit_with_retry(self._connection, self._busy_policy)

    def load_event(self, event_id: str) -> EventEnvelope | None:
        self._require_initialized()
        row = self._connection.execute(
            "SELECT * FROM events WHERE event_id = ?", (event_id,)
        ).fetchone()
        if row is None:
            return None
        return _event_from_row(row)

    def load_payload(self, payload_ref: str) -> StoredPayload | None:
        self._require_initialized()
        row = self._connection.execute(
            """
            SELECT payload_ref, payload_bytes, created_at
            FROM event_payloads
            WHERE payload_ref = ?
            """,
            (payload_ref,),
        ).fetchone()
        if row is None:
            return None
        return StoredPayload(
            payload_ref=row["payload_ref"],
            payload_bytes=bytes(row["payload_bytes"]),
            created_at=row["created_at"],
        )

    def list_stream(self, stream_id: str) -> tuple[EventEnvelope, ...]:
        self._require_initialized()
        rows = self._connection.execute(
            "SELECT * FROM events WHERE stream_id = ? ORDER BY stream_version",
            (stream_id,),
        ).fetchall()
        return tuple(_event_from_row(row) for row in rows)

    def load_stream_meta(self, stream_id: str) -> StreamMeta:
        """Return persisted stream metadata or the empty-stream default."""

        self._require_initialized()
        return read_stream_meta(self._connection, stream_id)

    def raw_connection_for_tests(self) -> sqlite3.Connection:
        return self._connection


def _event_from_row(row: sqlite3.Row) -> EventEnvelope:
    return EventEnvelope(
        event_id=row["event_id"],
        event_type=row["event_type"],
        envelope_schema_version=row["envelope_schema_version"],
        payload_schema=row["payload_schema"],
        stream_id=row["stream_id"],
        stream_version=row["stream_version"],
        batch_id=row["batch_id"],
        batch_index=row["batch_index"],
        batch_size=row["batch_size"],
        occurred_at=row["occurred_at"],
        recorded_at=row["recorded_at"],
        producer=ProducerRef(row["producer_component"], row["producer_version"]),
        initiator=ActorRef(row["initiator_type"], row["initiator_id"]),
        authority=AuthorityRef(
            row["capability_lease_id"], row["capability_revision"]
        ),
        causation_id=row["causation_id"],
        correlation_id=row["correlation_id"],
        affects_domain_state=bool(row["affects_domain_state"]),
        payload_digest=row["payload_digest"],
        payload_ref=row["payload_ref"],
        previous_hash=row["previous_hash"],
        event_hash=row["event_hash"],
    )


def ensure_supported_sqlite_runtime(
    version: tuple[int, int, int] | None = None,
) -> None:
    actual = sqlite3.sqlite_version_info if version is None else version
    if actual < MINIMUM_SQLITE_VERSION:
        raise StorageError(
            f"unsupported SQLite runtime {actual}; "
            f"minimum is {MINIMUM_SQLITE_VERSION}"
        )
