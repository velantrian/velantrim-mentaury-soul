"""Adversarial conformance evidence for frozen NPG-v0.1."""

from __future__ import annotations

import ast
from dataclasses import replace
import inspect
import os

import pytest

from mentaury.contracts import CanonicalJSONError, canonical_json_bytes
import mentaury.non_projection.classifier as classifier_module
from mentaury.non_projection import (
    AnachronismRisk,
    Attribution,
    AttributedInterpretationEnvelope,
    AuthorityExclusions,
    Claim,
    ClaimClass,
    ContextDistanceLevel,
    ContextualDistance,
    Interpretation,
    InterpretationState,
    NonProjectionBudget,
    NonProjectionContractError,
    NonProjectionDecision,
    NonProjectionReason,
    ProjectionIntent,
    ProvenanceState,
    ReviewProvenance,
    ReviewRecord,
    ReviewerIndependence,
    ScopeBoundary,
    Sensitivity,
    SourceClass,
    SourceOrigin,
    SourceProvenance,
    SubjectRelation,
    classify_non_projection,
)

EXPECTED_CLEAN_FINGERPRINT = "6e0d6105651b905626ae1552d6ac58baf0f238520ce16eed31bece91bf9e4150"


def _budget(**changes: int) -> NonProjectionBudget:
    values = dict(
        max_string_bytes=4096,
        max_tuple_items=512,
        max_review_records=64,
        max_canonical_input_bytes=262144,
    )
    values.update(changes)
    return NonProjectionBudget(**values)


def _clean(**changes: object) -> AttributedInterpretationEnvelope:
    values = dict(
        envelope_version="AIE-v0.1",
        source_provenance=SourceProvenance(
            "source-1",
            "creator-1",
            SourceClass.CREATOR_TESTIMONY,
            SourceOrigin.PRIMARY,
            ProvenanceState.VERIFIED,
            "capture-1",
            Sensitivity.NORMAL,
            "usage-1",
            (),
        ),
        attribution=Attribution(
            "creator-1", "creator-1", SubjectRelation.NON_SELF, None, ("basis-1",)
        ),
        claim=Claim(
            "claim-1",
            ClaimClass.AUTOBIOGRAPHICAL_TESTIMONY,
            "statement-1",
            True,
        ),
        interpretation=Interpretation(
            "interpretation-1",
            "reviewer-1",
            InterpretationState.SUPPORTED,
            (),
            (),
        ),
        contextual_distance=ContextualDistance(
            ContextDistanceLevel.SAME_CONTEXT,
            ContextDistanceLevel.SAME_CONTEXT,
            ContextDistanceLevel.SAME_CONTEXT,
            ContextDistanceLevel.SAME_CONTEXT,
            ContextDistanceLevel.SAME_CONTEXT,
            AnachronismRisk.LOW,
        ),
        review_provenance=ReviewProvenance(()),
        scope=ScopeBoundary(("wisdom",), ("wisdom",), ("identity",), (), ()),
        authority_exclusions=AuthorityExclusions(
            False, False, False, False, False, False, False, False, False
        ),
        projection_intent=ProjectionIntent(
            ("wisdom",),
            False,
            False,
            False,
            False,
            False,
            False,
            0,
            False,
            False,
            False,
            False,
            False,
        ),
    )
    values.update(changes)
    return AttributedInterpretationEnvelope(**values)


def _canonical_input(
    envelope: AttributedInterpretationEnvelope, budget: NonProjectionBudget
) -> dict[str, object]:
    return {
        "domain": "MENTAURY_NPG_INPUT_V1",
        "non_projection_contract_version": "NPG-v0.1",
        "envelope_version": envelope.envelope_version,
        "canonical_profile": "MENTAURY_CANONICAL_JSON_V1",
        "source_provenance_scope": "CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY",
        "envelope": envelope.to_value(),
        "budget": budget.to_value(),
    }


# NPC-CTX: strict type/admission and hard-cap proof.
def test_npc_ctx_hard_caps_and_no_hidden_repair() -> None:
    with pytest.raises(NonProjectionContractError):
        SourceProvenance(
            "x" * 4097,
            None,
            SourceClass.RESEARCH_PRIMARY,
            SourceOrigin.PRIMARY,
            ProvenanceState.VERIFIED,
            None,
            Sensitivity.NORMAL,
            "usage",
            (),
        )
    with pytest.raises(NonProjectionContractError):
        ScopeBoundary(tuple(f"item-{i:04d}" for i in range(513)), (), (), (), ())
    with pytest.raises(NonProjectionContractError):
        ScopeBoundary(("z", "a"), (), (), (), ())
    with pytest.raises(NonProjectionContractError):
        SourceProvenance(
            " source ",
            None,
            SourceClass.RESEARCH_PRIMARY,
            SourceOrigin.PRIMARY,
            ProvenanceState.VERIFIED,
            None,
            Sensitivity.NORMAL,
            "usage",
            (),
        )
    with pytest.raises(NonProjectionContractError):
        SourceProvenance(
            "source",
            None,
            "RESEARCH_PRIMARY",  # type: ignore[arg-type]
            SourceOrigin.PRIMARY,
            ProvenanceState.VERIFIED,
            None,
            Sensitivity.NORMAL,
            "usage",
            (),
        )


def test_npc_ctx_review_order_duplicate_and_hard_count_are_rejected() -> None:
    first = ReviewRecord(
        "review-1", "reviewer-1", ReviewerIndependence.DERIVED, None, None, None, False
    )
    second = ReviewRecord(
        "review-2", "reviewer-2", ReviewerIndependence.DERIVED, None, None, None, False
    )
    with pytest.raises(NonProjectionContractError):
        ReviewProvenance((second, first))
    with pytest.raises(NonProjectionContractError):
        ReviewProvenance((first, first))
    too_many = tuple(
        ReviewRecord(
            f"review-{i:03d}",
            f"reviewer-{i:03d}",
            ReviewerIndependence.DERIVED,
            None,
            None,
            None,
            False,
        )
        for i in range(65)
    )
    with pytest.raises(NonProjectionContractError):
        ReviewProvenance(too_many)


def test_npc_ctx_wrong_nested_type_and_bool_are_rejected() -> None:
    base = _clean()
    with pytest.raises(NonProjectionContractError):
        AttributedInterpretationEnvelope(
            base.envelope_version,
            object(),  # type: ignore[arg-type]
            base.attribution,
            base.claim,
            base.interpretation,
            base.contextual_distance,
            base.review_provenance,
            base.scope,
            base.authority_exclusions,
            base.projection_intent,
        )
    with pytest.raises(NonProjectionContractError):
        Claim("claim", ClaimClass.FACTUAL, "statement", 1)  # type: ignore[arg-type]
    with pytest.raises(NonProjectionContractError):
        replace(base.projection_intent, claimed_independent_review_count=True)


def test_npc_ctx_forbidden_public_arguments_cannot_be_injected() -> None:
    for name in (
        "raw_text",
        "clock_provider",
        "environment",
        "repository",
        "backend",
        "model",
        "llm_client",
        "retriever",
        "atlas",
        "tool",
        "identity_registry",
        "relationship_registry",
        "prior_result",
        "fingerprint",
    ):
        with pytest.raises(TypeError):
            classify_non_projection(
                envelope=_clean(), budget=_budget(), **{name: object()}  # type: ignore[arg-type]
            )


def test_npc_ctx_hard_canonical_input_overflow_is_contract_error() -> None:
    base = _clean()
    material_gaps = tuple(f"{i:04d}-" + "x" * 600 for i in range(512))
    source = replace(base.source_provenance, material_gaps=material_gaps)
    with pytest.raises(NonProjectionContractError):
        classify_non_projection(
            envelope=replace(base, source_provenance=source), budget=_budget()
        )


# NPC-FP: exact canonical input/fingerprint fixtures and fail-closed behavior.
def test_npc_fp_exact_canonical_fixture_and_hash() -> None:
    envelope = _clean()
    budget = _budget()
    canonical_input = _canonical_input(envelope, budget)
    assert canonical_input["domain"] == "MENTAURY_NPG_INPUT_V1"
    assert canonical_input["non_projection_contract_version"] == "NPG-v0.1"
    assert canonical_input["envelope_version"] == "AIE-v0.1"
    assert canonical_input["canonical_profile"] == "MENTAURY_CANONICAL_JSON_V1"
    assert canonical_input["source_provenance_scope"] == "CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY"
    assert canonical_input["envelope"] == envelope.to_value()
    assert canonical_input["budget"] == budget.to_value()
    assert len(canonical_json_bytes(canonical_input)) == 2261
    result = classify_non_projection(envelope=envelope, budget=budget)
    assert result.input_fingerprint == EXPECTED_CLEAN_FINGERPRINT


def test_npc_fp_mutations_change_fingerprint_and_repeat_is_exact() -> None:
    base = _clean()
    first = classify_non_projection(envelope=base, budget=_budget())
    repeat = classify_non_projection(envelope=base, budget=_budget())
    changed_claim = replace(base, claim=replace(base.claim, statement_ref="statement-2"))
    changed_budget = _budget(max_tuple_items=511)
    assert first == repeat
    assert first.input_fingerprint == EXPECTED_CLEAN_FINGERPRINT
    assert (
        classify_non_projection(envelope=changed_claim, budget=_budget()).input_fingerprint
        != first.input_fingerprint
    )
    assert (
        classify_non_projection(envelope=base, budget=changed_budget).input_fingerprint
        != first.input_fingerprint
    )


def test_npc_fp_ambient_environment_does_not_change_hash(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first = classify_non_projection(envelope=_clean(), budget=_budget())
    monkeypatch.setenv("MENTAURY_UNRELATED_STATE", "changed")
    second = classify_non_projection(envelope=_clean(), budget=_budget())
    assert first.input_fingerprint == second.input_fingerprint == EXPECTED_CLEAN_FINGERPRINT


def test_npc_fp_canonicalization_failure_and_profile_mismatch_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail(_value: object) -> bytes:
        raise CanonicalJSONError("forced")

    monkeypatch.setattr(
        classifier_module.canonical_json_contract, "canonical_json_bytes", fail
    )
    result = classify_non_projection(envelope=_clean(), budget=_budget())
    assert result.decision is NonProjectionDecision.DEFER
    assert result.primary_reason is NonProjectionReason.CANONICALIZATION_FAILED
    assert result.input_fingerprint is None


def test_npc_fp_profile_mismatch_is_not_positive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        classifier_module.canonical_json_contract, "PROFILE_NAME", "OTHER_PROFILE"
    )
    result = classify_non_projection(envelope=_clean(), budget=_budget())
    assert result.decision is NonProjectionDecision.DEFER
    assert result.primary_reason is NonProjectionReason.CANONICALIZATION_FAILED


# NPC-DEC: precedence and each local budget dimension.
def test_npc_dec_defer_dominates_contested_and_contested_dominates_revise() -> None:
    base = _clean()
    conflicting = replace(
        base.source_provenance, provenance_state=ProvenanceState.CONFLICTING
    )
    unknown_context = replace(
        base.contextual_distance, historical=ContextDistanceLevel.UNKNOWN
    )
    defer_result = classify_non_projection(
        envelope=replace(
            base,
            source_provenance=conflicting,
            contextual_distance=unknown_context,
        ),
        budget=_budget(),
    )
    assert defer_result.decision is NonProjectionDecision.DEFER
    assert defer_result.primary_reason is NonProjectionReason.CONTEXT_UNKNOWN
    assert NonProjectionReason.PROVENANCE_CONFLICTING in defer_result.reasons

    no_actor = replace(base.source_provenance, source_actor_ref=None)
    contested = replace(
        base.interpretation,
        state=InterpretationState.CONTESTED,
        alternatives=("alt-a", "alt-b"),
        disconfirming_refs=("counter-1",),
    )
    contested_result = classify_non_projection(
        envelope=replace(
            base, source_provenance=no_actor, interpretation=contested
        ),
        budget=_budget(),
    )
    assert contested_result.decision is NonProjectionDecision.CONTESTED
    assert contested_result.primary_reason is NonProjectionReason.INTERPRETATION_CONTESTED
    assert NonProjectionReason.ATTRIBUTION_REPAIR_REQUIRED in contested_result.reasons


def test_npc_dec_all_local_budget_dimensions_defer() -> None:
    base = _clean()
    two_refs = replace(
        base.attribution, attribution_basis_refs=("basis-1", "basis-2")
    )
    assert (
        classify_non_projection(
            envelope=replace(base, attribution=two_refs),
            budget=_budget(max_tuple_items=1),
        ).primary_reason
        is NonProjectionReason.BUDGET_EXHAUSTED
    )
    assert (
        classify_non_projection(
            envelope=base, budget=_budget(max_string_bytes=4)
        ).primary_reason
        is NonProjectionReason.BUDGET_EXHAUSTED
    )
    assert (
        classify_non_projection(
            envelope=base, budget=_budget(max_canonical_input_bytes=100)
        ).primary_reason
        is NonProjectionReason.BUDGET_EXHAUSTED
    )
    r1 = ReviewRecord(
        "review-1", "reviewer-1", ReviewerIndependence.DERIVED, None, None, None, False
    )
    r2 = ReviewRecord(
        "review-2", "reviewer-2", ReviewerIndependence.DERIVED, None, None, None, False
    )
    with_reviews = replace(base, review_provenance=ReviewProvenance((r1, r2)))
    assert (
        classify_non_projection(
            envelope=with_reviews, budget=_budget(max_review_records=1)
        ).primary_reason
        is NonProjectionReason.BUDGET_EXHAUSTED
    )


# NPC-SC concrete frozen readiness scenarios not already proven one-to-one by NPC-T tests.
@pytest.mark.parametrize(
    ("scenario_id", "envelope", "decision", "reason"),
    [
        ("NPC-SC-001", _clean(), NonProjectionDecision.PASS_ATTRIBUTED, NonProjectionReason.PASS_ATTRIBUTED),
        (
            "NPC-SC-002",
            replace(
                _clean(),
                source_provenance=replace(
                    _clean().source_provenance,
                    source_class=SourceClass.HISTORICAL_PRIMARY,
                ),
                claim=replace(_clean().claim, claim_class=ClaimClass.NORMATIVE),
                scope=replace(
                    _clean().scope, transfer_limits=("context-bound",)
                ),
            ),
            NonProjectionDecision.PASS_ATTRIBUTED,
            NonProjectionReason.PASS_ATTRIBUTED,
        ),
        (
            "NPC-SC-003",
            replace(
                _clean(),
                projection_intent=replace(
                    _clean().projection_intent,
                    claimed_independent_review_count=1,
                ),
            ),
            NonProjectionDecision.REJECT,
            NonProjectionReason.CORRELATED_CONSENSUS_LAUNDERING,
        ),
        (
            "NPC-SC-007",
            replace(
                _clean(),
                source_provenance=replace(
                    _clean().source_provenance,
                    source_ref="prestigious-source",
                    source_class=SourceClass.RESEARCH_PRIMARY,
                ),
                interpretation=replace(
                    _clean().interpretation,
                    disconfirming_refs=("stronger-contrary-evidence",),
                ),
            ),
            NonProjectionDecision.PASS_ATTRIBUTED,
            NonProjectionReason.PASS_ATTRIBUTED,
        ),
        (
            "NPC-SC-008",
            replace(
                _clean(),
                source_provenance=replace(
                    _clean().source_provenance,
                    source_class=SourceClass.HISTORICAL_SECONDARY,
                ),
            ),
            NonProjectionDecision.REVISE_REQUIRED,
            NonProjectionReason.CONTEXT_SCOPE_REPAIR_REQUIRED,
        ),
        (
            "NPC-SC-011",
            replace(
                _clean(),
                source_provenance=replace(
                    _clean().source_provenance,
                    provenance_state=ProvenanceState.UNKNOWN,
                ),
            ),
            NonProjectionDecision.DEFER,
            NonProjectionReason.PROVENANCE_UNKNOWN,
        ),
        (
            "NPC-SC-CONTESTED-001",
            replace(
                _clean(),
                interpretation=replace(
                    _clean().interpretation,
                    state=InterpretationState.CONTESTED,
                    alternatives=("alt-a", "alt-b"),
                    disconfirming_refs=("counter-1",),
                ),
            ),
            NonProjectionDecision.CONTESTED,
            NonProjectionReason.INTERPRETATION_CONTESTED,
        ),
    ],
)
def test_npc_scenarios(
    scenario_id: str,
    envelope: AttributedInterpretationEnvelope,
    decision: NonProjectionDecision,
    reason: NonProjectionReason,
) -> None:
    result = classify_non_projection(envelope=envelope, budget=_budget())
    assert scenario_id.startswith("NPC-SC-")
    assert result.decision is decision
    assert result.primary_reason is reason


# NPC-M: non-escalation across prestige, context loss, self, M3 and relationship state.
def test_npc_metamorphic_non_escalation() -> None:
    base = _clean()
    baseline = classify_non_projection(envelope=base, budget=_budget())
    prestigious = replace(
        base,
        source_provenance=replace(
            base.source_provenance,
            source_ref="prestigious-source",
            source_class=SourceClass.RESEARCH_PRIMARY,
        ),
    )
    assert classify_non_projection(
        envelope=prestigious, budget=_budget()
    ).decision is NonProjectionDecision.PASS_ATTRIBUTED

    context_removed = replace(
        base,
        contextual_distance=replace(
            base.contextual_distance, historical=ContextDistanceLevel.UNKNOWN
        ),
    )
    assert classify_non_projection(
        envelope=context_removed, budget=_budget()
    ).decision is NonProjectionDecision.DEFER

    verified_self = replace(
        base,
        attribution=replace(
            base.attribution,
            subject_ref="mentaury",
            subject_relation=SubjectRelation.VERIFIED_SELF,
            self_basis_ref="caller-only-basis",
        ),
    )
    assert classify_non_projection(
        envelope=verified_self, budget=_budget()
    ).primary_reason is NonProjectionReason.SELF_BASIS_UNVERIFIED

    m3_attempt = replace(
        base,
        authority_exclusions=replace(
            base.authority_exclusions, m3_nomination_or_write=True
        ),
    )
    assert classify_non_projection(
        envelope=m3_attempt, budget=_budget()
    ).primary_reason is NonProjectionReason.IDENTITY_TRAIT_PROJECTION

    relationship_attempt = replace(
        base,
        authority_exclusions=replace(
            base.authority_exclusions, relationship_authority=True
        ),
    )
    assert classify_non_projection(
        envelope=relationship_attempt, budget=_budget()
    ).primary_reason is NonProjectionReason.RELATIONSHIP_PROJECTION
    assert classify_non_projection(envelope=base, budget=_budget()) == baseline


# NPC-PURE: AST import allowlist + runtime sentinels, without confusing required
# authority-exclusion field names (for example action_gate_authority) with calls.
def test_npc_pure_import_surface_is_allowlisted() -> None:
    source = inspect.getsource(classifier_module)
    tree = ast.parse(source)
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    assert roots <= {
        "__future__",
        "collections",
        "dataclasses",
        "enum",
        "hashlib",
        "typing",
        "mentaury",
        "contracts",
    }


def test_npc_pure_call_touches_no_ambient_io_clock_random_subprocess_or_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import builtins
    import random
    import socket
    import subprocess
    import time

    def bomb(*_args: object, **_kwargs: object):
        raise AssertionError("ambient authority surface touched")

    monkeypatch.setattr(builtins, "open", bomb)
    monkeypatch.setattr(socket, "socket", bomb)
    monkeypatch.setattr(subprocess, "run", bomb)
    monkeypatch.setattr(subprocess, "Popen", bomb)
    monkeypatch.setattr(time, "time", bomb)
    monkeypatch.setattr(random, "random", bomb)
    monkeypatch.setattr(os, "getenv", bomb)

    result = classify_non_projection(envelope=_clean(), budget=_budget())
    assert result.decision is NonProjectionDecision.PASS_ATTRIBUTED
    assert result.input_fingerprint == EXPECTED_CLEAN_FINGERPRINT


def test_npc_pure_result_exposes_no_reusable_authority_handle() -> None:
    value = classify_non_projection(envelope=_clean(), budget=_budget()).to_value()
    assert set(value) == {
        "decision",
        "primary_reason",
        "reasons",
        "triggered_threat_ids",
        "effective_independent_review_count",
        "input_fingerprint",
        "contract_version",
        "envelope_version",
        "canonical_profile",
        "source_provenance_scope",
    }
