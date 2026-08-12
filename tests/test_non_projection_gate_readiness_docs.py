"""Structural assertions for the docs-only Non-Projection Gate readiness contract."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS = (ROOT / "docs" / "research" / "NON_PROJECTION_GATE_CONTRACT_READINESS.md").read_text(
    encoding="utf-8"
)
SELECTION = (ROOT / "docs" / "research" / "POST_P1_003_MILESTONE_SELECTION.md").read_text(
    encoding="utf-8"
)
CURRENT_STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(encoding="utf-8")


def test_readiness_is_docs_only_and_runtime_remains_unassigned() -> None:
    assert "FROZEN_DOCS · READINESS_READY · DOCS_ONLY" in READINESS
    assert "NON_PROJECTION_GATE_CONTRACT_READINESS = READY" in READINESS
    assert "Selected readiness model:       ATTRIBUTED_INTERPRETATION_ENVELOPE" in READINESS
    assert "P1-004 assignment:              NONE" in READINESS
    assert "Non-Projection runtime:         NOT_AUTHORIZED" in READINESS
    assert "Non-Projection Owner GO:        NOT_GRANTED" in READINESS
    assert "Implementation authorization:   NONE" in READINESS


def test_readiness_consumes_the_post_p1_003_selection_without_widening_it() -> None:
    assert "Selected bounded work:        NON_PROJECTION_GATE_CONTRACT_READINESS" in SELECTION
    assert "P1-004 assignment:            NONE" in SELECTION
    assert "Implementation authorization: NONE" in SELECTION
    assert "READINESS READY ≠ IMPLEMENTATION CONTRACT" in READINESS
    assert "Implementation contract:         NOT_FROZEN" in READINESS


def test_self_attribution_is_fail_closed() -> None:
    for marker in (
        "VERIFIED_SELF",
        "NON_SELF",
        "UNKNOWN",
        "safe attribution = NON_SELF or UNKNOWN",
        "VERIFIED_SELF     = unavailable from source prestige",
        "creator said it            → VERIFIED_SELF     = FORBIDDEN",
        'user asks "make it yours"  → VERIFIED_SELF     = FORBIDDEN',
    ):
        assert marker in READINESS


def test_claim_and_reviewer_boundaries_are_explicit() -> None:
    for marker in (
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
        "INDEPENDENT",
        "PARTIALLY_CORRELATED",
        "DERIVED",
        "UNKNOWN independence                  ≠ independent evidence",
    ):
        assert marker in READINESS


def test_fail_closed_readiness_vocabulary_and_precedence_are_frozen() -> None:
    for marker in (
        "PASS_ATTRIBUTED",
        "REVISE_REQUIRED",
        "CONTESTED",
        "DEFER",
        "REJECT",
        "REJECT\n> DEFER\n> CONTESTED\n> REVISE_REQUIRED\n> PASS_ATTRIBUTED",
    ):
        assert marker in READINESS


def test_positive_result_has_no_truth_identity_or_execution_authority() -> None:
    for marker in (
        "≠ factual truth proof",
        "≠ Mentaury autobiography",
        "≠ identity claim",
        "≠ stable M3 trait",
        "≠ relationship claim",
        "≠ commitment",
        "≠ consent",
        "≠ capability",
        "≠ Action Gate PASS",
        "≠ retrieval permission",
        "≠ tool/execution permission",
        "≠ deployment permission",
    ):
        assert marker in READINESS


def test_threat_scenario_and_metamorphic_families_are_complete() -> None:
    for number in range(1, 13):
        assert f"NPG-T{number:02d}" in READINESS
        assert f"NPG-SC-{number:03d}" in READINESS

    for number in range(1, 9):
        assert f"MT-NPG-{number:03d}" in READINESS


def test_character_and_p1_contracts_cannot_be_silently_widened() -> None:
    for marker in (
        "P1-001 contract = unchanged",
        "P1-002 contract = unchanged",
        "P1-003 contract = unchanged",
        "MENTAURY_CANON_V0.1 = unchanged",
        "Character presentation\n→ cannot alter Non-Projection result",
        "PASS_ATTRIBUTED + P1_003_ELIGIBLE_FOR_NEXT_GATE\n≠ Action Gate PASS",
    ):
        assert marker in READINESS


def test_existing_repository_runtime_stop_remains_current() -> None:
    assert "NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED" in CURRENT_STATUS
    assert "Runtime activation milestone: NOT_SELECTED · NOT_AUTHORIZED" in ROADMAP
    assert "Phase 2 implementation:       IMPLEMENTED_BOUNDED" in ROADMAP
    assert "Phase 3 contract:             FROZEN_DOCS · PCR-v0.1" in ROADMAP
    assert "Phase 3 Owner GO:             CONSUMED_BY_PR_103" in ROADMAP
    assert "Phase 3 implementation:       IMPLEMENTED_BOUNDED" in ROADMAP
    for marker in (
        "Action Gate:                     NOT_AUTHORIZED",
        "Retrieval execution:             NOT_AUTHORIZED",
        "Tool execution:                  NOT_AUTHORIZED",
        "Identity runtime:                NOT_AUTHORIZED",
        "Relationship runtime:            NOT_AUTHORIZED",
        "Direct or indirect M3 write:     FORBIDDEN",
        "Runtime deployment:              NOT_AUTHORIZED",
    ):
        assert marker in READINESS


def test_readiness_requires_new_authority_ladder_before_code() -> None:
    for marker in (
        "READINESS_READY_DOCS_ONLY",
        "→ separate candidate selection",
        "→ separate implementation-contract freeze",
        "→ explicit separate Owner GO",
        "→ clean Tier A implementation PR",
    ):
        assert marker in READINESS
