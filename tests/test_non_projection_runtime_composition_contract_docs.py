"""Structural guards for the frozen Phase 1 NPG runtime composition contract."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS = (
    ROOT / "docs" / "research" / "NON_PROJECTION_RUNTIME_COMPOSITION_READINESS.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)
RECEIPT = (
    ROOT / "docs" / "NON_PROJECTION_RUNTIME_COMPOSITION_IMPLEMENTATION_AUTHORIZATION.md"
).read_text(encoding="utf-8")


def test_phase_1_readiness_answers_who_what_where() -> None:
    for document in (READINESS, CONTRACT):
        assert "SAME_ATTEMPT_SHADOW_COORDINATOR" in document
        assert "NON_PROJECTION_SHADOW_COORDINATOR" in document
        assert "AIE-v0.1" in document
        assert "NonProjectionBudget" in document
        assert "same-attempt" in document.lower()
        assert "shadow observation" in document.lower()
        assert "prior NonProjectionResult" in document
        assert "FORBIDDEN" in document


def test_frozen_contract_preserves_npg_authority_ceiling() -> None:
    assert "PASS_ATTRIBUTED" in CONTRACT
    assert "= at most no bounded Non-Projection blocker found" in CONTRACT

    for forbidden_strengthening in (
        "AUTHORIZED",
        "ALLOW_ACTION",
        "ALLOW_RETRIEVAL",
        "SUPPORTED_TRUTH",
        "IDENTITY_CONFIRMED",
        "RELATIONSHIP_CONFIRMED",
        "CONSENT_CONFIRMED",
        "M3_APPROVED",
    ):
        assert forbidden_strengthening in CONTRACT

    for marker in (
        "ACTION_GATE = NOT_AUTHORIZED",
        "RETRIEVAL_EXECUTION = NOT_AUTHORIZED",
        "TOOL_EXECUTION = NOT_AUTHORIZED",
        "IDENTITY_RUNTIME = NOT_AUTHORIZED",
        "RELATIONSHIP_RUNTIME = NOT_AUTHORIZED",
        "DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN",
        "RUNTIME_DEPLOYMENT = NOT_AUTHORIZED",
    ):
        assert marker in CONTRACT


def test_phase_1_freeze_is_historical_and_phase_2_is_now_bounded_complete() -> None:
    assert "PHASE_1_NON_PROJECTION_RUNTIME_COMPOSITION = COMPLETE" in CONTRACT
    assert "PHASE_2_IMPLEMENTATION = NOT_STARTED" in CONTRACT
    assert "PHASE_2_OWNER_GO = NOT_GRANTED" in CONTRACT
    assert "historical Phase-1 freeze" in STATUS

    assert "PHASE_2_NPG_SHADOW_COMPOSITION_IMPLEMENTED_BOUNDED" in STATUS
    assert "PHASE_2_OWNER_GO_CONSUMED_BY_PR_96" in STATUS
    assert "Phase 2 Owner GO:             CONSUMED_BY_PR_96" in ROADMAP
    assert "Phase 2 implementation:       IMPLEMENTED_BOUNDED" in ROADMAP
    assert "Runtime activation milestone: NOT_SELECTED · NOT_AUTHORIZED" in ROADMAP
    assert "OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED" in RECEIPT


def test_reserved_phase_2_package_matches_frozen_surface_without_broader_wiring() -> None:
    reserved = ROOT / "src" / "mentaury" / "composition" / "non_projection_shadow"
    expected = {"__init__.py", "contracts.py", "coordinator.py"}
    assert {path.name for path in reserved.glob("*.py")} == expected

    for path in (ROOT / "src" / "mentaury").rglob("*.py"):
        if reserved in path.parents or "non_projection" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        assert "evaluate_non_projection_shadow" not in text, (
            f"unexpected shadow runtime wiring outside reserved package: {path.relative_to(ROOT)}"
        )


def test_contract_freezes_adversarial_and_metamorphic_families() -> None:
    for index in range(1, 13):
        assert f"NRC-T{index:02d}" in CONTRACT
    for index in range(1, 11):
        assert f"NRC-M{index:02d}" in CONTRACT

    assert "STOP_AND_RECONCILE" in CONTRACT
    assert "Mandatory stop" in CONTRACT
