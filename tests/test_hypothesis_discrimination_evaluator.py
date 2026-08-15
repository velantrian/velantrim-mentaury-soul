"""Executable HDE-v0.1 threat, metamorphic, budget and purity coverage."""

from __future__ import annotations

import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from hashlib import sha256
from pathlib import Path

import pytest

from mentaury.claims import (
    HARD_MAX_CANONICAL_INPUT_BYTES as PCR_MAX_CANONICAL,
    HARD_MAX_STRING_BYTES as PCR_MAX_STRING,
    HARD_MAX_TUPLE_ITEMS as PCR_MAX_TUPLE,
    ClaimRepresentation,
    ClaimScope,
    EpistemicRole,
    ProvenanceSource,
    RepresentationBudget,
    represent_provenance_claim,
)
from mentaury.contracts import canonical_json
from mentaury.discrimination import (
    CANONICAL_PROFILE,
    HARD_MAX_CANONICAL_INPUT_BYTES,
    HARD_MAX_STRING_BYTES,
    HARD_MAX_TUPLE_ITEMS,
    HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION,
    INPUT_FINGERPRINT_DOMAIN,
    DiscriminationClass,
    DiscriminationEvaluation,
    DiscriminationEvaluationBudget,
    DiscriminationProposal,
    HypothesisDiscriminationContractError,
    OutcomePrediction,
    PredictionState,
    evaluate_hypothesis_discrimination,
)
from mentaury.epistemic_types import ClaimType
from mentaury.non_projection import (
    ClaimClass,
    ProvenanceState,
    Sensitivity,
    SourceClass,
    SourceOrigin,
    SubjectRelation,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "mentaury" / "discrimination"


def hypothesis(claim_id: str, role: EpistemicRole = EpistemicRole.HYPOTHESIS):
    source = ProvenanceSource(
        source_ref=f"source:{claim_id}",
        source_actor_ref="actor:researcher",
        source_class=SourceClass.RESEARCH_PRIMARY,
        source_origin=SourceOrigin.PRIMARY,
        provenance_state=ProvenanceState.VERIFIED,
        publication_or_capture_context_ref="context:phase6",
        sensitivity=Sensitivity.NORMAL,
        usage_boundary_ref="usage:research",
        material_gaps=(),
        derivation_refs=(),
    )
    claim = ClaimRepresentation(
        claim_id=claim_id,
        statement_ref=f"statement:{claim_id}",
        claim_class=ClaimClass.FACTUAL,
        claim_type=ClaimType.CONTEXTUAL,
        epistemic_role=role,
        directly_stated=False,
        speaker_ref="actor:researcher",
        subject_ref="subject:system",
        subject_relation=SubjectRelation.NON_SELF,
        basis_refs=("basis:phase6",),
        evidence_refs=(),
    )
    scope = ClaimScope(
        applies_to=("context:phase6",),
        may_support=("question:failure-mode",),
        does_not_establish=("truth:universal",),
        unknowns=(),
        transfer_limits=("scope:bounded",),
    )
    return represent_provenance_claim(
        source=source,
        claim=claim,
        scope=scope,
        budget=RepresentationBudget(PCR_MAX_STRING, PCR_MAX_TUPLE, PCR_MAX_CANONICAL),
    )


def outcome(
    ref: str,
    h1: PredictionState,
    h2: PredictionState,
    basis: tuple[str, ...] = ("basis:expectation",),
) -> OutcomePrediction:
    return OutcomePrediction(ref, h1, h2, basis)


def proposal(**changes: object) -> DiscriminationProposal:
    values: dict[str, object] = {
        "contract_version": "HDE-v0.1",
        "h1": hypothesis("claim:h1"),
        "h2": hypothesis("claim:h2"),
        "proposed_observation_ref": "observation:temperature-voltage",
        "design_origin_ref": "origin:mentaury-design",
        "design_basis_refs": ("basis:failure-interval",),
        "outcomes": (
            outcome("outcome:a", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED),
            outcome("outcome:b", PredictionState.NOT_PREDICTED, PredictionState.PREDICTED),
        ),
        "partition_scope_ref": "scope:failure-interval",
        "partition_complete_for_scope": True,
    }
    values.update(changes)
    return DiscriminationProposal(**values)  # type: ignore[arg-type]


def budget(**changes: object) -> DiscriminationEvaluationBudget:
    values: dict[str, object] = {
        "max_string_bytes": HARD_MAX_STRING_BYTES,
        "max_tuple_items": HARD_MAX_TUPLE_ITEMS,
        "max_canonical_input_bytes": HARD_MAX_CANONICAL_INPUT_BYTES,
    }
    values.update(changes)
    return DiscriminationEvaluationBudget(**values)  # type: ignore[arg-type]


def evaluate(p: DiscriminationProposal | None = None) -> DiscriminationEvaluation:
    return evaluate_hypothesis_discrimination(p or proposal(), budget())


def test_hde_t01_contract_surface_and_distinct_hypotheses() -> None:
    assert HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION == "HDE-v0.1"
    assert CANONICAL_PROFILE == "MENTAURY_CANONICAL_JSON_V1"
    assert INPUT_FINGERPRINT_DOMAIN == "MENTAURY_HYPOTHESIS_DISCRIMINATION_INPUT_V1"
    assert (HARD_MAX_STRING_BYTES, HARD_MAX_TUPLE_ITEMS, HARD_MAX_CANONICAL_INPUT_BYTES) == (4096, 512, 262144)
    assert tuple(inspect.signature(evaluate_hypothesis_discrimination).parameters) == ("proposal", "budget")
    assert evaluate().classification is DiscriminationClass.DISCRIMINATING


def test_hde_t02_m07_same_exact_pcr_identity_rejected() -> None:
    h = hypothesis("claim:same")
    with pytest.raises(HypothesisDiscriminationContractError):
        proposal(h1=h, h2=h)


def test_hde_t03_non_hypothesis_roles_rejected() -> None:
    for role in (EpistemicRole.OBSERVATION, EpistemicRole.INFERENCE):
        with pytest.raises(HypothesisDiscriminationContractError):
            proposal(h1=hypothesis(f"claim:{role.value.lower()}", role))


def test_hde_t04_t05_discriminating_vs_non_discriminating() -> None:
    assert evaluate().classification is DiscriminationClass.DISCRIMINATING
    same = proposal(outcomes=(
        outcome("outcome:a", PredictionState.PREDICTED, PredictionState.PREDICTED),
        outcome("outcome:b", PredictionState.NOT_PREDICTED, PredictionState.NOT_PREDICTED),
    ))
    result = evaluate(same)
    assert result.classification is DiscriminationClass.NON_DISCRIMINATING
    assert result.differential_outcome_refs == ()


def test_hde_t06_t07_inconclusive_unknown_or_incomplete() -> None:
    unknown = proposal(outcomes=(
        outcome("outcome:a", PredictionState.UNKNOWN, PredictionState.NOT_PREDICTED),
        outcome("outcome:b", PredictionState.NOT_PREDICTED, PredictionState.PREDICTED),
    ))
    result = evaluate(unknown)
    assert result.classification is DiscriminationClass.INCONCLUSIVE_STRUCTURE
    assert result.unknown_outcome_refs == ("outcome:a",)
    assert result.differential_outcome_refs == ("outcome:b",)
    assert evaluate(proposal(partition_complete_for_scope=False)).classification is DiscriminationClass.INCONCLUSIVE_STRUCTURE


def test_hde_t08_t09_provenance_is_required() -> None:
    for changes in ({"design_origin_ref": ""}, {"design_basis_refs": ()}, {"partition_scope_ref": ""}):
        with pytest.raises(HypothesisDiscriminationContractError):
            proposal(**changes)
    with pytest.raises(HypothesisDiscriminationContractError):
        outcome("outcome:x", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED, ())


def test_hde_t10_m03_canonical_unique_collections() -> None:
    with pytest.raises(HypothesisDiscriminationContractError):
        proposal(outcomes=(
            outcome("outcome:a", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED),
            outcome("outcome:a", PredictionState.NOT_PREDICTED, PredictionState.PREDICTED),
        ))
    with pytest.raises(HypothesisDiscriminationContractError):
        proposal(outcomes=(
            outcome("outcome:b", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED),
            outcome("outcome:a", PredictionState.NOT_PREDICTED, PredictionState.PREDICTED),
        ))
    with pytest.raises(HypothesisDiscriminationContractError):
        proposal(design_basis_refs=("basis:a", "basis:a"))


def test_hde_t11_m09_no_confidence_probability_trust_weight_surface() -> None:
    forbidden = {"confidence", "probability", "trust", "weight", "score"}
    for cls in (OutcomePrediction, DiscriminationProposal, DiscriminationEvaluation):
        assert not ({field.name for field in fields(cls)} & forbidden)
    with pytest.raises(TypeError):
        OutcomePrediction(  # type: ignore[call-arg]
            "outcome:x", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED,
            ("basis:x",), confidence=0.9,
        )


def test_hde_t12_no_evidence_gate_or_truth_result_vocabulary() -> None:
    assert {item.value for item in DiscriminationClass} == {
        "DISCRIMINATING", "NON_DISCRIMINATING", "INCONCLUSIVE_STRUCTURE"
    }
    text = repr(evaluate().to_value())
    for forbidden in ("SUPPORTED", "CONTRADICTED", "TRUE", "FALSE", "PROVEN", "BELIEVED"):
        assert forbidden not in text


def test_hde_t13_m10_fingerprint_is_deterministic_and_reproducible() -> None:
    p = proposal()
    b = budget()
    first = evaluate_hypothesis_discrimination(p, b)
    second = evaluate_hypothesis_discrimination(p, b)
    encoded = canonical_json.canonical_json_bytes({
        "contract_version": "HDE-v0.1", "proposal": p.to_value(), "budget": b.to_value()
    })
    expected = sha256(b"MENTAURY_HYPOTHESIS_DISCRIMINATION_INPUT_V1\x00" + encoded).hexdigest()
    assert first == second
    assert first.input_fingerprint == expected


def test_hde_t14_t15_no_hidden_io_runtime_or_mutation_imports() -> None:
    allowed = {"__future__", "dataclasses", "enum", "typing", "hashlib", "mentaury.claims", "mentaury.contracts"}
    forbidden = ("requests", "httpx", "urllib", "socket", "subprocess", "sqlite", "sqlalchemy", "random", "datetime", "asyncio", "threading", "multiprocessing", "evidence_gate", "belief", "identity", "relationship", "action", "scheduler", "retrieval", "tool", "openai")
    for path in (PACKAGE / "contracts.py", PACKAGE / "evaluator.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        for imported in imports:
            assert imported in allowed
            assert not any(token in imported.lower() for token in forbidden)


def test_hde_t16_m04_m05_relation_refs_have_no_semantic_authority() -> None:
    causal = evaluate(proposal(design_basis_refs=("relation:causal",)))
    correlational = evaluate(proposal(design_basis_refs=("relation:correlational",)))
    assert causal.classification is correlational.classification
    assert causal.differential_outcome_refs == correlational.differential_outcome_refs
    assert causal.input_fingerprint != correlational.input_fingerprint
    assert not hasattr(causal, "causal")


def test_hde_m01_renaming_nonsemantic_refs_preserves_classification() -> None:
    renamed = proposal(
        proposed_observation_ref="observation:renamed",
        design_origin_ref="origin:renamed",
        design_basis_refs=("basis:renamed",),
        partition_scope_ref="scope:renamed",
        outcomes=(
            outcome("outcome:c", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED, ("basis:renamed",)),
            outcome("outcome:d", PredictionState.NOT_PREDICTED, PredictionState.PREDICTED, ("basis:renamed",)),
        ),
    )
    assert evaluate().classification is evaluate(renamed).classification


def test_hde_m02_swapping_hypotheses_and_columns_is_equivalent() -> None:
    p = proposal()
    swapped = replace(
        p,
        h1=p.h2,
        h2=p.h1,
        outcomes=tuple(
            OutcomePrediction(o.outcome_ref, o.h2_prediction, o.h1_prediction, o.expectation_basis_refs)
            for o in p.outcomes
        ),
    )
    a, b = evaluate(p), evaluate(swapped)
    assert (a.classification, a.differential_outcome_refs, a.unknown_outcome_refs) == (
        b.classification, b.differential_outcome_refs, b.unknown_outcome_refs
    )


def test_hde_m06_removing_only_differential_removes_discrimination() -> None:
    p = proposal(outcomes=(
        outcome("outcome:a", PredictionState.PREDICTED, PredictionState.PREDICTED),
        outcome("outcome:b", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED),
    ))
    assert evaluate(p).classification is DiscriminationClass.DISCRIMINATING
    assert evaluate(replace(p, outcomes=(p.outcomes[0],))).classification is DiscriminationClass.NON_DISCRIMINATING


def test_immutability_exact_types_budgets_and_empty_partition_fail_closed() -> None:
    o = outcome("outcome:x", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED)
    with pytest.raises(FrozenInstanceError):
        o.outcome_ref = "changed"  # type: ignore[misc]
    with pytest.raises(HypothesisDiscriminationContractError):
        evaluate_hypothesis_discrimination(object(), budget())  # type: ignore[arg-type]
    with pytest.raises(HypothesisDiscriminationContractError):
        proposal(partition_complete_for_scope=1)
    with pytest.raises(HypothesisDiscriminationContractError):
        proposal(outcomes=())
    for value in (0, -1, True, 1.0):
        with pytest.raises(HypothesisDiscriminationContractError):
            budget(max_string_bytes=value)
    with pytest.raises(HypothesisDiscriminationContractError):
        evaluate_hypothesis_discrimination(proposal(proposed_observation_ref="abcd"), budget(max_string_bytes=3))
    with pytest.raises(HypothesisDiscriminationContractError):
        evaluate_hypothesis_discrimination(proposal(), budget(max_canonical_input_bytes=64))


def test_hde_canonical_profile_drift_stops_after_valid_pcr_inputs_exist(monkeypatch: pytest.MonkeyPatch) -> None:
    p = proposal()
    b = budget()
    monkeypatch.setattr(canonical_json, "PROFILE_NAME", "DRIFTED_PROFILE")
    with pytest.raises(HypothesisDiscriminationContractError, match="STOP_AND_RECONCILE"):
        evaluate_hypothesis_discrimination(p, b)
