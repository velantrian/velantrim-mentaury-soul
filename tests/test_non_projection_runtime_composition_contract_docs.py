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
    for marker in (
        "PASS_ATTRIBUTED",
        "≠ truth proof",
        "≠ autobiography",
        "≠ stable identity trait",
        "≠ Action Gate PASS",
        "≠ retrieval permission",
        "≠ tool permission",
        "≠ execution permission",
        "≠ deployment permission",
    ):
        assert marker in CONTRACT

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


def test_phase_1_is_frozen_without_owner_go_or_runtime_implementation() -> None:
    for document in (CONTRACT, STATUS):
        assert "NPG-COMP-v0.1" in document
        assert "FROZEN_DOCS" in document
        assert "NOT_GRANTED" in document
        assert "NOT_AUTHORIZED" in document
        assert "NOT_ASSIGNED" in document

    assert "PHASE_1_NON_PROJECTION_RUNTIME_COMPOSITION = COMPLETE" in CONTRACT
    assert "PHASE_1_NON_PROJECTION_RUNTIME_COMPOSITION = COMPLETE" in STATUS
    assert "PHASE_2_IMPLEMENTATION = NOT_STARTED" in CONTRACT
    assert "PHASE_2_OWNER_GO = NOT_GRANTED" in CONTRACT
    assert "PHASE_2_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "PHASE_2_OWNER_GO_NOT_GRANTED" in STATUS

    # Phase 1 is docs-only. The older roadmap's "next runtime milestone" marker
    # remains correct because no Phase 2 runtime milestone is selected/authorized.
    assert "Next runtime milestone:        NOT_SELECTED · NOT_AUTHORIZED" in ROADMAP


def test_no_phase_2_source_package_or_runtime_wiring_exists() -> None:
    reserved = ROOT / "src" / "mentaury" / "composition" / "non_projection_shadow"
    assert not reserved.exists()

    for path in (ROOT / "src" / "mentaury").rglob("*.py"):
        if "non_projection" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        assert "classify_non_projection" not in text, (
            f"unexpected NPG runtime wiring outside pure package: {path.relative_to(ROOT)}"
        )


def test_contract_freezes_adversarial_and_metamorphic_families() -> None:
    for index in range(1, 13):
        assert f"NRC-T{index:02d}" in CONTRACT
    for index in range(1, 11):
        assert f"NRC-M{index:02d}" in CONTRACT

    assert "STOP_AND_RECONCILE" in CONTRACT
    assert "Mandatory stop" in CONTRACT
