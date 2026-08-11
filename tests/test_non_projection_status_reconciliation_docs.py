"""Structural regression checks for the post-#91 NPG status reconciliation."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)
INDEX = (ROOT / "docs" / "research" / "RESEARCH_INDEX.md").read_text(
    encoding="utf-8"
)
RECONCILIATION = (
    ROOT
    / "docs"
    / "research"
    / "NON_PROJECTION_STATUS_RECONCILIATION_2026_08_12.md"
).read_text(encoding="utf-8")


def test_current_status_no_longer_publishes_pre_freeze_authority() -> None:
    for stale_marker in (
        "NON_PROJECTION_IMPLEMENTATION_CONTRACT_NOT_FROZEN",
        "NON_PROJECTION_OWNER_GO_NOT_GRANTED",
        "NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION_NONE",
    ):
        assert stale_marker not in STATUS

    for current_marker in (
        "NON_PROJECTION_IMPLEMENTATION_CONTRACT_FROZEN_DOCS",
        "NON_PROJECTION_OWNER_GO_CONSUMED_BY_PR_90",
        "NON_PROJECTION_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
        "NON_PROJECTION_RUNTIME_NOT_AUTHORIZED",
        "P1_004_NOT_ASSIGNED",
    ):
        assert current_marker in STATUS


def test_current_navigation_surfaces_share_npg_completion_state() -> None:
    for document in (STATUS, ROADMAP, INDEX, RECONCILIATION):
        assert "NPG-v0.1" in document
        assert "PURE_NON_PROJECTION_CLASSIFIER" in document
        assert "IMPLEMENTED_BOUNDED" in document
        assert "NOT_AUTHORIZED" in document
        assert "NOT_ASSIGNED" in document

    assert "Implementation contract:      FROZEN_DOCS · NPG-v0.1" in ROADMAP
    assert "Non-Projection Owner GO:      CONSUMED_BY_PR_90" in ROADMAP
    assert "Implementation contract:      FROZEN_DOCS · NPG-v0.1" in INDEX
    assert "Non-Projection Owner GO:      CONSUMED_BY_PR_90" in INDEX


def test_historical_readiness_state_is_labelled_as_historical_not_current() -> None:
    assert "## 8. 🪞 Historical Post-P1-003 Non-Projection selection" in ROADMAP
    assert "historical selection-time provenance only" in ROADMAP
    assert "Historical owning records" in INDEX
    assert "Historical `NOT_FROZEN`, `NOT_GRANTED`, `NONE` or `NOT_STARTED` values" in RECONCILIATION


def test_reconciliation_adds_no_runtime_or_execution_authority() -> None:
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
        assert marker in RECONCILIATION

    assert "Authority added by this record: NONE" in RECONCILIATION
    assert "Source/runtime code change:     NONE" in RECONCILIATION
    assert "Phase 1 — Non-Projection Runtime Composition Contract" in RECONCILIATION
    assert "is not started or authorized by this record" in RECONCILIATION
