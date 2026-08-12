"""Structural guards for verified PCR-v0.1 Phase 3 completion."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = (
    ROOT / "docs" / "PROVENANCE_CLAIM_REPRESENTATION_IMPLEMENTATION_AUTHORIZATION.md"
).read_text(encoding="utf-8")
GO = (
    ROOT / "docs" / "research" / "PROVENANCE_CLAIM_REPRESENTATION_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)
INDEX = (ROOT / "docs" / "research" / "RESEARCH_INDEX.md").read_text(
    encoding="utf-8"
)


def test_completion_receipt_records_exact_verified_implementation() -> None:
    for marker in (
        "OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED",
        "PCR-v0.1_ONLY",
        "Implementation PR:         #103",
        "11aec32bf499fc8925ab685dadc4a626325da892",
        "31570253296 · SUCCESS · 909 passed",
        "4913627170",
        "c63488af7f10bf3e7f423fee8071a13f4c2e02db",
        "31570390275 · SUCCESS · 909 passed",
        "Merge signature:            VERIFIED · VALID",
        "Correctness pass:           PASS",
        "Adversarial pass:           PASS",
        "Authorization boundary:     PRESERVED",
        "Independent human review:   NO",
    ):
        assert marker in RECEIPT


def test_single_use_owner_go_is_consumed_not_reusable() -> None:
    assert "Single-use authorization:       YES" in GO
    assert "Owner GO:                       GRANTED" in GO
    assert "PHASE_3_OWNER_GO = CONSUMED_BY_PR_103" in RECEIPT
    assert "It cannot authorize Phase 4" in RECEIPT
    assert "PCR-v0.1 Owner GO consumed ≠ reusable authority" in ROADMAP
    assert "PCR-v0.1 Owner GO consumed ≠ reusable authority" in INDEX


def test_exact_three_file_source_surface_is_retained() -> None:
    package = ROOT / "src" / "mentaury" / "claims"
    assert {path.name for path in package.glob("*.py")} == {
        "__init__.py",
        "contracts.py",
        "representation.py",
    }
    for path in (
        "src/mentaury/claims/__init__.py",
        "src/mentaury/claims/contracts.py",
        "src/mentaury/claims/representation.py",
    ):
        assert path in RECEIPT
        assert path in STATUS


def test_frozen_pcr_families_are_completion_evidence() -> None:
    for marker in (
        "PCR-T01…PCR-T12 = EXECUTABLE · PASS",
        "PCR-M01…PCR-M10 = EXECUTABLE · PASS",
        "PCR-P01…PCR-P08 = EXECUTABLE · PASS",
    ):
        assert marker in RECEIPT
    tests = (ROOT / "tests" / "test_provenance_claim_representation.py").read_text(
        encoding="utf-8"
    )
    assert 'ids=[f"PCR-T{i:02d}" for i in range(1, 13)]' in tests
    assert '[f"PCR-M{i:02d}" for i in range(1, 11)]' in tests
    assert '[f"PCR-P{i:02d}" for i in range(1, 9)]' in tests


def test_current_navigation_surfaces_share_phase3_completion_state() -> None:
    for document in (STATUS, ROADMAP, INDEX, RECEIPT):
        assert "PCR-v0.1" in document
        assert "PURE_PROVENANCE_CLAIM_RECORD" in document
        assert "CONSUMED_BY_PR_103" in document
        assert "IMPLEMENTED_BOUNDED" in document
        assert "PHASE_3_RUNTIME" in document or "Phase 3 runtime" in document
        assert "NOT_AUTHORIZED" in document
        assert "PHASE_4" in document or "Phase 4" in document
        assert "NOT_STARTED" in document
        assert "NOT_GRANTED" in document

    assert "PHASE_3_PROVENANCE_CLAIM_REPRESENTATION_IMPLEMENTED_BOUNDED" in STATUS
    assert "PHASE_3_OWNER_GO_CONSUMED_BY_PR_103" in STATUS
    assert "Phase 3 implementation:       IMPLEMENTED_BOUNDED" in ROADMAP
    assert "Phase 3 Owner GO:             CONSUMED_BY_PR_103" in ROADMAP
    assert "Phase 3 implementation:       IMPLEMENTED_BOUNDED" in INDEX
    assert "Phase 3 Owner GO:             CONSUMED_BY_PR_103" in INDEX


def test_completion_preserves_representation_only_boundary() -> None:
    for marker in (
        "ClaimClass ≠ ClaimType ≠ EpistemicRole",
        "SOURCE / PROVENANCE ≠ CLAIM ≠ EVIDENCE STATUS ≠ BELIEF STATUS ≠ TRUTH",
        "Evidence Gate remains the sole owner of `SUPPORTED / CONTRADICTED`",
        "Source-level\nresearch admission remains separately owned",
        "not a bearer token",
    ):
        assert marker in RECEIPT


def test_completion_preserves_negative_authority_ceiling() -> None:
    for marker in (
        "PHASE_3_RUNTIME = NOT_AUTHORIZED",
        "PHASE_4_EPISTEMIC_PROMOTION_REVISION = NOT_STARTED",
        "PHASE_4_OWNER_GO = NOT_GRANTED",
        "NON_PROJECTION_RUNTIME = NOT_AUTHORIZED",
        "P1_004 = NOT_ASSIGNED",
        "ACTION_GATE = NOT_AUTHORIZED",
        "RETRIEVAL_EXECUTION = NOT_AUTHORIZED",
        "ATLAS_ACCESS = NOT_AUTHORIZED",
        "TOOL_EXECUTION = NOT_AUTHORIZED",
        "IDENTITY_RUNTIME = NOT_AUTHORIZED",
        "RELATIONSHIP_RUNTIME = NOT_AUTHORIZED",
        "DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN",
        "PERSISTENCE = NOT_AUTHORIZED",
        "RUNTIME_DEPLOYMENT = NOT_AUTHORIZED",
        "AUTONOMOUS_BACKGROUND_LOOP = NOT_AUTHORIZED",
        "NEXT_BOUNDED_MILESTONE = NOT_SELECTED · NOT_AUTHORIZED",
    ):
        assert marker in RECEIPT
