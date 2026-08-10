"""Structural assertions for the docs-only NPG-v0.1 implementation contract."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT / "docs" / "research" / "NON_PROJECTION_IMPLEMENTATION_CONTRACT.md"
).read_text(encoding="utf-8")
READINESS = (
    ROOT / "docs" / "research" / "NON_PROJECTION_GATE_CONTRACT_READINESS.md"
).read_text(encoding="utf-8")
SELECTION = (
    ROOT / "docs" / "research" / "NON_PROJECTION_GATE_CANDIDATE_SELECTION.md"
).read_text(encoding="utf-8")


def test_contract_is_frozen_docs_only_without_owner_go_or_p1_004() -> None:
    for marker in (
        "FROZEN_DOCS · DOCS_ONLY · IMPLEMENTATION_CONTRACT",
        "Selected candidate:                  PURE_NON_PROJECTION_CLASSIFIER",
        "Contract version:                    NPG-v0.1",
        "P1-004 assignment:                   NOT_ASSIGNED",
        "Non-Projection Owner GO:             NOT_GRANTED",
        "Implementation authorization:        NONE",
        "Runtime implementation:              NOT_AUTHORIZED",
        "Runtime activation:                  NOT_AUTHORIZED",
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
        'NON_PROJECTION_CONTRACT_VERSION              = "NPG-v0.1"',
        'ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION   = "AIE-v0.1"',
        'CANONICAL_PROFILE                            = "MENTAURY_CANONICAL_JSON_V1"',
        'ENVELOPE_FINGERPRINT_DOMAIN                  = "MENTAURY_NPG_ENVELOPE_V1"',
        'CLASSIFICATION_FINGERPRINT_DOMAIN            = "MENTAURY_NPG_CLASSIFICATION_V1"',
        "HARD_MAX_ENVELOPE_BYTES                      = 262144",
        "HARD_MAX_REVIEW_RECORDS                      = 64",
        "HARD_MAX_SCOPE_ENTRIES                       = 128",
        "HARD_MAX_REFERENCE_COUNT                     = 512",
        "MAX_REFERENCE_UTF8_BYTES                     = 4096",
    ):
        assert marker in CONTRACT


def test_frozen_readiness_vocabulary_is_retained() -> None:
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


def test_exact_immutable_schema_is_frozen() -> None:
    classes = (
        "class SourceProvenance:",
        "class Attribution:",
        "class Claim:",
        "class Interpretation:",
        "class ContextualDistance:",
        "class ReviewRecord:",
        "class ReviewProvenance:",
        "class ScopeBoundary:",
        "class AuthorityExclusions:",
        "class ProposedUse:",
        "class AttributedInterpretationEnvelope:",
        "class NonProjectionBudget:",
        "class NonProjectionResult:",
    )
    for marker in classes:
        assert marker in CONTRACT

    for marker in (
        "source_provenance: SourceProvenance",
        "attribution: Attribution",
        "claim: Claim",
        "interpretation: Interpretation",
        "contextual_distance: ContextualDistance",
        "review_provenance: ReviewProvenance",
        "scope: ScopeBoundary",
        "authority_exclusions: AuthorityExclusions",
        "proposed_use: ProposedUse",
    ):
        assert marker in CONTRACT


def test_malformed_policy_and_no_hidden_normalization_are_explicit() -> None:
    for marker in (
        "class NonProjectionContractError(ValueError):",
        "It does **not** return a classification.",
        "every tuple of string references is already sorted and unique",
        "no hidden trimming, sorting, aliasing, case folding, semantic mapping or",
        "normalization is allowed",
        '"creator:1" ≠ "CREATOR:1"',
    ):
        assert marker in CONTRACT


def test_verified_self_is_fail_closed_in_v0_1() -> None:
    for marker in (
        "`NPG-v0.1` intentionally contains **no identity/continuation binding**.",
        "NON_SELF      → eligible for bounded evaluation",
        "UNKNOWN       → DEFER · SUBJECT_RELATION_UNKNOWN",
        "VERIFIED_SELF → DEFER · SELF_EVIDENCE_BINDING_UNSUPPORTED",
    ):
        assert marker in CONTRACT


def test_reviewer_correlation_algorithm_is_exact() -> None:
    for marker in (
        "effective_independent_review_count",
        "independence_class == INDEPENDENT",
        "saw_prior_output == False",
        "provider_ref` occurs in exactly one review record",
        "prompt_family_ref` occurs in exactly one review record",
        "context_snapshot_ref` occurs in exactly one review record",
        "claimed_independent_review_count > effective_independent_review_count",
        "Repeated correlated evidence never becomes independent by quantity.",
    ):
        assert marker in CONTRACT


def test_all_twelve_threats_have_exact_executable_mapping() -> None:
    for number in range(1, 13):
        threat = f"NPG-T{number:02d}"
        assert threat in CONTRACT
        assert threat in READINESS

    mappings = (
        "present_as_mentaury_autobiography == True",
        "authority_exclusions.capability_authority",
        "proposed_use.truth_mode == UNIVERSAL_FACT",
        "proposed_use.adopt_source_emotion_as_drive == True",
        "proposed_use.character_override_evidence == True",
        "proposed_use.generalize_beyond_scope == True",
        "claimed_independent_review_count > effective_independent_review_count",
        "proposed_use.context_collapsed == True",
        "proposed_use.relationship_adoption == True",
        "proposed_use.identity_trait_adoption == True",
        "proposed_use.interpretation_as_direct_source == True",
        "proposed_use.consent_transfer == True",
    )
    for marker in mappings:
        assert marker in CONTRACT


def test_fail_closed_precedence_and_reason_families_are_frozen() -> None:
    assert (
        "REJECT\n> DEFER\n> CONTESTED\n> REVISE_REQUIRED\n> PASS_ATTRIBUTED"
        in CONTRACT
    )
    for marker in (
        "BUDGET_EXHAUSTED",
        "SUBJECT_RELATION_UNKNOWN",
        "SELF_EVIDENCE_BINDING_UNSUPPORTED",
        "PROVENANCE_UNKNOWN",
        "SOURCE_CLASS_UNKNOWN",
        "SOURCE_ORIGIN_UNKNOWN",
        "CONTEXT_DISTANCE_UNKNOWN",
        "SCOPE_UNRESOLVED",
        "PROVENANCE_CONFLICTING",
        "INTERPRETATION_CONTESTED",
        "PROVENANCE_PARTIAL",
        "ATTRIBUTION_REPAIR_REQUIRED",
        "CONTEXT_ACKNOWLEDGEMENT_REQUIRED",
    ):
        assert marker in CONTRACT


def test_fingerprints_are_derived_not_caller_authority() -> None:
    for marker in (
        "MENTAURY_NPG_ENVELOPE_V1",
        "MENTAURY_NPG_CLASSIFICATION_V1",
        "hashlib.sha256(bytes).hexdigest()",
        "lowercase 64-character SHA-256 hex strings",
        "Fingerprints are derived evidence only and grant no authority.",
        "caller fingerprint                             = FORBIDDEN API",
    ):
        assert marker in CONTRACT


def test_inherited_scenario_outcomes_are_preserved() -> None:
    expected = {
        "NPG-SC-001": "`PASS_ATTRIBUTED` | `PASS_ATTRIBUTED`",
        "NPG-SC-002": "`PASS_ATTRIBUTED` | `PASS_ATTRIBUTED`",
        "NPG-SC-003": "`REJECT` | `NPG-T07`",
        "NPG-SC-004": "`REJECT` | `NPG-T03`",
        "NPG-SC-005": "`REJECT` | `NPG-T04`",
        "NPG-SC-006": "`REJECT` | `NPG-T01`",
        "NPG-SC-007": "`PASS_ATTRIBUTED` | `PASS_ATTRIBUTED`",
        "NPG-SC-009": "`REJECT` | `NPG-T09`",
        "NPG-SC-010": "`REJECT` | `NPG-T05`",
        "NPG-SC-012": "`REJECT` | `NPG-T02`",
    }
    for scenario, suffix in expected.items():
        assert f"| `{scenario}` | {suffix} |" in CONTRACT

    assert "| `NPG-SC-008` | `REVISE_REQUIRED` |" in CONTRACT
    assert "CONTEXT_ACKNOWLEDGEMENT_REQUIRED" in CONTRACT
    assert "| `NPG-SC-011` | `DEFER` |" in CONTRACT
    assert "PROVENANCE_UNKNOWN" in CONTRACT
    assert "NPG-SC-CONTESTED-001" in CONTRACT
    assert "→ CONTESTED · INTERPRETATION_CONTESTED" in CONTRACT


def test_executable_matrix_families_are_frozen() -> None:
    for marker in (
        "NPG-ADM-001…NPG-ADM-020",
        "NPG-THR-001…NPG-THR-012",
        "NPG-SC-001…NPG-SC-012",
        "NPG-SC-CONTESTED-001",
        "NPG-DEC-001…NPG-DEC-012",
        "NPG-FP-001…NPG-FP-008",
        "MT-NPG-001…MT-NPG-008",
        "NPG-PURE-001…NPG-PURE-010",
    ):
        assert marker in CONTRACT

    for number in range(1, 9):
        marker = f"MT-NPG-{number:03d}"
        assert marker in CONTRACT
        assert marker in READINESS


def test_purity_boundary_is_explicit() -> None:
    for marker in (
        "no network access",
        "no filesystem access",
        "no database / vector / graph access",
        "no model / LLM call",
        "no retrieval / Atlas lookup",
        "no persistence / event append / M2/M3 mutation",
        "no identity / relationship registry lookup",
        "no Action Gate / capability / tool invocation",
        "no ambient clock / random / environment dependency",
        "import has no side effects and same input is deterministic",
    ):
        assert marker in CONTRACT


def test_p1_character_canon_and_authority_boundaries_remain_closed() -> None:
    for marker in (
        "P1-001 contract = unchanged",
        "P1-002 contract = unchanged",
        "P1-003 contract = unchanged",
        "MENTAURY_CANON_V0.1 = unchanged",
        "P1_003_ELIGIBLE_FOR_NEXT_GATE\n+ PASS_ATTRIBUTED\n≠ Action Gate PASS",
        "Character presentation\n→ cannot change envelope provenance",
        "P1_004 = NOT_ASSIGNED",
        "NON_PROJECTION_OWNER_GO = NOT_GRANTED",
        "IMPLEMENTATION_AUTHORIZATION = NONE",
        "NON_PROJECTION_RUNTIME = NOT_AUTHORIZED",
    ):
        assert marker in CONTRACT


def test_next_step_is_owner_go_only_not_implementation() -> None:
    for marker in (
        "NON_PROJECTION_IMPLEMENTATION_CONTRACT_FROZEN_DOCS_ONLY",
        "explicit separate NON_PROJECTION_OWNER_GO_AUTHORIZED_BOUNDED",
        "No later state follows automatically.",
        "CONTRACT FROZEN ≠ OWNER GO.",
        "THIS DOCUMENT DOES NOT AUTHORIZE IMPLEMENTATION.",
    ):
        assert marker in CONTRACT
