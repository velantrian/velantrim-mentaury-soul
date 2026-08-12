"""Structural guards for verified NPG-COMP-v0.1 Phase 2 completion."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = (
    ROOT / "docs" / "NON_PROJECTION_RUNTIME_COMPOSITION_IMPLEMENTATION_AUTHORIZATION.md"
).read_text(encoding="utf-8")
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


def test_completion_receipt_records_exact_verified_implementation() -> None:
    for marker in (
        "OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED",
        "NPG-COMP-v0.1_ONLY",
        "Implementation PR:         #96",
        "8a7b524de46c042e0479186ea4564f363248a366",
        "31548525699 · SUCCESS · 842 passed",
        "4911798445",
        "153d64d142e5b5555bc3a942cb0beedce89b91e0",
        "31548659423 · SUCCESS · 842 passed",
        "Correctness pass:           PASS",
        "Adversarial pass:           PASS",
        "Authorization boundary:     PRESERVED",
        "Independent human review:   NO",
    ):
        assert marker in RECEIPT


def test_current_surfaces_share_phase_2_completion_state() -> None:
    for document in (STATUS, ROADMAP, INDEX, RECEIPT):
        assert "NPG-COMP-v0.1" in document
        assert "CONSUMED_BY_PR_96" in document
        assert "IMPLEMENTED_BOUNDED" in document
        assert "NON_PROJECTION_RUNTIME" in document
        assert "NOT_AUTHORIZED" in document
        assert "P1_004" in document
        assert "NOT_ASSIGNED" in document

    assert "PHASE_2_NPG_SHADOW_COMPOSITION_IMPLEMENTED_BOUNDED" in STATUS
    assert "Phase 2 implementation:       IMPLEMENTED_BOUNDED" in ROADMAP
    assert "Phase 2 implementation:       IMPLEMENTED_BOUNDED" in INDEX


def test_single_use_owner_go_is_consumed_not_reusable() -> None:
    assert "single-use" in GO
    assert "PHASE_2_OWNER_GO = CONSUMED_BY_PR_96" in RECEIPT
    assert "It cannot authorize any later runtime wiring" in RECEIPT
    assert "NPG-COMP-v0.1 Owner GO consumed ≠ reusable authority" in ROADMAP
    assert "NPG-COMP-v0.1 Owner GO consumed ≠ reusable authority" in INDEX


def test_exact_three_file_source_surface_is_retained() -> None:
    package = ROOT / "src" / "mentaury" / "composition" / "non_projection_shadow"
    assert {path.name for path in package.glob("*.py")} == {
        "__init__.py",
        "contracts.py",
        "coordinator.py",
    }
    for path in (
        "src/mentaury/composition/non_projection_shadow/__init__.py",
        "src/mentaury/composition/non_projection_shadow/contracts.py",
        "src/mentaury/composition/non_projection_shadow/coordinator.py",
    ):
        assert path in RECEIPT
        assert path in STATUS


def test_frozen_nrc_families_are_completion_evidence() -> None:
    assert "NRC-T01…NRC-T12" in RECEIPT
    assert "NRC-M01…NRC-M10" in RECEIPT
    tests = (ROOT / "tests" / "test_non_projection_shadow_composition.py").read_text(
        encoding="utf-8"
    )
    assert 'tuple(f"NRC-T{i:02d}" for i in range(1, 13))' in tests
    assert 'f"NRC-M{i:02d}" for i in range(1, 11)' in tests
    assert 'ids=[f"NRC-T{i:02d}" for i in range(1, 13)]' in tests
    assert "test_nrc_metamorphic_contract_families_are_behaviorally_covered" in tests


def test_completion_preserves_all_negative_authority_boundaries() -> None:
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
        "PHASE_3_PROVENANCE_CLAIM_REPRESENTATION = NOT_STARTED",
        "PHASE_3_OWNER_GO = NOT_GRANTED",
    ):
        assert marker in RECEIPT


def test_positive_result_stays_classification_evidence_only() -> None:
    for marker in (
        "≠ truth proof",
        "≠ Mentaury autobiography",
        "≠ stable identity trait",
        "≠ capability or Action Gate PASS",
        "≠ retrieval permission",
        "≠ tool permission",
        "≠ execution permission",
        "≠ M3 authority",
        "≠ deployment permission",
    ):
        assert marker in RECEIPT


def test_next_milestone_is_not_selected_or_authorized() -> None:
    assert "NEXT_BOUNDED_MILESTONE = NOT_SELECTED · NOT_AUTHORIZED" in STATUS
    assert "Next bounded milestone:       NOT_SELECTED · NOT_AUTHORIZED" in ROADMAP
    assert "Next execution milestone:     NOT_SELECTED · NOT_AUTHORIZED" in INDEX
    assert "PHASE_3_PROVENANCE_CLAIM_REPRESENTATION = NOT_STARTED" in RECEIPT
    assert "PHASE_3_OWNER_GO = NOT_GRANTED" in RECEIPT
