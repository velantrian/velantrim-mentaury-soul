"""Structural event schemas for P0-014 belief lifecycle facts and audits."""

from __future__ import annotations

from mentaury.validation import (
    ArraySpec,
    EventSchemaDefinition,
    IntegerSpec,
    ObjectSpec,
    StringSpec,
)

from .contracts import (
    AUTHORITY_CHECK_FAILED,
    BELIEF_CREATED,
    BELIEF_CREATED_SCHEMA,
    BELIEF_DECISION_SCHEMA,
    BELIEF_REVISED,
    BELIEF_REVISED_SCHEMA,
    BELIEF_REVISION_REJECTED,
    COMMAND_REJECTED,
    CONTRADICTION_REGISTERED,
    CONTRADICTION_REGISTERED_SCHEMA,
    EVIDENCE_ATTACHED,
    EVIDENCE_ATTACHED_SCHEMA,
    INVARIANT_CHECK_FAILED,
)


def _strings(*, min_items: int = 0) -> ArraySpec:
    return ArraySpec(StringSpec(min_length=1), min_items=min_items)


def belief_schema_definitions() -> tuple[EventSchemaDefinition, ...]:
    """Return strict v1 schemas; enum membership remains lifecycle policy."""

    return (
        EventSchemaDefinition(
            event_type=BELIEF_CREATED,
            payload_schema=BELIEF_CREATED_SCHEMA,
            affects_domain_state=True,
            payload=ObjectSpec(
                {
                    "belief_id": StringSpec(min_length=1),
                    "statement": StringSpec(min_length=1),
                    "claim_type": StringSpec(min_length=1),
                    "status": StringSpec(min_length=1),
                    "revision": IntegerSpec(minimum=1),
                },
                required=frozenset(
                    {"belief_id", "statement", "claim_type", "status", "revision"}
                ),
            ),
        ),
        EventSchemaDefinition(
            event_type=EVIDENCE_ATTACHED,
            payload_schema=EVIDENCE_ATTACHED_SCHEMA,
            affects_domain_state=True,
            payload=ObjectSpec(
                {
                    "belief_id": StringSpec(min_length=1),
                    "evidence_ref": StringSpec(min_length=1),
                    "side": StringSpec(min_length=1),
                    "note": StringSpec(min_length=1),
                },
                required=frozenset({"belief_id", "evidence_ref", "side"}),
            ),
        ),
        EventSchemaDefinition(
            event_type=CONTRADICTION_REGISTERED,
            payload_schema=CONTRADICTION_REGISTERED_SCHEMA,
            affects_domain_state=True,
            payload=ObjectSpec(
                {
                    "belief_id": StringSpec(min_length=1),
                    "contradiction_id": StringSpec(min_length=1),
                    "statement": StringSpec(min_length=1),
                    "evidence_refs": _strings(min_items=1),
                    "resulting_status": StringSpec(min_length=1),
                },
                required=frozenset(
                    {
                        "belief_id",
                        "contradiction_id",
                        "statement",
                        "evidence_refs",
                        "resulting_status",
                    }
                ),
            ),
        ),
        EventSchemaDefinition(
            event_type=BELIEF_REVISED,
            payload_schema=BELIEF_REVISED_SCHEMA,
            affects_domain_state=True,
            payload=ObjectSpec(
                {
                    "belief_id": StringSpec(min_length=1),
                    "previous_revision": IntegerSpec(minimum=1),
                    "new_revision": IntegerSpec(minimum=2),
                    "previous_statement": StringSpec(min_length=1),
                    "new_statement": StringSpec(min_length=1),
                    "previous_status": StringSpec(min_length=1),
                    "new_status": StringSpec(min_length=1),
                    "reason": StringSpec(min_length=1),
                    "evidence_refs": _strings(min_items=1),
                    "addressed_contradiction_ids": _strings(),
                },
                required=frozenset(
                    {
                        "belief_id",
                        "previous_revision",
                        "new_revision",
                        "previous_statement",
                        "new_statement",
                        "previous_status",
                        "new_status",
                        "reason",
                        "evidence_refs",
                        "addressed_contradiction_ids",
                    }
                ),
            ),
        ),
        *tuple(
            EventSchemaDefinition(
                event_type=event_type,
                payload_schema=BELIEF_DECISION_SCHEMA,
                affects_domain_state=False,
                payload=ObjectSpec(
                    {
                        "command_id": StringSpec(min_length=1),
                        "command_type": StringSpec(min_length=1),
                        "belief_id": StringSpec(min_length=1),
                        "rejection_code": StringSpec(min_length=1),
                        "message": StringSpec(min_length=1),
                        "expected_stream_version": IntegerSpec(minimum=0),
                        "current_belief_revision": IntegerSpec(minimum=0),
                        "requested_belief_revision": IntegerSpec(minimum=0),
                    },
                    required=frozenset(
                        {
                            "command_id",
                            "command_type",
                            "belief_id",
                            "rejection_code",
                            "message",
                            "expected_stream_version",
                            "current_belief_revision",
                            "requested_belief_revision",
                        }
                    ),
                ),
            )
            for event_type in (
                COMMAND_REJECTED,
                BELIEF_REVISION_REJECTED,
                AUTHORITY_CHECK_FAILED,
                INVARIANT_CHECK_FAILED,
            )
        ),
    )
