"""Единый helper для INSERT строки ``events``.

Три writer-path (sqlite_store / atomic_batch / redaction) раньше держали
идентичные 24-колоночные INSERT. Этот leaf-модуль централизует SQL и
порядок значений без изменения schema, transaction boundaries,
BEGIN IMMEDIATE, rollback, ordering, hash/digest allocation или
error normalization.
"""

from __future__ import annotations

import sqlite3
from typing import Final

from mentaury.contracts import EventEnvelope

EVENT_INSERT_SQL: Final[str] = """
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
"""

EVENT_INSERT_COLUMN_COUNT: Final[int] = 24


def event_row_values(event: EventEnvelope) -> tuple[object, ...]:
    values = (
        event.event_id,
        event.event_type,
        event.envelope_schema_version,
        event.payload_schema,
        event.stream_id,
        event.stream_version,
        event.batch_id,
        event.batch_index,
        event.batch_size,
        event.occurred_at,
        event.recorded_at,
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
    )
    if len(values) != EVENT_INSERT_COLUMN_COUNT:
        raise RuntimeError(
            f"event row must contain {EVENT_INSERT_COLUMN_COUNT} values, "
            f"got {len(values)}"
        )
    return values


def insert_event_row(
    connection: sqlite3.Connection,
    event: EventEnvelope,
) -> None:
    connection.execute(EVENT_INSERT_SQL, event_row_values(event))
