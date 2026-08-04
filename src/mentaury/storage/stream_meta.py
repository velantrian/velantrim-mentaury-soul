"""P0-009 stream metadata read/update primitives."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from mentaury.contracts import EventEnvelope

from .concurrency import VersionConflictError

GENESIS_HASH = "sha256:genesis"


@dataclass(frozen=True, slots=True)
class StreamMeta:
    stream_id: str
    current_version: int
    last_event_hash: str
    event_count: int
    persisted: bool


def read_stream_meta(connection: sqlite3.Connection, stream_id: str) -> StreamMeta:
    row = connection.execute(
        """
        SELECT stream_id, current_version, last_event_hash, event_count
        FROM stream_meta WHERE stream_id = ?
        """,
        (stream_id,),
    ).fetchone()
    if row is None:
        return StreamMeta(stream_id, 0, GENESIS_HASH, 0, False)
    return StreamMeta(
        stream_id=row["stream_id"],
        current_version=row["current_version"],
        last_event_hash=row["last_event_hash"],
        event_count=row["event_count"],
        persisted=True,
    )


def require_expected_stream_version(
    connection: sqlite3.Connection,
    first_event: EventEnvelope,
) -> StreamMeta:
    meta = read_stream_meta(connection, first_event.stream_id)
    expected = meta.current_version + 1
    if first_event.stream_version != expected:
        raise VersionConflictError(first_event.stream_id, first_event.stream_version)
    return meta


def update_stream_meta(
    connection: sqlite3.Connection,
    events: tuple[EventEnvelope, ...],
    previous: StreamMeta,
) -> None:
    if not events:
        raise ValueError("events cannot be empty")
    last = events[-1]
    event_count = previous.event_count + len(events)
    connection.execute(
        """
        INSERT INTO stream_meta(
            stream_id, current_version, last_event_hash, event_count
        ) VALUES (?, ?, ?, ?)
        ON CONFLICT(stream_id) DO UPDATE SET
            current_version = excluded.current_version,
            last_event_hash = excluded.last_event_hash,
            event_count = excluded.event_count
        """,
        (last.stream_id, last.stream_version, last.event_hash, event_count),
    )
