"""Structural assertions for the post-P1-003 docs-only milestone selection."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTION = (ROOT / "docs" / "research" / "POST_P1_003_MILESTONE_SELECTION.md").read_text(
    encoding="utf-8"
)
CURRENT_STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)


def test_selection_is_docs_only_and_selects_no_runtime_milestone() -> None:
    assert "ARCHITECTURE_SELECTION · DOCS_ONLY" in SELECTION
    assert "Selection result:             NO_RUNTIME_MILESTONE_SELECTED" in SELECTION
    assert "Selected bounded work:        NON_PROJECTION_GATE_CONTRACT_READINESS" in SELECTION
    assert "P1-004 assignment:            NONE" in SELECTION
    assert "Implementation authorization: NONE" in SELECTION


def test_selection_preserves_completed_p1_003_authority_boundary() -> None:
    for marker in (
        "P1_003_IMPLEMENTATION = IMPLEMENTED_BOUNDED",
        "P1_003_OWNER_GO = CONSUMED",
        "P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED",
        "NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED",
    ):
        assert marker in SELECTION

    assert "P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_IMPLEMENTED_BOUNDED" in CURRENT_STATUS
    assert "P1_003_OWNER_GO_CONSUMED" in CURRENT_STATUS
    assert "NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED" in CURRENT_STATUS
    assert "Runtime activation milestone: NOT_SELECTED · NOT_AUTHORIZED" in ROADMAP
    assert "Next bounded implementation:  NPG-COMP-v0.1_SHADOW · AUTHORIZED_NOT_STARTED" in ROADMAP


def test_non_projection_readiness_creates_no_execution_or_identity_authority() -> None:
    for marker in (
        "Non-Projection runtime:       NOT_AUTHORIZED",
        "Non-Projection Owner GO:      NOT_GRANTED",
        "Action Gate authority:        NONE",
        "Retrieval authority:          NONE",
        "Tool authority:               NONE",
        "Identity authority:           NONE",
        "Relationship authority:       NONE",
        "Direct or indirect M3 write:  FORBIDDEN",
        "Deployment authority:         NONE",
    ):
        assert marker in SELECTION


def test_selection_keeps_high_risk_runtime_candidates_deferred() -> None:
    assert "A. Action Gate contract/readiness" in SELECTION
    assert "E. Identity / continuity bounded runtime" in SELECTION
    assert "F. Relationship runtime" in SELECTION
    assert "DEFER" in SELECTION
    assert "Why not Action Gate:" in SELECTION
    assert "Why not identity runtime:" in SELECTION


def test_projection_threat_and_adversarial_requirements_are_explicit() -> None:
    for number in range(1, 13):
        assert f"NPG-T{number:02d}" in SELECTION
        assert f"NPG-SC-{number:03d}" in SELECTION

    for number in range(1, 9):
        assert f"MT-NPG-{number:03d}" in SELECTION


def test_positive_non_projection_result_cannot_become_permission() -> None:
    for marker in (
        "≠ factual truth proof",
        "≠ identity claim",
        "≠ M3 nomination",
        "≠ relationship claim",
        "≠ consent",
        "≠ capability",
        "≠ Action Gate PASS",
        "≠ retrieval permission",
        "≠ tool/execution permission",
    ):
        assert marker in SELECTION


def test_selection_requires_later_separate_authority_cycle_before_code() -> None:
    assert "separate candidate selection / contract freeze / Owner GO remains required before code" in SELECTION
    assert "P1-004:                     NOT_ASSIGNED" in SELECTION
    assert "Implementation GO:          NONE" in SELECTION
