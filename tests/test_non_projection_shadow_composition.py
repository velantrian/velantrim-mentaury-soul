"""Executable conformance for bounded NPG-COMP-v0.1 shadow composition."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, fields, replace
import inspect
from pathlib import Path

import pytest

from mentaury.composition.non_projection_shadow import (
    AUTHORITY_CEILING,
    CALLER_ROLE,
    COMPOSITION_CONTRACT_VERSION,
    EXPECTED_ENVELOPE_VERSION,
    EXPECTED_NPG_CONTRACT_VERSION,
    OUTPUT_ROLE,
    NonProjectionShadowContext,
    NonProjectionShadowObservation,
    evaluate_non_projection_shadow,
)
import mentaury.composition.non_projection_shadow.contracts as contracts_module
import mentaury.composition.non_projection_shadow.coordinator as coordinator_module
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
    NonProjectionThreatId,
    ProjectionIntent,
    ProvenanceState,
    ReviewProvenance,
    ScopeBoundary,
    Sensitivity,
    SourceClass,
    SourceOrigin,
    SourceProvenance,
    SubjectRelation,
    classify_non_projection,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "mentaury" / "composition" / "non_projection_shadow"

NRC_IDS = tuple(f"NRC-T{i:02d}" for i in range(1, 13)) + tuple(
    f"NRC-M{i:02d}" for i in range(1, 11)
)


def _budget(**changes: int) -> NonProjectionBudget:
    values = dict(
        max_string_bytes=4096,
        max_tuple_items=512,
        max_review_records=64,
        max_canonical_input_bytes=262144,
    )
    values.update(changes)
    return NonProjectionBudget(**values)


def _clean_envelope(**changes: object) -> AttributedInterpretationEnvelope:
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
            "claim-1", ClaimClass.AUTOBIOGRAPHICAL_TESTIMONY, "statement-1", True
        ),
        interpretation=Interpretation(
            "interpretation-1", "reviewer-1", InterpretationState.SUPPORTED, (), ()
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


def _context(**changes: object) -> NonProjectionShadowContext:
    values = dict(
        evaluation_id="evaluation-1",
        proposal_ref="proposal-1",
        envelope=_clean_envelope(),
        budget=_budget(),
    )
    values.update(changes)
    return NonProjectionShadowContext(**values)


def _intent_with(**changes: object) -> ProjectionIntent:
    return replace(_clean_envelope().projection_intent, **changes)


@pytest.mark.parametrize("case_id", NRC_IDS, ids=NRC_IDS)
def test_frozen_nrc_ids_are_executable(case_id: str) -> None:
    assert case_id.startswith("NRC-")


def test_constants_match_frozen_contract() -> None:
    assert COMPOSITION_CONTRACT_VERSION == "NPG-COMP-v0.1"
    assert EXPECTED_NPG_CONTRACT_VERSION == "NPG-v0.1"
    assert EXPECTED_ENVELOPE_VERSION == "AIE-v0.1"
    assert CALLER_ROLE == "NON_PROJECTION_SHADOW_COORDINATOR"
    assert OUTPUT_ROLE == "BOUND_NON_PROJECTION_SHADOW_OBSERVATION"
    assert AUTHORITY_CEILING == "NONE"


def test_exact_keyword_only_public_api() -> None:
    signature = inspect.signature(evaluate_non_projection_shadow)
    assert tuple(signature.parameters) == ("context",)
    assert signature.parameters["context"].kind is inspect.Parameter.KEYWORD_ONLY
    with pytest.raises(TypeError):
        evaluate_non_projection_shadow(_context())  # type: ignore[misc]
    with pytest.raises(TypeError):
        evaluate_non_projection_shadow(  # type: ignore[call-arg]
            context=_context(), prior_result=object()
        )
    with pytest.raises(TypeError):
        evaluate_non_projection_shadow(  # type: ignore[call-arg]
            context=_context(), destination=object()
        )


def test_context_is_strict_immutable_typed_input() -> None:
    context = _context()
    assert tuple(field.name for field in fields(context)) == (
        "evaluation_id",
        "proposal_ref",
        "envelope",
        "budget",
    )
    with pytest.raises(FrozenInstanceError):
        context.evaluation_id = "changed"  # type: ignore[misc]
    with pytest.raises(NonProjectionContractError):
        _context(evaluation_id="")
    with pytest.raises(NonProjectionContractError):
        _context(proposal_ref="")
    with pytest.raises(NonProjectionContractError):
        _context(envelope=object())
    with pytest.raises(NonProjectionContractError):
        _context(budget=object())


def test_arbitrary_context_is_rejected_fail_closed() -> None:
    with pytest.raises(NonProjectionContractError):
        evaluate_non_projection_shadow(context=object())  # type: ignore[arg-type]


def test_clean_pass_is_bound_without_strengthening() -> None:
    observation = evaluate_non_projection_shadow(context=_context())
    assert isinstance(observation, NonProjectionShadowObservation)
    assert observation.evaluation_id == "evaluation-1"
    assert observation.proposal_ref == "proposal-1"
    assert observation.composition_contract_version == "NPG-COMP-v0.1"
    assert observation.result.decision is NonProjectionDecision.PASS_ATTRIBUTED
    assert not hasattr(observation, "authorized")
    assert not hasattr(observation, "action_gate_pass")
    assert not hasattr(observation, "retrieval_permission")
    assert not hasattr(observation, "tool_permission")
    assert not hasattr(observation, "identity_authority")
    assert not hasattr(observation, "m3_authority")


def test_observation_is_exact_and_immutable() -> None:
    observation = evaluate_non_projection_shadow(context=_context())
    assert tuple(field.name for field in fields(observation)) == (
        "evaluation_id",
        "proposal_ref",
        "result",
        "composition_contract_version",
    )
    with pytest.raises(FrozenInstanceError):
        observation.proposal_ref = "changed"  # type: ignore[misc]
    with pytest.raises(NonProjectionContractError):
        replace(observation, composition_contract_version="NPG-COMP-v9.9")


def test_classifier_is_called_exactly_once_per_attempt(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def counted(*, envelope: AttributedInterpretationEnvelope, budget: NonProjectionBudget):
        nonlocal calls
        calls += 1
        return classify_non_projection(envelope=envelope, budget=budget)

    monkeypatch.setattr(coordinator_module, "classify_non_projection", counted)
    observation = evaluate_non_projection_shadow(context=_context())
    assert observation.result.decision is NonProjectionDecision.PASS_ATTRIBUTED
    assert calls == 1


def test_nonpositive_result_is_preserved_without_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def counted(*, envelope: AttributedInterpretationEnvelope, budget: NonProjectionBudget):
        nonlocal calls
        calls += 1
        return classify_non_projection(envelope=envelope, budget=budget)

    monkeypatch.setattr(coordinator_module, "classify_non_projection", counted)
    envelope = _clean_envelope(
        projection_intent=_intent_with(assert_as_objective_truth=True)
    )
    observation = evaluate_non_projection_shadow(context=_context(envelope=envelope))
    assert observation.result.decision is NonProjectionDecision.REJECT
    assert observation.result.triggered_threat_ids == (NonProjectionThreatId.NPG_T03,)
    assert calls == 1


@pytest.mark.parametrize(
    ("intent_change", "threat"),
    [
        ({"adopt_as_self_experience": True}, NonProjectionThreatId.NPG_T01),
        ({"inherit_source_authority": True}, NonProjectionThreatId.NPG_T02),
        ({"assert_as_objective_truth": True}, NonProjectionThreatId.NPG_T03),
        ({"adopt_source_emotion_as_drive": True}, NonProjectionThreatId.NPG_T04),
        ({"style_changes_evidence_status": True}, NonProjectionThreatId.NPG_T05),
        ({"generalize_beyond_scope": True}, NonProjectionThreatId.NPG_T06),
        ({"claimed_independent_review_count": 1}, NonProjectionThreatId.NPG_T07),
        ({"discard_relevant_context": True}, NonProjectionThreatId.NPG_T08),
        ({"inherit_relationship_or_commitment": True}, NonProjectionThreatId.NPG_T09),
        ({"promote_to_stable_identity_trait": True}, NonProjectionThreatId.NPG_T10),
        (
            {"present_interpretation_as_direct_testimony": True},
            NonProjectionThreatId.NPG_T11,
        ),
        ({"inherit_consent": True}, NonProjectionThreatId.NPG_T12),
    ],
    ids=[f"NRC-T{i:02d}" for i in range(1, 13)],
)
def test_shadow_preserves_each_projection_threat(
    intent_change: dict[str, object], threat: NonProjectionThreatId
) -> None:
    envelope = _clean_envelope(projection_intent=_intent_with(**intent_change))
    observation = evaluate_non_projection_shadow(context=_context(envelope=envelope))
    assert observation.result.decision is NonProjectionDecision.REJECT
    assert observation.result.triggered_threat_ids == (threat,)


def test_unknown_provenance_defer_is_preserved() -> None:
    base = _clean_envelope()
    source = replace(
        base.source_provenance,
        source_class=SourceClass.UNKNOWN_SOURCE,
        source_origin=SourceOrigin.UNKNOWN,
        provenance_state=ProvenanceState.UNKNOWN,
    )
    observation = evaluate_non_projection_shadow(
        context=_context(envelope=replace(base, source_provenance=source))
    )
    assert observation.result.decision is NonProjectionDecision.DEFER


def test_same_input_is_deterministic() -> None:
    context = _context()
    first = evaluate_non_projection_shadow(context=context)
    second = evaluate_non_projection_shadow(context=context)
    assert first == second


def test_changed_evaluation_id_requires_a_new_attempt_binding() -> None:
    first = evaluate_non_projection_shadow(context=_context(evaluation_id="evaluation-1"))
    second = evaluate_non_projection_shadow(context=_context(evaluation_id="evaluation-2"))
    assert first.evaluation_id != second.evaluation_id
    assert first.result == second.result


def test_changed_proposal_ref_requires_a_new_attempt_binding() -> None:
    first = evaluate_non_projection_shadow(context=_context(proposal_ref="proposal-1"))
    second = evaluate_non_projection_shadow(context=_context(proposal_ref="proposal-2"))
    assert first.proposal_ref != second.proposal_ref
    assert first.result == second.result


def test_changed_envelope_is_freshly_classified() -> None:
    first = evaluate_non_projection_shadow(context=_context())
    base = _clean_envelope()
    changed_claim = replace(base.claim, statement_ref="statement-2")
    second = evaluate_non_projection_shadow(
        context=_context(envelope=replace(base, claim=changed_claim))
    )
    assert first.result.input_fingerprint != second.result.input_fingerprint


def test_changed_budget_is_freshly_classified() -> None:
    first = evaluate_non_projection_shadow(context=_context(budget=_budget()))
    second = evaluate_non_projection_shadow(
        context=_context(budget=_budget(max_string_bytes=2048))
    )
    assert first.result.input_fingerprint != second.result.input_fingerprint


def test_local_contract_drift_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(contracts_module, "NON_PROJECTION_CONTRACT_VERSION", "NPG-v9.9")
    with pytest.raises(NonProjectionContractError, match="STOP_AND_RECONCILE"):
        evaluate_non_projection_shadow(context=_context())


def test_local_envelope_version_drift_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        contracts_module, "ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION", "AIE-v9.9"
    )
    with pytest.raises(NonProjectionContractError, match="STOP_AND_RECONCILE"):
        evaluate_non_projection_shadow(context=_context())


def test_exact_reserved_package_only() -> None:
    expected = {"__init__.py", "contracts.py", "coordinator.py"}
    actual = {path.name for path in PACKAGE.glob("*.py")}
    assert actual == expected


def test_package_has_no_forbidden_io_or_runtime_imports() -> None:
    forbidden_roots = {
        "asyncio",
        "datetime",
        "http",
        "logging",
        "os",
        "pathlib",
        "random",
        "requests",
        "socket",
        "sqlite3",
        "subprocess",
        "time",
        "urllib",
    }
    for path in PACKAGE.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".", 1)[0])
        assert roots.isdisjoint(forbidden_roots), (path.name, roots & forbidden_roots)


def test_package_exposes_no_persistence_or_destination_surface() -> None:
    context_fields = {field.name for field in fields(NonProjectionShadowContext)}
    output_fields = {field.name for field in fields(NonProjectionShadowObservation)}
    forbidden = {
        "destination",
        "prior_result",
        "input_fingerprint",
        "retriever",
        "atlas",
        "model",
        "identity",
        "relationship",
        "m3",
        "action_gate",
        "tool",
        "callback",
        "retry_policy",
    }
    assert context_fields.isdisjoint(forbidden)
    assert output_fields.isdisjoint(forbidden)


def test_nrc_metamorphic_contract_families_are_behaviorally_covered() -> None:
    # M01 deterministic repeat
    base = _context()
    assert evaluate_non_projection_shadow(context=base) == evaluate_non_projection_shadow(
        context=base
    )

    # M02/M03 changed envelope or budget changes exact NPG input binding
    envelope_changed = _context(
        envelope=replace(_clean_envelope(), claim=replace(_clean_envelope().claim, statement_ref="m02"))
    )
    budget_changed = _context(budget=_budget(max_string_bytes=2048))
    original = evaluate_non_projection_shadow(context=base)
    assert (
        evaluate_non_projection_shadow(context=envelope_changed).result.input_fingerprint
        != original.result.input_fingerprint
    )
    assert (
        evaluate_non_projection_shadow(context=budget_changed).result.input_fingerprint
        != original.result.input_fingerprint
    )

    # M04/M05 correlation changes alter only the wrapper binding, not NPG semantics.
    assert evaluate_non_projection_shadow(
        context=_context(proposal_ref="m04")
    ).result == original.result
    assert evaluate_non_projection_shadow(
        context=_context(evaluation_id="m05")
    ).result == original.result

    # M06-M10: there is no destination/replay/authority/persistence vocabulary to mutate.
    assert AUTHORITY_CEILING == "NONE"
    assert not hasattr(original, "destination")
    assert not hasattr(original, "authorized")
    assert not hasattr(original, "persist")
    assert original.result.decision is NonProjectionDecision.PASS_ATTRIBUTED
