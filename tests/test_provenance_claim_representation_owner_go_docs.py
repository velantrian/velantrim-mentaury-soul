"""Structural guards for the explicit PCR-v0.1 Owner GO authority record."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GO = (ROOT / "docs" / "research" / "PROVENANCE_CLAIM_REPRESENTATION_OWNER_GO_DECISION.md").read_text(encoding="utf-8")
CONTRACT = (ROOT / "docs" / "research" / "PROVENANCE_CLAIM_REPRESENTATION_CONTRACT_V0_1.md").read_text(encoding="utf-8")


def test_owner_go_is_exact_and_single_use() -> None:
    for marker in (
        "Owner GO:                       GRANTED",
        "Owner GO scope:                 PCR-v0.1_ONLY",
        "Single-use authorization:       YES",
        "GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_3_IMPLEMENTATION",
        "Phase 3 implementation:         NOT_STARTED",
        "Phase 3 runtime:                NOT_AUTHORIZED",
        "Phase 4:                        NOT_AUTHORIZED",
    ):
        assert marker in GO


def test_authorized_surface_matches_frozen_contract() -> None:
    assert "Contract version:                    PCR-v0.1" in CONTRACT
    assert "PURE_PROVENANCE_CLAIM_RECORD" in CONTRACT
    for path in (
        "src/mentaury/claims/__init__.py",
        "src/mentaury/claims/contracts.py",
        "src/mentaury/claims/representation.py",
    ):
        assert path in GO
        assert path in CONTRACT
    assert "def represent_provenance_claim(" in GO
    assert "def represent_provenance_claim(" in CONTRACT


def test_owner_go_does_not_grant_broader_authority() -> None:
    for marker in (
        "Source admission authority:     NONE",
        "Evidence Gate authority:        UNCHANGED",
        "Belief promotion/revision:      NOT_AUTHORIZED",
        "Retrieval / Atlas:              NOT_AUTHORIZED",
        "Tools / Action Gate:            NOT_AUTHORIZED",
        "Identity / relationship:        NOT_AUTHORIZED",
        "Direct or indirect M3 write:    FORBIDDEN",
        "Persistence:                    NOT_AUTHORIZED",
        "Deployment:                     NOT_AUTHORIZED",
        "NON_PROJECTION_RUNTIME = NOT_AUTHORIZED",
        "AUTONOMOUS_BACKGROUND_LOOP = NOT_AUTHORIZED",
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
