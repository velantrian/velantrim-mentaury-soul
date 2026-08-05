"""Adversarial R0 proof for redaction row ↔ audit event ↔ payload linkage."""

from __future__ import annotations

import json

import pytest

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    EventEnvelope,
    ProducerRef,
    canonical_json_bytes,
)
from mentaury.storage import (
    REDACTION_EVENT_TYPE,
    REDACTION_PAYLOAD_SCHEMA,
    IntegrityCode,
    R0IntegrityVerifier,
    RedactionRequest,
    SQLiteEventPayloadStore,
    SQLiteRedactionExecutor,
    VerificationBudget,
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


def _verifier(store: SQLiteEventPayloadStore) -> R0IntegrityVerifier:
    return R0IntegrityVerifier(
        store,
        _registry(),
        VerificationBudget(
            max_events=100,
            max_payload_bytes=10_000,
            max_total_payload_bytes=100_000,
        ),
    )


def _append_target(store: SQLiteEventPayloadStore) -> EventEnvelope:
    event = EventEnvelope(
        event_id="EVT-1",
        event_type="TEST_EVENT",
        envelope_schema_version=1,
        payload_schema="test-event/v1",
        stream_id="test:stream",
        stream_version=1,
        batch_id="BATCH-EVT-1",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-05T00:00:00Z",
        recorded_at="2026-08-05T00:00:00Z",
        producer=ProducerRef("redaction-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-1", 1),
        causation_id="CMD-EVT-1",
        correlation_id="CORR-1",
        affects_domain_state=True,
        payload_digest="sha256:untrusted",
        payload_ref="PAYLOAD-EVT-1",
        previous_hash="sha256:untrusted",
        event_hash="sha256:untrusted",
    )
    return store.append_one(event, {"n": 1}, registry=_registry())


def _request() -> RedactionRequest:
    return RedactionRequest(
        idempotency_key="REDACT-1",
        command_id="CMD-REDACT-1",
        target_event_id="EVT-1",
        target_stream="test:stream",
        expected_stream_version=1,
        reason="user-requested erasure",
        issuer=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-1", 1),
        correlation_id="CORR-REDACT-1",
        audit_event_id="AUDIT-1",
        producer=ProducerRef("redaction-test", "0.1.0"),
        occurred_at="2026-08-05T01:00:00Z",
        recorded_at="2026-08-05T01:00:00Z",
    )


def _apply_redaction(store: SQLiteEventPayloadStore) -> None:
    SQLiteRedactionExecutor(store, _registry()).redact(_request())


def _insert_forged_redaction(
    store: SQLiteEventPayloadStore,
    *,
    target_event_id: str = "EVT-1",
    target_stream_id: str = "test:stream",
    target_payload_ref: str = "PAYLOAD-EVT-1",
    audit_event_id: str = "AUDIT-GHOST",
) -> None:
    store.raw_connection_for_tests().execute(
        """
        INSERT INTO redactions(
            target_event_id, idempotency_key, fingerprint,
            target_stream_id, target_payload_ref, audit_event_id,
            reason, capability_lease_id, capability_revision, redacted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            target_event_id,
            f"FORGED-{target_event_id}",
            "sha256:forged",
            target_stream_id,
            target_payload_ref,
            audit_event_id,
            "forged reason",
            "CAP-1",
            1,
            "2026-08-05T01:00:00Z",
        ),
    )


def _assert_failure(
    store: SQLiteEventPayloadStore,
    expected: IntegrityCode,
) -> None:
    report = _verifier(store).verify_stream("test:stream")
    assert not report.ok
    assert report.failure is not None
    assert report.failure.code is expected


def test_r0_rejects_forged_row_without_audit_event() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_target(store)
        store.raw_connection_for_tests().execute(
            "DELETE FROM event_payloads WHERE payload_ref = 'PAYLOAD-EVT-1'"
        )
        _insert_forged_redaction(store)

        _assert_failure(store, IntegrityCode.REDACTION_AUDIT_EVENT_MISSING)


def test_r0_rejects_redaction_row_for_missing_target_event() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_target(store)
        _insert_forged_redaction(
            store,
            target_event_id="EVT-GHOST",
            target_payload_ref="PAYLOAD-GHOST",
        )

        _assert_failure(store, IntegrityCode.REDACTION_TARGET_EVENT_MISSING)


@pytest.mark.parametrize(
    ("column", "value", "expected"),
    [
        (
            "event_type",
            "TEST_EVENT",
            IntegrityCode.REDACTION_AUDIT_TYPE_MISMATCH,
        ),
        (
            "payload_schema",
            "test-event/v1",
            IntegrityCode.REDACTION_AUDIT_SCHEMA_MISMATCH,
        ),
        (
            "stream_id",
            "other:stream",
            IntegrityCode.REDACTION_AUDIT_STREAM_MISMATCH,
        ),
    ],
)
def test_r0_rejects_wrong_audit_event_identity(
    column: str,
    value: str,
    expected: IntegrityCode,
) -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_target(store)
        _apply_redaction(store)
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER events_are_immutable_on_update")
        connection.execute(
            f"UPDATE events SET {column} = ? WHERE event_id = 'AUDIT-1'",
            (value,),
        )

        _assert_failure(store, expected)


def test_r0_rejects_missing_audit_payload() -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_target(store)
        _apply_redaction(store)
        audit_event = store.load_event("AUDIT-1")
        assert audit_event is not None
        store.raw_connection_for_tests().execute(
            "DELETE FROM event_payloads WHERE payload_ref = ?",
            (audit_event.payload_ref,),
        )

        _assert_failure(store, IntegrityCode.REDACTION_AUDIT_PAYLOAD_MISSING)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("target_event_id", "EVT-OTHER"),
        ("target_stream_id", "other:stream"),
        ("target_payload_ref", "PAYLOAD-OTHER"),
        ("reason", "different reason"),
        (
            "authority",
            {"capability_lease_id": "CAP-OTHER", "capability_revision": 9},
        ),
    ],
)
def test_r0_rejects_mismatched_audit_payload(
    field: str,
    value: object,
) -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_target(store)
        _apply_redaction(store)
        audit_event = store.load_event("AUDIT-1")
        assert audit_event is not None
        stored = store.load_payload(audit_event.payload_ref)
        assert stored is not None
        payload = json.loads(stored.payload_bytes.decode("utf-8"))
        payload[field] = value

        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER payload_material_cannot_be_rewritten")
        connection.execute(
            "UPDATE event_payloads SET payload_bytes = ? WHERE payload_ref = ?",
            (canonical_json_bytes(payload), audit_event.payload_ref),
        )

        _assert_failure(store, IntegrityCode.REDACTION_AUDIT_PAYLOAD_MISMATCH)


@pytest.mark.parametrize(
    ("assignment", "expected"),
    [
        (
            "reason = 'different reason'",
            IntegrityCode.REDACTION_AUDIT_PAYLOAD_MISMATCH,
        ),
        (
            "capability_lease_id = 'CAP-OTHER'",
            IntegrityCode.REDACTION_AUTHORITY_MISMATCH,
        ),
        (
            "capability_revision = 9",
            IntegrityCode.REDACTION_AUTHORITY_MISMATCH,
        ),
    ],
)
def test_r0_rejects_mismatched_redaction_row(
    assignment: str,
    expected: IntegrityCode,
) -> None:
    with SQLiteEventPayloadStore.in_memory() as store:
        store.initialize_schema()
        _append_target(store)
        _apply_redaction(store)
        connection = store.raw_connection_for_tests()
        connection.execute("DROP TRIGGER redactions_are_immutable_on_update")
        connection.execute(
            f"UPDATE redactions SET {assignment} WHERE target_event_id = 'EVT-1'"
        )

        _assert_failure(store, expected)
