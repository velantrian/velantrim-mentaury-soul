"""Structural guards retaining historical Phase 4 boundaries after implementation GO."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)
INDEX = (ROOT / "docs" / "research" / "RESEARCH_INDEX.md").read_text(
    encoding="utf-8"
)
CONTRACT = (
    ROOT / "docs" / "research" / "EPISTEMIC_PROMOTION_REVISION_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")
OWNER_GO = (
    ROOT / "docs" / "research" / "EPISTEMIC_PROMOTION_REVISION_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")
IMPLEMENTATION = (
    ROOT / "docs" / "research" / "EPISTEMIC_PROMOTION_REVISION_IMPLEMENTATION_V0_1.md"
).read_text(encoding="utf-8")


def test_historical_surfaces_retain_phase4_frozen_state() -> None:
    for document in (STATUS, ROADMAP, INDEX, CONTRACT):
        assert "EPR-v0.1" in document
        assert "PURE_EPISTEMIC_CHANGE_ROUTER" in document
        assert "PHASE_4_OWNER_GO" in document
        assert "NOT_GRANTED" in document
        assert "PHASE_4_RUNTIME" in document
        assert "NOT_AUTHORIZED" in document
        assert "CLAIM_TO_BELIEF_BINDING" in document
        assert "NOT_IMPLEMENTED" in document
        assert "TERMINAL_RECONSIDERATION_LINEAGE" in document

    assert "PHASE_4_EPISTEMIC_PROMOTION_REVISION_READINESS_READY" in STATUS
    assert "PHASE_4_CANDIDATE_SELECTION_SELECTED" in STATUS
    assert "PHASE_4_IMPLEMENTATION_CONTRACT_FROZEN_DOCS" in STATUS
    assert "PHASE_4_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "Phase 4 readiness:            READY · FROZEN_DOCS · DOCS_ONLY" in ROADMAP
    assert "Phase 4 contract:             FROZEN_DOCS · EPR-v0.1" in ROADMAP
    assert "Phase 4 implementation:       NOT_STARTED" in ROADMAP
    assert "Phase 4 readiness:            READY · DOCS_ONLY" in INDEX
    assert "Phase 4 contract:             FROZEN_DOCS · EPR-v0.1" in INDEX
    assert "Phase 4 implementation:       NOT_STARTED" in INDEX


def test_phase4_freeze_preserves_existing_owners() -> None:
    assert "P0-014" in CONTRACT or "P0_014" in CONTRACT
    assert "P0-015" in CONTRACT or "P0_015" in CONTRACT
    assert "Evidence Gate remains sole support/contradiction authority" in STATUS
    assert "P0-015 remains sole owner" in ROADMAP
    assert "Evidence Gate remains the sole owner" in INDEX
    assert "P0-015 Evidence Gate authority:      UNCHANGED" in CONTRACT


def test_later_epr_implementation_go_does_not_grant_runtime_authority() -> None:
    assert (ROOT / "src" / "mentaury" / "epistemic_change").exists()
    assert "Owner GO:                          GRANTED" in OWNER_GO
    assert "Runtime GO:                        NOT_GRANTED" in OWNER_GO
    assert "Runtime activation: NONE" in IMPLEMENTATION
    for marker in (
        "PHASE_4_RUNTIME_NOT_AUTHORIZED",
        "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS_READY",
        "PHASE_5_CANDIDATE_SELECTION_SELECTED",
        "PHASE_5_IMPLEMENTATION_CONTRACT_FROZEN_DOCS",
        "PHASE_5_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
        "PHASE_5_OWNER_GO_CONSUMED_BY_PR_119",
        "PHASE_5_RUNTIME_NOT_AUTHORIZED",
        "PHASE_6_RUNTIME_NOT_AUTHORIZED",
        "ACTION_GATE_NOT_AUTHORIZED",
        "RETRIEVAL_EXECUTION_NOT_AUTHORIZED",
        "TOOL_EXECUTION_NOT_AUTHORIZED",
        "DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN",
        "RUNTIME_DEPLOYMENT_NOT_AUTHORIZED",
    ):
        assert marker in STATUS


def test_phase4_reconciliation_records_verified_contract_freeze() -> None:
    for document in (STATUS, ROADMAP, INDEX):
        assert "#106" in document
        assert "e95d1539c5023ce36d83652bdb3d482c4090f2ef" in document
        assert "31574946826" in document
        assert "927 passed" in document
        assert "4914115826" in document
        assert "8a86b9c4eff9435bbf8724defaee6e399a4cdeb0" in document
        assert "31575119904" in document


def test_historical_phase4_owner_go_absence_is_not_rewritten_retroactively() -> None:
    assert "PHASE_4_OWNER_GO_NOT_GRANTED" in STATUS
    assert "PHASE_4_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "Phase 4 Owner GO:             NOT_GRANTED" in ROADMAP
    assert "Phase 4 Owner GO:             NOT_GRANTED" in INDEX
    assert "new explicit Owner GO" in CONTRACT
    assert "Historical documents" in OWNER_GO

    for surface in (STATUS, ROADMAP, INDEX):
        assert "PURE_ANCHORED_TYPED_RELATION_RECORD" in surface
        assert "FROZEN_DOCS" in surface
        assert "PHASE_5_OWNER_GO" in surface
        assert "CONSUMED" in surface
        assert "PHASE_5_IMPLEMENTATION" in surface
        assert "IMPLEMENTED_BOUNDED" in surface
        assert "PHASE_5_RUNTIME" in surface
        assert "NOT_AUTHORIZED" in surface
