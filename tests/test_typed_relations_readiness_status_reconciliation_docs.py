"""Structural guards for Phase 5 Typed Relations readiness status reconciliation."""

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
DISCRIMINATION = (
    ROOT
    / "docs"
    / "research"
    / "POST_PHASE4_COGNITIVE_MILESTONE_DISCRIMINATION.md"
).read_text(encoding="utf-8")

SURFACES = (STATUS, ROADMAP, INDEX)


def test_all_truth_surfaces_expose_phase5_readiness_without_implementation() -> None:
    for surface in SURFACES:
        assert "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS" in surface
        assert "ANCHORED_TYPED_RELATION_CANDIDATE" in surface
        assert "PHASE_5_CANDIDATE_SELECTION" in surface
        assert "NOT_STARTED" in surface
        assert "PHASE_5_IMPLEMENTATION_CONTRACT" in surface
        assert "NOT_FROZEN" in surface
        assert "PHASE_5_IMPLEMENTATION" in surface
        assert "PHASE_5_OWNER_GO" in surface
        assert "NOT_GRANTED" in surface
        assert "PHASE_5_RUNTIME" in surface
        assert "NOT_AUTHORIZED" in surface


def test_current_status_no_longer_collapses_readiness_into_not_started() -> None:
    assert "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS_READY" in STATUS
    assert "PHASE_5_TYPED_RELATIONS_NOT_STARTED" not in STATUS
    assert "POST_PHASE_4_COGNITIVE_MILESTONE_DISCRIMINATION_COMPLETE" in STATUS


def test_roadmap_and_index_link_owning_phase5_documents() -> None:
    for surface in (ROADMAP, INDEX):
        assert "POST_PHASE4_COGNITIVE_MILESTONE_DISCRIMINATION.md" in surface
        assert "TYPED_RELATIONS_CONTRACT_READINESS.md" in surface
        assert "Phase 5 READINESS_READY ≠ candidate selection / contract freeze / Owner GO" in surface


def test_relation_authority_ceiling_is_visible_across_navigation() -> None:
    for surface in (ROADMAP, INDEX):
        for marker in (
            "RELATION ≠ TRUTH",
            "RELATION TYPE ≠ CONFIDENCE",
            "CORRELATIONAL ≠ CAUSAL",
            "ANALOGICAL ≠ MECHANISTIC",
            "EVIDENTIAL ≠ SUPPORTED",
            "CONTRADICTORY ≠ EvidenceGateOutcome.CONTRADICTED",
        ):
            assert marker in surface


def test_owning_readiness_and_discrimination_remain_non_implementation() -> None:
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


def test_phase4_epr_remains_unimplemented_and_unauthorized() -> None:
    assert "PHASE_4_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "PHASE_4_OWNER_GO_NOT_GRANTED" in STATUS
    assert "PHASE_4_RUNTIME_NOT_AUTHORIZED" in STATUS
    for surface in (ROADMAP, INDEX):
        assert "Phase 4 implementation:       NOT_STARTED" in surface
        assert "Phase 4 Owner GO:             NOT_GRANTED" in surface
        assert "Phase 4 runtime:              NOT_AUTHORIZED" in surface


def test_next_boundary_is_docs_only_candidate_and_contract_freeze() -> None:
    for surface in (STATUS, ROADMAP):
        assert "PHASE_5_TYPED_RELATIONS_CANDIDATE_SELECTION_AND_CONTRACT_FREEZE" in surface
    assert "STOP" in STATUS
    assert "STOP" in ROADMAP
