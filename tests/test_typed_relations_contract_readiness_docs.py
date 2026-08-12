"""Structural guards for Phase 5 Typed Relations contract readiness."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_CONTRACT_READINESS.md"
).read_text(encoding="utf-8")
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
PCR = (
    ROOT
    / "docs"
    / "research"
    / "PROVENANCE_CLAIM_REPRESENTATION_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")
EPR = (
    ROOT
    / "docs"
    / "research"
    / "EPISTEMIC_PROMOTION_REVISION_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_readiness_is_docs_only_and_not_implementation_authority() -> None:
    for marker in (
        "Status:                              READY · FROZEN_DOCS · DOCS_ONLY",
        "PHASE_5_TYPED_RELATIONS_CONTRACT_READINESS = READY",
        "PHASE_5_CANDIDATE_SELECTION = NOT_STARTED",
        "PHASE_5_IMPLEMENTATION_CONTRACT = NOT_FROZEN",
        "PHASE_5_IMPLEMENTATION = NOT_STARTED",
        "PHASE_5_OWNER_GO = NOT_GRANTED",
        "PHASE_5_RUNTIME = NOT_AUTHORIZED",
        "READINESS READY ≠ IMPLEMENTATION CONTRACT ≠ OWNER GO",
    ):
        assert marker in READINESS


def test_relation_vocabulary_is_closed_and_preserves_unknown() -> None:
    for relation_type in (
        "CAUSAL",
        "CORRELATIONAL",
        "TEMPORAL",
        "ANALOGICAL",
        "TAXONOMIC",
        "MECHANISTIC",
        "EVIDENTIAL",
        "CONTRADICTORY",
        "UNKNOWN",
    ):
        assert relation_type in READINESS
    assert "core vocabulary must be **closed**" in READINESS
    assert "UNKNOWN cannot be implicitly upgraded" in READINESS


def test_relation_semantics_cannot_launder_epistemic_authority() -> None:
    for invariant in (
        "CORRELATIONAL\n≠ CAUSAL",
        "ANALOGICAL\n≠ MECHANISTIC",
        "TEMPORAL\n≠ CAUSAL",
        "EVIDENTIAL\n≠ SUPPORTED",
        "CONTRADICTORY\n≠ EvidenceGateOutcome.CONTRADICTED",
        "GRAPH ADJACENCY\n≠ epistemic relation",
        "MULTIPLE LINKS\n≠ confidence propagation",
        "RELATION ORIGIN ≠ RELATION TYPE ≠ RELATION TRUTH",
    ):
        assert invariant in READINESS


def test_endpoints_bind_exact_pcr_identity() -> None:
    assert "claim_id" in PCR
    assert "input_fingerprint" in PCR
    assert "claim_id + ProvenanceClaimRecord.input_fingerprint" in READINESS
    assert "PHASE_5_ENDPOINT_BINDING = PCR_CLAIM_ID_PLUS_INPUT_FINGERPRINT" in READINESS
    for forbidden in (
        "statement_ref alone",
        "graph node id alone",
        "embedding/vector id",
        "LLM-generated summary",
    ):
        assert forbidden in READINESS


def test_relation_origin_is_separate_from_type_and_truth() -> None:
    for marker in (
        "SOURCE_ASSERTED",
        "MENTAURY_DERIVED",
        "EXTERNAL_DERIVED",
        "origin_actor_ref",
        "generated relation is not evidence for itself",
    ):
        assert marker in READINESS


def test_scope_preserves_conditional_generalization() -> None:
    for marker in (
        "conditions",
        "moderators",
        "exceptions",
        "unknowns",
        "transfer_limits",
        "no listed exception\n≠ universal law",
        "Scope Erasure",
    ):
        assert marker in READINESS


def test_no_confidence_or_graph_authority_in_v0_1() -> None:
    assert "No confidence, probability or reliability field in v0.1" in READINESS
    assert "PHASE_5_RELATION_CONFIDENCE = NOT_IN_V0_1" in READINESS
    assert "PHASE_5_GRAPH_AUTHORITY = NONE" in READINESS
    assert "no database / graph persistence" in READINESS
    assert "no LLM/model/embedding/retriever/Atlas" in READINESS


def test_existing_phase4_authority_remains_unchanged() -> None:
    assert "PHASE_4_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "PHASE_4_OWNER_GO_NOT_GRANTED" in STATUS
    assert "PHASE_4_RUNTIME_NOT_AUTHORIZED" in STATUS
    assert "Owner GO:                            NOT_GRANTED" in EPR
    assert "Implementation:                      NOT_STARTED" in EPR


def test_no_typed_relations_source_package_exists() -> None:
    assert not (ROOT / "src" / "mentaury" / "relations").exists()
    assert not (ROOT / "src" / "mentaury" / "typed_relations").exists()


def test_future_contract_requirements_are_bounded_and_testable() -> None:
    for family in ("TR-T01", "TR-T16", "TR-M01", "TR-M12", "TR-P01", "TR-P12"):
        assert family in READINESS
    assert "exactly two endpoint ClaimAnchors" in READINESS
    assert "No transitive closure" in READINESS
    assert "Caller-supplied final fingerprint is forbidden" in READINESS


def test_mandatory_stop_blocks_candidate_freeze_and_owner_go() -> None:
    for marker in (
        "Typed Relations candidate implementation",
        "Typed Relations implementation contract freeze",
        "Typed Relations Owner GO",
        "EPR-v0.1 implementation",
        "autonomous/background cognition",
        "runtime activation",
        "deployment",
    ):
        assert marker in READINESS
    assert "PHASE_5_TYPED_RELATIONS_CANDIDATE_SELECTION_AND_CONTRACT_FREEZE · DOCS_ONLY" in READINESS
