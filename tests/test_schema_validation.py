from __future__ import annotations

from dataclasses import replace
from decimal import Decimal

import pytest

from mentaury.contracts import (
    ActorRef,
    AuthorityRef,
    EventEnvelope,
    PendingEvent,
    ProducerRef,
)
from mentaury.validation import (
    ArraySpec,
    BooleanSpec,
    EventSchemaDefinition,
    IntegerSpec,
    ObjectSpec,
    OneOfSpec,
    SchemaRegistry,
    SchemaValidationError,
    StringSpec,
    ValidationCode,
)


def definition() -> EventSchemaDefinition:
    return EventSchemaDefinition(
        event_type="BELIEF_CREATED",
        payload_schema="belief-created/v1",
        affects_domain_state=True,
        payload=ObjectSpec(
            properties={
                "belief_id": StringSpec(min_length=1),
                "statement": StringSpec(min_length=1),
                "confidence_basis": ObjectSpec(
                    properties={
                        "sources": ArraySpec(
                            StringSpec(min_length=1), min_items=1
                        ),
                        "reviewed": BooleanSpec(),
                    },
                    required=frozenset({"sources", "reviewed"}),
                ),
                "revision": OneOfSpec(
                    (IntegerSpec(minimum=1), StringSpec(min_length=1))
                ),
            },
            required=frozenset(
                {"belief_id", "statement", "confidence_basis"}
            ),
        ),
    )


def registry() -> SchemaRegistry:
    return SchemaRegistry([definition()])


def payload(**changes: object) -> dict[object, object]:
    value: dict[object, object] = {
        "belief_id": "B-204",
        "statement": "alpha",
        "confidence_basis": {
            "sources": ["E-1"],
            "reviewed": True,
        },
    }
    value.update(changes)
    return value


def pending(**changes: object) -> PendingEvent:
    value: dict[str, object] = {
        "event_type": "BELIEF_CREATED",
        "payload_schema": "belief-created/v1",
        "affects_domain_state": True,
        "payload": payload(),
    }
    value.update(changes)
    return PendingEvent(**value)  # type: ignore[arg-type]


def envelope(**changes: object) -> EventEnvelope:
    value = EventEnvelope(
        event_id="EVT-1",
        event_type="BELIEF_CREATED",
        envelope_schema_version=1,
        payload_schema="belief-created/v1",
        stream_id="belief:B-204",
        stream_version=1,
        batch_id="BATCH-1",
        batch_index=0,
        batch_size=1,
        occurred_at="2026-08-05T00:00:00Z",
        recorded_at="2026-08-05T00:00:00Z",
        producer=ProducerRef("validator-test", "0.1.0"),
        initiator=ActorRef("operator", "operator:primary"),
        authority=AuthorityRef("CAP-81", 2),
        causation_id="CMD-1",
        correlation_id="CORR-1",
        affects_domain_state=True,
        payload_digest="sha256:payload",
        payload_ref="PAYLOAD-1",
        previous_hash="sha256:genesis",
        event_hash="sha256:event",
    )
    return replace(value, **changes)


def codes(issues: tuple[object, ...]) -> set[ValidationCode]:
    return {issue.code for issue in issues}  # type: ignore[attr-defined]


def test_registry_is_immutable_and_rejects_duplicates() -> None:
    properties = {"value": StringSpec()}
    spec = ObjectSpec(properties, required=frozenset({"value"}))
    properties["injected"] = StringSpec()
    assert "injected" not in spec.properties
    with pytest.raises(ValueError, match="duplicate event type"):
        SchemaRegistry([definition(), definition()])


def test_unknown_event_type_fails_closed() -> None:
    issues = registry().validate_pending_event(
        pending(event_type="UNKNOWN")
    )
    assert codes(issues) == {ValidationCode.UNKNOWN_EVENT_TYPE}


def test_identity_mismatches_are_reported_together() -> None:
    invalid = envelope(
        payload_schema="belief-created/v2",
        envelope_schema_version=2,
        affects_domain_state=False,
    )
    assert codes(registry().validate_event_envelope(invalid)) == {
        ValidationCode.EVENT_SCHEMA_MISMATCH,
        ValidationCode.UNSUPPORTED_ENVELOPE_VERSION,
        ValidationCode.AFFECTS_DOMAIN_STATE_MISMATCH,
    }


def test_required_and_forbidden_fields_are_reported() -> None:
    value = payload(undeclared="no")
    del value["statement"]
    issues = registry().validate_pending_event(pending(payload=value))
    assert codes(issues) == {
        ValidationCode.MISSING_REQUIRED_FIELD,
        ValidationCode.FORBIDDEN_FIELD,
    }


def test_nested_array_and_boolean_types_are_checked() -> None:
    value = payload(
        confidence_basis={"sources": [], "reviewed": "yes"}
    )
    assert codes(
        registry().validate_pending_event(pending(payload=value))
    ) == {
        ValidationCode.ARRAY_TOO_SHORT,
        ValidationCode.TYPE_MISMATCH,
    }


@pytest.mark.parametrize("bad", [1.0, 2**53])
def test_pending_unsupported_numbers_are_rejected(bad: object) -> None:
    issues = registry().validate_pending_event(
        pending(payload=payload(revision=bad))
    )
    assert codes(issues) == {ValidationCode.UNSUPPORTED_NUMERIC}


def test_raw_decimal_and_non_string_key_are_rejected() -> None:
    decimal_issues = registry().validate_event_payload(
        envelope(), payload(revision=Decimal("1"))  # type: ignore[arg-type]
    )
    keyed = payload()
    keyed[7] = "invalid"
    key_issues = registry().validate_event_payload(
        envelope(), keyed  # type: ignore[arg-type]
    )
    assert codes(decimal_issues) == {ValidationCode.UNSUPPORTED_NUMERIC}
    assert ValidationCode.NON_STRING_OBJECT_KEY in codes(key_issues)


def test_invalid_unicode_is_rejected() -> None:
    issues = registry().validate_pending_event(
        pending(payload=payload(statement="\ud800"))
    )
    assert codes(issues) == {ValidationCode.INVALID_UNICODE}


def test_external_payload_is_checked_against_event_identity() -> None:
    value = payload(confidence_basis={"sources": ["E-1"]})
    issues = registry().validate_event_payload(
        envelope(), value  # type: ignore[arg-type]
    )
    assert codes(issues) == {ValidationCode.MISSING_REQUIRED_FIELD}
    assert issues[0].path == "$.confidence_basis.reviewed"


def test_valid_pending_event_passes_and_require_returns() -> None:
    assert registry().validate_pending_event(pending()) == ()
    registry().require_pending_event(pending())


def test_require_raises_stable_issue_collection() -> None:
    with pytest.raises(SchemaValidationError) as captured:
        registry().require_pending_event(
            pending(payload={"belief_id": "", "statement": ""})
        )
    assert len(captured.value.issues) >= 3
    assert "MISSING_REQUIRED_FIELD" in str(captured.value)


def test_cyclic_external_payload_is_rejected() -> None:
    cyclic: list[object] = []
    cyclic.append(cyclic)
    cycle_registry = SchemaRegistry(
        [
            EventSchemaDefinition(
                event_type="BELIEF_CREATED",
                payload_schema="belief-created/v1",
                affects_domain_state=True,
                payload=ObjectSpec(
                    {"matrix": ArraySpec(ArraySpec(StringSpec()))},
                    required=frozenset({"matrix"}),
                ),
            )
        ]
    )
    issues = cycle_registry.validate_event_payload(
        envelope(), {"matrix": cyclic}
    )
    assert codes(issues) == {ValidationCode.CYCLIC_VALUE}
