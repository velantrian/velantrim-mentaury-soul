"""Structural guards for the Phase 5 ATR-v0.1 docs-only contract freeze."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_CONTRACT_READINESS.md"
).read_text(encoding="utf-8")
SELECTION = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_CANDIDATE_SELECTION.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT / "docs" / "research" / "TYPED_RELATIONS_PURE_RECORD_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_candidate_and_contract_are_exactly_selected_and_frozen() -> None:
    assert "ANCHORED_TYPED_RELATION_CANDIDATE" in READINESS
    assert "ANCHORED_TYPED_RELATION_CANDIDATE" in SELECTION

    for document in (SELECTION, CONTRACT):
        assert "PURE_ANCHORED_TYPED_RELATION_RECORD" in document
        assert "ATR-v0.1" in document
        assert "Owner GO:" in document
        assert "NOT_GRANTED" in document
        assert "Runtime:" in document
        assert "NOT_AUTHORIZED" in document

    assert "PHASE_5_TYPED_RELATIONS_CANDIDATE_SELECTION = SELECTED" in SELECTION
    assert "PHASE_5_TYPED_RELATIONS_IMPLEMENTATION_CONTRACT = FROZEN_DOCS" in CONTRACT
    assert "PHASE_5_TYPED_RELATIONS_IMPLEMENTATION = NOT_STARTED" in CONTRACT
    assert "PHASE_5_TYPED_RELATIONS_OWNER_GO = NOT_GRANTED" in CONTRACT


def test_contract_freeze_has_no_source_implementation() -> None:
    assert not (ROOT / "src" / "mentaury" / "relations").exists()
    assert "src/mentaury/relations/__init__.py" in CONTRACT
    assert "src/mentaury/relations/contracts.py" in CONTRACT
    assert "src/mentaury/relations/representation.py" in CONTRACT
    assert "Nothing in\n> this document authorizes creation of `src/mentaury/relations/**`" in CONTRACT


def test_exact_public_api_is_frozen() -> None:
    for fragment in (
        "represent_typed_relation(",
        "endpoints: RelationEndpoints",
        "semantics: RelationSemantics",
        "provenance: RelationProvenance",
        "scope: RelationScope",
        "budget: RelationRepresentationBudget",
        ") -> AnchoredTypedRelationRecord",
    ):
        assert fragment in CONTRACT


def test_exact_contract_types_are_frozen() -> None:
    for type_name in (
        "class RelationType(StrEnum):",
        "class RelationOrientation(StrEnum):",
        "class RelationOrigin(StrEnum):",
        "class ScopeReferenceKind(StrEnum):",
        "class ClaimAnchor:",
        "class RelationEndpoints:",
        "class RelationSemantics:",
        "class ScopeReference:",
        "class RelationProvenance:",
        "class RelationScope:",
        "class RelationRepresentationBudget:",
        "class AnchoredTypedRelationRecord:",
    ):
        assert type_name in CONTRACT


def test_relation_vocabularies_remain_closed() -> None:
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
        assert relation_type in CONTRACT

    for orientation in ("DIRECTED", "SYMMETRIC", "UNKNOWN"):
        assert orientation in CONTRACT

    for origin in (
        "SOURCE_ASSERTED",
        "MENTAURY_DERIVED",
        "EXTERNAL_DERIVED",
        "UNKNOWN",
    ):
        assert origin in CONTRACT

    assert "No open caller-defined enum extension is admitted in ATR-v0.1" in CONTRACT


def test_scope_reference_shape_separates_claim_and_context() -> None:
    for fragment in (
        "CLAIM_ANCHOR",
        "CONTEXT_REF",
        "claim_input_fingerprint REQUIRED",
        "claim_input_fingerprint MUST be None",
        "CONTEXT_REF ≠ CLAIM",
        "CLAIM_ANCHOR ≠ EVIDENCE SUPPORT",
    ):
        assert fragment in CONTRACT


def test_relation_semantic_ceilings_are_frozen() -> None:
    for law in (
        "CORRELATIONAL ≠ CAUSAL",
        "TEMPORAL ≠ CAUSAL",
        "ANALOGICAL ≠ MECHANISTIC",
        "EVIDENTIAL ≠ SUPPORTED",
        "CONTRADICTORY ≠ EvidenceGateOutcome.CONTRADICTED",
        "SOURCE_ASSERTED ≠ true",
        "MENTAURY_DERIVED ≠ independent evidence for itself",
        "GRAPH LINK / PATH / COUNT ≠ EPISTEMIC AUTHORITY",
    ):
        assert law in CONTRACT


def test_no_confidence_or_evidence_gate_surface_is_selected() -> None:
    assert "No field for confidence, probability, reliability, support status" in CONTRACT
    assert "TR-P07 no Evidence Gate invocation" in CONTRACT
    assert "P0-015" in CONTRACT
    assert "sole Evidence Gate support/contradiction evaluation owner" in CONTRACT


def test_endpoint_identity_and_orientation_rules_are_frozen() -> None:
    for fragment in (
        "claim_id",
        "claim_input_fingerprint",
        "left_anchor != right_anchor",
        "left_anchor → right_anchor",
        "Unsorted symmetric endpoints fail closed",
        "CAUSAL         → DIRECTED only",
        "CORRELATIONAL  → SYMMETRIC only",
        "CONTRADICTORY  → SYMMETRIC only",
    ):
        assert fragment in CONTRACT


def test_origin_invariants_are_explicit() -> None:
    for fragment in (
        "### SOURCE_ASSERTED",
        "### MENTAURY_DERIVED",
        "### EXTERNAL_DERIVED",
        "### UNKNOWN",
        "origin_actor_ref = REQUIRED",
        "source_assertion_anchor = REQUIRED",
        "basis_anchors = NON_EMPTY",
        "origin_actor_ref = MUST be None",
    ):
        assert fragment in CONTRACT


def test_budget_and_fingerprint_semantics_are_frozen() -> None:
    for fragment in (
        'TYPED_RELATION_CONTRACT_VERSION = "ATR-v0.1"',
        'CANONICAL_PROFILE = "MENTAURY_CANONICAL_JSON_V1"',
        'INPUT_FINGERPRINT_DOMAIN = "MENTAURY_ANCHORED_TYPED_RELATION_INPUT_V1"',
        "HARD_MAX_STRING_BYTES = 4096",
        "HARD_MAX_TUPLE_ITEMS = 512",
        "HARD_MAX_CANONICAL_INPUT_BYTES = 262144",
        "TypedRelationContractError",
        "TypedRelationBudgetExceeded",
        "exact-input identity evidence",
        "≠ truth",
        "≠ support",
        "≠ confidence",
        "≠ permission",
    ):
        assert fragment in CONTRACT


def test_all_frozen_requirement_families_are_present() -> None:
    for index in range(1, 17):
        assert f"TR-T{index:02d}" in CONTRACT
    for index in range(1, 13):
        assert f"TR-M{index:02d}" in CONTRACT
        assert f"TR-P{index:02d}" in CONTRACT


def test_readiness_invariants_are_not_weakened() -> None:
    for fragment in (
        "ClaimAnchor",
        "CAUSAL",
        "CORRELATIONAL",
        "EVIDENTIAL",
        "CONTRADICTORY",
        "MENTAURY_DERIVED",
        "conditions",
        "moderators",
        "exceptions",
        "unknowns",
        "transfer_limits",
        "TR-T16",
        "TR-M12",
        "TR-P12",
    ):
        assert fragment in READINESS
        assert fragment in CONTRACT


def test_mandatory_stop_requires_new_single_use_owner_go() -> None:
    assert "MANDATORY STOP" in CONTRACT
    assert "ATR-v0.1_ONLY" in CONTRACT
    assert "new explicit single-use Owner GO" in CONTRACT
    assert "Generic “continue/do it” from a\n> prior milestone is not reusable implementation authority" in CONTRACT
