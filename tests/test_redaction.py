from __future__ import annotations

import sqlite3
import threading
from pathlib import Path
from queue import Queue

import pytest

from mentaury.contracts import ActorRef, AuthorityRef, EventEnvelope, ProducerRef
from mentaury.storage import (
    REDACTION_EVENT_TYPE,
    REDACTION_PAYLOAD_SCHEMA,
    CrossStreamRedactionError,
    IntegrityCode,
    R0IntegrityVerifier,
    RedactionConflictError,
    RedactionRequest,
    RedactionStatus,
    SQLiteRedactionExecutor,
    SQLiteEventPayloadStore,
    TargetAlreadyRedactedError,
    TargetEventNotFoundError,
    VerificationBudget,
    VersionConflictError,
    redaction_fingerprint,
)
from mentaury.validation import (
    EventSchemaDefinition,
    IntegerSpec,
    ObjectSpec,
    SchemaRegistry,
    StringSpec,
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
            ),
            EventSchemaDefinition(
                event_type=REDACTION_EVENT_TYPE,
                payload_schema=REDACTION_PAYLOAD_SCHEMA,
                affects_domain_state=True,
                payload=ObjectSpec(
                    {
                        "target_event_id": StringSpec(min_length=1),
                        "target_stream_id": StringSpec(min_length=1),
                        "target_payload_ref": StringSpec(min_length=1),
                        "reason": StringSpec(min_length=1),
                        "authority": ObjectSpec(
                            {
                                "capability_lease_id": StringSpec(min_length=1),
                                "capability_revision": IntegerSpec(minimum=0),
                            },
                            required=frozenset(
                                {"capability_lease_id", "capability_revision"}
                            ),
                        ),
                    },
                    required=frozenset(
                        {
                            "target_event_id",
                            "target_stream_id",
                            "target_payload_ref",
                            "reason",
                            "authority",
                        }
                    ),
                ),
            ),
        ]
    )


def verification_budget() -> VerificationBudget:
    return VerificationBudget(
        max_events=100, max_payload_bytes=10_000, max_total_payload_bytes=100_000
    )


def verifier(store: SQLiteEventPayloadStore) -> R0IntegrityVerifier:
    return R0IntegrityVerifier(store, registry(), verification_budget())


def target_event(
    *,
    event_id: str = "EVT-1",
    stream_id: str = "test:stream",
    version: int = 1,
) -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id,
        event_type="TEST_EVENT",
        envelope_schema_version=1,
        payload_schema="test-event/v1",
        stream_id=stream_id,
        stream_version=version,
        batch_id=f"BATCH-{event_id}",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-05T00:00:00Z",
        recorded_at="2026-08-05T00:00:00Z",
        producer=ProducerRef("redaction-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-1", 1),
        causation_id=f"CMD-{event_id}",
        correlation_id="CORR-1",
        affects_domain_state=True,
        payload_digest="sha256:untrusted",
        payload_ref=f"PAYLOAD-{event_id}",
        previous_hash="sha256:untrusted",
        event_hash="sha256:untrusted",
    )


def append_target(
    store: SQLiteEventPayloadStore,
    *,
    event_id: str = "EVT-1",
    stream_id: str = "test:stream",
    version: int = 1,
    n: int = 1,
) -> EventEnvelope:
    return store.append_one(
        target_event(event_id=event_id, stream_id=stream_id, version=version),
        {"n": n},
        registry=registry(),
    )


def redaction_request(
    *,
    idempotency_key: str = "REDACT-1",
    command_id: str = "CMD-REDACT-1",
    target_event_id: str = "EVT-1",
    target_stream: str = "test:stream",
    expected_stream_version: int = 1,
    reason: str = "user-requested erasure",
    correlation_id: str = "CORR-REDACT-1",
    audit_event_id: str = "AUDIT-1",
) -> RedactionRequest:
    return RedactionRequest(
        idempotency_key=idempotency_key,
        command_id=command_id,
        target_event_id=target_event_id,
        target_stream=target_stream,
        expected_stream_version=expected_stream_version,
        reason=reason,
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-1", 1),
        correlation_id=correlation_id,
        audit_event_id=audit_event_id,
        producer=ProducerRef("redaction-test", "0.1.0"),
        occurred_at="2026-08-05T01:00:00Z",
        recorded_at="2026-08-05T01:00:00Z",
    )


def executor(store: SQLiteEventPayloadStore) -> SQLiteRedactionExecutor:
    return SQLiteRedactionExecutor(store, registry())


def test_redaction_removes_payload_and_appends_audit_event_atomically() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        result = executor(store).redact(redaction_request())

        assert result.status is RedactionStatus.REDACTED
        assert result.audit_event_id == "AUDIT-1"
        assert result.audit_stream_version == 2

        assert store.load_payload("PAYLOAD-EVT-1") is None
        stream = store.list_stream("test:stream")
        assert [event.event_id for event in stream] == ["EVT-1", "AUDIT-1"]
        assert stream[1].event_type == REDACTION_EVENT_TYPE
        assert stream[1].previous_hash == stream[0].event_hash
        meta = store.load_stream_meta("test:stream")
        assert meta.current_version == 2
        assert meta.event_count == 2

        row = store.raw_connection_for_tests().execute(
            "SELECT * FROM redactions WHERE target_event_id = 'EVT-1'"
        ).fetchone()
        assert row is not None
        assert row["target_payload_ref"] == "PAYLOAD-EVT-1"
        assert row["audit_event_id"] == "AUDIT-1"

        # The original event row is untouched: its hash is still verifiable.
        assert stream[0].event_hash != "sha256:untrusted"
        assert stream[0].payload_digest != "sha256:untrusted"


def test_cross_stream_redaction_is_rejected_and_payload_untouched() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store, stream_id="stream:A")
        request = redaction_request(target_stream="stream:B")
        with pytest.raises(CrossStreamRedactionError):
            executor(store).redact(request)
        assert store.load_payload("PAYLOAD-EVT-1") is not None
        assert store.list_stream("stream:A") == store.list_stream("stream:A")
        assert len(store.list_stream("stream:A")) == 1


def test_missing_target_event_is_rejected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        request = redaction_request(target_event_id="EVT-GHOST")
        with pytest.raises(TargetEventNotFoundError):
            executor(store).redact(request)
        count = store.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM redactions"
        ).fetchone()[0]
        assert count == 0


def test_stale_expected_version_leaves_payload_untouched() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        stale = redaction_request(expected_stream_version=5)
        with pytest.raises(VersionConflictError):
            executor(store).redact(stale)
        assert store.load_payload("PAYLOAD-EVT-1") is not None
        assert len(store.list_stream("test:stream")) == 1
        count = store.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM redactions"
        ).fetchone()[0]
        assert count == 0


def test_repeated_request_with_same_key_is_idempotent() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        first = executor(store).redact(redaction_request())
        replay = executor(store).redact(redaction_request())

        assert first.status is RedactionStatus.REDACTED
        assert replay.status is RedactionStatus.ALREADY_REDACTED
        assert replay.fingerprint == first.fingerprint
        assert replay.audit_event_id == first.audit_event_id
        assert len(store.list_stream("test:stream")) == 2


def test_conflicting_request_under_same_key_is_rejected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        executor(store).redact(redaction_request())
        conflicting = redaction_request(reason="a different, unrelated reason")
        with pytest.raises(RedactionConflictError):
            executor(store).redact(conflicting)
        assert len(store.list_stream("test:stream")) == 2


def test_duplicate_redaction_under_different_key_is_rejected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        executor(store).redact(redaction_request(idempotency_key="REDACT-1"))
        again = redaction_request(
            idempotency_key="REDACT-2",
            command_id="CMD-REDACT-2",
            audit_event_id="AUDIT-2",
            expected_stream_version=2,
        )
        with pytest.raises(TargetAlreadyRedactedError):
            executor(store).redact(again)
        assert len(store.list_stream("test:stream")) == 2


def test_fingerprint_ignores_volatile_ids_but_not_semantic_fields() -> None:
    first = redaction_request()
    retry = redaction_request(
        command_id="CMD-OTHER",
        audit_event_id="AUDIT-OTHER",
        correlation_id="CORR-OTHER",
    )
    changed_reason = redaction_request(reason="different reason")
    assert redaction_fingerprint(first) == redaction_fingerprint(retry)
    assert redaction_fingerprint(first) != redaction_fingerprint(changed_reason)


def test_redaction_records_are_immutable() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        executor(store).redact(redaction_request())
        connection = store.raw_connection_for_tests()
        with pytest.raises(sqlite3.IntegrityError, match="cannot be updated"):
            connection.execute(
                "UPDATE redactions SET reason = 'changed' WHERE target_event_id = 'EVT-1'"
            )
        with pytest.raises(sqlite3.IntegrityError, match="cannot be deleted"):
            connection.execute("DELETE FROM redactions")


def test_failure_after_payload_delete_rolls_back_before_audit_event() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        store.raw_connection_for_tests().execute(
            """
            CREATE TRIGGER fail_audit_event_insert
            BEFORE INSERT ON events
            WHEN NEW.event_type = 'REDACTION_RECORDED'
            BEGIN
                SELECT RAISE(ABORT, 'forced audit event failure');
            END
            """
        )
        with pytest.raises(sqlite3.IntegrityError, match="forced"):
            executor(store).redact(redaction_request())

        assert store.load_payload("PAYLOAD-EVT-1") is not None
        assert len(store.list_stream("test:stream")) == 1
        assert store.load_stream_meta("test:stream").event_count == 1
        count = store.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM redactions"
        ).fetchone()[0]
        assert count == 0


def test_failure_after_audit_event_rolls_back_before_stream_meta_and_evidence() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        store.raw_connection_for_tests().execute(
            """
            CREATE TRIGGER fail_redaction_evidence_insert
            BEFORE INSERT ON redactions
            BEGIN
                SELECT RAISE(ABORT, 'forced evidence failure');
            END
            """
        )
        with pytest.raises(sqlite3.IntegrityError, match="forced"):
            executor(store).redact(redaction_request())

        # The whole transaction rolled back: payload reappears, no audit event,
        # stream_meta untouched. An audit append failure never leaves a
        # half-applied redaction.
        assert store.load_payload("PAYLOAD-EVT-1") is not None
        assert len(store.list_stream("test:stream")) == 1
        assert store.load_stream_meta("test:stream").event_count == 1


def test_failure_at_stream_meta_update_rolls_back_everything() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        store.raw_connection_for_tests().execute(
            """
            CREATE TRIGGER fail_stream_meta_update
            BEFORE UPDATE ON stream_meta
            BEGIN
                SELECT RAISE(ABORT, 'forced stream_meta failure');
            END
            """
        )
        with pytest.raises(sqlite3.IntegrityError, match="forced"):
            executor(store).redact(redaction_request())

        # The audit event insert succeeded before this trigger fired, but the
        # whole transaction still rolls back: no audit event, no stream_meta
        # change, and the target payload reappears.
        assert store.load_payload("PAYLOAD-EVT-1") is not None
        assert len(store.list_stream("test:stream")) == 1
        assert store.load_stream_meta("test:stream").event_count == 1
        count = store.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM redactions"
        ).fetchone()[0]
        assert count == 0


def test_target_payload_already_absent_is_rejected_defensively() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        store.raw_connection_for_tests().execute(
            "DELETE FROM event_payloads WHERE payload_ref = 'PAYLOAD-EVT-1'"
        )
        with pytest.raises(Exception, match="already absent"):
            executor(store).redact(redaction_request())
        count = store.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM redactions"
        ).fetchone()[0]
        assert count == 0


def test_r0_passes_before_and_after_redaction() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        before = verifier(store).verify_stream("test:stream")
        assert before.ok
        assert before.checked_events == 1

        executor(store).redact(redaction_request())

        after = verifier(store).verify_stream("test:stream")
        assert after.ok
        assert after.checked_events == 2


def test_r0_detects_reappeared_payload_after_redaction() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        executor(store).redact(redaction_request())
        # Simulate tampering: payload material reappears for a supposedly
        # redacted event.
        store.raw_connection_for_tests().execute(
            "INSERT INTO event_payloads(payload_ref, payload_bytes, created_at) "
            "VALUES ('PAYLOAD-EVT-1', ?, ?)",
            (b'{"n":1}', "2026-08-05T00:00:00Z"),
        )
        report = verifier(store).verify_stream("test:stream")
        assert not report.ok
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.REDACTED_PAYLOAD_STILL_PRESENT
        assert report.failure.event_id == "EVT-1"


def test_r0_detects_redaction_payload_ref_mismatch() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        executor(store).redact(redaction_request())
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER redactions_are_immutable_on_update")
        connection.execute(
            "UPDATE redactions SET target_payload_ref = 'PAYLOAD-OTHER' "
            "WHERE target_event_id = 'EVT-1'"
        )
        report = verifier(store).verify_stream("test:stream")
        assert not report.ok
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.REDACTION_PAYLOAD_REF_MISMATCH


def test_redaction_and_r0_survive_explicit_reopen(tmp_path: Path) -> None:
    database = tmp_path / "redaction.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as store:
        store.initialize_schema()
        append_target(store)
        executor(store).redact(redaction_request())

    with SQLiteEventPayloadStore.connect(database) as reopened:
        assert reopened.load_payload("PAYLOAD-EVT-1") is None
        assert len(reopened.list_stream("test:stream")) == 2
        report = verifier(reopened).verify_stream("test:stream")
        assert report.ok
        row = reopened.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM redactions"
        ).fetchone()[0]
        assert row == 1


def _run_redaction(
    database: Path,
    request: RedactionRequest,
    barrier: threading.Barrier,
    outcomes: Queue[object],
) -> None:
    from mentaury.storage import BusyRetryPolicy

    policy = BusyRetryPolicy(max_attempts=50, backoff_seconds=0.002)
    try:
        with SQLiteEventPayloadStore.connect(database, busy_policy=policy) as store:
            barrier.wait()
            result = SQLiteRedactionExecutor(store, registry(), policy).redact(request)
            outcomes.put(result.status)
    except BaseException as exc:  # captured for deterministic test assertion
        outcomes.put(exc)


def test_concurrent_redaction_attempts_produce_one_winner(tmp_path: Path) -> None:
    database = tmp_path / "concurrent-redaction.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as setup:
        setup.initialize_schema()
        append_target(setup)

    first = redaction_request(idempotency_key="REDACT-A", audit_event_id="AUDIT-A")
    second = redaction_request(idempotency_key="REDACT-B", audit_event_id="AUDIT-B")
    barrier = threading.Barrier(2)
    outcomes: Queue[object] = Queue()
    threads = [
        threading.Thread(target=_run_redaction, args=(database, first, barrier, outcomes)),
        threading.Thread(target=_run_redaction, args=(database, second, barrier, outcomes)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)
        assert not thread.is_alive()

    values = [outcomes.get_nowait(), outcomes.get_nowait()]
    assert sum(value is RedactionStatus.REDACTED for value in values) == 1
    assert sum(isinstance(value, TargetAlreadyRedactedError) for value in values) == 1
    with SQLiteEventPayloadStore.connect(database) as check:
        assert len(check.list_stream("test:stream")) == 2
        assert check.load_payload("PAYLOAD-EVT-1") is None
