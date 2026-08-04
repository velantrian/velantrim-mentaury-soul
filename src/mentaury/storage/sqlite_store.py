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

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    EventEnvelope,
    ProducerRef,
    canonical_json_bytes,
    canonical_timestamp,
)

SCHEMA_VERSION: Final[int] = 1


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


class SQLiteEventPayloadStore:
    """Replaceable first-profile adapter for P0-004 storage primitives."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")

    @classmethod
    def connect(cls, path: str | Path) -> Self:
        """Open a database explicitly without initializing its schema."""

        connection = sqlite3.connect(path, isolation_level=None)
        return cls(connection)

    @classmethod
    def in_memory(cls) -> Self:
        """Open an explicit isolated in-memory database for deterministic tests."""

        return cls.connect(":memory:")

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def initialize_schema(self) -> None:
        """Create the P0-004 tables and immutability triggers explicitly."""

        self._connection.executescript(_SCHEMA_SQL)
        version = self._connection.execute(
            "SELECT schema_version FROM p0_schema_meta WHERE singleton = 1"
        ).fetchone()
        if version is None or version["schema_version"] != SCHEMA_VERSION:
            raise StorageError("unsupported P0 storage schema version")

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
        """Atomically store one external payload and one immutable event row.

        The supplied digest/hash fields are recorded but deliberately not
        computed or verified in P0-004. Real multi-event append belongs to
        P0-006.
        """

        if not isinstance(event, EventEnvelope):
            raise TypeError("event must be an EventEnvelope")
        self._require_initialized()
        payload_bytes = canonical_json_bytes(payload)
        created_at = canonical_timestamp(event.recorded_at)

        try:
            self._connection.execute("BEGIN")
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
        except Exception:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise
        else:
            self._connection.execute("COMMIT")

    def load_event(self, event_id: str) -> EventEnvelope | None:
        """Reconstruct the complete immutable envelope metadata."""

        self._require_initialized()
        row = self._connection.execute(
            "SELECT * FROM events WHERE event_id = ?", (event_id,)
        ).fetchone()
        if row is None:
            return None
        return _event_from_row(row)

    def load_payload(self, payload_ref: str) -> StoredPayload | None:
        """Load external payload bytes without interpreting domain schema."""

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
        """Return immutable envelope metadata in stream-version order."""

        self._require_initialized()
        rows = self._connection.execute(
            "SELECT * FROM events WHERE stream_id = ? ORDER BY stream_version",
            (stream_id,),
        ).fetchall()
        return tuple(_event_from_row(row) for row in rows)

    def raw_connection_for_tests(self) -> sqlite3.Connection:
        """Expose the connection only for adversarial infrastructure tests.

        This method is not a domain capability. It exists so tests can prove
        SQLite triggers reject direct event-row mutation.
        """

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
