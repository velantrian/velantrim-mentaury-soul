"""Structural guards for the explicit HDE-v0.1 Owner GO authority record."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GO = (
    ROOT
    / "docs"
    / "research"
    / "HYPOTHESIS_DISCRIMINATION_EVALUATOR_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "HYPOTHESIS_DISCRIMINATION_EVALUATOR_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_owner_go_is_exact_and_single_use() -> None:
    for marker in (
        "Owner GO:                       GRANTED",
        "Owner GO scope:                 HDE-v0.1_ONLY",
        "Single-use authorization:       YES",
        "GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_6_IMPLEMENTATION",
        "Phase 6 implementation:         NOT_STARTED",
        "Phase 6 runtime:                NOT_AUTHORIZED",
    ):
        assert marker in GO


def test_authorized_surface_matches_frozen_contract() -> None:
    assert "Contract:                       HDE-v0.1" in CONTRACT
    assert "PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR" in CONTRACT
    for path in (
        "src/mentaury/discrimination/__init__.py",
        "src/mentaury/discrimination/contracts.py",
        "src/mentaury/discrimination/evaluator.py",
        "tests/test_hypothesis_discrimination_evaluator.py",
    ):
        assert path in GO
        assert path in CONTRACT
    assert "evaluate_hypothesis_discrimination(" in GO
    assert "evaluate_hypothesis_discrimination(" in CONTRACT


def test_owner_go_does_not_grant_broader_authority() -> None:
    for marker in (
        "Evidence Gate authority:        NONE · P0-015 UNCHANGED",
        "Belief mutation authority:      NONE",
        "Retrieval / tools / network:    NONE",
        "Action / scheduler authority:   NOT_AUTHORIZED",
        "Identity / relationship:        NOT_AUTHORIZED",
        "Direct or indirect M3 write:    FORBIDDEN",
        "Autonomous cognition loop:      NOT_AUTHORIZED",
        "OBSERVATION_EXECUTION = NOT_AUTHORIZED",
        "EVIDENCE_COLLECTION = NOT_AUTHORIZED",
        "AUTONOMOUS_COGNITION = NOT_AUTHORIZED",
    ):
        assert marker in GO


def test_owner_go_preserves_hde_semantic_ceiling() -> None:
    for marker in (
        "DISCRIMINATING | NON_DISCRIMINATING | INCONCLUSIVE_STRUCTURE",
        "no confidence/probability/trust/weight surface",
        "no `SUPPORTED` / `CONTRADICTED` output or P0-015 invocation",
        "no ATR relation laundering into evidence or causal authority",
        "no self-evidence loop from Mentaury-derived test design",
    ):
        assert marker in GO


def test_owner_go_requires_fresh_separate_implementation_cycle() -> None:
    for marker in (
        "fresh exact-main compatibility check",
        "clean implementation branch",
        "exact reserved four-file source/test surface",
        "exact-head CI",
        "correctness + adversarial review",
        "guarded protected merge",
        "resulting-main CI",
        "Owner GO consumed",
        "STOP_AND_RECONCILE",
    ):
        assert marker in GO
