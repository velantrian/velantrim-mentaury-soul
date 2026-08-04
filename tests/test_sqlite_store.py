from __future__ import annotations

import json
import sqlite3
from dataclasses import replace
from pathlib import Path

import pytest

from mentaury.contracts import ActorRef, AuthorityRef, EventEnvelope, ProducerRef
from mentaury.storage import (
    SQLiteEventPayloadStore,
    StoreNotInitializedError,
    VersionConflictError,
)


def event(
    *,
    event_id: str = "EVT-1",
    payload_ref: str = "PAYLOAD-1",
    stream_version: int = 1,
    event_hash: str = "sha256:event",
) -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id,
        event_type="BELIEF_CREATED",
        envelope_schema_version=1,
        payload_schema="belief-created/v1",
        stream_id="belief:B-204",
        stream_version=stream_version,
        batch_id=f"BATCH-{stream_version}",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-05T00:00:00+02:00",
        recorded_at="2026-08-04T22:00:00.120Z",
        producer=ProducerRef("belief-command-handler", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-81", 2),
        causation_id="CMD-1",
        correlation_id="CORR-12",
        affects_domain_state=True,
        payload_digest="sha256:not-verified-in-p0-004",
        payload_ref=payload_ref,
        previous_hash="sha256:genesis",
        event_hash=event_hash,
    )


def test_schema_initialization_is_explicit() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        with pytest.raises(StoreNotInitializedError):
            store.load_event("EVT-1")
        store.initialize_schema()
        assert store.load_event("EVT-1") is None


def test_event_and_payload_are_stored_separately_and_reconstructed() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        original = event()
        store.append_one(original, {"statement": "alpha", "evidence": ["E-1"]})

        assert store.load_event("EVT-1") == replace(
            original,
            occurred_at="2026-08-04T22:00:00Z",
            recorded_at="2026-08-04T22:00:00.120Z",
        )
        payload = store.load_payload("PAYLOAD-1")
        assert payload is not None
        assert json.loads(payload.payload_bytes) == {
            "evidence": ["E-1"],
            "statement": "alpha",
        }
        columns = {
            row[1]
            for row in store.raw_connection_for_tests().execute(
                "PRAGMA table_info(events)"
            )
        }
        assert "payload_bytes" not in columns


def test_event_reconstruction_normalizes_timestamps() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        store.append_one(event(), {"statement": "alpha"})
        loaded = store.load_event("EVT-1")
        assert loaded is not None
        assert loaded.occurred_at == "2026-08-04T22:00:00Z"
        assert loaded.recorded_at == "2026-08-04T22:00:00.120Z"


def test_direct_event_update_and_delete_are_rejected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        store.append_one(event(), {"statement": "alpha"})
        connection = store.raw_connection_for_tests()

        with pytest.raises(sqlite3.IntegrityError, match="cannot be updated"):
            connection.execute(
                "UPDATE events SET event_type = 'CHANGED' WHERE event_id = 'EVT-1'"
            )
        with pytest.raises(sqlite3.IntegrityError, match="cannot be deleted"):
            connection.execute("DELETE FROM events WHERE event_id = 'EVT-1'")

        assert store.load_event("EVT-1") is not None


def test_payload_material_cannot_be_rewritten_in_place() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        store.append_one(event(), {"statement": "alpha"})
        with pytest.raises(sqlite3.IntegrityError, match="cannot be rewritten"):
            store.raw_connection_for_tests().execute(
                "UPDATE event_payloads SET payload_bytes = X'00' WHERE payload_ref = 'PAYLOAD-1'"
            )


def test_failed_event_insert_rolls_back_new_payload() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        store.append_one(event(), {"statement": "alpha"})

        duplicate_version = event(
            event_id="EVT-2",
            payload_ref="PAYLOAD-2",
            stream_version=1,
        )
        with pytest.raises(VersionConflictError):
            store.append_one(duplicate_version, {"statement": "beta"})

        assert store.load_event("EVT-2") is None
        assert store.load_payload("PAYLOAD-2") is None


def test_stream_listing_is_ordered() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        store.append_one(event(), {"n": 1})
        store.append_one(
            event(
                event_id="EVT-2",
                payload_ref="PAYLOAD-2",
                stream_version=2,
                event_hash="sha256:event-2",
            ),
            {"n": 2},
        )
        assert [item.event_id for item in store.list_stream("belief:B-204")] == [
            "EVT-1",
            "EVT-2",
        ]


def test_p0_004_records_but_does_not_verify_digest_or_hash() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        arbitrary = event(event_hash="not-a-real-hash")
        store.append_one(arbitrary, {"statement": "alpha"})
        loaded = store.load_event("EVT-1")
        assert loaded is not None
        assert loaded.event_hash == "not-a-real-hash"


def test_database_persists_across_explicit_reopen(tmp_path: Path) -> None:
    database = tmp_path / "mentaury.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        store.append_one(event(), {"statement": "alpha"})

    with SQLiteEventPayloadStore.connect(database) as reopened:
        assert reopened.load_event("EVT-1") is not None
        assert reopened.load_payload("PAYLOAD-1") is not None


def test_no_public_payload_deletion_api_exists() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        assert not hasattr(store, "delete_payload")
        assert not hasattr(store, "redact_payload")
