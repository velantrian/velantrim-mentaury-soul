"""Adversarial conformance evidence for every frozen NPG-v0.1 obligation family."""

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
    NonProjectionThreatId,
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
    values = {
        "max_string_bytes": 4096,
        "max_tuple_items": 512,
        "max_review_records": 64,
        "max_canonical_input_bytes": 262144,
    }
    values.update(changes)
    return NonProjectionBudget(**values)


def _clean(**changes: object) -> AttributedInterpretationEnvelope:
    values = {
        "envelope_version": "AIE-v0.1",
        "source_provenance": SourceProvenance(
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
        "attribution": Attribution(
            "creator-1", "creator-1", SubjectRelation.NON_SELF, None, ("basis-1",)
        ),
        "claim": Claim(
            "claim-1",
            ClaimClass.AUTOBIOGRAPHICAL_TESTIMONY,
            "statement-1",
            True,
        ),
        "interpretation": Interpretation(
            "interpretation-1",
            "reviewer-1",
            InterpretationState.SUPPORTED,
            (),
            (),
        ),
        "contextual_distance": ContextualDistance(
            ContextDistanceLevel.SAME_CONTEXT,
            ContextDistanceLevel.SAME_CONTEXT,
            ContextDistanceLevel.SAME_CONTEXT,
            ContextDistanceLevel.SAME_CONTEXT,
            ContextDistanceLevel.SAME_CONTEXT,
            AnachronismRisk.LOW,
        ),
        "review_provenance": ReviewProvenance(()),
        "scope": ScopeBoundary(
            ("wisdom",), ("wisdom",), ("identity",), (), ()
        ),
        "authority_exclusions": AuthorityExclusions(
            False, False, False, False, False, False, False, False, False
        ),
        "projection_intent": ProjectionIntent(
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
    }
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


def _rank(decision: NonProjectionDecision) -> int:
    return {
        NonProjectionDecision.PASS_ATTRIBUTED: 0,
        NonProjectionDecision.REVISE_REQUIRED: 1,
        NonProjectionDecision.CONTESTED: 2,
        NonProjectionDecision.DEFER: 3,
        NonProjectionDecision.REJECT: 4,
    }[decision]


# NPC-CTX-003…013, 016…017, 019…022: exact admission, hard caps, and no repair.
def test_npc_ctx_hard_string_cap_is_contract_error() -> None:
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


def test_npc_ctx_hard_tuple_cap_is_contract_error() -> None:
    items = tuple(f"item-{index:04d}" for index in range(513))
    with pytest.raises(NonProjectionContractError):
        ScopeBoundary(items, (), (), (), ())


def test_npc_ctx_review_order_uniqueness_and_hard_cap_are_strict() -> None:
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
            f"review-{index:03d}",
            f"reviewer-{index:03d}",
            ReviewerIndependence.DERIVED,
            None,
            None,
            None,
            False,
        )
        for index in range(65)
    )
    with pytest.raises(NonProjectionContractError):
        ReviewProvenance(too_many)


def test_npc_ctx_nested_types_bool_and_count_are_exact() -> None:
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
        Claim("c", ClaimClass.FACTUAL, "s", 1)  # type: ignore[arg-type]
    with pytest.raises(NonProjectionContractError):
        replace(base.projection_intent, claimed_independent_review_count=True)


def test_npc_ctx_api_rejects_every_forbidden_extra_input_family() -> None:
    forbidden = (
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
    )
    for name in forbidden:
        with pytest.raises(TypeError):
            classify_non_projection(
                envelope=_clean(), budget=_budget(), **{name: object()}  # type: ignore[arg-type]
            )


def test_npc_ctx_no_hidden_trim_sort_or_alias_repair() -> None:
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
        ScopeBoundary(("z", "a"), (), (), (), ())
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


def test_npc_ctx_hard_canonical_input_cap_is_contract_error() -> None:
    large_sorted = tuple(
        f"{index:04d}-" + ("x" * 600) for index in range(512)
    )
    base = _clean()
    source = replace(base.source_provenance, material_gaps=large_sorted)
    with pytest.raises(NonProjectionContractError):
        classify_non_projection(envelope=replace(base, source_provenance=source), budget=_budget())


# NPC-FP-001…008: exact canonical projection and fingerprint evidence.
def test_npc_fp_exact_canonical_input_fixture() -> None:
    envelope = _clean()
    budget = _budget()
    expected = {
        "domain": "MENTAURY_NPG_INPUT_V1",
        "non_projection_contract_version": "NPG-v0.1",
        "envelope_version": "AIE-v0.1",
        "canonical_profile": "MENTAURY_CANONICAL_JSON_V1",
        "source_provenance_scope": "CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY",
        "envelope": {
            "envelope_version": "AIE-v0.1",
            "source_provenance": {
                "source_ref": "source-1",
                "source_actor_ref": "creator-1",
                "source_class": "CREATOR_TESTIMONY",
                "source_origin": "PRIMARY",
                "provenance_state": "VERIFIED",
                "publication_or_capture_context_ref": "capture-1",
                "sensitivity": "NORMAL",
                "usage_boundary_ref": "usage-1",
                "material_gaps": [],
            },
            "attribution": {
                "speaker_ref": "creator-1",
                "subject_ref": "creator-1",
                "subject_relation": "NON_SELF",
                "self_basis_ref": None,
                "attribution_basis_refs": ["basis-1"],
            },
            "claim": {
                "claim_id": "claim-1",
                "claim_class": "AUTOBIOGRAPHICAL_TESTIMONY",
                "statement_ref": "statement-1",
                "directly_stated": True,
            },
            "interpretation": {
                "interpretation_ref": "interpretation-1",
                "interpreter_ref": "reviewer-1",
                "state": "SUPPORTED",
                "alternatives": [],
                "disconfirming_refs": [],
            },
            "contextual_distance": {
                "historical": "SAME_CONTEXT",
                "cultural": "SAME_CONTEXT",
                "terminology": "SAME_CONTEXT",
                "translation_or_paraphrase": "SAME_CONTEXT",
                "source_distance": "SAME_CONTEXT",
                "anachronism_risk": "LOW",
            },
            "review_provenance": {"reviews": []},
            "scope": {
                "applies_to": ["wisdom"],
                "may_support": ["wisdom"],
                "does_not_establish": ["identity"],
                "unknowns": [],
                "transfer_limits": [],
            },
            "authority_exclusions": {
                "factual_truth_proof": False,
                "identity_authority": False,
                "relationship_authority": False,
                "consent_authority": False,
                "capability_authority": False,
                "action_gate_authority": False,
                "retrieval_authority": False,
                "tool_execution_authority": False,
                "m3_nomination_or_write": False,
            },
            "projection_intent": {
                "proposed_applies_to": ["wisdom"],
                "adopt_as_self_experience": False,
                "inherit_source_authority": False,
                "assert_as_objective_truth": False,
                "adopt_source_emotion_as_drive": False,
                "style_changes_evidence_status": False,
                "generalize_beyond_scope": False,
                "claimed_independent_review_count": 0,
                "discard_relevant_context": False,
                "inherit_relationship_or_commitment": False,
                "promote_to_stable_identity_trait": False,
                "present_interpretation_as_direct_testimony": False,
                "inherit_consent": False,
            },
        },
        "budget": {
            "max_string_bytes": 4096,
            "max_tuple_items": 512,
            "max_review_records": 64,
            "max_canonical_input_bytes": 262144,
        },
    }
    assert _canonical_input(envelope, budget) == expected
    assert len(canonical_json_bytes(expected)) == 2261


def test_npc_fp_exact_sha256_fixture_and_repeatability() -> None:
    first = classify_non_projection(envelope=_clean(), budget=_budget())
    second = classify_non_projection(envelope=_clean(), budget=_budget())
    assert first.input_fingerprint == EXPECTED_CLEAN_FINGERPRINT
    assert second.input_fingerprint == EXPECTED_CLEAN_FINGERPRINT
    assert first == second


def test_npc_fp_relevant_envelope_and_budget_mutations_change_fingerprint() -> None:
    base = _clean()
    original = classify_non_projection(envelope=base, budget=_budget())
    changed_claim = replace(base, claim=replace(base.claim, statement_ref="statement-2"))
    changed_budget = _budget(max_tuple_items=511)
    assert classify_non_projection(envelope=changed_claim, budget=_budget()).input_fingerprint != original.input_fingerprint
    assert classify_non_projection(envelope=base, budget=changed_budget).input_fingerprint != original.input_fingerprint


def test_npc_fp_ambient_environment_does_not_change_fingerprint(monkeypatch: pytest.MonkeyPatch) -> None:
    first = classify_non_projection(envelope=_clean(), budget=_budget())
    monkeypatch.setenv("MENTAURY_NPG_UNRELATED", "different-runtime-state")
    second = classify_non_projection(envelope=_clean(), budget=_budget())
    assert first.input_fingerprint == second.input_fingerprint == EXPECTED_CLEAN_FINGERPRINT


def test_npc_fp_canonicalization_failure_never_maps_positive(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(_value: object) -> bytes:
        raise CanonicalJSONError("forced canonical failure")

    monkeypatch.setattr(classifier_module.canonical_json_contract, "canonical_json_bytes", fail)
    result = classify_non_projection(envelope=_clean(), budget=_budget())
    assert result.decision is NonProjectionDecision.DEFER
    assert result.primary_reason is NonProjectionReason.CANONICALIZATION_FAILED
    assert result.input_fingerprint is None


def test_npc_fp_profile_mismatch_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(classifier_module.canonical_json_contract, "PROFILE_NAME", "OTHER_PROFILE")
    result = classify_non_projection(envelope=_clean(), budget=_budget())
    assert result.decision is NonProjectionDecision.DEFER
    assert result.primary_reason is NonProjectionReason.CANONICALIZATION_FAILED


# NPC-DEC-003…006, 014, 016: complete precedence and local-budget behavior.
def test_npc_dec_defer_dominates_contested() -> None:
    base = _clean()
    source = replace(base.source_provenance, provenance_state=ProvenanceState.CONFLICTING)
    context = replace(base.contextual_distance, historical=ContextDistanceLevel.UNKNOWN)
    result = classify_non_projection(
        envelope=replace(base, source_provenance=source, contextual_distance=context),
        budget=_budget(),
    )
    assert result.decision is NonProjectionDecision.DEFER
    assert result.primary_reason is NonProjectionReason.CONTEXT_UNKNOWN
    assert NonProjectionReason.PROVENANCE_CONFLICTING in result.reasons


def test_npc_dec_contested_dominates_revise() -> None:
    base = _clean()
    source = replace(base.source_provenance, source_actor_ref=None)
    interpretation = replace(
        base.interpretation,
        state=InterpretationState.CONTESTED,
        alternatives=("alt-a", "alt-b"),
        disconfirming_refs=("counter-1",),
    )
    result = classify_non_projection(
        envelope=replace(base, source_provenance=source, interpretation=interpretation),
        budget=_budget(),
    )
    assert result.decision is NonProjectionDecision.CONTESTED
    assert result.primary_reason is NonProjectionReason.INTERPRETATION_CONTESTED
    assert NonProjectionReason.ATTRIBUTION_REPAIR_REQUIRED in result.reasons


def test_npc_dec_all_local_budget_dimensions_defer_without_repair() -> None:
    base = _clean()
    two_refs = replace(base.attribution, attribution_basis_refs=("basis-1", "basis-2"))
    assert classify_non_projection(envelope=replace(base, attribution=two_refs), budget=_budget(max_tuple_items=1)).primary_reason is NonProjectionReason.BUDGET_EXHAUSTED
    assert classify_non_projection(envelope=base, budget=_budget(max_string_bytes=4)).primary_reason is NonProjectionReason.BUDGET_EXHAUSTED
    assert classify_non_projection(envelope=base, budget=_budget(max_canonical_input_bytes=100)).primary_reason is NonProjectionReason.BUDGET_EXHAUSTED

    r1 = ReviewRecord("review-1", "reviewer-1", ReviewerIndependence.DERIVED, None, None, None, False)
    r2 = ReviewRecord("review-2", "reviewer-2", ReviewerIndependence.DERIVED, None, None, None, False)
    with_reviews = replace(base, review_provenance=ReviewProvenance((r1, r2)))
    assert classify_non_projection(envelope=with_reviews, budget=_budget(max_review_records=1)).primary_reason is NonProjectionReason.BUDGET_EXHAUSTED


def test_npc_dec_reason_and_threat_order_are_repeatable() -> None:
    base = _clean()
    intent = replace(
        base.projection_intent,
        adopt_as_self_experience=True,
        assert_as_objective_truth=True,
        inherit_consent=True,
    )
    envelope = replace(base, projection_intent=intent)
    first = classify_non_projection(envelope=envelope, budget=_budget())
    second = classify_non_projection(envelope=envelope, budget=_budget())
    assert first == second
    assert first.triggered_threat_ids == (
        NonProjectionThreatId.NPG_T01,
        NonProjectionThreatId.NPG_T03,
        NonProjectionThreatId.NPG_T12,
    )


# NPC-SC-001…012 + contested: frozen readiness outcomes as concrete fixtures.
@pytest.mark.parametrize(
    ("scenario_id", "envelope", "decision", "reason"),
    [
        ("NPC-SC-001", _clean(), NonProjectionDecision.PASS_ATTRIBUTED, NonProjectionReason.PASS_ATTRIBUTED),
        (
            "NPC-SC-002",
            replace(
                _clean(),
                source_provenance=replace(_clean().source_provenance, source_class=SourceClass.HISTORICAL_PRIMARY),
                claim=replace(_clean().claim, claim_class=ClaimClass.NORMATIVE),
                scope=replace(_clean().scope, transfer_limits=("context-bound",)),
            ),
            NonProjectionDecision.PASS_ATTRIBUTED,
            NonProjectionReason.PASS_ATTRIBUTED,
        ),
        (
            "NPC-SC-003",
            replace(_clean(), projection_intent=replace(_clean().projection_intent, claimed_independent_review_count=1)),
            NonProjectionDecision.REJECT,
            NonProjectionReason.CORRELATED_CONSENSUS_LAUNDERING,
        ),
        (
            "NPC-SC-004",
            replace(
                _clean(),
                source_provenance=replace(_clean().source_provenance, source_class=SourceClass.LITERARY_OR_METAPHORICAL),
                claim=replace(_clean().claim, claim_class=ClaimClass.METAPHORICAL),
                projection_intent=replace(_clean().projection_intent, assert_as_objective_truth=True),
            ),
            NonProjectionDecision.REJECT,
            NonProjectionReason.TRUTH_ESCALATION,
        ),
        (
            "NPC-SC-005",
            replace(_clean(), projection_intent=replace(_clean().projection_intent, adopt_source_emotion_as_drive=True)),
            NonProjectionDecision.REJECT,
            NonProjectionReason.EMOTION_TO_DRIVE_PROJECTION,
        ),
        (
            "NPC-SC-006",
            replace(_clean(), projection_intent=replace(_clean().projection_intent, adopt_as_self_experience=True)),
            NonProjectionDecision.REJECT,
            NonProjectionReason.AUTOBIOGRAPHY_LAUNDERING,
        ),
        (
            "NPC-SC-007",
            replace(
                _clean(),
                source_provenance=replace(_clean().source_provenance, source_class=SourceClass.RESEARCH_PRIMARY, source_ref="prestigious-source"),
                interpretation=replace(_clean().interpretation, disconfirming_refs=("stronger-contrary-evidence",)),
            ),
            NonProjectionDecision.PASS_ATTRIBUTED,
            NonProjectionReason.PASS_ATTRIBUTED,
        ),
        (
            "NPC-SC-008",
            replace(_clean(), source_provenance=replace(_clean().source_provenance, source_class=SourceClass.HISTORICAL_SECONDARY)),
            NonProjectionDecision.REVISE_REQUIRED,
            NonProjectionReason.CONTEXT_SCOPE_REPAIR_REQUIRED,
        ),
        (
            "NPC-SC-009",
            replace(_clean(), projection_intent=replace(_clean().projection_intent, inherit_relationship_or_commitment=True)),
            NonProjectionDecision.REJECT,
            NonProjectionReason.RELATIONSHIP_PROJECTION,
        ),
        (
            "NPC-SC-010",
            replace(_clean(), projection_intent=replace(_clean().projection_intent, style_changes_evidence_status=True)),
            NonProjectionDecision.REJECT,
            NonProjectionReason.STYLE_TO_BELIEF_PROJECTION,
        ),
        (
            "NPC-SC-011",
            replace(_clean(), source_provenance=replace(_clean().source_provenance, provenance_state=ProvenanceState.UNKNOWN)),
            NonProjectionDecision.DEFER,
            NonProjectionReason.PROVENANCE_UNKNOWN,
        ),
        (
            "NPC-SC-012",
            replace(_clean(), authority_exclusions=replace(_clean().authority_exclusions, action_gate_authority=True)),
            NonProjectionDecision.REJECT,
            NonProjectionReason.AUTHORITY_INHERITANCE,
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
    ids=[f"NPC-SC-{index:03d}" for index in range(1, 13)] + ["NPC-SC-CONTESTED-001"],
)
def test_frozen_scenarios(
    scenario_id: str,
    envelope: AttributedInterpretationEnvelope,
    decision: NonProjectionDecision,
    reason: NonProjectionReason,
) -> None:
    result = classify_non_projection(envelope=envelope, budget=_budget())
    assert scenario_id.startswith("NPC-SC-")
    assert result.decision is decision
    assert result.primary_reason is reason


# NPC-M-001…008: non-escalation and determinism.
def test_npc_m_001_attribution_survives_interpretation_presentation_change() -> None:
    base = _clean()
    changed = replace(base, interpretation=replace(base.interpretation, interpretation_ref="presentation-variant"))
    assert changed.attribution == base.attribution
    assert classify_non_projection(envelope=changed, budget=_budget()).decision is NonProjectionDecision.PASS_ATTRIBUTED


def test_npc_m_002_prestige_cannot_escalate_authority() -> None:
    base = _clean()
    prestigious = replace(base, source_provenance=replace(base.source_provenance, source_ref="prestigious-source", source_class=SourceClass.RESEARCH_PRIMARY))
    result = classify_non_projection(envelope=prestigious, budget=_budget())
    assert result.decision is NonProjectionDecision.PASS_ATTRIBUTED
    assert result.triggered_threat_ids == ()


def test_npc_m_003_repetition_or_correlation_cannot_create_independence() -> None:
    base = _clean()
    r1 = ReviewRecord("review-1", "reviewer-1", ReviewerIndependence.INDEPENDENT, "provider-1", "prompt-1", "context-1", False)
    r2 = ReviewRecord("review-2", "reviewer-2", ReviewerIndependence.INDEPENDENT, "provider-1", "prompt-2", "context-2", False)
    intent = replace(base.projection_intent, claimed_independent_review_count=1)
    result = classify_non_projection(envelope=replace(base, review_provenance=ReviewProvenance((r1, r2)), projection_intent=intent), budget=_budget())
    assert result.effective_independent_review_count == 0
    assert result.primary_reason is NonProjectionReason.CORRELATED_CONSENSUS_LAUNDERING


def test_npc_m_004_removing_context_cannot_make_result_more_permissive() -> None:
    base_result = classify_non_projection(envelope=_clean(), budget=_budget())
    base = _clean()
    degraded = replace(base, contextual_distance=replace(base.contextual_distance, historical=ContextDistanceLevel.UNKNOWN))
    degraded_result = classify_non_projection(envelope=degraded, budget=_budget())
    assert _rank(degraded_result.decision) >= _rank(base_result.decision)


def test_npc_m_005_self_substitution_requires_fail_closed_new_evaluation() -> None:
    base = _clean()
    self_attribution = replace(base.attribution, subject_ref="mentaury", subject_relation=SubjectRelation.VERIFIED_SELF, self_basis_ref="unbound-self-basis")
    result = classify_non_projection(envelope=replace(base, attribution=self_attribution), budget=_budget())
    assert result.decision is NonProjectionDecision.DEFER
    assert result.primary_reason is NonProjectionReason.SELF_BASIS_UNVERIFIED


def test_npc_m_006_no_m3_amplification() -> None:
    base = _clean()
    result = classify_non_projection(envelope=replace(base, authority_exclusions=replace(base.authority_exclusions, m3_nomination_or_write=True)), budget=_budget())
    assert result.decision is NonProjectionDecision.REJECT
    assert result.primary_reason is NonProjectionReason.IDENTITY_TRAIT_PROJECTION


def test_npc_m_007_no_relationship_amplification() -> None:
    base = _clean()
    result = classify_non_projection(envelope=replace(base, authority_exclusions=replace(base.authority_exclusions, relationship_authority=True)), budget=_budget())
    assert result.decision is NonProjectionDecision.REJECT
    assert result.primary_reason is NonProjectionReason.RELATIONSHIP_PROJECTION


def test_npc_m_008_exact_repeat_is_deterministic() -> None:
    first = classify_non_projection(envelope=_clean(), budget=_budget())
    second = classify_non_projection(envelope=_clean(), budget=_budget())
    assert first == second


# NPC-PURE-001…010: imports and call path carry no ambient authority surface.
def test_npc_pure_import_surface_is_bounded_to_stdlib_internal_contract_and_canonical_json() -> None:
    source = inspect.getsource(classifier_module)
    tree = ast.parse(source)
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])
    assert imported_roots <= {
        "__future__",
        "collections",
        "dataclasses",
        "enum",
        "hashlib",
        "typing",
        "mentaury",
        "contracts",
    }
    forbidden_tokens = (
        "socket",
        "requests",
        "urllib",
        "sqlite",
        "subprocess",
        "pathlib",
        "os.environ",
        "getenv",
        "time.time",
        "datetime.now",
        "random",
        "model_client",
        "llm",
        "retriever",
        "atlas",
        "identity_registry",
        "relationship_registry",
        "action_gate",
        "plugin",
    )
    lowered = source.lower()
    assert all(token.lower() not in lowered for token in forbidden_tokens)


def test_npc_pure_call_does_not_use_ambient_filesystem_network_subprocess_clock_random_or_env(
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


def test_npc_pure_result_contains_no_authority_or_mutation_handle() -> None:
    result = classify_non_projection(envelope=_clean(), budget=_budget())
    value = result.to_value()
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
    rendered = repr(value).lower()
    for forbidden in (
        "capability_lease",
        "tool_handle",
        "mutation_command",
        "storage_locator",
        "identity_proof",
        "relationship_state",
        "deployment",
    ):
        assert forbidden not in rendered
