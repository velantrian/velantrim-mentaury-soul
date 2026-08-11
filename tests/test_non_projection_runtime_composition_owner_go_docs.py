"""Structural guards for the one-time NPG-COMP-v0.1 Owner GO decision."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GO = (
    ROOT
    / "docs"
    / "research"
    / "NON_PROJECTION_RUNTIME_COMPOSITION_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_owner_go_is_exact_and_single_use() -> None:
    for marker in (
        "OWNER GO DECISION: GO",
        "NPG-COMP-v0.1_ONLY",
        "PHASE_2_OWNER_GO = GRANTED",
        "GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_2_IMPLEMENTATION",
        "single-use",
    ):
        assert marker in GO


def test_go_does_not_claim_implementation_or_runtime_activation() -> None:
    for marker in (
        "Phase 2 implementation:         NOT_STARTED",
        "Non-Projection runtime:         NOT_AUTHORIZED",
        "P1-004 assignment:              NOT_ASSIGNED",
        "ACTION_GATE = NOT_AUTHORIZED",
        "RETRIEVAL_EXECUTION = NOT_AUTHORIZED",
        "TOOL_EXECUTION = NOT_AUTHORIZED",
        "IDENTITY_RUNTIME = NOT_AUTHORIZED",
        "RELATIONSHIP_RUNTIME = NOT_AUTHORIZED",
        "DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN",
        "RUNTIME_DEPLOYMENT = NOT_AUTHORIZED",
    ):
        assert marker in GO


def test_authorized_surface_matches_frozen_contract() -> None:
    for marker in (
        "SAME_ATTEMPT_SHADOW_COORDINATOR",
        "NON_PROJECTION_SHADOW_COORDINATOR_ONLY",
        "AIE-v0.1",
        "NonProjectionBudget",
        "PRIOR_RESULT_INPUT = FORBIDDEN",
        "RESULT_REPLAY_AS_AUTHORITY = FORBIDDEN",
        "evaluate_non_projection_shadow",
    ):
        assert marker in GO
        assert marker in CONTRACT


def test_owner_go_record_remains_pre_implementation_provenance() -> None:
    assert "It does not itself implement" in GO
    assert "Phase 2 implementation:         NOT_STARTED" in GO
    reserved = ROOT / "src" / "mentaury" / "composition" / "non_projection_shadow"
    assert reserved.is_dir()
    assert {path.name for path in reserved.glob("*.py")} == {
        "__init__.py",
        "contracts.py",
        "coordinator.py",
    }


def test_implementation_must_cover_frozen_matrices() -> None:
    assert "NRC-T01…NRC-T12" in GO
    assert "NRC-M01…NRC-M10" in GO
    for index in range(1, 13):
        assert f"NRC-T{index:02d}" in CONTRACT
    for index in range(1, 11):
        assert f"NRC-M{index:02d}" in CONTRACT


def test_compatibility_stop_is_explicit() -> None:
    assert "STOP_AND_RECONCILE" in GO
    assert "STOP_AND_RECONCILE" in CONTRACT
