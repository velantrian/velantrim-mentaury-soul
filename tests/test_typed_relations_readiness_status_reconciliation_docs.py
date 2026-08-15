"""Structural guards for current Phase 5 ATR-v0.1 status reconciliation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (
    ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md"
).read_text(encoding="utf-8")
INDEX = (ROOT / "docs" / "research" / "RESEARCH_INDEX.md").read_text(
    encoding="utf-8"
)
READINESS = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_CONTRACT_READINESS.md"
).read_text(encoding="utf-8")
SELECTION = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_CANDIDATE_SELECTION.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_PURE_RECORD_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")
DISCRIMINATION = (
    ROOT
    / "docs"
    / "research"
    / "POST_PHASE4_COGNITIVE_MILESTONE_DISCRIMINATION.md"
).read_text(encoding="utf-8")
OWNER_GO = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")

SURFACES = (STATUS, ROADMAP, INDEX)


def test_all_truth_surfaces_preserve_phase5_contract_freeze_checkpoint() -> None:
    for surface in SURFACES:
        assert "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS" in surface
        assert "ANCHORED_TYPED_RELATION_CANDIDATE" in surface
        assert "PHASE_5_CANDIDATE_SELECTION" in surface
        assert "SELECTED" in surface
        assert "PURE_ANCHORED_TYPED_RELATION_RECORD" in surface
        assert "PHASE_5_IMPLEMENTATION_CONTRACT" in surface
        assert "FROZEN_DOCS" in surface
        assert "ATR-v0.1" in surface or "ATR_V0_1" in surface
        assert "PHASE_5_IMPLEMENTATION" in surface
        assert "NOT_STARTED" in surface
        assert "PHASE_5_OWNER_GO" in surface
        assert "NOT_GRANTED" in surface
        assert "PHASE_5_RUNTIME" in surface
        assert "NOT_AUTHORIZED" in surface


def test_current_status_no_longer_collapses_readiness_into_not_started() -> None:
    assert "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS_READY" in STATUS
    assert "PHASE_5_TYPED_RELATIONS_NOT_STARTED" not in STATUS
    assert "POST_PHASE_4_COGNITIVE_MILESTONE_DISCRIMINATION_COMPLETE" in STATUS
    assert "PHASE_5_CANDIDATE_SELECTION_SELECTED" in STATUS
    assert "PHASE_5_CANDIDATE_PURE_ANCHORED_TYPED_RELATION_RECORD" in STATUS
    assert "PHASE_5_IMPLEMENTATION_CONTRACT_FROZEN_DOCS" in STATUS
    assert "PHASE_5_CONTRACT_VERSION_ATR_V0_1" in STATUS


def test_roadmap_and_index_link_all_owning_phase5_documents() -> None:
    for surface in (ROADMAP, INDEX):
        assert "POST_PHASE4_COGNITIVE_MILESTONE_DISCRIMINATION.md" in surface
        assert "TYPED_RELATIONS_CONTRACT_READINESS.md" in surface
        assert "TYPED_RELATIONS_CANDIDATE_SELECTION.md" in surface
        assert "TYPED_RELATIONS_PURE_RECORD_CONTRACT_V0_1.md" in surface
        assert "Phase 5 READINESS_READY ≠ candidate selection / contract freeze / Owner GO" in surface
        assert "ATR-v0.1 FROZEN_DOCS ≠ Owner GO / implementation / runtime authority" in surface


def test_relation_authority_ceiling_is_visible_across_navigation() -> None:
    for surface in (ROADMAP, INDEX):
        for marker in (
            "RELATION ≠ TRUTH",
            "RELATION TYPE ≠ CONFIDENCE",
            "CORRELATIONAL ≠ CAUSAL",
            "ANALOGICAL ≠ MECHANISTIC",
            "EVIDENTIAL ≠ SUPPORTED",
            "CONTRADICTORY ≠ EvidenceGateOutcome.CONTRADICTED",
            "GRAPH LINK / PATH / COUNT ≠ EPISTEMIC AUTHORITY",
        ):
            assert marker in surface


def test_owning_readiness_preserves_historical_pre_selection_state() -> None:
    assert "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS = READY" in READINESS
    assert "PHASE_5_CANDIDATE_SELECTION = NOT_STARTED" in READINESS
    assert "PHASE_5_IMPLEMENTATION_CONTRACT = NOT_FROZEN" in READINESS
    assert "PHASE_5_OWNER_GO = NOT_GRANTED" in READINESS
    assert "PHASE_5_RUNTIME = NOT_AUTHORIZED" in READINESS
    assert (
        "NEXT_BOUNDED_READINESS_MILESTONE = "
        "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS"
    ) in DISCRIMINATION
    assert "NEXT_IMPLEMENTATION_MILESTONE = NOT_SELECTED" in DISCRIMINATION


def test_selection_and_contract_preserve_freeze_time_state() -> None:
    assert "PHASE_5_TYPED_RELATIONS_CANDIDATE_SELECTION = SELECTED" in SELECTION
    assert "PHASE_5_TYPED_RELATIONS_CANDIDATE = PURE_ANCHORED_TYPED_RELATION_RECORD" in SELECTION
    assert "PHASE_5_TYPED_RELATIONS_CONTRACT_VERSION = ATR-v0.1" in SELECTION
    assert "PHASE_5_TYPED_RELATIONS_IMPLEMENTATION_CONTRACT = FROZEN_DOCS" in CONTRACT
    assert "PHASE_5_TYPED_RELATIONS_CONTRACT_VERSION = ATR-v0.1" in CONTRACT
    assert "PHASE_5_TYPED_RELATIONS_IMPLEMENTATION = NOT_STARTED" in CONTRACT
    assert "PHASE_5_TYPED_RELATIONS_OWNER_GO = NOT_GRANTED" in CONTRACT
    assert "PHASE_5_TYPED_RELATIONS_RUNTIME = NOT_AUTHORIZED" in CONTRACT


def test_current_surfaces_record_verified_pr114_contract_freeze() -> None:
    for surface in SURFACES:
        assert "#114" in surface
        assert "fef6b21c4d3062a228471ccd206297b25d2d3ecc" in surface
        assert "31592892692" in surface
        assert "970 passed" in surface
        assert "4916049299" in surface
        assert "083825e1cc7b69c133650b51afb8fc1d34b97533" in surface
        assert "31593058722" in surface


def test_phase4_epr_remains_unimplemented_and_unauthorized() -> None:
    assert "PHASE_4_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "PHASE_4_OWNER_GO_NOT_GRANTED" in STATUS
    assert "PHASE_4_RUNTIME_NOT_AUTHORIZED" in STATUS
    for surface in (ROADMAP, INDEX):
        assert "Phase 4 implementation:       NOT_STARTED" in surface
        assert "Phase 4 Owner GO:             NOT_GRANTED" in surface
        assert "Phase 4 runtime:              NOT_AUTHORIZED" in surface


def test_separate_single_use_owner_go_now_supersedes_freeze_time_stop_for_implementation_only() -> None:
    assert "Owner GO:                       GRANTED" in OWNER_GO
    assert "Owner GO scope:                 ATR-v0.1_ONLY" in OWNER_GO
    assert "Single-use authorization:       YES" in OWNER_GO
    assert "Phase 5 runtime:                NOT_AUTHORIZED" in OWNER_GO
    assert "Phase 6 runtime:                NOT_AUTHORIZED" in OWNER_GO
    assert "new explicit single-use Owner GO" in CONTRACT
    assert "src/mentaury/relations/**" in STATUS
