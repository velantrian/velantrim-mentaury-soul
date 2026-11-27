from __future__ import annotations

import sqlite3
import threading
import time
import types
from dataclasses import replace
from pathlib import Path
from queue import Queue

import pytest

from mentaury.contracts import ActorRef, AuthorityRef, EventEnvelope, ProducerRef
from mentaury.storage import concurrency as concurrency_module
from mentaury.storage import (
    REDACTION_EVENT_TYPE,
    REDACTION_PAYLOAD_SCHEMA,
    CrossStreamRedactionError,
    IntegrityCode,
    R0IntegrityVerifier,
    RedactionConflictError,
    RedactionEvidenceInUseError,
    RedactionRequest,
    RedactionStatus,
    SQLiteRedactionExecutor,
    SQLiteEventPayloadStore,
    TargetAlreadyRedactedError,
    TargetEventNotFoundError,
    TargetPayloadMissingError,
    GENESIS_HASH,
    VerificationBudget,
    VersionConflictError,
    redaction_fingerprint,
    seal_event_bytes,
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
        stream_a = store.list_stream("stream:A")
        assert [event.event_id for event in stream_a] == ["EVT-1"]
        assert store.list_stream("stream:B") == ()


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
        with pytest.raises(TargetPayloadMissingError, match="already absent"):
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


# ---------------------------------------------------------------------------
# Stage 02: redaction must not delete committed redaction-audit evidence.
#
# Scenario map (derived from the Stage 02 brief; the original Manus R01-R10
# text was not available in-repo):
#   R01 direct attempt on an audit event       R06 ALREADY_REDACTED preserved
#   R02 alias via shared payload_ref/stream    R07 no active own transaction, store reusable
#   R03 not a bare event_type rule             R08 error leaks no reason/payload
#   R04 every table unchanged after refusal    R09 two-connection committed-link race
#   R05 refusal repeatable, no new receipt     R10 R0 diagnostics on corrupt history intact
# ---------------------------------------------------------------------------

_TABLES = (
    "events",
    "event_payloads",
    "stream_meta",
    "idempotency_records",
    "redactions",
)
_REASON_SECRET = "SECRET-REASON-do-not-leak"


def _state(store: SQLiteEventPayloadStore) -> dict[str, list[tuple[object, ...]]]:
    connection = store.raw_connection_for_tests()
    return {
        table: [
            tuple(row)
            for row in connection.execute(f"SELECT * FROM {table} ORDER BY 1, 2").fetchall()
        ]
        for table in _TABLES
    }


def _redacted_store() -> SQLiteEventPayloadStore:
    """In-memory store with EVT-1 redacted; audit event AUDIT-1 is evidence."""

    store = SQLiteEventPayloadStore.in_memory()
    store.initialize_schema()
    append_target(store)
    executor(store).redact(redaction_request())
    return store


def _attack_audit_request(**overrides: object) -> RedactionRequest:
    values: dict[str, object] = dict(
        idempotency_key="REDACT-ATTACK",
        command_id="CMD-ATTACK",
        target_event_id="AUDIT-1",
        expected_stream_version=2,
        audit_event_id="AUDIT-ATTACK",
        correlation_id="CORR-ATTACK",
        reason=_REASON_SECRET,
    )
    values.update(overrides)
    return redaction_request(**values)  # type: ignore[arg-type]


def _insert_alias_event(store: SQLiteEventPayloadStore) -> None:
    """Synthetic fixture: an event in another stream sharing the audit payload_ref.

    The public API cannot produce this (payload_ref is the payload primary key),
    so it is inserted raw to prove the guard is by payload reference, globally.
    """

    audit = store.load_event("AUDIT-1")
    assert audit is not None
    alias = seal_event_bytes(
        replace(
            target_event(event_id="EVT-ALIAS", stream_id="other:stream", version=1),
            payload_ref=audit.payload_ref,
        ),
        b'{"n":1}',
        previous_hash=GENESIS_HASH,
    )
    store._insert_event(alias)


def test_r01_direct_redaction_of_audit_event_is_refused_and_changes_nothing() -> None:
    with _redacted_store() as store:
        before = _state(store)
        with pytest.raises(RedactionEvidenceInUseError) as captured:
            executor(store).redact(_attack_audit_request())
        assert captured.value.target_event_id == "AUDIT-1"
        assert store.load_payload("PAYLOAD-REDACTION-AUDIT-1") is not None
        assert _state(store) == before  # R04: all affected tables identical


def test_r02_alias_in_other_stream_sharing_audit_payload_ref_is_refused() -> None:
    with _redacted_store() as store:
        _insert_alias_event(store)
        before = _state(store)
        request = redaction_request(
            idempotency_key="REDACT-ALIAS",
            command_id="CMD-ALIAS",
            target_event_id="EVT-ALIAS",
            target_stream="other:stream",
            expected_stream_version=0,
            audit_event_id="AUDIT-ALIAS",
        )
        with pytest.raises(RedactionEvidenceInUseError):
            executor(store).redact(request)
        assert store.load_payload("PAYLOAD-REDACTION-AUDIT-1") is not None
        assert _state(store) == before


def test_r03_protection_is_linkage_based_not_a_bare_event_type_rule() -> None:
    """A REDACTION_RECORDED event no ``redactions`` row points at is redactable."""

    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        unlinked = replace(
            target_event(event_id="EVT-LOOKALIKE"),
            event_type=REDACTION_EVENT_TYPE,
            payload_schema=REDACTION_PAYLOAD_SCHEMA,
            payload_ref="PAYLOAD-LOOKALIKE",
        )
        store.append_one(
            unlinked,
            {
                "target_event_id": "EVT-X",
                "target_stream_id": "test:stream",
                "target_payload_ref": "PAYLOAD-X",
                "reason": "unrelated",
                "authority": {"capability_lease_id": "CAP-1", "capability_revision": 1},
            },
            registry=registry(),
        )
        result = executor(store).redact(
            redaction_request(target_event_id="EVT-LOOKALIKE")
        )
        assert result.status is RedactionStatus.REDACTED
        assert store.load_payload("PAYLOAD-LOOKALIKE") is None


def test_r05_refusal_is_repeatable_and_writes_no_receipt() -> None:
    with _redacted_store() as store:
        before = _state(store)
        for key in ("REDACT-ATTACK", "REDACT-ATTACK", "REDACT-ATTACK-2"):
            with pytest.raises(RedactionEvidenceInUseError):
                executor(store).redact(_attack_audit_request(idempotency_key=key))
        assert _state(store) == before
        count = store.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM redactions WHERE idempotency_key LIKE 'REDACT-ATTACK%'"
        ).fetchone()[0]
        assert count == 0


def test_r06_previously_successful_request_still_replays_already_redacted() -> None:
    with _redacted_store() as store:
        with pytest.raises(RedactionEvidenceInUseError):
            executor(store).redact(_attack_audit_request())
        replay = executor(store).redact(redaction_request())
        assert replay.status is RedactionStatus.ALREADY_REDACTED
        assert replay.audit_event_id == "AUDIT-1"


def test_r07_refusal_leaves_no_open_transaction_and_store_stays_usable() -> None:
    with _redacted_store() as store:
        connection = store.raw_connection_for_tests()
        with pytest.raises(RedactionEvidenceInUseError):
            executor(store).redact(_attack_audit_request())
        assert not connection.in_transaction
        append_target(store, event_id="EVT-2", version=3, n=2)
        result = executor(store).redact(
            redaction_request(
                idempotency_key="REDACT-2",
                target_event_id="EVT-2",
                expected_stream_version=3,
                audit_event_id="AUDIT-2",
            )
        )
        assert result.status is RedactionStatus.REDACTED
        assert not connection.in_transaction


def test_r07b_refusal_does_not_disturb_a_foreign_transaction() -> None:
    from mentaury.storage import TransactionOwnershipError

    with _redacted_store() as store:
        connection = store.raw_connection_for_tests()
        connection.execute("CREATE TABLE sentinel(x)")
        connection.execute("BEGIN")
        connection.execute("INSERT INTO sentinel VALUES (1)")
        with pytest.raises(TransactionOwnershipError):
            executor(store).redact(_attack_audit_request())
        assert connection.in_transaction
        assert connection.execute("SELECT COUNT(*) FROM sentinel").fetchone()[0] == 1
        connection.execute("ROLLBACK")


def test_r08_error_message_carries_no_reason_or_payload() -> None:
    with _redacted_store() as store:
        with pytest.raises(RedactionEvidenceInUseError) as captured:
            executor(store).redact(_attack_audit_request())
        text = str(captured.value) + repr(captured.value.args)
        assert _REASON_SECRET not in text
        assert "user-requested erasure" not in text  # the stored audit reason
        assert "target_payload_ref" not in text  # no payload field material


def test_r09_committed_evidence_from_another_connection_is_seen_after_lock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A holds the write lock mid-COMMIT; B (separate connection) waits, then
    must observe A's now-committed audit link and refuse to delete it."""

    from mentaury.storage import BusyRetryPolicy

    database = tmp_path / "evidence-race.sqlite3"
    with SQLiteEventPayloadStore.connect(database) as setup:
        setup.initialize_schema()
        append_target(setup)

    policy = BusyRetryPolicy(max_attempts=2000, backoff_seconds=0.002)
    a_holding_lock = threading.Event()
    release_a = threading.Event()
    b_retrying = threading.Event()
    outcomes: dict[str, object] = {}

    def writer_a() -> None:
        try:
            with SQLiteEventPayloadStore.connect(database, busy_policy=policy) as store:
                def authorizer(action: int, arg1: object, *_: object) -> int:
                    if action == sqlite3.SQLITE_TRANSACTION and arg1 == "COMMIT":
                        a_holding_lock.set()
                        assert release_a.wait(10)
                    return sqlite3.SQLITE_OK

                store.raw_connection_for_tests().set_authorizer(authorizer)
                outcomes["a"] = SQLiteRedactionExecutor(
                    store, registry(), policy
                ).redact(redaction_request(idempotency_key="REDACT-A", audit_event_id="AUDIT-A"))
        except BaseException as exc:
            outcomes["a"] = exc

    def writer_b() -> None:
        try:
            with SQLiteEventPayloadStore.connect(database, busy_policy=policy) as store:
                outcomes["b"] = SQLiteRedactionExecutor(
                    store, registry(), policy
                ).redact(
                    _attack_audit_request(
                        idempotency_key="REDACT-B",
                        target_event_id="AUDIT-A",
                        audit_event_id="AUDIT-B",
                    )
                )
        except BaseException as exc:
            outcomes["b"] = exc

    # B's backoff sleeps only happen when BEGIN IMMEDIATE failed on A's held
    # lock, so counting them proves B really contended while A held the lock.
    real_sleep = time.sleep
    sleeps = 0

    def counting_sleep(seconds: float) -> None:
        nonlocal sleeps
        sleeps += 1
        if sleeps >= 3:
            b_retrying.set()
        real_sleep(seconds)

    monkeypatch.setattr(
        concurrency_module, "time", types.SimpleNamespace(sleep=counting_sleep)
    )

    thread_a = threading.Thread(target=writer_a)
    thread_b = threading.Thread(target=writer_b)
    thread_a.start()
    assert a_holding_lock.wait(10)
    thread_b.start()
    assert b_retrying.wait(10), f"B never contended for the write lock: {outcomes!r}"
    release_a.set()
    thread_a.join(timeout=10)
    thread_b.join(timeout=10)
    assert not thread_a.is_alive() and not thread_b.is_alive()

    assert getattr(outcomes["a"], "status", None) is RedactionStatus.REDACTED
    assert isinstance(outcomes["b"], RedactionEvidenceInUseError)
    with SQLiteEventPayloadStore.connect(database) as check:
        assert check.load_payload("PAYLOAD-REDACTION-AUDIT-A") is not None
        assert len(check.list_stream("test:stream")) == 2
        assert check.load_event("AUDIT-B") is None
        assert check.raw_connection_for_tests().execute(
            "SELECT COUNT(*) FROM redactions"
        ).fetchone()[0] == 1
        assert not check.raw_connection_for_tests().in_transaction


def test_r10_r0_diagnostics_on_corrupt_history_are_unchanged() -> None:
    """Forged row pointing at a missing audit event: the guard stays out of the
    way and R0 still reports its specific pre-existing failure code."""

    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        append_target(store)
        append_target(store, event_id="EVT-2", version=2, n=2)
        connection = store.raw_connection_for_tests()
        connection.execute("DELETE FROM event_payloads WHERE payload_ref = 'PAYLOAD-EVT-1'")
        connection.execute(
            """
            INSERT INTO redactions(
                target_event_id, idempotency_key, fingerprint, target_stream_id,
                target_payload_ref, audit_event_id, reason, capability_lease_id,
                capability_revision, redacted_at
            ) VALUES ('EVT-1', 'FORGED', 'sha256:forged', 'test:stream',
                      'PAYLOAD-EVT-1', 'AUDIT-GHOST', 'forged', 'CAP-1', 1,
                      '2026-08-05T01:00:00Z')
            """
        )
        report = verifier(store).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.REDACTION_AUDIT_EVENT_MISSING

        # Unrelated, legitimately redactable target is not blocked by the
        # dangling forged row (INNER JOIN finds no audit event).
        result = executor(store).redact(
            redaction_request(
                idempotency_key="REDACT-2",
                target_event_id="EVT-2",
                expected_stream_version=2,
                audit_event_id="AUDIT-2",
            )
        )
        assert result.status is RedactionStatus.REDACTED
        report = verifier(store).verify_stream("test:stream")
        assert report.failure is not None
        assert report.failure.code is IntegrityCode.REDACTION_AUDIT_EVENT_MISSING
