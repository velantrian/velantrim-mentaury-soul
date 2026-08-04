from __future__ import annotations

import sqlite3
from dataclasses import replace

import pytest

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    EventEnvelope,
    ProducerRef,
)
from mentaury.storage import (
    BatchEntry,
    BatchInvariantError,
    SQLiteAtomicBatchAppender,
    SQLiteEventPayloadStore,
)


def event(
    index: int,
    *,
    batch_size: int = 3,
    batch_id: str = "BATCH-1",
) -> EventEnvelope:
    return EventEnvelope(
        event_id=f"EVT-{index + 1}",
        event_type="BELIEF_EVENT",
        envelope_schema_version=1,
        payload_schema="belief-event/v1",
        stream_id="belief:B-204",
        stream_version=index + 1,
        batch_id=batch_id,
        batch_index=index,
        batch_size=batch_size,
        occurred_at="2026-08-05T00:00:00Z",
        recorded_at="2026-08-05T00:00:00Z",
        producer=ProducerRef("batch-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-81", 2),
        causation_id="CMD-1",
        correlation_id="CORR-1",
        affects_domain_state=True,
        payload_digest=f"sha256:payload-{index}",
        payload_ref=f"PAYLOAD-{index + 1}",
        previous_hash=f"sha256:previous-{index}",
        event_hash=f"sha256:event-{index}",
    )


def entries(count: int = 3) -> tuple[BatchEntry, ...]:
    return tuple(
        BatchEntry(event(index, batch_size=count), {"index": index})
        for index in range(count)
    )


def test_successful_batch_persists_all_events_and_payloads() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        receipt = SQLiteAtomicBatchAppender(store).append(entries())
        assert receipt.event_ids == ("EVT-1", "EVT-2", "EVT-3")
        assert receipt.first_stream_version == 1
        assert receipt.last_stream_version == 3
        assert [
            item.event_id
            for item in store.list_stream("belief:B-204")
        ] == list(receipt.event_ids)
        assert all(
            store.load_payload(f"PAYLOAD-{index}") is not None
            for index in range(1, 4)
        )


def test_failure_in_middle_rolls_back_entire_new_batch() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        old = replace(
            event(0, batch_size=1),
            event_id="OLD",
            batch_id="OLD",
            stream_version=2,
            payload_ref="OLD-PAYLOAD",
        )
        store.append_one(old, {"old": True})
        with pytest.raises(sqlite3.IntegrityError):
            SQLiteAtomicBatchAppender(store).append(entries())
        assert store.load_event("EVT-1") is None
        assert store.load_event("EVT-3") is None
        assert store.load_payload("PAYLOAD-1") is None
        assert store.load_payload("PAYLOAD-3") is None
        assert store.load_event("OLD") is not None


def test_late_payload_conflict_rolls_back_prior_new_rows() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        old = replace(
            event(0, batch_size=1),
            event_id="OLD",
            batch_id="OLD",
            stream_id="other:stream",
            payload_ref="PAYLOAD-3",
        )
        store.append_one(old, {"old": True})
        with pytest.raises(sqlite3.IntegrityError):
            SQLiteAtomicBatchAppender(store).append(entries())
        assert store.load_event("EVT-1") is None
        assert store.load_event("EVT-2") is None
        assert store.load_payload("PAYLOAD-1") is None
        assert store.load_payload("PAYLOAD-2") is None
        assert store.load_event("OLD") is not None


def test_empty_batch_is_rejected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        with pytest.raises(BatchInvariantError, match="empty"):
            SQLiteAtomicBatchAppender(store).append(())


@pytest.mark.parametrize(
    ("replacement", "message"),
    [
        (lambda item: replace(item, batch_id="OTHER"), "batch_id"),
        (lambda item: replace(item, batch_size=4), "batch_size"),
        (lambda item: replace(item, batch_index=2), "batch_index"),
        (lambda item: replace(item, stream_version=7), "contiguous"),
        (lambda item: replace(item, stream_id="other:stream"), "one stream"),
        (lambda item: replace(item, causation_id="OTHER"), "causation_id"),
    ],
)
def test_incoherent_batch_metadata_is_rejected(
    replacement,
    message: str,
) -> None:
    batch = list(entries())
    batch[1] = BatchEntry(
        replacement(batch[1].event),
        {"index": 1},
    )
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        with pytest.raises(BatchInvariantError, match=message):
            SQLiteAtomicBatchAppender(store).append(batch)
        assert store.list_stream("belief:B-204") == ()


def test_serialization_failure_occurs_before_transaction() -> None:
    batch = list(entries())
    batch[1] = BatchEntry(batch[1].event, {"bad": 1.0})
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        with pytest.raises(ValueError, match="float"):
            SQLiteAtomicBatchAppender(store).append(batch)
        assert not store.raw_connection_for_tests().in_transaction
        assert store.list_stream("belief:B-204") == ()


def test_retry_is_not_idempotent_yet() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteAtomicBatchAppender(store)
        appender.append(entries())
        with pytest.raises(sqlite3.IntegrityError):
            appender.append(entries())
        assert len(store.list_stream("belief:B-204")) == 3
