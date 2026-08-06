"""Strict P0-015 schemas for evidence-gated belief decisions."""

from __future__ import annotations

from mentaury.validation import (
    ArraySpec,
    BooleanSpec,
    EventSchemaDefinition,
    IntegerSpec,
    ObjectSpec,
    StringSpec,
)

from .contracts import (
    BELIEF_EVIDENCE_GATED,
    BELIEF_EVIDENCE_GATED_SCHEMA,
    EVIDENCE_GATE_DECISION_SCHEMA,
    EVIDENCE_GATE_REJECTED,
)


def _strings(*, min_items: int = 0) -> ArraySpec:
    return ArraySpec(StringSpec(min_length=1), min_items=min_items)


def _policy_spec() -> ObjectSpec:
    return ObjectSpec(
        {
            "policy_id": StringSpec(min_length=1),
            "allowed_claim_types": _strings(min_items=1),
            "minimum_source_groups_for": IntegerSpec(minimum=1),
            "minimum_source_groups_against": IntegerSpec(minimum=1),
            "minimum_reliability_milli": IntegerSpec(minimum=0, maximum=1000),
            "minimum_relevance_milli": IntegerSpec(minimum=0, maximum=1000),
            "maximum_age_seconds": IntegerSpec(minimum=1),
        },
        required=frozenset(
            {
                "policy_id",
                "allowed_claim_types",
                "minimum_source_groups_for",
                "minimum_source_groups_against",
                "minimum_reliability_milli",
                "minimum_relevance_milli",
                "maximum_age_seconds",
            }
        ),
    )


def _record_spec() -> ObjectSpec:
    return ObjectSpec(
        {
            "evidence_ref": StringSpec(min_length=1),
            "side": StringSpec(min_length=1),
            "source_group": StringSpec(min_length=1),
            "provenance_ref": StringSpec(min_length=1),
            "content_digest": StringSpec(min_length=71),
            "observed_at": StringSpec(min_length=1),
            "reliability_milli": IntegerSpec(minimum=0, maximum=1000),
            "relevance_milli": IntegerSpec(minimum=0, maximum=1000),
            "revoked": BooleanSpec(),
        },
        required=frozenset(
            {
                "evidence_ref",
                "side",
                "source_group",
                "provenance_ref",
                "content_digest",
                "observed_at",
                "reliability_milli",
                "relevance_milli",
                "revoked",
            }
        ),
    )


def _receipt_spec() -> ObjectSpec:
    return ObjectSpec(
        {
            "profile": StringSpec(min_length=1),
            "belief_id": StringSpec(min_length=1),
            "belief_revision": IntegerSpec(minimum=1),
            "claim_type": StringSpec(min_length=1),
            "statement_digest": StringSpec(min_length=71),
            "evaluated_at": StringSpec(min_length=1),
            "policy_id": StringSpec(min_length=1),
            "policy_digest": StringSpec(min_length=71),
            "evidence_set_digest": StringSpec(min_length=71),
            "outcome": StringSpec(min_length=1),
            "qualifying_for_refs": _strings(),
            "qualifying_against_refs": _strings(),
            "source_groups_for": _strings(),
            "source_groups_against": _strings(),
            "rejected_refs": _strings(),
            "receipt_digest": StringSpec(min_length=71),
        },
        required=frozenset(
            {
                "profile",
                "belief_id",
                "belief_revision",
                "claim_type",
                "statement_digest",
                "evaluated_at",
                "policy_id",
                "policy_digest",
                "evidence_set_digest",
                "outcome",
                "qualifying_for_refs",
                "qualifying_against_refs",
                "source_groups_for",
                "source_groups_against",
                "rejected_refs",
                "receipt_digest",
            }
        ),
    )


def evidence_gate_schema_definitions() -> tuple[EventSchemaDefinition, ...]:
    return (
        EventSchemaDefinition(
            event_type=BELIEF_EVIDENCE_GATED,
            payload_schema=BELIEF_EVIDENCE_GATED_SCHEMA,
            affects_domain_state=True,
            payload=ObjectSpec(
                {
                    "belief_id": StringSpec(min_length=1),
                    "previous_revision": IntegerSpec(minimum=1),
                    "new_revision": IntegerSpec(minimum=2),
                    "claim_type": StringSpec(min_length=1),
                    "statement": StringSpec(min_length=1),
                    "previous_status": StringSpec(min_length=1),
                    "new_status": StringSpec(min_length=1),
                    "evaluated_at": StringSpec(min_length=1),
                    "policy": _policy_spec(),
                    "records": ArraySpec(_record_spec(), min_items=1),
                    "receipt": _receipt_spec(),
                },
                required=frozenset(
                    {
                        "belief_id",
                        "previous_revision",
                        "new_revision",
                        "claim_type",
                        "statement",
                        "previous_status",
                        "new_status",
                        "evaluated_at",
                        "policy",
                        "records",
                        "receipt",
                    }
                ),
            ),
        ),
        EventSchemaDefinition(
            event_type=EVIDENCE_GATE_REJECTED,
            payload_schema=EVIDENCE_GATE_DECISION_SCHEMA,
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
                    "receipt": _receipt_spec(),
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
        ),
    )
