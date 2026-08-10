"""Регрессия: единый 24-колоночный INSERT helper для events."""

from __future__ import annotations

import re

from mentaury.contracts import ActorRef, AuthorityRef, EventEnvelope, ProducerRef
from mentaury.storage._event_rows import (
    EVENT_INSERT_COLUMN_COUNT,
    EVENT_INSERT_SQL,
    event_row_values,
)

_EXPECTED_COLUMNS = (
    "event_id",
    "event_type",
    "envelope_schema_version",
    "payload_schema",
    "stream_id",
    "stream_version",
    "batch_id",
    "batch_index",
    "batch_size",
    "occurred_at",
    "recorded_at",
    "producer_component",
    "producer_version",
    "initiator_type",
    "initiator_id",
    "capability_lease_id",
    "capability_revision",
    "causation_id",
    "correlation_id",
    "affects_domain_state",
    "payload_digest",
    "payload_ref",
    "previous_hash",
    "event_hash",
)


def _sample_event() -> EventEnvelope:
    return EventEnvelope(
        event_id="EVT-ROW-1",
        event_type="BELIEF_CREATED",
        envelope_schema_version=1,
        payload_schema="belief-created/v1",
        stream_id="belief:row-test",
        stream_version=1,
        batch_id="BATCH-1",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-06T00:00:00Z",
        recorded_at="2026-08-06T00:00:00Z",
        producer=ProducerRef("event-row-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-ROW", 1),
        causation_id="CMD-ROW-1",
        correlation_id="CORR-ROW-1",
        affects_domain_state=True,
        payload_digest="sha256:deadbeef",
        payload_ref="PAYLOAD-ROW-1",
        previous_hash="sha256:genesis",
        event_hash="sha256:event",
    )


def test_event_row_values_returns_exactly_24_values() -> None:
    values = event_row_values(_sample_event())
    assert len(values) == 24
    assert len(values) == EVENT_INSERT_COLUMN_COUNT


def test_event_insert_sql_column_order_matches_schema() -> None:
    match = re.search(
        r"INSERT INTO events\(\s*(.*?)\s*\)\s*VALUES",
        EVENT_INSERT_SQL,
        flags=re.DOTALL,
    )
    assert match is not None
    columns = tuple(
        part.strip() for part in match.group(1).replace("\n", " ").split(",")
    )
    assert columns == _EXPECTED_COLUMNS
    assert len(columns) == 24


def test_event_row_values_field_order_matches_columns() -> None:
    event = _sample_event()
    values = event_row_values(event)
    expected = (
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
        1,
        event.payload_digest,
        event.payload_ref,
        event.previous_hash,
        event.event_hash,
    )
    assert values == expected
