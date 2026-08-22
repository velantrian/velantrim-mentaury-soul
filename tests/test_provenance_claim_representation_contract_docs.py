"""Structural guards for the docs-only Phase 3 PCR-v0.1 contract freeze."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = (
    ROOT / "docs" / "research" / "PROVENANCE_CLAIM_REPRESENTATION_READINESS.md"
).read_text(encoding="utf-8")
SELECTION = (
    ROOT
    / "docs"
    / "research"
    / "PROVENANCE_CLAIM_REPRESENTATION_CANDIDATE_SELECTION.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT / "docs" / "research" / "PROVENANCE_CLAIM_REPRESENTATION_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)
INDEX = (ROOT / "docs" / "research" / "RESEARCH_INDEX.md").read_text(
    encoding="utf-8"
)


def test_phase3_readiness_and_candidate_are_bounded() -> None:
    assert "READINESS_READY · DOCS_ONLY" in READINESS
    assert "PURE_PROVENANCE_CLAIM_RECORD" in SELECTION
    for document in (READINESS, SELECTION, CONTRACT):
        assert "Owner GO" in document
        assert "NOT_GRANTED" in document or "NOT GRANTED" in document
        assert "NOT_STARTED" in document
        assert "FORBIDDEN" in document


def test_claim_axes_are_explicitly_distinct() -> None:
    for document in (READINESS, CONTRACT):
        assert "ClaimClass" in document
        assert "ClaimType" in document
    assert "epistemic role" in READINESS.lower()
    assert "EpistemicRole" in CONTRACT
    assert "ClaimClass\n≠ ClaimType\n≠ EpistemicRole" in CONTRACT
    for role in (
        "OBSERVATION",
        "TESTIMONY",
        "EVIDENCE_CANDIDATE",
        "HYPOTHESIS",
        "INFERENCE",
        "INTERPRETATION",
        "METAPHORICAL_EXPRESSION",
        "UNKNOWN",
    ):
        assert role in CONTRACT


def test_evidence_gate_remains_the_only_support_owner() -> None:
    for document in (READINESS, CONTRACT):
        assert "Evidence Gate" in document
        assert "SUPPORTED" in document
        assert "CONTRADICTED" in document
    assert "`evidence_refs` are references only" in CONTRACT
    assert "≠ EvidenceGateOutcome.SUPPORTED" in CONTRACT
    assert "≠ EvidenceGateOutcome.CONTRADICTED" in CONTRACT


def test_source_admission_is_not_duplicated() -> None:
    assert "source-level research admission" in READINESS
    assert "does not execute, duplicate or replace that gate" in READINESS
    assert "Source admission authority:          NONE" in CONTRACT
    assert "source admission result" in CONTRACT


def test_frozen_api_and_reserved_package_are_exact() -> None:
    package = ROOT / "src" / "mentaury" / "claims"
    expected = {"__init__.py", "contracts.py", "representation.py"}
    for path in (
        "src/mentaury/claims/__init__.py",
        "src/mentaury/claims/contracts.py",
        "src/mentaury/claims/representation.py",
    ):
        assert path in SELECTION
        assert path in CONTRACT
    assert "def represent_provenance_claim(" in CONTRACT
    assert package.exists()
    assert {path.name for path in package.glob("*.py")} == expected


def test_frozen_threat_metamorphic_and_purity_families_are_complete() -> None:
    for index in range(1, 13):
        assert f"PCR-T{index:02d}" in CONTRACT
    for index in range(1, 11):
        assert f"PCR-M{index:02d}" in CONTRACT
    for index in range(1, 9):
        assert f"PCR-P{index:02d}" in CONTRACT


def test_no_numeric_pseudo_precision_or_authority_laundering() -> None:
    for forbidden_input in (
        "confidence / probability / reliability score",
        "EvidenceGateOutcome / EvidenceGateReceipt",
        "BeliefStatus / promotion decision",
        "retriever / Atlas / graph / database / filesystem",
        "tool / Action Gate handle",
        "identity / relationship registry",
    ):
        assert forbidden_input in CONTRACT
    for marker in (
        "Retrieval / Atlas authority:         NONE",
        "Direct or indirect M3 write:         FORBIDDEN",
        "Persistence authority:               NONE",
        "Deployment authority:                NONE",
    ):
        assert marker in CONTRACT


def test_current_navigation_surfaces_preserve_phase3_contract_identity() -> None:
    for document in (STATUS, ROADMAP, INDEX):
        assert "PCR-v0.1" in document
        assert "PURE_PROVENANCE_CLAIM_RECORD" in document
        assert "FROZEN_DOCS" in document
        assert "NOT_AUTHORIZED" in document

    # Readiness/selection remain frozen historical documents; the current
    # authoritative state must now report the consumed implementation outcome.
    assert "PHASE_3_PROVENANCE_CLAIM_REPRESENTATION_IMPLEMENTED_BOUNDED" in STATUS
    assert "PHASE_3_IMPLEMENTATION_CONTRACT_FROZEN_DOCS" in STATUS
    assert "PHASE_3_CONTRACT_VERSION_PCR_V0_1" in STATUS
    assert "PHASE_3_OWNER_GO_CONSUMED_BY_PR_103" in STATUS
    assert "PHASE_3_RUNTIME_NOT_AUTHORIZED" in STATUS


def test_phase3_contract_does_not_authorize_phase4_or_runtime() -> None:
    assert "Belief promotion/revision authority: NONE" in CONTRACT
    assert "Runtime activation:                  NOT_AUTHORIZED" in CONTRACT
    for document in (STATUS, ROADMAP, INDEX):
        assert "Phase 4" in document or "PHASE_4" in document
    assert "PHASE_4_EPISTEMIC_PROMOTION_REVISION_READINESS_READY" in STATUS
    assert "PHASE_4_IMPLEMENTATION_CONTRACT_FROZEN_DOCS" in STATUS
    # Historical pre-implementation literals remain retained below the current
    # checkpoint, while current truth records the later bounded implementation.
    assert "PHASE_4_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "PHASE_4_OWNER_GO_NOT_GRANTED" in STATUS
    assert "PHASE_4_IMPLEMENTATION_IMPLEMENTED_BOUNDED" in STATUS
    assert "PHASE_4_OWNER_GO_CONSUMED_BY_PR_148" in STATUS
    assert "PHASE_4_RUNTIME_NOT_AUTHORIZED" in STATUS
