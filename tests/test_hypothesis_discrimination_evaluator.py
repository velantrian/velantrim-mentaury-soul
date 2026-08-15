"""Executable HDE-v0.1 threat, metamorphic, budget and purity coverage."""

from __future__ import annotations

import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from hashlib import sha256
from pathlib import Path

import pytest

from mentaury.claims import (
    HARD_MAX_CANONICAL_INPUT_BYTES as PCR_HARD_MAX_CANONICAL_INPUT_BYTES,
    HARD_MAX_STRING_BYTES as PCR_HARD_MAX_STRING_BYTES,
    HARD_MAX_TUPLE_ITEMS as PCR_HARD_MAX_TUPLE_ITEMS,
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


def make_source(source_ref: str) -> ProvenanceSource:
    return ProvenanceSource(
        source_ref=source_ref,
        source_actor_ref="actor:researcher",
        source_class=SourceClass.RESEARCH_PRIMARY,
        source_origin=SourceOrigin.PRIMARY,
        provenance_state=ProvenanceState.VERIFIED,
        publication_or_capture_context_ref="context:phase6-test",
        sensitivity=Sensitivity.NORMAL,
        usage_boundary_ref="usage:research",
        material_gaps=(),
        derivation_refs=(),
    )


def make_claim(claim_id: str, role: EpistemicRole = EpistemicRole.HYPOTHESIS) -> ClaimRepresentation:
    return ClaimRepresentation(
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


def make_claim_scope() -> ClaimScope:
    return ClaimScope(
        applies_to=("context:phase6-test",),
        may_support=("question:failure-mode",),
        does_not_establish=("truth:universal",),
        unknowns=(),
        transfer_limits=("scope:bounded",),
    )


def make_pcr_budget() -> RepresentationBudget:
    return RepresentationBudget(
        max_string_bytes=PCR_HARD_MAX_STRING_BYTES,
        max_tuple_items=PCR_HARD_MAX_TUPLE_ITEMS,
        max_canonical_input_bytes=PCR_HARD_MAX_CANONICAL_INPUT_BYTES,
    )


def make_hypothesis(
    claim_id: str,
    *,
    role: EpistemicRole = EpistemicRole.HYPOTHESIS,
):
    return represent_provenance_claim(
        source=make_source(f"source:{claim_id}"),
        claim=make_claim(claim_id, role),
        scope=make_claim_scope(),
        budget=make_pcr_budget(),
    )


def make_budget(**changes: object) -> DiscriminationEvaluationBudget:
    values: dict[str, object] = {
        "max_string_bytes": HARD_MAX_STRING_BYTES,
        "max_tuple_items": HARD_MAX_TUPLE_ITEMS,
        "max_canonical_input_bytes": HARD_MAX_CANONICAL_INPUT_BYTES,
    }
    values.update(changes)
    return DiscriminationEvaluationBudget(**values)  # type: ignore[arg-type]


def make_outcome(
    ref: str,
    h1: PredictionState,
    h2: PredictionState,
    *,
    basis: tuple[str, ...] = ("basis:expectation",),
) -> OutcomePrediction:
    return OutcomePrediction(
        outcome_ref=ref,
        h1_prediction=h1,
        h2_prediction=h2,
        expectation_basis_refs=basis,
    )


def make_proposal(**changes: object) -> DiscriminationProposal:
    values: dict[str, object] = {
        "contract_version": HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION,
        "h1": make_hypothesis("claim:h1"),
        "h2": make_hypothesis("claim:h2"),
        "proposed_observation_ref": "observation:temperature-and-voltage",
        "design_origin_ref": "origin:mentaury-derived-test-design",
        "design_basis_refs": ("basis:failure-interval",),
        "outcomes": (
            make_outcome(
                "outcome:temperature-high-voltage-stable",
                PredictionState.PREDICTED,
                PredictionState.NOT_PREDICTED,
            ),
            make_outcome(
                "outcome:temperature-normal-voltage-drop",
                PredictionState.NOT_PREDICTED,
                PredictionState.PREDICTED,
            ),
        ),
        "partition_scope_ref": "scope:failure-interval",
        "partition_complete_for_scope": True,
    }
    values.update(changes)
    return DiscriminationProposal(**values)  # type: ignore[arg-type]


def evaluate(proposal: DiscriminationProposal | None = None):
    return evaluate_hypothesis_discrimination(
        proposal or make_proposal(),
        make_budget(),
    )


# HDE-T01 / contract surface

def test_contract_constants_signature_and_distinct_hypotheses_are_accepted() -> None:
    assert HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION == "HDE-v0.1"
    assert CANONICAL_PROFILE == "MENTAURY_CANONICAL_JSON_V1"
    assert INPUT_FINGERPRINT_DOMAIN == "MENTAURY_HYPOTHESIS_DISCRIMINATION_INPUT_V1"
    assert HARD_MAX_STRING_BYTES == 4096
    assert HARD_MAX_TUPLE_ITEMS == 512
    assert HARD_MAX_CANONICAL_INPUT_BYTES == 262144
    assert tuple(inspect.signature(evaluate_hypothesis_discrimination).parameters) == (
        "proposal",
        "budget",
    )
    result = evaluate()
    assert result.classification is DiscriminationClass.DISCRIMINATING


# HDE-T02 / HDE-M07

def test_exact_same_hypothesis_identity_is_rejected() -> None:
    h1 = make_hypothesis("claim:same")
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(h1=h1, h2=h1)


# HDE-T03

def test_non_hypothesis_pcr_role_is_rejected() -> None:
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(h1=make_hypothesis("claim:h1-observation", role=EpistemicRole.OBSERVATION))
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(h2=make_hypothesis("claim:h2-inference", role=EpistemicRole.INFERENCE))


# HDE-T04

def test_differential_known_outcome_is_discriminating() -> None:
    result = evaluate()
    assert result.classification is DiscriminationClass.DISCRIMINATING
    assert result.differential_outcome_refs == (
        "outcome:temperature-high-voltage-stable",
        "outcome:temperature-normal-voltage-drop",
    )
    assert result.unknown_outcome_refs == ()


# HDE-T05 / HDE-M08

def test_all_same_known_outcomes_are_non_discriminating() -> None:
    proposal = make_proposal(
        outcomes=(
            make_outcome(
                "outcome:a",
                PredictionState.PREDICTED,
                PredictionState.PREDICTED,
            ),
            make_outcome(
                "outcome:b",
                PredictionState.NOT_PREDICTED,
                PredictionState.NOT_PREDICTED,
            ),
        )
    )
    result = evaluate(proposal)
    assert result.classification is DiscriminationClass.NON_DISCRIMINATING
    assert result.differential_outcome_refs == ()


# HDE-T06

def test_unknown_prediction_is_inconclusive_and_never_forces_winner() -> None:
    proposal = make_proposal(
        outcomes=(
            make_outcome(
                "outcome:a",
                PredictionState.UNKNOWN,
                PredictionState.NOT_PREDICTED,
            ),
            make_outcome(
                "outcome:b",
                PredictionState.NOT_PREDICTED,
                PredictionState.PREDICTED,
            ),
        )
    )
    result = evaluate(proposal)
    assert result.classification is DiscriminationClass.INCONCLUSIVE_STRUCTURE
    assert result.unknown_outcome_refs == ("outcome:a",)
    assert result.differential_outcome_refs == ("outcome:b",)


# HDE-T07

def test_incomplete_partition_is_inconclusive() -> None:
    result = evaluate(make_proposal(partition_complete_for_scope=False))
    assert result.classification is DiscriminationClass.INCONCLUSIVE_STRUCTURE


# HDE-T08

def test_missing_design_provenance_is_rejected() -> None:
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(design_origin_ref="")
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(design_basis_refs=())
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(partition_scope_ref="")


# HDE-T09

def test_missing_expectation_basis_is_rejected() -> None:
    with pytest.raises(HypothesisDiscriminationContractError):
        make_outcome(
            "outcome:a",
            PredictionState.PREDICTED,
            PredictionState.NOT_PREDICTED,
            basis=(),
        )


# HDE-T10

def test_duplicate_or_unsorted_outcome_refs_are_rejected() -> None:
    duplicate = (
        make_outcome("outcome:a", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED),
        make_outcome("outcome:a", PredictionState.NOT_PREDICTED, PredictionState.PREDICTED),
    )
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(outcomes=duplicate)
    unsorted = (
        make_outcome("outcome:b", PredictionState.PREDICTED, PredictionState.NOT_PREDICTED),
        make_outcome("outcome:a", PredictionState.NOT_PREDICTED, PredictionState.PREDICTED),
    )
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(outcomes=unsorted)


# HDE-T11 / HDE-M09

def test_confidence_probability_trust_weight_are_not_representable() -> None:
    proposal_fields = {field.name for field in fields(DiscriminationProposal)}
    outcome_fields = {field.name for field in fields(OutcomePrediction)}
    evaluation_fields = {field.name for field in fields(DiscriminationEvaluation)}
    forbidden = {"confidence", "probability", "trust", "weight", "score"}
    assert not (proposal_fields & forbidden)
    assert not (outcome_fields & forbidden)
    assert not (evaluation_fields & forbidden)
    with pytest.raises(TypeError):
        OutcomePrediction(  # type: ignore[call-arg]
            outcome_ref="outcome:a",
            h1_prediction=PredictionState.PREDICTED,
            h2_prediction=PredictionState.NOT_PREDICTED,
            expectation_basis_refs=("basis:a",),
            confidence=0.9,
        )


# HDE-T12

def test_result_has_no_evidence_gate_or_truth_vocabulary() -> None:
    assert {item.value for item in DiscriminationClass} == {
        "DISCRIMINATING",
        "NON_DISCRIMINATING",
        "INCONCLUSIVE_STRUCTURE",
    }
    projected = evaluate().to_value()
    text = repr(projected)
    for forbidden in ("SUPPORTED", "CONTRADICTED", "VERIFIED", "PROVEN", "BELIEVED"):
        assert forbidden not in text


# HDE-T13 / HDE-M10

def test_deterministic_canonical_fingerprint_is_independently_reproduced() -> None:
    proposal = make_proposal()
    budget = make_budget()
    first = evaluate_hypothesis_discrimination(proposal, budget)
    second = evaluate_hypothesis_discrimination(proposal, budget)
    encoded = canonical_json.canonical_json_bytes(
        {
            "contract_version": "HDE-v0.1",
            "proposal": proposal.to_value(),
            "budget": budget.to_value(),
        }
    )
    expected = sha256(
        b"MENTAURY_HYPOTHESIS_DISCRIMINATION_INPUT_V1\x00" + encoded
    ).hexdigest()
    assert first == second
    assert first.input_fingerprint == expected


# HDE-T14 / HDE-T15

def test_source_surface_has_no_hidden_io_runtime_or_mutation_imports() -> None:
    allowed_roots = {
        "__future__",
        "dataclasses",
        "enum",
        "typing",
        "hashlib",
        "mentaury.claims",
        "mentaury.contracts",
    }
    forbidden_fragments = (
        "requests",
        "httpx",
        "urllib",
        "socket",
        "subprocess",
        "sqlite",
        "sqlalchemy",
        "random",
        "datetime",
        "time",
        "asyncio",
        "threading",
        "multiprocessing",
        "evidence_gate",
        "belief",
        "identity",
        "relationship",
        "action",
        "scheduler",
        "retrieval",
        "tool",
        "openai",
    )
    for path in (PACKAGE / "contracts.py", PACKAGE / "evaluator.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        for imported in imports:
            assert imported.startswith(".") or imported in allowed_roots
            assert not any(fragment in imported.lower() for fragment in forbidden_fragments)


# HDE-T16 / HDE-M04 / HDE-M05

def test_relation_basis_refs_cannot_change_classification_or_create_causal_authority() -> None:
    causal_design = make_proposal(design_basis_refs=("relation:causal",))
    correlational_design = make_proposal(design_basis_refs=("relation:correlational",))
    causal_result = evaluate(causal_design)
    correlational_result = evaluate(correlational_design)
    assert causal_result.classification is correlational_result.classification
    assert causal_result.differential_outcome_refs == correlational_result.differential_outcome_refs
    assert not hasattr(causal_result, "causal")
    assert causal_result.input_fingerprint != correlational_result.input_fingerprint


# HDE-M01

def test_renaming_nonsemantic_refs_preserves_classification() -> None:
    original = evaluate(make_proposal())
    renamed = evaluate(
        make_proposal(
            proposed_observation_ref="observation:renamed",
            design_origin_ref="origin:renamed",
            design_basis_refs=("basis:renamed",),
            partition_scope_ref="scope:renamed",
            outcomes=(
                make_outcome(
                    "outcome:a-renamed",
                    PredictionState.PREDICTED,
                    PredictionState.NOT_PREDICTED,
                    basis=("basis:expectation-renamed",),
                ),
                make_outcome(
                    "outcome:b-renamed",
                    PredictionState.NOT_PREDICTED,
                    PredictionState.PREDICTED,
                    basis=("basis:expectation-renamed",),
                ),
            ),
        )
    )
    assert original.classification is renamed.classification


# HDE-M02

def test_swapping_hypotheses_and_prediction_columns_is_equivalent() -> None:
    proposal = make_proposal()
    swapped = replace(
        proposal,
        h1=proposal.h2,
        h2=proposal.h1,
        outcomes=tuple(
            OutcomePrediction(
                outcome_ref=outcome.outcome_ref,
                h1_prediction=outcome.h2_prediction,
                h2_prediction=outcome.h1_prediction,
                expectation_basis_refs=outcome.expectation_basis_refs,
            )
            for outcome in proposal.outcomes
        ),
    )
    first = evaluate(proposal)
    second = evaluate(swapped)
    assert first.classification is second.classification
    assert first.differential_outcome_refs == second.differential_outcome_refs
    assert first.unknown_outcome_refs == second.unknown_outcome_refs


# HDE-M03

def test_duplicate_basis_reference_is_rejected_and_cannot_improve_result() -> None:
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(design_basis_refs=("basis:a", "basis:a"))
    with pytest.raises(HypothesisDiscriminationContractError):
        make_outcome(
            "outcome:a",
            PredictionState.PREDICTED,
            PredictionState.NOT_PREDICTED,
            basis=("basis:a", "basis:a"),
        )


# HDE-M06

def test_removing_only_differential_outcome_removes_discrimination() -> None:
    proposal = make_proposal(
        outcomes=(
            make_outcome(
                "outcome:a",
                PredictionState.PREDICTED,
                PredictionState.PREDICTED,
            ),
            make_outcome(
                "outcome:b",
                PredictionState.PREDICTED,
                PredictionState.NOT_PREDICTED,
            ),
        )
    )
    assert evaluate(proposal).classification is DiscriminationClass.DISCRIMINATING
    reduced = replace(proposal, outcomes=(proposal.outcomes[0],))
    assert evaluate(reduced).classification is DiscriminationClass.NON_DISCRIMINATING


def test_contract_objects_are_immutable() -> None:
    outcome = make_outcome(
        "outcome:a",
        PredictionState.PREDICTED,
        PredictionState.NOT_PREDICTED,
    )
    with pytest.raises(FrozenInstanceError):
        outcome.outcome_ref = "outcome:changed"  # type: ignore[misc]
    result = evaluate()
    with pytest.raises(FrozenInstanceError):
        result.classification = DiscriminationClass.NON_DISCRIMINATING  # type: ignore[misc]


def test_exact_types_enums_strings_bool_and_tuple_invariants_fail_closed() -> None:
    with pytest.raises(HypothesisDiscriminationContractError):
        evaluate_hypothesis_discrimination(object(), make_budget())  # type: ignore[arg-type]
    with pytest.raises(HypothesisDiscriminationContractError):
        make_outcome("outcome:a", "PREDICTED", PredictionState.NOT_PREDICTED)  # type: ignore[arg-type]
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(partition_complete_for_scope=1)
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(design_basis_refs=("basis:b", "basis:a"))
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(proposed_observation_ref=" padded")


def test_local_budgets_fail_closed_without_truncation() -> None:
    proposal = make_proposal(proposed_observation_ref="abcd")
    with pytest.raises(HypothesisDiscriminationContractError):
        evaluate_hypothesis_discrimination(proposal, make_budget(max_string_bytes=3))
    with pytest.raises(HypothesisDiscriminationContractError):
        evaluate_hypothesis_discrimination(proposal, make_budget(max_tuple_items=1))
    with pytest.raises(HypothesisDiscriminationContractError):
        evaluate_hypothesis_discrimination(
            proposal,
            make_budget(max_canonical_input_bytes=64),
        )


def test_budget_values_require_exact_positive_int_and_hard_cap() -> None:
    for value in (0, -1, True, 1.0):
        with pytest.raises(HypothesisDiscriminationContractError):
            make_budget(max_string_bytes=value)
    with pytest.raises(HypothesisDiscriminationContractError):
        make_budget(max_tuple_items=HARD_MAX_TUPLE_ITEMS + 1)
    with pytest.raises(HypothesisDiscriminationContractError):
        make_budget(max_canonical_input_bytes=HARD_MAX_CANONICAL_INPUT_BYTES + 1)


def test_canonical_profile_drift_stops_and_reconciles(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(canonical_json, "PROFILE_NAME", "DRIFTED_PROFILE")
    with pytest.raises(HypothesisDiscriminationContractError, match="STOP_AND_RECONCILE"):
        evaluate()


def test_empty_outcome_partition_is_invalid_not_domain_invalid_result() -> None:
    with pytest.raises(HypothesisDiscriminationContractError):
        make_proposal(outcomes=())
    assert "INVALID" not in {item.value for item in DiscriminationClass}
