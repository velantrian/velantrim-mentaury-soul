"""Guards for post-#94 NPG-COMP Owner GO reconciliation and later consumption."""

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
RECEIPT = (
    ROOT / "docs" / "NON_PROJECTION_RUNTIME_COMPOSITION_IMPLEMENTATION_AUTHORIZATION.md"
).read_text(encoding="utf-8")


def test_current_surfaces_share_consumed_phase_2_state() -> None:
    for document in (STATUS, ROADMAP, INDEX, RECEIPT):
        assert "NPG-COMP-v0.1" in document
        assert "CONSUMED_BY_PR_96" in document
        assert "IMPLEMENTED_BOUNDED" in document
        assert "NOT_AUTHORIZED" in document
        assert "NOT_ASSIGNED" in document


def test_owner_go_scope_remains_exact_and_historical_single_use() -> None:
    for document in (GO, STATUS, ROADMAP, INDEX, RECON, RECEIPT):
        assert "NPG-COMP-v0.1_ONLY" in document
    assert "single-use" in GO
    assert "single-use" in RECON
    assert "single-use" in RECEIPT
    assert "Owner GO consumed ≠ reusable authority" in INDEX or "Owner GO consumed ≠ reusable authority" in ROADMAP


def test_phase_1_not_granted_and_phase_2_grant_are_historical() -> None:
    assert "Historical Phase 1" in STATUS
    assert "historical Phase-1 freeze" in STATUS
    assert "PHASE_2_OWNER_GO = NOT_GRANTED" in STATUS
    assert "PR #94 later granted" in STATUS
    assert "Historical Phase 1 records are not rewritten" in RECON
    assert "GRANTED_BY_PR_94" in RECON
    assert "CONSUMED_BY_PR_96" in STATUS


def test_reconciliation_record_itself_added_no_authority() -> None:
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


def test_reconciliation_preceded_later_clean_implementation() -> None:
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
