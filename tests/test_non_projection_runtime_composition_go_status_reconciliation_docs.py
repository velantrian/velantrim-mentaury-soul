"""Guards for post-#94 NPG-COMP Owner GO current-status reconciliation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)
INDEX = (ROOT / "docs" / "research" / "RESEARCH_INDEX.md").read_text(
    encoding="utf-8"
)
GO = (
    ROOT
    / "docs"
    / "research"
    / "NON_PROJECTION_RUNTIME_COMPOSITION_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")
RECON = (
    ROOT
    / "docs"
    / "research"
    / "NON_PROJECTION_RUNTIME_COMPOSITION_GO_STATUS_RECONCILIATION_2026_08_12.md"
).read_text(encoding="utf-8")


def test_current_surfaces_share_active_phase_2_go_state() -> None:
    for document in (STATUS, ROADMAP, INDEX):
        assert "NPG-COMP-v0.1" in document
        assert "GRANTED_BY_PR_94" in document or "GRANTED · NPG-COMP-v0.1_ONLY" in document
        assert "NOT_STARTED" in document
        assert "NOT_AUTHORIZED" in document
        assert "NOT_ASSIGNED" in document


def test_owner_go_scope_is_single_use_and_exact() -> None:
    for document in (GO, STATUS, ROADMAP, INDEX, RECON):
        assert "NPG-COMP-v0.1_ONLY" in document
        assert "SINGLE_USE" in document or "single-use" in document


def test_phase_1_not_granted_value_is_historical_not_current() -> None:
    assert "Historical Phase 1" in STATUS
    assert "historical Phase-1 freeze" in STATUS
    assert "PHASE_2_OWNER_GO = NOT_GRANTED" in STATUS
    assert "PR #94 later granted" in STATUS
    assert "Historical Phase 1 records are not rewritten" in RECON


def test_reconciliation_adds_no_implementation_or_runtime_authority() -> None:
    assert "New authority added:      NONE" in RECON
    assert "Source/runtime code:      NONE" in RECON
    for marker in (
        "NON_PROJECTION_RUNTIME = NOT_AUTHORIZED",
        "P1_004 = NOT_ASSIGNED",
        "ACTION_GATE = NOT_AUTHORIZED",
        "RETRIEVAL_EXECUTION = NOT_AUTHORIZED",
        "TOOL_EXECUTION = NOT_AUTHORIZED",
        "IDENTITY_RUNTIME = NOT_AUTHORIZED",
        "RELATIONSHIP_RUNTIME = NOT_AUTHORIZED",
        "DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN",
        "RUNTIME_DEPLOYMENT = NOT_AUTHORIZED",
    ):
        assert marker in RECON


def test_reconciliation_precedes_later_clean_implementation() -> None:
    assert "STOP_AND_RECONCILE" in RECON
    assert "fresh exact-main compatibility check" in RECON
    assert "Source/runtime code:      NONE" in RECON
    reserved = ROOT / "src" / "mentaury" / "composition" / "non_projection_shadow"
    assert reserved.is_dir()
    assert {path.name for path in reserved.glob("*.py")} == {
        "__init__.py",
        "contracts.py",
        "coordinator.py",
    }
