"""Structural guards for the historical Phase 6 HDE-v0.1 readiness freeze.

The readiness/contract documents remain historical docs-only evidence. Once the
separate explicit HDE-v0.1 Owner GO exists, the exact reserved package may exist
without rewriting those historical documents.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = (
    ROOT / "docs" / "research" / "PHASE_6_HYPOTHESIS_DISCRIMINATION_READINESS.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT / "docs" / "research" / "HYPOTHESIS_DISCRIMINATION_EVALUATOR_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")
PCR = (ROOT / "src" / "mentaury" / "claims" / "contracts.py").read_text(
    encoding="utf-8"
)
ATR = (ROOT / "src" / "mentaury" / "relations" / "contracts.py").read_text(
    encoding="utf-8"
)
OWNER_GO_PATH = (
    ROOT
    / "docs"
    / "research"
    / "HYPOTHESIS_DISCRIMINATION_EVALUATOR_OWNER_GO_DECISION.md"
)


def test_existing_owners_are_reused() -> None:
    assert 'HYPOTHESIS = "HYPOTHESIS"' in PCR
    assert 'INFERENCE = "INFERENCE"' in PCR
    assert 'CORRELATIONAL = "CORRELATIONAL"' in ATR
    assert 'CAUSAL = "CAUSAL"' in ATR
    for marker in (
        "No new `HypothesisRecord`, `InferenceRecord`, `RelationRecord`, `EvidenceVerdict`",
        "P0-015 remains sole owner of `SUPPORTED / CONTRADICTED`",
        "EPR-v0.1 remains routing-only and unimplemented",
    ):
        assert marker in READINESS + CONTRACT


def test_actual_gap_is_outcome_mapping_not_hypothesis_representation() -> None:
    for marker in (
        "qualitative expected outcome under H1 vs H2",
        "verify at least one supplied outcome separates H1/H2",
        "WELL_FORMED_H1 + WELL_FORMED_H2 + WELL_FORMED_RELATIONS",
        "NON_DISCRIMINATING_OBSERVATION",
        "no existing contract violation",
    ):
        assert marker in READINESS


def test_candidate_comparison_selects_minimal_evaluator_only() -> None:
    for marker in (
        "A · `NO_NEW_PRIMITIVE` / benchmark convention only",
        "B · `PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR`",
        "C · `PURE_DISCRIMINATION_PLAN_RECORD`",
        "D · record + evaluator",
        "**SELECTED**",
        "rejected as unnecessary surface",
    ):
        assert marker in READINESS


def test_frozen_api_and_input_output_are_explicit() -> None:
    for marker in (
        "evaluate_hypothesis_discrimination(",
        "proposal: DiscriminationProposal",
        "budget: DiscriminationEvaluationBudget",
        ") -> DiscriminationEvaluation",
        "PREDICTED",
        "NOT_PREDICTED",
        "UNKNOWN",
        "DISCRIMINATING",
        "NON_DISCRIMINATING",
        "INCONCLUSIVE_STRUCTURE",
        "input_fingerprint: lowercase sha256 hex",
    ):
        assert marker in CONTRACT


def test_non_discriminating_structure_cannot_pass() -> None:
    for marker in (
        "all represented outcomes identical under H1/H2 can never yield `DISCRIMINATING`",
        "elif one or more DIFFERENTIAL outcomes exist:",
        "DISCRIMINATING",
        "else:",
        "NON_DISCRIMINATING",
    ):
        assert marker in CONTRACT


def test_inconclusive_and_incomplete_inputs_do_not_force_closure() -> None:
    for marker in (
        "partition_complete_for_scope is False",
        "any UNKNOWN_PAIR exists",
        "INCONCLUSIVE_STRUCTURE",
        "an incomplete/unknown mapping can never force a winner",
        "`WAIT` / `DEFER` remain benchmark/planning outcomes",
    ):
        assert marker in CONTRACT + READINESS


def test_no_evidence_gate_or_confidence_authority() -> None:
    for marker in (
        "PROPOSED OBSERVATION ≠ EVIDENCE",
        "DISCRIMINATION ≠ EVIDENCE GATE VERDICT",
        "MENTAURY_DERIVED_TEST_DESIGN ≠ INDEPENDENT_EVIDENCE",
        "confidence/probability/trust/weight fields forbidden",
        "no SUPPORTED/CONTRADICTED vocabulary in result",
    ):
        assert marker in READINESS + CONTRACT


def test_threat_model_and_metamorphic_matrix_are_frozen() -> None:
    for threat in range(1, 17):
        assert f"T{threat}" in READINESS
    for case in range(1, 11):
        assert f"HDE-M{case:02d}" in READINESS
    for case in range(1, 17):
        assert f"HDE-T{case:02d}" in CONTRACT


def test_reserved_source_surface_requires_separate_owner_go_if_present() -> None:
    reserved = (
        "src/mentaury/discrimination/__init__.py",
        "src/mentaury/discrimination/contracts.py",
        "src/mentaury/discrimination/evaluator.py",
        "tests/test_hypothesis_discrimination_evaluator.py",
    )
    for marker in reserved:
        assert marker in CONTRACT

    package = ROOT / "src" / "mentaury" / "discrimination"
    implementation_test = ROOT / "tests" / "test_hypothesis_discrimination_evaluator.py"
    if package.exists() or implementation_test.exists():
        assert OWNER_GO_PATH.exists()
        owner_go = OWNER_GO_PATH.read_text(encoding="utf-8")
        assert "Owner GO scope:                 HDE-v0.1_ONLY" in owner_go
        assert "Single-use authorization:       YES" in owner_go
        assert package.is_dir()
        assert implementation_test.is_file()
        assert {path.name for path in package.iterdir() if path.is_file()} == {
            "__init__.py",
            "contracts.py",
            "evaluator.py",
        }


def test_historical_readiness_documents_preserve_pre_owner_go_state() -> None:
    for marker in (
        "PHASE_6_READINESS = SELECTED_CANDIDATE_CONTRACT_FROZEN_DOCS_TESTS_ONLY",
        "PHASE_6_CANDIDATE = PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR",
        "PHASE_6_IMPLEMENTATION_CONTRACT = HDE-v0.1 · FROZEN_DOCS_TESTS_ONLY",
        "PHASE_6_IMPLEMENTATION = NOT_STARTED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = NOT_GRANTED",
        "PHASE_6_RUNTIME = NOT_AUTHORIZED",
    ):
        assert marker in READINESS
        assert marker in CONTRACT or marker.startswith("PHASE_6_READINESS")
