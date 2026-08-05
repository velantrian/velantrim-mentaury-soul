from __future__ import annotations

import sqlite3
from dataclasses import replace
from pathlib import Path

import pytest

from mentaury.contracts import ActorRef, AuthorityRef, EventEnvelope, ProducerRef
from mentaury.storage import (
    GENESIS_HASH,
    IntegrityCode,
    R0IntegrityVerifier,
    SQLiteAtomicBatchAppender,
    SQLiteEventPayloadStore,
    StorageError,
    BatchEntry,
    seal_event,
)
from mentaury.validation import (
    EventSchemaDefinition,
    IntegerSpec,
    ObjectSpec,
    SchemaRegistry,
)


def registry() -> SchemaRegistry:
    return SchemaRegistry(
        [
            EventSchemaDefinition(
                event_type="TEST_EVENT",
                payload_schema="test-event/v1",
                affects_domain_state=True,
                payload=ObjectSpec(
                    {"n": IntegerSpec(minimum=0)},
                    required=frozenset({"n"}),
                ),
            )
        ]
    )


def raw_event(
    version: int,
    *,
    batch_id: str | None = None,
    batch_index: int = 0,
    batch_size: int = 1,
) -> EventEnvelope:
    return EventEnvelope(
        event_id=f"EVT-{version}",
        event_type="TEST_EVENT",
        envelope_schema_version=1,
        payload_schema="test-event/v1",
        stream_id="test:stream",
        stream_version=version,
        batch_id=batch_id or f"BATCH-{version}",
        batch_index=batch_index,
        batch_size=batch_size,
        occurred_at="2026-08-05T00:00:00Z",
        recorded_at="2026-08-05T00:00:00Z",
        producer=ProducerRef("integrity-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-81", 2),
        causation_id=f"CMD-{version}",
        correlation_id="CORR-1",
        affects_domain_state=True,
        payload_digest="sha256:untrusted",
        payload_ref=f"PAYLOAD-{version}",
        previous_hash="sha256:untrusted",
        event_hash="sha256:untrusted",
    )


def append_valid_stream(
    store: SQLiteEventPayloadStore,
    count: int = 3,
) -> tuple[EventEnvelope, ...]:
    events: list[EventEnvelope] = []
    for version in range(1, count + 1):
        payload = {"n": version}
        committed = store.append_one(
            raw_event(version),
            payload,
            registry=registry(),
        )
        events.append(committed)
    return tuple(events)


def drop_event_update_guard(store: SQLiteEventPayloadStore) -> None:
    store.raw_connection_for_tests().execute(
        "DROP TRIGGER events_are_immutable_on_update"
    )


def test_valid_stream_passes_full_r0() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store)
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.ok
        assert report.checked_events == 3
        assert report.failure is None
        meta = store.load_stream_meta("test:stream")
        assert meta.current_version == 3
        assert meta.event_count == 3


def test_empty_stream_uses_genesis_defaults() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        report = R0IntegrityVerifier(store, registry()).verify_stream("empty")
        assert report.ok
        assert report.checked_events == 0
        meta = store.load_stream_meta("empty")
        assert meta.current_version == 0
        assert meta.last_event_hash == GENESIS_HASH
        assert not meta.persisted


def test_payload_tampering_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 1)
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER payload_material_cannot_be_rewritten")
        connection.execute(
            "UPDATE event_payloads SET payload_bytes = ? WHERE payload_ref = 'PAYLOAD-1'",
            (b'{"n":999}',),
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.PAYLOAD_DIGEST_MISMATCH


def test_noncanonical_payload_bytes_are_detected_before_digest_comparison() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 1)
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER payload_material_cannot_be_rewritten")
        connection.execute(
            "UPDATE event_payloads SET payload_bytes = ? WHERE payload_ref = 'PAYLOAD-1'",
            (b'{ "n" : 1 }',),
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.PAYLOAD_NOT_CANONICAL


def test_event_hash_tampering_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 1)
        drop_event_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE events SET event_hash = 'sha256:tampered' WHERE event_id = 'EVT-1'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.EVENT_HASH_MISMATCH


def test_previous_hash_tampering_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 2)
        drop_event_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE events SET previous_hash = 'sha256:wrong' WHERE event_id = 'EVT-2'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.PREVIOUS_HASH_MISMATCH
        assert report.failure.event_id == "EVT-2"


def test_stream_version_gap_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 2)
        drop_event_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE events SET stream_version = 3 WHERE event_id = 'EVT-2'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.STREAM_VERSION_GAP


def test_incomplete_batch_tampering_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 1)
        drop_event_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE events SET batch_size = 2 WHERE event_id = 'EVT-1'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.BATCH_INCOMPLETE


def test_missing_payload_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 1)
        store.raw_connection_for_tests().execute(
            "DELETE FROM event_payloads WHERE payload_ref = 'PAYLOAD-1'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.PAYLOAD_MISSING


def test_unregistered_event_type_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 1)
        drop_event_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE events SET event_type = 'UNKNOWN' WHERE event_id = 'EVT-1'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.SCHEMA_INVALID


def test_stream_meta_tail_tampering_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 2)
        store.raw_connection_for_tests().execute(
            "UPDATE stream_meta SET last_event_hash = 'sha256:wrong' WHERE stream_id = 'test:stream'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.STREAM_META_HASH_MISMATCH


def test_stream_meta_count_tampering_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 2)
        store.raw_connection_for_tests().execute(
            "UPDATE stream_meta SET event_count = 99 WHERE stream_id = 'test:stream'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.STREAM_META_COUNT_MISMATCH


def test_seal_event_recomputes_digest_and_hash() -> None:
    payload = {"n": 1}
    sealed = seal_event(raw_event(1), payload, previous_hash=GENESIS_HASH)
    assert sealed.payload_digest.startswith("sha256:")
    assert sealed.event_hash.startswith("sha256:")
    assert sealed.payload_digest != "sha256:untrusted"
    assert sealed.event_hash != "sha256:untrusted"


def test_batch_order_tampering_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        payload1 = {"n": 1}
        first = raw_event(1, batch_id="BATCH-X", batch_index=0, batch_size=2)
        payload2 = {"n": 2}
        second = replace(
            raw_event(2, batch_id="BATCH-X", batch_index=1, batch_size=2),
            causation_id=first.causation_id,
        )
        SQLiteAtomicBatchAppender(store, registry()).append(
            (BatchEntry(first, payload1), BatchEntry(second, payload2))
        )
        drop_event_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE events SET batch_index = 0 WHERE event_id = 'EVT-2'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.BATCH_ORDER_MISMATCH


def test_stream_meta_version_tampering_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_valid_stream(store, 2)
        store.raw_connection_for_tests().execute(
            "UPDATE stream_meta SET current_version = 99 WHERE stream_id = 'test:stream'"
        )
        report = R0IntegrityVerifier(store, registry()).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.STREAM_META_VERSION_MISMATCH


def _downgrade_database_to_v2(database: Path, *, tamper: bool) -> None:
    connection = sqlite3.connect(database, isolation_level=None)
    connection.execute("DROP TABLE stream_meta")
    connection.execute("UPDATE p0_schema_meta SET schema_version = 2 WHERE singleton = 1")
    if tamper:
        connection.execute("DROP TRIGGER events_are_immutable_on_update")
        connection.execute(
            "UPDATE events SET event_hash = 'sha256:corrupted' WHERE event_id = 'EVT-1'"
        )
    connection.close()


def test_populated_v2_migration_verifies_history_before_backfill(tmp_path: Path) -> None:
    database = tmp_path / "valid-v2.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        append_valid_stream(store, 2)
    _downgrade_database_to_v2(database, tamper=False)

    with SQLiteEventPayloadStore.connect(database) as migrated:
        migrated.initialize_schema(migration_registry=registry())
        meta = migrated.load_stream_meta("test:stream")
        assert meta.current_version == 2
        assert meta.event_count == 2
        assert R0IntegrityVerifier(migrated, registry()).verify_stream("test:stream").ok


def test_corrupted_v2_migration_fails_closed_without_stream_meta(tmp_path: Path) -> None:
    database = tmp_path / "corrupted-v2.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        append_valid_stream(store, 1)
    _downgrade_database_to_v2(database, tamper=True)

    with SQLiteEventPayloadStore.connect(database) as candidate:
        with pytest.raises(StorageError, match="event hash mismatch"):
            candidate.initialize_schema(migration_registry=registry())
        version = candidate.raw_connection_for_tests().execute(
            "SELECT schema_version FROM p0_schema_meta WHERE singleton = 1"
        ).fetchone()[0]
        assert version == 2
        with pytest.raises(sqlite3.OperationalError):
            candidate.raw_connection_for_tests().execute(
                "SELECT stream_id FROM stream_meta LIMIT 0"
            )


def test_populated_v2_migration_requires_registry(tmp_path: Path) -> None:
    database = tmp_path / "registry-required-v2.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        append_valid_stream(store, 1)
    _downgrade_database_to_v2(database, tamper=False)

    with SQLiteEventPayloadStore.connect(database) as candidate:
        with pytest.raises(StorageError, match="migration_registry"):
            candidate.initialize_schema()
        version = candidate.raw_connection_for_tests().execute(
            "SELECT schema_version FROM p0_schema_meta WHERE singleton = 1"
        ).fetchone()[0]
        assert version == 2
