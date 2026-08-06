"""P0-011 adversarial integrity gate for R0 and stored replay receipts."""

from __future__ import annotations

from dataclasses import replace
import json

import pytest

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    CommandEnvelope,
    EventEnvelope,
    PendingEvent,
    ProducerRef,
    canonical_json_bytes,
)
from mentaury.storage import (
    REDACTION_EVENT_TYPE,
    REDACTION_PAYLOAD_SCHEMA,
    BatchEntry,
    IdempotencyReceiptIntegrityError,
    IntegrityCode,
    IdempotentBatchRequest,
    R0IntegrityVerifier,
    RedactionRequest,
    SQLiteEventPayloadStore,
    SQLiteIdempotentBatchAppender,
    SQLiteRedactionExecutor,
    VerificationBudget,
    compute_event_hash,
)
from mentaury.validation import (
    EventSchemaDefinition,
    IntegerSpec,
    ObjectSpec,
    SchemaRegistry,
    StringSpec,
)


def _registry() -> SchemaRegistry:
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


def _budget() -> VerificationBudget:
    return VerificationBudget(
        max_events=100,
        max_payload_bytes=10_000,
        max_total_payload_bytes=100_000,
    )


def _verifier(store: SQLiteEventPayloadStore) -> R0IntegrityVerifier:
    return R0IntegrityVerifier(store, _registry(), _budget())


def _raw_event(
    *,
    event_id: str,
    version: int,
    stream_id: str = "test:stream",
    event_type: str = "TEST_EVENT",
    payload_schema: str = "test-event/v1",
    payload_ref: str | None = None,
    batch_id: str | None = None,
    batch_index: int = 0,
    batch_size: int = 1,
    authority: AuthorityRef | None = None,
) -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id,
        event_type=event_type,
        envelope_schema_version=1,
        payload_schema=payload_schema,
        stream_id=stream_id,
        stream_version=version,
        batch_id=batch_id or f"BATCH-{event_id}",
        batch_index=batch_index,
        batch_size=batch_size,
        occurred_at="2026-08-06T00:00:00Z",
        recorded_at="2026-08-06T00:00:00Z",
        producer=ProducerRef("p0-011-adversary", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=authority or AuthorityRef("CAP-1", 1),
        causation_id=f"CMD-{event_id}",
        correlation_id="CORR-P0-011",
        affects_domain_state=True,
        payload_digest="sha256:untrusted",
        payload_ref=payload_ref or f"PAYLOAD-{event_id}",
        previous_hash="sha256:untrusted",
        event_hash="sha256:untrusted",
    )


def _append_test_event(
    store: SQLiteEventPayloadStore,
    *,
    event_id: str,
    version: int,
    stream_id: str = "test:stream",
    payload_ref: str | None = None,
) -> EventEnvelope:
    return store.append_one(
        _raw_event(
            event_id=event_id,
            version=version,
            stream_id=stream_id,
            payload_ref=payload_ref,
        ),
        {"n": version},
        registry=_registry(),
    )


def _append_stream(
    store: SQLiteEventPayloadStore,
    count: int,
) -> tuple[EventEnvelope, ...]:
    return tuple(
        _append_test_event(store, event_id=f"EVT-{version}", version=version)
        for version in range(1, count + 1)
    )


def _assert_integrity_failure(
    store: SQLiteEventPayloadStore,
    expected: IntegrityCode,
    *,
    stream_id: str = "test:stream",
) -> None:
    report = _verifier(store).verify_stream(stream_id)
    assert not report.ok
    assert report.failure is not None
    assert report.failure.code is expected


def _redaction_request() -> RedactionRequest:
    return RedactionRequest(
        idempotency_key="REDACT-P0-011",
        command_id="CMD-REDACT-P0-011",
        target_event_id="EVT-1",
        target_stream="test:stream",
        expected_stream_version=1,
        reason="adversarial fixture",
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-1", 1),
        correlation_id="CORR-REDACT-P0-011",
        audit_event_id="AUDIT-1",
        producer=ProducerRef("p0-011-adversary", "0.1.0"),
        occurred_at="2026-08-06T01:00:00Z",
        recorded_at="2026-08-06T01:00:00Z",
    )


def _apply_redaction(store: SQLiteEventPayloadStore) -> None:
    SQLiteRedactionExecutor(store, _registry()).redact(_redaction_request())


def _drop_event_update_guard(store: SQLiteEventPayloadStore) -> None:
    store.raw_connection_for_tests().execute(
        "DROP TRIGGER events_are_immutable_on_update"
    )


def _drop_event_delete_guard(store: SQLiteEventPayloadStore) -> None:
    store.raw_connection_for_tests().execute(
        "DROP TRIGGER events_are_immutable_on_delete"
    )


def _drop_payload_update_guard(store: SQLiteEventPayloadStore) -> None:
    store.raw_connection_for_tests().execute(
        "DROP TRIGGER payload_material_cannot_be_rewritten"
    )


def test_actual_middle_event_deletion_is_detected_as_version_gap() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 3)
        _drop_event_delete_guard(store)
        store.raw_connection_for_tests().execute(
            "DELETE FROM events WHERE event_id = 'EVT-2'"
        )

        _assert_integrity_failure(store, IntegrityCode.STREAM_VERSION_GAP)


def test_actual_tail_event_deletion_is_detected_by_stream_meta() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 2)
        _drop_event_delete_guard(store)
        store.raw_connection_for_tests().execute(
            "DELETE FROM events WHERE event_id = 'EVT-2'"
        )

        _assert_integrity_failure(
            store,
            IntegrityCode.STREAM_META_VERSION_MISMATCH,
        )


def test_invalid_utf8_payload_fails_before_schema_processing() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 1)
        _drop_payload_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE event_payloads SET payload_bytes = ? "
            "WHERE payload_ref = 'PAYLOAD-EVT-1'",
            (b"\xff",),
        )

        _assert_integrity_failure(store, IntegrityCode.PAYLOAD_DECODE_ERROR)


def test_top_level_array_payload_is_rejected_as_non_object() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 1)
        _drop_payload_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE event_payloads SET payload_bytes = ? "
            "WHERE payload_ref = 'PAYLOAD-EVT-1'",
            (b"[]",),
        )

        _assert_integrity_failure(store, IntegrityCode.SCHEMA_INVALID)


def test_duplicate_json_keys_are_rejected_as_noncanonical() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 1)
        _drop_payload_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE event_payloads SET payload_bytes = ? "
            "WHERE payload_ref = 'PAYLOAD-EVT-1'",
            (b'{"n":1,"n":1}',),
        )

        _assert_integrity_failure(store, IntegrityCode.PAYLOAD_NOT_CANONICAL)


def test_self_consistent_event_hash_cannot_hide_wrong_previous_hash() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 2)
        event = store.load_event("EVT-2")
        assert event is not None
        tampered = replace(event, previous_hash="sha256:attacker-controlled")
        forged_hash = compute_event_hash(tampered)

        _drop_event_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE events SET previous_hash = ?, event_hash = ? "
            "WHERE event_id = 'EVT-2'",
            (tampered.previous_hash, forged_hash),
        )

        _assert_integrity_failure(store, IntegrityCode.PREVIOUS_HASH_MISMATCH)


def test_redacted_payload_reappearance_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 1)
        _apply_redaction(store)
        store.raw_connection_for_tests().execute(
            "INSERT INTO event_payloads(payload_ref, payload_bytes, created_at) "
            "VALUES (?, ?, ?)",
            (
                "PAYLOAD-EVT-1",
                canonical_json_bytes({"n": 1}),
                "2026-08-06T00:00:00Z",
            ),
        )

        _assert_integrity_failure(
            store,
            IntegrityCode.REDACTED_PAYLOAD_STILL_PRESENT,
        )


def test_invalid_utf8_redaction_audit_payload_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 1)
        _apply_redaction(store)
        audit = store.load_event("AUDIT-1")
        assert audit is not None

        _drop_payload_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE event_payloads SET payload_bytes = ? WHERE payload_ref = ?",
            (b"\xff", audit.payload_ref),
        )

        _assert_integrity_failure(
            store,
            IntegrityCode.REDACTION_AUDIT_PAYLOAD_DECODE_ERROR,
        )


def test_noncanonical_redaction_audit_payload_is_detected() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 1)
        _apply_redaction(store)
        audit = store.load_event("AUDIT-1")
        assert audit is not None
        stored = store.load_payload(audit.payload_ref)
        assert stored is not None
        decoded = json.loads(stored.payload_bytes.decode("utf-8"))
        noncanonical = json.dumps(decoded, ensure_ascii=False, indent=2).encode("utf-8")

        _drop_payload_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE event_payloads SET payload_bytes = ? WHERE payload_ref = ?",
            (noncanonical, audit.payload_ref),
        )

        _assert_integrity_failure(
            store,
            IntegrityCode.REDACTION_AUDIT_PAYLOAD_NOT_CANONICAL,
        )


def test_redaction_audit_digest_tampering_is_detected_from_linkage() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_stream(store, 1)
        _apply_redaction(store)

        _drop_event_update_guard(store)
        store.raw_connection_for_tests().execute(
            "UPDATE events SET payload_digest = 'sha256:tampered' "
            "WHERE event_id = 'AUDIT-1'"
        )

        _assert_integrity_failure(
            store,
            IntegrityCode.REDACTION_AUDIT_PAYLOAD_DIGEST_MISMATCH,
        )


def test_redaction_audit_must_follow_target_event() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        audit_payload = {
            "target_event_id": "EVT-TARGET",
            "target_stream_id": "test:stream",
            "target_payload_ref": "PAYLOAD-TARGET",
            "reason": "adversarial fixture",
            "authority": {
                "capability_lease_id": "CAP-1",
                "capability_revision": 1,
            },
        }
        store.append_one(
            _raw_event(
                event_id="AUDIT-EARLY",
                version=1,
                event_type=REDACTION_EVENT_TYPE,
                payload_schema=REDACTION_PAYLOAD_SCHEMA,
                payload_ref="PAYLOAD-AUDIT-EARLY",
            ),
            audit_payload,
            registry=_registry(),
        )
        _append_test_event(
            store,
            event_id="EVT-TARGET",
            version=2,
            payload_ref="PAYLOAD-TARGET",
        )
        connection = store.raw_connection_for_tests()
        connection.execute(
            "DELETE FROM event_payloads WHERE payload_ref = 'PAYLOAD-TARGET'"
        )
        connection.execute(
            """
            INSERT INTO redactions(
                target_event_id, idempotency_key, fingerprint,
                target_stream_id, target_payload_ref, audit_event_id,
                reason, capability_lease_id, capability_revision, redacted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "EVT-TARGET",
                "REDACT-EARLY",
                "sha256:fixture",
                "test:stream",
                "PAYLOAD-TARGET",
                "AUDIT-EARLY",
                "adversarial fixture",
                "CAP-1",
                1,
                "2026-08-06T01:00:00Z",
            ),
        )

        _assert_integrity_failure(
            store,
            IntegrityCode.REDACTION_AUDIT_ORDER_MISMATCH,
        )


def _idempotent_request() -> IdempotentBatchRequest:
    command = CommandEnvelope(
        command_id="CMD-IDEMP-P0-011",
        command_type="TEST_COMMAND",
        command_schema="test-command/v1",
        target_stream="idempotency:stream",
        expected_stream_version=0,
        issued_at="2026-08-06T00:00:00Z",
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-1", 1),
        correlation_id="CORR-IDEMP-P0-011",
        idempotency_key="IDEMP-P0-011",
        payload={"intent": "append-two"},
    )
    pending = tuple(
        PendingEvent(
            event_type="TEST_EVENT",
            payload_schema="test-event/v1",
            affects_domain_state=True,
            payload={"n": index},
        )
        for index in (1, 2)
    )
    entries = tuple(
        BatchEntry(
            _raw_event(
                event_id=f"IDEMP-EVT-{index}",
                version=index,
                stream_id=command.target_stream,
                payload_ref=f"IDEMP-PAYLOAD-{index}",
                batch_id="IDEMP-BATCH",
                batch_index=index - 1,
                batch_size=2,
                authority=command.authority,
            ),
            {"n": index},
        )
        for index in (1, 2)
    )
    aligned_entries = tuple(
        BatchEntry(
            replace(
                entry.event,
                initiator=command.issuer,
                causation_id=command.command_id,
                correlation_id=command.correlation_id,
            ),
            entry.payload,
        )
        for entry in entries
    )
    return IdempotentBatchRequest(command, pending, aligned_entries)


def _corrupt_idempotency_record(
    store: SQLiteEventPayloadStore,
    assignment: str,
    parameters: tuple[object, ...] = (),
) -> None:
    connection = store.raw_connection_for_tests()
    connection.execute("DROP TRIGGER idempotency_records_are_immutable_on_update")
    connection.execute(
        f"UPDATE idempotency_records SET {assignment} "
        "WHERE idempotency_key = 'IDEMP-P0-011'",
        parameters,
    )


def test_malformed_stored_idempotency_json_fails_closed() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        _corrupt_idempotency_record(
            store,
            "event_ids_json = ?",
            (b"{",),
        )

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="event_ids_json",
        ):
            appender.append(request)
        assert len(store.list_stream("idempotency:stream")) == 2


def test_stored_idempotency_receipt_cannot_reference_missing_event() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        _corrupt_idempotency_record(
            store,
            "event_ids_json = ?",
            (canonical_json_bytes(["IDEMP-EVT-1", "IDEMP-EVT-GHOST"]),),
        )

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="does not exist",
        ):
            appender.append(request)


def test_stored_idempotency_receipt_event_order_is_verified() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        _corrupt_idempotency_record(
            store,
            "event_ids_json = ?",
            (canonical_json_bytes(["IDEMP-EVT-2", "IDEMP-EVT-1"]),),
        )

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="batch_index",
        ):
            appender.append(request)


def test_stored_idempotency_receipt_version_span_is_verified() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        _corrupt_idempotency_record(store, "last_stream_version = 3")

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="version span",
        ):
            appender.append(request)



def test_stored_receipt_cannot_redirect_to_another_stream() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        _corrupt_idempotency_record(store, "stream_id = 'other:stream'")

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="target_stream",
        ):
            appender.append(request)


def test_stored_receipt_must_start_after_expected_version() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        _corrupt_idempotency_record(
            store,
            "first_stream_version = 2, last_stream_version = 3",
        )

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="command expectation",
        ):
            appender.append(request)


def test_stored_receipt_verifies_full_batch_shape() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER events_are_immutable_on_update")
        connection.execute(
            "UPDATE events SET batch_size = 3 WHERE event_id = 'IDEMP-EVT-1'"
        )

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="batch_size",
        ):
            appender.append(request)


def test_stored_receipt_verifies_fingerprinted_event_semantics() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        appender = SQLiteIdempotentBatchAppender(store, _registry())
        request = _idempotent_request()
        appender.append(request)
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER events_are_immutable_on_update")
        connection.execute(
            "UPDATE events SET payload_digest = 'sha256:forged' "
            "WHERE event_id = 'IDEMP-EVT-1'"
        )

        with pytest.raises(
            IdempotencyReceiptIntegrityError,
            match="payload_digest",
        ):
            appender.append(request)
