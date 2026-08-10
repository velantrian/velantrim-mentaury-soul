"""Structural assertions for the reconciled docs-only NPG-v0.1 contract."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")
READINESS = (
    ROOT / "docs" / "research" / "NON_PROJECTION_GATE_CONTRACT_READINESS.md"
).read_text(encoding="utf-8")
SELECTION = (
    ROOT / "docs" / "research" / "NON_PROJECTION_GATE_CANDIDATE_SELECTION.md"
).read_text(encoding="utf-8")


def test_contract_freezes_docs_only_without_owner_go_or_p1_004() -> None:
    for marker in (
        "FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT",
        "Contract version:                    NPG-v0.1",
        "Candidate:                           PURE_NON_PROJECTION_CLASSIFIER",
        "Implementation contract:             FROZEN_DOCS",
        "P1-004 assignment:                   NOT_ASSIGNED",
        "Non-Projection Owner GO:             NOT_GRANTED",
        "Implementation authorization:        NONE",
        "Runtime implementation:              NOT_AUTHORIZED",
        "Runtime activation:                  NOT_AUTHORIZED",
        "CONTRACT FROZEN ≠ OWNER GO.",
        "THIS DOCUMENT DOES NOT AUTHORIZE IMPLEMENTATION.",
    ):
        assert marker in CONTRACT

    assert "P1_004                              = NOT_ASSIGNED" in SELECTION
    assert "NON_PROJECTION_OWNER_GO            = NOT_GRANTED" in SELECTION


def test_exact_package_and_public_api_are_frozen() -> None:
    for marker in (
        "src/mentaury/non_projection/__init__.py",
        "src/mentaury/non_projection/contracts.py",
        "src/mentaury/non_projection/classifier.py",
        "def classify_non_projection(",
        "envelope: AttributedInterpretationEnvelope",
        "budget: NonProjectionBudget",
        ") -> NonProjectionResult:",
    ):
        assert marker in CONTRACT


def test_versions_domains_and_hard_caps_are_exact() -> None:
    for marker in (
        'NON_PROJECTION_CONTRACT_VERSION            = "NPG-v0.1"',
        'ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION = "AIE-v0.1"',
        'CANONICAL_PROFILE                          = "MENTAURY_CANONICAL_JSON_V1"',
        'INPUT_FINGERPRINT_DOMAIN                   = "MENTAURY_NPG_INPUT_V1"',
        'SOURCE_PROVENANCE_SCOPE                    = "CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY"',
        "HARD_MAX_STRING_BYTES                      = 4096",
        "HARD_MAX_TUPLE_ITEMS                       = 512",
        "HARD_MAX_REVIEW_RECORDS                    = 64",
        "HARD_MAX_CANONICAL_INPUT_BYTES             = 262144",
    ):
        assert marker in CONTRACT


def test_hard_caps_and_local_budget_have_distinct_fail_closed_semantics() -> None:
    for marker in (
        "hard caps are admission constraints; caller local",
        "limits are classification constraints",
        "hard-cap overflow   → NonProjectionContractError",
        "local-budget overflow while still inside hard caps → DEFER · BUDGET_EXHAUSTED",
        "every string reference is valid UTF-8 and inside **hard caps**",
        "classified as `DEFER · BUDGET_EXHAUSTED`",
        "NPC-DEC-014 valid local over-budget input → DEFER without truncation",
    ):
        assert marker in CONTRACT


def test_readiness_vocabulary_is_preserved() -> None:
    source_classes = (
        "CREATOR_TESTIMONY",
        "CURRENT_USER_TESTIMONY",
        "HISTORICAL_PRIMARY",
        "HISTORICAL_SECONDARY",
        "LITERARY_OR_METAPHORICAL",
        "RESEARCH_PRIMARY",
        "RESEARCH_SECONDARY",
        "MODEL_INTERPRETATION",
        "REVIEW_OUTPUT",
        "UNKNOWN_SOURCE",
    )
    claim_classes = (
        "FACTUAL",
        "CAUSAL",
        "PREDICTIVE",
        "NORMATIVE",
        "VALUE",
        "AUTOBIOGRAPHICAL_TESTIMONY",
        "RELATIONSHIP_TESTIMONY",
        "CONSENT_STATEMENT",
        "INTERPRETIVE",
        "METAPHORICAL",
    )
    decisions = (
        "PASS_ATTRIBUTED",
        "REVISE_REQUIRED",
        "CONTESTED",
        "DEFER",
        "REJECT",
    )
    for marker in source_classes + claim_classes + decisions:
        assert marker in CONTRACT
        assert marker in READINESS


def test_exact_immutable_contract_types_are_frozen() -> None:
    for marker in (
        "class SourceProvenance:",
        "class Attribution:",
        "class Claim:",
        "class Interpretation:",
        "class ContextualDistance:",
        "class ReviewRecord:",
        "class ReviewProvenance:",
        "class ScopeBoundary:",
        "class AuthorityExclusions:",
        "class ProjectionIntent:",
        "class AttributedInterpretationEnvelope:",
        "class NonProjectionBudget:",
        "class NonProjectionResult:",
        "provider_ref: str | None",
        "claimed_independent_review_count: int",
        "effective_independent_review_count: int",
    ):
        assert marker in CONTRACT


def test_malformed_policy_and_no_hidden_normalization_are_frozen() -> None:
    for marker in (
        "class NonProjectionContractError(ValueError):",
        "A contract error returns no ordinary classification",
        "every tuple of strings is already lexicographically sorted and unique",
        "no hidden trimming, sorting, aliasing, case folding, translation or semantic",
        '"creator-1" ≠ " creator-1 "',
        "reordered tuples ≠ silently repaired tuples",
    ):
        assert marker in CONTRACT


def test_verified_self_is_fail_closed() -> None:
    for marker in (
        "NPG-v0.1 intentionally owns no identity/continuation binder.",
        "NON_SELF      → eligible for bounded evaluation",
        "UNKNOWN       → DEFER · SUBJECT_RELATION_UNKNOWN",
        "VERIFIED_SELF → DEFER · SELF_BASIS_UNVERIFIED",
    ):
        assert marker in CONTRACT


def test_reviewer_correlation_is_computed_not_trusted() -> None:
    for marker in (
        "computes `effective_independent_review_count`",
        "independence == INDEPENDENT",
        "saw_prior_output == False",
        "provider_ref occurs exactly once among non-null provider refs",
        "prompt_family_ref occurs exactly once among non-null prompt-family refs",
        "context_snapshot_ref occurs exactly once among non-null context-snapshot refs",
        "> effective_independent_review_count",
        "same provider/model only  ≠ independent convergence",
        "repeated derived reviews  ≠ additional independent evidence",
    ):
        assert marker in CONTRACT


def test_all_twelve_threats_are_mapped_and_inherited() -> None:
    for number in range(1, 13):
        marker = f"NPG-T{number:02d}"
        assert marker in CONTRACT
        assert marker in READINESS

    for marker in (
        "adopt_as_self_experience == True",
        "inherit_source_authority == True",
        "assert_as_objective_truth == True",
        "adopt_source_emotion_as_drive == True",
        "style_changes_evidence_status == True",
        "generalize_beyond_scope == True",
        "claimed_independent_review_count > effective_independent_review_count",
        "discard_relevant_context == True",
        "inherit_relationship_or_commitment == True",
        "promote_to_stable_identity_trait == True",
        "present_interpretation_as_direct_testimony == True",
        "inherit_consent == True",
    ):
        assert marker in CONTRACT


def test_fail_closed_precedence_and_reason_families_are_exact() -> None:
    assert "REJECT\n> DEFER\n> CONTESTED\n> REVISE_REQUIRED\n> PASS_ATTRIBUTED" in CONTRACT
    for marker in (
        "ENVELOPE_VERSION_UNVERIFIED",
        "BUDGET_EXHAUSTED",
        "CANONICALIZATION_FAILED",
        "SOURCE_CLASS_UNKNOWN",
        "SOURCE_ORIGIN_UNKNOWN",
        "PROVENANCE_UNKNOWN",
        "PROVENANCE_MATERIAL_GAP",
        "SUBJECT_RELATION_UNKNOWN",
        "SELF_BASIS_UNVERIFIED",
        "INTERPRETATION_UNKNOWN",
        "CONTEXT_UNKNOWN",
        "SCOPE_UNKNOWN",
        "PROVENANCE_CONFLICTING",
        "INTERPRETATION_CONTESTED",
        "ATTRIBUTION_REPAIR_REQUIRED",
        "CONTEXT_SCOPE_REPAIR_REQUIRED",
    ):
        assert marker in CONTRACT


def test_partial_provenance_and_historical_repair_match_readiness() -> None:
    for marker in (
        "provenance_state == PARTIAL and material_gaps != ()",
        "`PARTIAL` provenance with `material_gaps == ()` is not automatically deferred",
        "scope.transfer_limits == ()",
        "source_class == HISTORICAL_PRIMARY",
        "source_class == HISTORICAL_SECONDARY",
        "→ REVISE_REQUIRED · CONTEXT_SCOPE_REPAIR_REQUIRED",
    ):
        assert marker in CONTRACT


def test_input_fingerprint_is_derived_evidence_only() -> None:
    for marker in (
        "MENTAURY_NPG_INPUT_V1",
        "CALLER_SUPPLIED_ATTRIBUTED_VALUES_ONLY",
        "canonical_json_bytes(...) ",
        "hashlib.sha256(bytes).hexdigest()",
        "lowercase 64-character SHA-256 hex",
        "fingerprint is derived audit evidence only",
    ):
        assert marker.strip() in CONTRACT


def test_exact_readiness_scenarios_are_preserved_without_013() -> None:
    for number in range(1, 13):
        assert f"`NPG-SC-{number:03d}`" in CONTRACT
        assert f"`NPG-SC-{number:03d}`" in READINESS

    assert "NPG-SC-CONTESTED-001" in CONTRACT
    assert "No `NPG-SC-013` is created by this contract." in CONTRACT
    assert "`NPG-SC-008` | historical advice lacks transfer limits" in CONTRACT
    assert "REVISE_REQUIRED · CONTEXT_SCOPE_REPAIR_REQUIRED" in CONTRACT
    assert "`NPG-SC-011` | materially unknown source identity/provenance" in CONTRACT
    assert "DEFER · PROVENANCE_UNKNOWN" in CONTRACT


def test_metamorphic_and_executable_families_are_frozen() -> None:
    for number in range(1, 9):
        marker = f"MT-NPG-{number:03d}"
        assert marker in CONTRACT
        assert marker in READINESS

    for marker in (
        "NPC-CTX-001…022",
        "NPC-FP-001…008",
        "NPC-DEC-001…016",
        "NPC-T-001…012",
        "NPC-SC-001…NPC-SC-012",
        "NPC-SC-CONTESTED-001",
        "NPC-M-001…008",
        "NPC-PURE-001…010",
    ):
        assert marker in CONTRACT


def test_purity_and_no_hidden_authority_are_explicit() -> None:
    for marker in (
        "no ambient filesystem/database/network use",
        "no vector/graph/Atlas retrieval",
        "no ambient clock/random dependency",
        "no environment-variable authority",
        "no model/LLM invocation",
        "no persistence/event/replay/belief/identity/relationship/M2/M3 mutation",
        "no Action Gate/capability/tool/subprocess/dynamic-plugin invocation",
        "canonical_json dependency",
    ):
        assert marker in CONTRACT


def test_p1_character_canon_and_authority_boundaries_remain_closed() -> None:
    for marker in (
        "P1-001 contract = unchanged",
        "P1-002 contract = unchanged",
        "P1-003 contract = unchanged",
        "MENTAURY_CANON_V0.1 = unchanged",
        "P1_003_ELIGIBLE_FOR_NEXT_GATE\n+ PASS_ATTRIBUTED\n≠ Action Gate PASS",
        "Character presentation\n→ cannot alter provenance",
        "P1_004                                 = NOT_ASSIGNED",
        "NON_PROJECTION_OWNER_GO                = NOT_GRANTED",
        "IMPLEMENTATION_AUTHORIZATION           = NONE",
        "NON_PROJECTION_RUNTIME                 = NOT_AUTHORIZED",
    ):
        assert marker in CONTRACT


def test_next_step_is_separate_owner_go_only() -> None:
    for marker in (
        "NON_PROJECTION_IMPLEMENTATION_CONTRACT_FROZEN_DOCS_ONLY",
        "separate explicit Owner GO decision",
        "only if GO: clean Tier A bounded implementation milestone",
        "No wording in this document constitutes that GO.",
    ):
        assert marker in CONTRACT
