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

CURRENT_SURFACES = (STATUS, ROADMAP, INDEX)


def test_all_current_surfaces_record_phase5_implemented_bounded() -> None:
    for surface in CURRENT_SURFACES:
        assert "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS" in surface
        assert "ANCHORED_TYPED_RELATION_CANDIDATE" in surface
        assert "PURE_ANCHORED_TYPED_RELATION_RECORD" in surface
        assert "PHASE_5_IMPLEMENTATION_CONTRACT" in surface
        assert "FROZEN_DOCS" in surface
        assert "ATR-v0.1" in surface or "ATR_V0_1" in surface
        assert "PHASE_5_IMPLEMENTATION" in surface
        assert "IMPLEMENTED_BOUNDED" in surface
        assert "PHASE_5_OWNER_GO" in surface
        assert "CONSUMED" in surface
        assert "#119" in surface
        assert "PHASE_5_RUNTIME" in surface
        assert "NOT_AUTHORIZED" in surface


def test_current_status_records_exact_phase5_completion_boundary() -> None:
    for marker in (
        "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS_READY",
        "POST_PHASE_4_COGNITIVE_MILESTONE_DISCRIMINATION_COMPLETE",
        "PHASE_5_CANDIDATE_SELECTION_SELECTED",
        "PHASE_5_CANDIDATE_PURE_ANCHORED_TYPED_RELATION_RECORD",
        "PHASE_5_IMPLEMENTATION_CONTRACT_FROZEN_DOCS",
        "PHASE_5_CONTRACT_VERSION_ATR_V0_1",
        "PHASE_5_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
        "PHASE_5_OWNER_GO_CONSUMED_BY_PR_119",
        "PHASE_5_OWNER_GO_SCOPE_ATR_V0_1_ONLY",
        "PHASE_5_IMPLEMENTATION_AUTHORIZATION_CONSUMED_ATR_V0_1_ONLY",
        "PHASE_5_ATR_T01_T16_EXECUTABLE_PASS",
        "PHASE_5_ATR_M01_M12_EXECUTABLE_PASS",
        "PHASE_5_ATR_P01_P12_EXECUTABLE_PASS",
        "PHASE_5_RUNTIME_NOT_AUTHORIZED",
        "PHASE_6_RESEARCH_PREPARATION_AUTHORIZED_DOCS_TESTS_ONLY",
        "PHASE_6_RUNTIME_NOT_AUTHORIZED",
    ):
        assert marker in STATUS


def test_roadmap_and_index_link_all_owning_phase5_documents() -> None:
    for surface in (ROADMAP, INDEX):
        for path in (
            "POST_PHASE4_COGNITIVE_MILESTONE_DISCRIMINATION.md",
            "TYPED_RELATIONS_CONTRACT_READINESS.md",
            "TYPED_RELATIONS_CANDIDATE_SELECTION.md",
            "TYPED_RELATIONS_PURE_RECORD_CONTRACT_V0_1.md",
            "TYPED_RELATIONS_OWNER_GO_DECISION.md",
        ):
            assert path in surface
        assert "ATR-v0.1 IMPLEMENTED_BOUNDED ≠ runtime authority" in surface


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


def test_current_surfaces_retain_contract_freeze_evidence() -> None:
    for surface in CURRENT_SURFACES:
        for marker in (
            "#114",
            "fef6b21c4d3062a228471ccd206297b25d2d3ecc",
            "31592892692",
            "970 passed",
            "4916049299",
            "083825e1cc7b69c133650b51afb8fc1d34b97533",
            "31593058722",
        ):
            assert marker in surface


def test_current_surfaces_record_verified_pr119_implementation() -> None:
    for surface in CURRENT_SURFACES:
        for marker in (
            "#119",
            "63ae721e830fb56b659a4f0cfe8e1be27467d6e6",
            "31870356904",
            "1059 passed",
            "4943131188",
            "398c9be48b7764d63aee532f267df837be7e4e3b",
            "31870435973",
        ):
            assert marker in surface


def test_phase4_epr_remains_unimplemented_and_unauthorized() -> None:
    assert "PHASE_4_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "PHASE_4_OWNER_GO_NOT_GRANTED" in STATUS
    assert "PHASE_4_RUNTIME_NOT_AUTHORIZED" in STATUS
    for surface in (ROADMAP, INDEX):
        assert "Phase 4 implementation:       NOT_STARTED" in surface
        assert "Phase 4 Owner GO:             NOT_GRANTED" in surface
        assert "Phase 4 runtime:              NOT_AUTHORIZED" in surface


def test_owner_go_is_historical_grant_but_currently_consumed() -> None:
    assert "Owner GO:                       GRANTED" in OWNER_GO
    assert "Owner GO scope:                 ATR-v0.1_ONLY" in OWNER_GO
    assert "Single-use authorization:       YES" in OWNER_GO
    assert "Phase 5 runtime:                NOT_AUTHORIZED" in OWNER_GO
    assert "Phase 6 runtime:                NOT_AUTHORIZED" in OWNER_GO
    assert "new explicit single-use Owner GO" in CONTRACT
    assert "PHASE_5_OWNER_GO_CONSUMED_BY_PR_119" in STATUS
    assert "PHASE_5_IMPLEMENTATION_IMPLEMENTED_BOUNDED" in STATUS
