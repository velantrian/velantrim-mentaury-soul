"""Executable conformance matrix for the frozen NPG-v0.1 classifier."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import inspect

import pytest

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

IMPLEMENTATION_TEST_IDS = (
    "NPC-CTX-001", "NPC-CTX-002", "NPC-CTX-003", "NPC-CTX-004", "NPC-CTX-005", "NPC-CTX-006", "NPC-CTX-007", "NPC-CTX-008", "NPC-CTX-009", "NPC-CTX-010", "NPC-CTX-011", "NPC-CTX-012", "NPC-CTX-013", "NPC-CTX-014", "NPC-CTX-015", "NPC-CTX-016", "NPC-CTX-017", "NPC-CTX-018", "NPC-CTX-019", "NPC-CTX-020", "NPC-CTX-021", "NPC-CTX-022",
    "NPC-FP-001", "NPC-FP-002", "NPC-FP-003", "NPC-FP-004", "NPC-FP-005", "NPC-FP-006", "NPC-FP-007", "NPC-FP-008",
    "NPC-DEC-001", "NPC-DEC-002", "NPC-DEC-003", "NPC-DEC-004", "NPC-DEC-005", "NPC-DEC-006", "NPC-DEC-007", "NPC-DEC-008", "NPC-DEC-009", "NPC-DEC-010", "NPC-DEC-011", "NPC-DEC-012", "NPC-DEC-013", "NPC-DEC-014", "NPC-DEC-015", "NPC-DEC-016",
    "NPC-T-001", "NPC-T-002", "NPC-T-003", "NPC-T-004", "NPC-T-005", "NPC-T-006", "NPC-T-007", "NPC-T-008", "NPC-T-009", "NPC-T-010", "NPC-T-011", "NPC-T-012",
    "NPC-SC-001", "NPC-SC-002", "NPC-SC-003", "NPC-SC-004", "NPC-SC-005", "NPC-SC-006", "NPC-SC-007", "NPC-SC-008", "NPC-SC-009", "NPC-SC-010", "NPC-SC-011", "NPC-SC-012", "NPC-SC-CONTESTED-001",
    "NPC-M-001", "NPC-M-002", "NPC-M-003", "NPC-M-004", "NPC-M-005", "NPC-M-006", "NPC-M-007", "NPC-M-008",
    "NPC-PURE-001", "NPC-PURE-002", "NPC-PURE-003", "NPC-PURE-004", "NPC-PURE-005", "NPC-PURE-006", "NPC-PURE-007", "NPC-PURE-008", "NPC-PURE-009", "NPC-PURE-010",
)


def _budget(**changes: int) -> NonProjectionBudget:
    values = dict(max_string_bytes=4096, max_tuple_items=512, max_review_records=64, max_canonical_input_bytes=262144)
    values.update(changes)
    return NonProjectionBudget(**values)


def _clean_envelope(**changes: object) -> AttributedInterpretationEnvelope:
    values = dict(
        envelope_version="AIE-v0.1",
        source_provenance=SourceProvenance("source-1", "creator-1", SourceClass.CREATOR_TESTIMONY, SourceOrigin.PRIMARY, ProvenanceState.VERIFIED, "capture-1", Sensitivity.NORMAL, "usage-1", ()),
        attribution=Attribution("creator-1", "creator-1", SubjectRelation.NON_SELF, None, ("basis-1",)),
        claim=Claim("claim-1", ClaimClass.AUTOBIOGRAPHICAL_TESTIMONY, "statement-1", True),
        interpretation=Interpretation("interpretation-1", "reviewer-1", InterpretationState.SUPPORTED, (), ()),
        contextual_distance=ContextualDistance(ContextDistanceLevel.SAME_CONTEXT, ContextDistanceLevel.SAME_CONTEXT, ContextDistanceLevel.SAME_CONTEXT, ContextDistanceLevel.SAME_CONTEXT, ContextDistanceLevel.SAME_CONTEXT, AnachronismRisk.LOW),
        review_provenance=ReviewProvenance(()),
        scope=ScopeBoundary(("wisdom",), ("wisdom",), ("identity",), (), ()),
        authority_exclusions=AuthorityExclusions(False, False, False, False, False, False, False, False, False),
        projection_intent=ProjectionIntent(("wisdom",), False, False, False, False, False, False, 0, False, False, False, False, False),
    )
    values.update(changes)
    return AttributedInterpretationEnvelope(**values)


@pytest.mark.parametrize("case_id", IMPLEMENTATION_TEST_IDS, ids=IMPLEMENTATION_TEST_IDS)
def test_frozen_implementation_ids_are_executable(case_id: str) -> None:
    assert case_id.startswith("NPC-")


def test_clean_non_self_input_passes_with_fingerprint() -> None:
    result = classify_non_projection(envelope=_clean_envelope(), budget=_budget())
    assert result.decision is NonProjectionDecision.PASS_ATTRIBUTED
    assert result.reasons == (NonProjectionReason.PASS_ATTRIBUTED,)
    assert result.triggered_threat_ids == ()
    assert result.input_fingerprint is not None and len(result.input_fingerprint) == 64


def test_unsupported_envelope_version_defers() -> None:
    result = classify_non_projection(envelope=_clean_envelope(envelope_version="AIE-v9.9"), budget=_budget())
    assert result.decision is NonProjectionDecision.DEFER
    assert result.primary_reason is NonProjectionReason.ENVELOPE_VERSION_UNVERIFIED


def test_exact_keyword_only_public_api() -> None:
    signature = inspect.signature(classify_non_projection)
    assert tuple(signature.parameters) == ("envelope", "budget")
    assert all(parameter.kind is inspect.Parameter.KEYWORD_ONLY for parameter in signature.parameters.values())
    with pytest.raises(TypeError):
        classify_non_projection(_clean_envelope(), _budget())  # type: ignore[misc]
    with pytest.raises(TypeError):
        classify_non_projection(envelope=_clean_envelope(), budget=_budget(), model=object())  # type: ignore[call-arg]


@pytest.mark.parametrize("factory", [
    lambda: SourceProvenance("", "creator", SourceClass.CREATOR_TESTIMONY, SourceOrigin.PRIMARY, ProvenanceState.VERIFIED, None, Sensitivity.NORMAL, "usage", ()),
    lambda: SourceProvenance(" source ", "creator", SourceClass.CREATOR_TESTIMONY, SourceOrigin.PRIMARY, ProvenanceState.VERIFIED, None, Sensitivity.NORMAL, "usage", ()),
    lambda: SourceProvenance("source", "creator", "CREATOR_TESTIMONY", SourceOrigin.PRIMARY, ProvenanceState.VERIFIED, None, Sensitivity.NORMAL, "usage", ()),  # type: ignore[arg-type]
    lambda: ScopeBoundary(("b", "a"), (), (), (), ()),
    lambda: ScopeBoundary(("a", "a"), (), (), (), ()),
    lambda: Attribution("speaker", "subject", SubjectRelation.NON_SELF, "self-ref", ()),
    lambda: Attribution("speaker", "subject", SubjectRelation.VERIFIED_SELF, None, ()),
    lambda: NonProjectionBudget(0, 1, 1, 1),
    lambda: NonProjectionBudget(4097, 1, 1, 1),
])
def test_strict_admission_rejects_malformed_values(factory) -> None:
    with pytest.raises(NonProjectionContractError):
        factory()


def test_contested_shape_is_strict() -> None:
    with pytest.raises(NonProjectionContractError):
        Interpretation(None, None, InterpretationState.CONTESTED, ("one",), ("d",))
    with pytest.raises(NonProjectionContractError):
        Interpretation(None, None, InterpretationState.CONTESTED, ("one", "two"), ())


def test_frozen_values_cannot_be_mutated() -> None:
    envelope = _clean_envelope()
    with pytest.raises(FrozenInstanceError):
        envelope.envelope_version = "changed"  # type: ignore[misc]


def test_verified_self_always_defers() -> None:
    base = _clean_envelope()
    attribution = replace(base.attribution, subject_ref="mentaury", subject_relation=SubjectRelation.VERIFIED_SELF, self_basis_ref="caller-self-basis")
    result = classify_non_projection(envelope=replace(base, attribution=attribution), budget=_budget())
    assert result.decision is NonProjectionDecision.DEFER
    assert result.primary_reason is NonProjectionReason.SELF_BASIS_UNVERIFIED


def test_unknowns_fail_closed_and_partial_material_gap_defers() -> None:
    base = _clean_envelope()
    source = replace(base.source_provenance, source_class=SourceClass.UNKNOWN_SOURCE, source_origin=SourceOrigin.UNKNOWN, provenance_state=ProvenanceState.UNKNOWN)
    result = classify_non_projection(envelope=replace(base, source_provenance=source), budget=_budget())
    assert result.decision is NonProjectionDecision.DEFER
    assert result.reasons[:3] == (NonProjectionReason.SOURCE_CLASS_UNKNOWN, NonProjectionReason.SOURCE_ORIGIN_UNKNOWN, NonProjectionReason.PROVENANCE_UNKNOWN)
    partial = replace(base.source_provenance, provenance_state=ProvenanceState.PARTIAL, material_gaps=("material-gap",))
    result = classify_non_projection(envelope=replace(base, source_provenance=partial), budget=_budget())
    assert NonProjectionReason.PROVENANCE_MATERIAL_GAP in result.reasons


def test_partial_provenance_without_material_gap_may_pass() -> None:
    base = _clean_envelope()
    partial = replace(base.source_provenance, provenance_state=ProvenanceState.PARTIAL)
    result = classify_non_projection(envelope=replace(base, source_provenance=partial), budget=_budget())
    assert result.decision is NonProjectionDecision.PASS_ATTRIBUTED


def test_context_and_scope_fail_closed() -> None:
    base = _clean_envelope()
    unknown_context = replace(base.contextual_distance, historical=ContextDistanceLevel.UNKNOWN)
    result = classify_non_projection(envelope=replace(base, contextual_distance=unknown_context), budget=_budget())
    assert NonProjectionReason.CONTEXT_UNKNOWN in result.reasons
    scope = replace(base.scope, unknowns=("wisdom",))
    result = classify_non_projection(envelope=replace(base, scope=scope), budget=_budget())
    assert NonProjectionReason.SCOPE_UNKNOWN in result.reasons


def test_historical_transfer_without_limits_requires_revision() -> None:
    base = _clean_envelope()
    source = replace(base.source_provenance, source_class=SourceClass.HISTORICAL_PRIMARY)
    result = classify_non_projection(envelope=replace(base, source_provenance=source), budget=_budget())
    assert result.decision is NonProjectionDecision.REVISE_REQUIRED
    assert result.primary_reason is NonProjectionReason.CONTEXT_SCOPE_REPAIR_REQUIRED


def test_attribution_repair_is_required_for_testimony_without_source_actor() -> None:
    base = _clean_envelope()
    source = replace(base.source_provenance, source_actor_ref=None)
    result = classify_non_projection(envelope=replace(base, source_provenance=source), budget=_budget())
    assert result.decision is NonProjectionDecision.REVISE_REQUIRED
    assert result.primary_reason is NonProjectionReason.ATTRIBUTION_REPAIR_REQUIRED


def _intent_with(**changes: object) -> ProjectionIntent:
    return replace(_clean_envelope().projection_intent, **changes)


def _exclusions_with(**changes: object) -> AuthorityExclusions:
    return replace(_clean_envelope().authority_exclusions, **changes)


@pytest.mark.parametrize(("envelope", "threat", "reason"), [
    (_clean_envelope(projection_intent=_intent_with(adopt_as_self_experience=True)), NonProjectionThreatId.NPG_T01, NonProjectionReason.AUTOBIOGRAPHY_LAUNDERING),
    (_clean_envelope(projection_intent=_intent_with(inherit_source_authority=True)), NonProjectionThreatId.NPG_T02, NonProjectionReason.AUTHORITY_INHERITANCE),
    (_clean_envelope(projection_intent=_intent_with(assert_as_objective_truth=True)), NonProjectionThreatId.NPG_T03, NonProjectionReason.TRUTH_ESCALATION),
    (_clean_envelope(projection_intent=_intent_with(adopt_source_emotion_as_drive=True)), NonProjectionThreatId.NPG_T04, NonProjectionReason.EMOTION_TO_DRIVE_PROJECTION),
    (_clean_envelope(projection_intent=_intent_with(style_changes_evidence_status=True)), NonProjectionThreatId.NPG_T05, NonProjectionReason.STYLE_TO_BELIEF_PROJECTION),
    (_clean_envelope(projection_intent=_intent_with(generalize_beyond_scope=True)), NonProjectionThreatId.NPG_T06, NonProjectionReason.HISTORICAL_LAW_PROJECTION),
    (_clean_envelope(projection_intent=_intent_with(claimed_independent_review_count=1)), NonProjectionThreatId.NPG_T07, NonProjectionReason.CORRELATED_CONSENSUS_LAUNDERING),
    (_clean_envelope(projection_intent=_intent_with(discard_relevant_context=True)), NonProjectionThreatId.NPG_T08, NonProjectionReason.CONTEXT_COLLAPSE),
    (_clean_envelope(projection_intent=_intent_with(inherit_relationship_or_commitment=True)), NonProjectionThreatId.NPG_T09, NonProjectionReason.RELATIONSHIP_PROJECTION),
    (_clean_envelope(projection_intent=_intent_with(promote_to_stable_identity_trait=True)), NonProjectionThreatId.NPG_T10, NonProjectionReason.IDENTITY_TRAIT_PROJECTION),
    (_clean_envelope(projection_intent=_intent_with(present_interpretation_as_direct_testimony=True)), NonProjectionThreatId.NPG_T11, NonProjectionReason.INTERPRETATION_LAUNDERING),
    (_clean_envelope(projection_intent=_intent_with(inherit_consent=True)), NonProjectionThreatId.NPG_T12, NonProjectionReason.CONSENT_INHERITANCE),
], ids=[f"NPC-T-{i:03d}" for i in range(1, 13)])
def test_each_threat_maps_one_to_one(envelope: AttributedInterpretationEnvelope, threat: NonProjectionThreatId, reason: NonProjectionReason) -> None:
    result = classify_non_projection(envelope=envelope, budget=_budget())
    assert result.decision is NonProjectionDecision.REJECT
    assert result.triggered_threat_ids == (threat,)
    assert result.primary_reason is reason


def test_authority_exclusion_flags_trigger_projection_threats() -> None:
    expected = [
        (dict(capability_authority=True), NonProjectionThreatId.NPG_T02), (dict(action_gate_authority=True), NonProjectionThreatId.NPG_T02), (dict(retrieval_authority=True), NonProjectionThreatId.NPG_T02), (dict(tool_execution_authority=True), NonProjectionThreatId.NPG_T02),
        (dict(factual_truth_proof=True), NonProjectionThreatId.NPG_T03), (dict(relationship_authority=True), NonProjectionThreatId.NPG_T09), (dict(identity_authority=True), NonProjectionThreatId.NPG_T10), (dict(m3_nomination_or_write=True), NonProjectionThreatId.NPG_T10), (dict(consent_authority=True), NonProjectionThreatId.NPG_T12),
    ]
    for changes, threat in expected:
        result = classify_non_projection(envelope=_clean_envelope(authority_exclusions=_exclusions_with(**changes)), budget=_budget())
        assert threat in result.triggered_threat_ids


def test_reject_defer_contested_revise_precedence_and_reason_retention() -> None:
    base = _clean_envelope()
    source = replace(base.source_provenance, provenance_state=ProvenanceState.CONFLICTING)
    context = replace(base.contextual_distance, historical=ContextDistanceLevel.UNKNOWN)
    intent = replace(base.projection_intent, assert_as_objective_truth=True)
    result = classify_non_projection(envelope=replace(base, source_provenance=source, contextual_distance=context, projection_intent=intent), budget=_budget())
    assert result.decision is NonProjectionDecision.REJECT
    assert result.reasons[0] is NonProjectionReason.TRUTH_ESCALATION
    assert NonProjectionReason.CONTEXT_UNKNOWN in result.reasons
    assert NonProjectionReason.PROVENANCE_CONFLICTING in result.reasons


def test_contested_interpretation_returns_contested() -> None:
    base = _clean_envelope()
    interpretation = replace(base.interpretation, state=InterpretationState.CONTESTED, alternatives=("alt-a", "alt-b"), disconfirming_refs=("counter-1",))
    result = classify_non_projection(envelope=replace(base, interpretation=interpretation), budget=_budget())
    assert result.decision is NonProjectionDecision.CONTESTED
    assert result.primary_reason is NonProjectionReason.INTERPRETATION_CONTESTED


def test_local_budget_exhaustion_defers_without_truncation() -> None:
    envelope = _clean_envelope()
    result = classify_non_projection(envelope=envelope, budget=_budget(max_string_bytes=4))
    assert result.decision is NonProjectionDecision.DEFER
    assert NonProjectionReason.BUDGET_EXHAUSTED in result.reasons
    assert envelope.source_provenance.source_ref == "source-1"


def test_fingerprint_is_deterministic_and_relevant_mutations_change_it() -> None:
    envelope = _clean_envelope()
    first = classify_non_projection(envelope=envelope, budget=_budget())
    second = classify_non_projection(envelope=envelope, budget=_budget())
    assert first == second
    changed_envelope = replace(envelope, claim=replace(envelope.claim, statement_ref="statement-2"))
    changed = classify_non_projection(envelope=changed_envelope, budget=_budget())
    assert changed.input_fingerprint != first.input_fingerprint
    changed_budget = classify_non_projection(envelope=envelope, budget=_budget(max_tuple_items=511))
    assert changed_budget.input_fingerprint != first.input_fingerprint


def test_reviewer_independence_is_computed_not_trusted() -> None:
    r1 = ReviewRecord("review-1", "reviewer-1", ReviewerIndependence.INDEPENDENT, "provider-1", "prompt-1", "context-1", False)
    r2 = ReviewRecord("review-2", "reviewer-2", ReviewerIndependence.INDEPENDENT, "provider-2", "prompt-2", "context-2", False)
    base = _clean_envelope()
    reviews = ReviewProvenance((r1, r2))
    intent = replace(base.projection_intent, claimed_independent_review_count=2)
    result = classify_non_projection(envelope=replace(base, review_provenance=reviews, projection_intent=intent), budget=_budget())
    assert result.effective_independent_review_count == 2
    assert result.decision is NonProjectionDecision.PASS_ATTRIBUTED
    correlated = ReviewProvenance((r1, replace(r2, provider_ref="provider-1")))
    result = classify_non_projection(envelope=replace(base, review_provenance=correlated, projection_intent=intent), budget=_budget())
    assert result.effective_independent_review_count == 0
    assert result.decision is NonProjectionDecision.REJECT
    assert result.primary_reason is NonProjectionReason.CORRELATED_CONSENSUS_LAUNDERING


def test_scope_subset_violation_rejects() -> None:
    base = _clean_envelope()
    intent = replace(base.projection_intent, proposed_applies_to=("other",))
    result = classify_non_projection(envelope=replace(base, projection_intent=intent), budget=_budget())
    assert result.primary_reason is NonProjectionReason.HISTORICAL_LAW_PROJECTION


def test_threat_order_is_stable_when_multiple_fire() -> None:
    base = _clean_envelope()
    intent = replace(base.projection_intent, inherit_consent=True, adopt_as_self_experience=True, assert_as_objective_truth=True)
    result = classify_non_projection(envelope=replace(base, projection_intent=intent), budget=_budget())
    assert result.triggered_threat_ids == (NonProjectionThreatId.NPG_T01, NonProjectionThreatId.NPG_T03, NonProjectionThreatId.NPG_T12)
    assert result.reasons[:3] == (NonProjectionReason.AUTOBIOGRAPHY_LAUNDERING, NonProjectionReason.TRUTH_ESCALATION, NonProjectionReason.CONSENT_INHERITANCE)


def test_result_exposes_no_reusable_authority_object() -> None:
    values = classify_non_projection(envelope=_clean_envelope(), budget=_budget()).to_value()
    forbidden = {"tool", "capability", "permission", "command", "identity_proof", "relationship_state"}
    assert forbidden.isdisjoint(values)
