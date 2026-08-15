"""Structural guards for the explicit ATR-v0.1 Owner GO authority record."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GO = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_PURE_RECORD_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_owner_go_is_exact_and_single_use() -> None:
    for marker in (
        "Owner GO:                       GRANTED",
        "Owner GO scope:                 ATR-v0.1_ONLY",
        "Single-use authorization:       YES",
        "GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_5_IMPLEMENTATION",
        "Phase 5 implementation:         NOT_STARTED",
        "Phase 5 runtime:                NOT_AUTHORIZED",
        "Phase 6 runtime:                NOT_AUTHORIZED",
    ):
        assert marker in GO


def test_authorized_surface_matches_frozen_contract() -> None:
    assert "Contract version:                    ATR-v0.1" in CONTRACT
    assert "PURE_ANCHORED_TYPED_RELATION_RECORD" in CONTRACT
    for path in (
        "src/mentaury/relations/__init__.py",
        "src/mentaury/relations/contracts.py",
        "src/mentaury/relations/representation.py",
    ):
        assert path in GO
        assert path in CONTRACT
    assert "def represent_typed_relation(" in GO
    assert "represent_typed_relation(" in CONTRACT


def test_owner_go_does_not_grant_broader_authority() -> None:
    for marker in (
        "Persistence / graph authority:  NONE",
        "Retrieval / Atlas authority:    NONE",
        "Evidence Gate authority:        UNCHANGED",
        "Belief mutation authority:      NONE",
        "Tools / Action Gate:            NOT_AUTHORIZED",
        "Identity / relationship:        NOT_AUTHORIZED",
        "Direct or indirect M3 write:    FORBIDDEN",
        "Autonomous cognition loop:      NOT_AUTHORIZED",
        "INFERENCE_BRIDGE_RUNTIME = NOT_AUTHORIZED",
        "AUTONOMOUS_COGNITION = NOT_AUTHORIZED",
    ):
        assert marker in GO


def test_owner_go_preserves_atr_semantic_ceiling() -> None:
    for marker in (
        "RELATION_CONFIDENCE = NOT_IN_V0_1",
        "GRAPH_AUTHORITY = NONE",
        "EVIDENCE_GATE_AUTHORITY = UNCHANGED",
        "no confidence/probability/reliability/weight/support/graph-score surface",
        "no relation-type promotion or truth/evidence/belief inference",
    ):
        assert marker in GO


def test_owner_go_requires_fresh_separate_implementation_cycle() -> None:
    for marker in (
        "fresh exact-main compatibility check",
        "clean implementation branch",
        "exact reserved three-file package",
        "exact-head CI",
        "Tier A correctness + adversarial review",
        "guarded protected merge",
        "resulting-main CI",
        "Owner GO consumed",
        "STOP_AND_RECONCILE",
    ):
        assert marker in GO
