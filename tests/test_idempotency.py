from __future__ import annotations

import sqlite3
from dataclasses import replace
from pathlib import Path

import pytest

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    CommandEnvelope,
    EventEnvelope,
    PendingEvent,
    ProducerRef,
)
from mentaury.storage import (
    SCHEMA_VERSION,
    BatchEntry,
    IdempotencyConflictError,
    IdempotencyInvariantError,
    IdempotencyStatus,
    IdempotentBatchRequest,
    SQLiteEventPayloadStore,
    SQLiteIdempotentBatchAppender,
    idempotency_fingerprint,
)
from mentaury.validation import EventSchemaDefinition, ObjectSpec, SchemaRegistry


def registry() -> SchemaRegistry:
    payload = ObjectSpec({}, additional_properties=True)
    return SchemaRegistry(
        [
            EventSchemaDefinition(
                event_type="BELIEF_CREATED",
                payload_schema="belief-created/v1",
                affects_domain_state=True,
                payload=payload,
            ),
            EventSchemaDefinition(
                event_type="EVIDENCE_ATTACHED",
                payload_schema="evidence-attached/v1",
                affects_domain_state=True,
                payload=payload,
            ),
        ]
    )


def command(
    *,
    command_id: str = "CMD-1",
    issued_at: str = "2026-08-05T00:00:00Z",
    correlation_id: str = "CORR-1",
    payload_value: str = "alpha",
    idempotency_key: str = "IDEMP-1",
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=command_id,
        command_type="CREATE_BELIEF",
        command_schema="create-belief/v1",
        target_stream="belief:B-204",
        expected_stream_version=0,
        issued_at=issued_at,
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-81", 2),
        correlation_id=correlation_id,
        idempotency_key=idempotency_key,
        payload={"statement": payload_value},
    )


def pending_batch(
    *,
    first_payload: str = "alpha",
    event_types: tuple[str, ...] = ("BELIEF_CREATED", "EVIDENCE_ATTACHED"),
    schemas: tuple[str, ...] = ("belief-created/v1", "evidence-attached/v1"),
) -> tuple[PendingEvent, ...]:
    return tuple(
        PendingEvent(
            event_type=event_type,
            payload_schema=schema,
            affects_domain_state=True,
            payload={"value": first_payload if index == 0 else f"evidence-{index}"},
        )
        for index, (event_type, schema) in enumerate(
            zip(event_types, schemas, strict=True)
        )
    )


def entries_for(
    cmd: CommandEnvelope,
    pending: tuple[PendingEvent, ...],
    *,
    generation: str = "A",
) -> tuple[BatchEntry, ...]:
    return tuple(
        BatchEntry(
            EventEnvelope(
                event_id=f"EVT-{generation}-{index}",
                event_type=item.event_type,
                envelope_schema_version=1,
                payload_schema=item.payload_schema,
                stream_id=cmd.target_stream,
                stream_version=cmd.expected_stream_version + index + 1,
                batch_id=f"BATCH-{generation}",
                batch_index=index,
                batch_size=len(pending),
                occurred_at="2026-08-05T00:00:00Z",
                recorded_at="2026-08-05T00:00:00Z",
                producer=ProducerRef("idempotency-test", "0.1.0"),
                initiator=cmd.issuer,
                authority=cmd.authority,
                causation_id=cmd.command_id,
                correlation_id=cmd.correlation_id,
                affects_domain_state=item.affects_domain_state,
                payload_digest=f"sha256:untrusted-payload-{generation}-{index}",
                payload_ref=f"PAYLOAD-{generation}-{index}",
                previous_hash=f"sha256:untrusted-previous-{generation}-{index}",
                event_hash=f"sha256:untrusted-event-{generation}-{index}",
            ),
            item.payload,
        )
        for index, item in enumerate(pending)
    )


def request(
    cmd: CommandEnvelope | None = None,
    pending: tuple[PendingEvent, ...] | None = None,
    *,
    generation: str = "A",
) -> IdempotentBatchRequest:
    actual_command = cmd or command()
    actual_pending = pending or pending_batch()
    return IdempotentBatchRequest(
        actual_command,
        actual_pending,
        entries_for(actual_command, actual_pending, generation=generation),
    )


def test_first_apply_persists_batch_idempotency_record_and_hash_chain() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        result = SQLiteIdempotentBatchAppender(store, registry()).append(request())
        assert result.status is IdempotencyStatus.APPLIED
        assert result.receipt.event_ids == ("EVT-A-0", "EVT-A-1")
        committed = store.list_stream("belief:B-204")
        assert len(committed) == 2
        assert committed[1].previous_hash == committed[0].event_hash
        assert all("untrusted" not in event.event_hash for event in committed)
        row = store.raw_connection_for_tests().execute(
            "SELECT fingerprint FROM idempotency_records WHERE idempotency_key = 'IDEMP-1'"
        ).fetchone()
        assert row is not None
        assert row["fingerprint"] == result.fingerprint


def test_semantic_retry_ignores_volatile_ids_and_replays_receipt() -> None:
    first = request()
    retry_command = command(
        command_id="CMD-RETRY",
        issued_at="2026-08-05T00:10:00Z",
        correlation_id="CORR-RETRY",
    )
    retry = request(retry_command, pending_batch(), generation="RETRY")
    assert idempotency_fingerprint(
        first.command, first.pending_events
    ) == idempotency_fingerprint(retry.command, retry.pending_events)

    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, registry())
        applied = appender.append(first)
        replayed = appender.append(retry)
        assert replayed.status is IdempotencyStatus.ALREADY_APPLIED
        assert replayed.fingerprint == applied.fingerprint
        assert replayed.receipt == applied.receipt
        assert [event.event_id for event in store.list_stream("belief:B-204")] == [
            "EVT-A-0",
            "EVT-A-1",
        ]
        assert store.load_payload("PAYLOAD-RETRY-0") is None


@pytest.mark.parametrize(
    "changed",
    [
        lambda: request(command(payload_value="beta"), pending_batch(), generation="B"),
        lambda: request(command(), pending_batch(first_payload="beta"), generation="B"),
        lambda: request(
            command(),
            pending_batch(event_types=("BELIEF_REPLACED", "EVIDENCE_ATTACHED")),
            generation="B",
        ),
        lambda: request(
            command(),
            pending_batch(schemas=("belief-created/v2", "evidence-attached/v1")),
            generation="B",
        ),
        lambda: request(
            command(),
            pending_batch(
                event_types=("BELIEF_CREATED",),
                schemas=("belief-created/v1",),
            ),
            generation="B",
        ),
        lambda: request(command(), tuple(reversed(pending_batch())), generation="B"),
    ],
)
def test_same_key_with_changed_semantics_is_conflict_before_new_write(changed) -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, registry())
        applied = appender.append(request())
        with pytest.raises(IdempotencyConflictError) as captured:
            appender.append(changed())
        assert captured.value.stored_fingerprint == applied.fingerprint
        assert len(store.list_stream("belief:B-204")) == 2


def test_request_alignment_rejects_pending_and_entry_mismatch() -> None:
    cmd = command()
    proposed = pending_batch()
    mismatched = list(entries_for(cmd, proposed))
    mismatched[0] = BatchEntry(
        replace(mismatched[0].event, event_type="OTHER"),
        mismatched[0].payload,
    )
    with pytest.raises(IdempotencyInvariantError, match="event_type"):
        IdempotentBatchRequest(cmd, proposed, tuple(mismatched))


def test_nested_entry_payload_is_snapshotted_before_fingerprint_use() -> None:
    cmd = command()
    mutable = {"value": ["alpha"]}
    proposed = (
        PendingEvent(
            event_type="BELIEF_CREATED",
            payload_schema="belief-created/v1",
            affects_domain_state=True,
            payload=mutable,
        ),
    )
    request_value = IdempotentBatchRequest(
        cmd,
        proposed,
        (BatchEntry(entries_for(cmd, proposed)[0].event, mutable),),
    )
    mutable["value"].append("mutated")
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        SQLiteIdempotentBatchAppender(store, registry()).append(request_value)
        stored = store.load_payload("PAYLOAD-A-0")
        assert stored is not None
        assert stored.payload_bytes == b'{"value":["alpha"]}'


def test_idempotency_record_failure_rolls_back_batch_and_stream_meta() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        store.raw_connection_for_tests().execute(
            """
            CREATE TRIGGER fail_idempotency_insert
            BEFORE INSERT ON idempotency_records
            BEGIN
                SELECT RAISE(ABORT, 'forced idempotency failure');
            END
            """
        )
        with pytest.raises(sqlite3.IntegrityError, match="forced"):
            SQLiteIdempotentBatchAppender(store, registry()).append(request())
        assert store.list_stream("belief:B-204") == ()
        assert store.load_payload("PAYLOAD-A-0") is None
        assert store.load_stream_meta("belief:B-204").event_count == 0
        count = store.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM idempotency_records"
        ).fetchone()[0]
        assert count == 0


def test_idempotency_records_are_immutable() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        SQLiteIdempotentBatchAppender(store, registry()).append(request())
        connection = store.raw_connection_for_tests()
        with pytest.raises(sqlite3.IntegrityError, match="cannot be updated"):
            connection.execute("UPDATE idempotency_records SET fingerprint = 'changed'")
        with pytest.raises(sqlite3.IntegrityError, match="cannot be deleted"):
            connection.execute("DELETE FROM idempotency_records")


def test_new_unregistered_event_is_rejected_with_zero_writes() -> None:
    proposed = pending_batch(
        event_types=("UNKNOWN",),
        schemas=("unknown/v1",),
    )
    candidate = request(command(), proposed, generation="BAD")
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        with pytest.raises(Exception):
            SQLiteIdempotentBatchAppender(store, registry()).append(candidate)
        assert store.list_stream("belief:B-204") == ()
        assert store.load_stream_meta("belief:B-204").event_count == 0
        count = store.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM idempotency_records"
        ).fetchone()[0]
        assert count == 0


def test_schema_version_one_migrates_to_current_empty_schema(tmp_path: Path) -> None:
    database = tmp_path / "legacy.sqlite3"
    connection = sqlite3.connect(database, isolation_level=None)
    connection.execute(
        "CREATE TABLE p0_schema_meta ("
        "singleton INTEGER PRIMARY KEY CHECK (singleton = 1), "
        "schema_version INTEGER NOT NULL CHECK (schema_version > 0))"
    )
    connection.execute("INSERT INTO p0_schema_meta VALUES (1, 1)")
    connection.close()

    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        version = store.raw_connection_for_tests().execute(
            "SELECT schema_version FROM p0_schema_meta WHERE singleton = 1"
        ).fetchone()[0]
        assert version == SCHEMA_VERSION == 3
        store.raw_connection_for_tests().execute(
            "SELECT idempotency_key FROM idempotency_records LIMIT 0"
        )
