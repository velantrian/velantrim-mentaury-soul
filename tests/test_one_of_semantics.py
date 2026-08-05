from __future__ import annotations

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    EventEnvelope,
    ProducerRef,
)
from mentaury.validation import (
    EventSchemaDefinition,
    ObjectSpec,
    OneOfSpec,
    SchemaRegistry,
    StringSpec,
    ValidationCode,
)


def event() -> EventEnvelope:
    return EventEnvelope(
        event_id="EVT-ONE-OF",
        event_type="ONE_OF_TEST",
        envelope_schema_version=1,
        payload_schema="one-of-test/v1",
        stream_id="test:one-of",
        stream_version=1,
        batch_id="BATCH-ONE-OF",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-05T00:00:00Z",
        recorded_at="2026-08-05T00:00:00Z",
        producer=ProducerRef("one-of-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-81", 2),
        causation_id="CMD-ONE-OF",
        correlation_id="CORR-ONE-OF",
        affects_domain_state=True,
        payload_digest="sha256:untrusted",
        payload_ref="PAYLOAD-ONE-OF",
        previous_hash="sha256:untrusted",
        event_hash="sha256:untrusted",
    )


def registry() -> SchemaRegistry:
    return SchemaRegistry(
        [
            EventSchemaDefinition(
                event_type="ONE_OF_TEST",
                payload_schema="one-of-test/v1",
                affects_domain_state=True,
                payload=ObjectSpec(
                    {
                        "value": OneOfSpec(
                            (StringSpec(min_length=0), StringSpec(min_length=1))
                        )
                    },
                    required=frozenset({"value"}),
                ),
            )
        ]
    )


def test_one_of_rejects_value_matching_multiple_options() -> None:
    issues = registry().validate_event_payload(event(), {"value": "alpha"})
    assert len(issues) == 1
    assert issues[0].code is ValidationCode.TYPE_MISMATCH
    assert "more than one" in issues[0].message


def test_one_of_accepts_value_matching_exactly_one_option() -> None:
    issues = registry().validate_event_payload(event(), {"value": ""})
    assert issues == ()
