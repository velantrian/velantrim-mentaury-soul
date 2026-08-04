from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import cast

import pytest

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    CommandEnvelope,
    EventEnvelope,
    PendingEvent,
    ProducerRef,
    snapshot_pending_batch,
)


def actor() -> ActorRef:
    return ActorRef(actor_type="operator", actor_id="operator:primary")


def authority() -> AuthorityRef:
    return AuthorityRef(capability_lease_id="CAP-81", capability_revision=2)


def test_command_takes_detached_immutable_payload_snapshot() -> None:
    source = {"statement": "alpha", "evidence": [{"id": "E-1"}]}
    command = CommandEnvelope(
        command_id="CMD-1",
        command_type="CREATE_BELIEF",
        command_schema="create-belief/v1",
        target_stream="belief:B-204",
        expected_stream_version=0,
        issued_at="2026-08-04T22:00:00Z",
        issuer=actor(),
        authority=authority(),
        correlation_id="CORR-12",
        idempotency_key="create-belief:B-204:request-1",
        payload=source,
    )

    source["statement"] = "mutated"
    cast(list[object], source["evidence"]).append({"id": "E-2"})

    assert command.payload["statement"] == "alpha"
    assert command.payload["evidence"] == ({"id": "E-1"},)
    with pytest.raises(TypeError):
        command.payload["statement"] = "forbidden"  # type: ignore[index]


def test_envelopes_are_frozen() -> None:
    pending = PendingEvent(
        event_type="BELIEF_CREATED",
        payload_schema="belief-created/v1",
        affects_domain_state=True,
        payload={"belief_id": "B-204"},
    )
    with pytest.raises(FrozenInstanceError):
        pending.event_type = "CHANGED"  # type: ignore[misc]


def test_command_requires_typed_actor_and_authority_refs() -> None:
    with pytest.raises(TypeError, match="issuer"):
        CommandEnvelope(
            command_id="CMD-1",
            command_type="CREATE_BELIEF",
            command_schema="create-belief/v1",
            target_stream="belief:B-204",
            expected_stream_version=0,
            issued_at="2026-08-04T22:00:00Z",
            issuer=cast(ActorRef, {"type": "operator"}),
            authority=authority(),
            correlation_id="CORR-12",
            idempotency_key="request-1",
            payload={},
        )


def test_command_rejects_negative_expected_version() -> None:
    with pytest.raises(ValueError, match="expected_stream_version"):
        CommandEnvelope(
            command_id="CMD-1",
            command_type="CREATE_BELIEF",
            command_schema="create-belief/v1",
            target_stream="belief:B-204",
            expected_stream_version=-1,
            issued_at="2026-08-04T22:00:00Z",
            issuer=actor(),
            authority=authority(),
            correlation_id="CORR-12",
            idempotency_key="request-1",
            payload={},
        )


def test_payload_rejects_non_portable_tree_values() -> None:
    with pytest.raises(TypeError, match="unsupported payload value type"):
        PendingEvent(
            event_type="BELIEF_CREATED",
            payload_schema="belief-created/v1",
            affects_domain_state=True,
            payload={"raw": b"bytes"},
        )


def test_pending_batch_snapshot_preserves_order() -> None:
    first = PendingEvent("FIRST", "first/v1", True, {"n": 1})
    second = PendingEvent("SECOND", "second/v1", False, {"n": 2})
    source = [first, second]

    batch = snapshot_pending_batch(source)
    source.reverse()

    assert batch == (first, second)


def test_pending_batch_must_not_be_empty() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        snapshot_pending_batch([])


def test_event_envelope_accepts_valid_batch_position() -> None:
    event = EventEnvelope(
        event_id="EVT-1",
        event_type="BELIEF_CREATED",
        envelope_schema_version=1,
        payload_schema="belief-created/v1",
        stream_id="belief:B-204",
        stream_version=1,
        batch_id="BATCH-1",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-04T22:00:00Z",
        recorded_at="2026-08-04T22:00:00.120Z",
        producer=ProducerRef("belief-command-handler", "0.1.0"),
        initiator=actor(),
        authority=authority(),
        causation_id="CMD-1",
        correlation_id="CORR-12",
        affects_domain_state=True,
        payload_digest="sha256:payload",
        payload_ref="PAYLOAD-1",
        previous_hash="sha256:genesis",
        event_hash="sha256:event",
    )

    assert event.batch_index == 0
    assert event.batch_size == 1
    assert not hasattr(event, "payload")


def test_event_envelope_rejects_out_of_range_batch_index() -> None:
    with pytest.raises(ValueError, match="batch_index"):
        EventEnvelope(
            event_id="EVT-1",
            event_type="BELIEF_CREATED",
            envelope_schema_version=1,
            payload_schema="belief-created/v1",
            stream_id="belief:B-204",
            stream_version=1,
            batch_id="BATCH-1",
            batch_index=1,
            batch_size=1,
            occurred_at="2026-08-04T22:00:00Z",
            recorded_at="2026-08-04T22:00:00.120Z",
            producer=ProducerRef("belief-command-handler", "0.1.0"),
            initiator=actor(),
            authority=authority(),
            causation_id="CMD-1",
            correlation_id="CORR-12",
            affects_domain_state=True,
            payload_digest="sha256:payload",
            payload_ref="PAYLOAD-1",
            previous_hash="sha256:genesis",
            event_hash="sha256:event",
        )
