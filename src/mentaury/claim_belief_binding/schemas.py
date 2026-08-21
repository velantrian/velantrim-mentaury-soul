"""Structural schema for the CBP-v0.1 binding event."""

from __future__ import annotations

from mentaury.validation import EventSchemaDefinition, IntegerSpec, ObjectSpec, StringSpec

from .contracts import BELIEF_CLAIM_BOUND, BELIEF_CLAIM_BOUND_SCHEMA


def claim_belief_binding_schema_definitions() -> tuple[EventSchemaDefinition, ...]:
    return (
        EventSchemaDefinition(
            event_type=BELIEF_CLAIM_BOUND,
            payload_schema=BELIEF_CLAIM_BOUND_SCHEMA,
            affects_domain_state=True,
            payload=ObjectSpec(
                {
                    "contract_version": StringSpec(min_length=1),
                    "belief_id": StringSpec(min_length=1),
                    "belief_revision": IntegerSpec(minimum=1),
                    "claim_id": StringSpec(min_length=1),
                    "claim_record_fingerprint": StringSpec(
                        min_length=64, pattern=r"[0-9a-f]{64}"
                    ),
                    "claim_type": StringSpec(min_length=1),
                    "statement_ref": StringSpec(min_length=1),
                    "statement_equivalence": StringSpec(min_length=1),
                    "binding_input_fingerprint": StringSpec(
                        min_length=64, pattern=r"[0-9a-f]{64}"
                    ),
                },
                required=frozenset(
                    {
                        "contract_version",
                        "belief_id",
                        "belief_revision",
                        "claim_id",
                        "claim_record_fingerprint",
                        "claim_type",
                        "statement_ref",
                        "statement_equivalence",
                        "binding_input_fingerprint",
                    }
                ),
            ),
        ),
    )
