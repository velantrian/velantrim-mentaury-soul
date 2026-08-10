"""Structural assertions for the docs-only Non-Projection candidate selection."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTION = (
    ROOT / "docs" / "research" / "NON_PROJECTION_GATE_CANDIDATE_SELECTION.md"
).read_text(encoding="utf-8")
READINESS = (
    ROOT / "docs" / "research" / "NON_PROJECTION_GATE_CONTRACT_READINESS.md"
).read_text(encoding="utf-8")


def test_candidate_is_selected_docs_only_without_runtime_assignment() -> None:
    assert "FROZEN_DOCS · DOCS_ONLY · CANDIDATE_SELECTION" in SELECTION
    assert "NON_PROJECTION_CANDIDATE_SELECTION = SELECTED" in SELECTION
    assert "NON_PROJECTION_CANDIDATE           = PURE_NON_PROJECTION_CLASSIFIER" in SELECTION
    assert "P1_004                              = NOT_ASSIGNED" in SELECTION
    assert "IMPLEMENTATION_CONTRACT            = NOT_FROZEN" in SELECTION
    assert "NON_PROJECTION_OWNER_GO            = NOT_GRANTED" in SELECTION
    assert "IMPLEMENTATION_AUTHORIZATION       = NONE" in SELECTION


def test_selected_candidate_is_pure_and_explicit_input_only() -> None:
    for marker in (
        "pure deterministic classifier over explicit caller-supplied",
        "explicit caller-supplied bounded values only",
        "no filesystem, database, graph or vector-store access",
        "no network access",
        "no Atlas lookup or retrieval",
        "no identity-registry or relationship-registry lookup",
        "no model/LLM call",
        "no persistence or event append",
        "no M2/M3 write or promotion",
        "no capability or Action Gate invocation",
        "no tool execution",
    ):
        assert marker in SELECTION


def test_candidate_inherits_frozen_readiness_families() -> None:
    for marker in (
        "NPG-T01…NPG-T12",
        "NPG-SC-001…NPG-SC-012",
        "MT-NPG-001…MT-NPG-008",
    ):
        assert marker in SELECTION
        assert marker in READINESS

    for number in range(1, 13):
        assert f"NPG-T{number:02d}" in READINESS
        assert f"NPG-SC-{number:03d}" in READINESS

    for number in range(1, 9):
        assert f"MT-NPG-{number:03d}" in READINESS


def test_fail_closed_result_precedence_is_preserved() -> None:
    for marker in (
        "PASS_ATTRIBUTED",
        "REVISE_REQUIRED",
        "CONTESTED",
        "DEFER",
        "REJECT",
        "REJECT\n> DEFER\n> CONTESTED\n> REVISE_REQUIRED\n> PASS_ATTRIBUTED",
    ):
        assert marker in SELECTION


def test_positive_result_has_no_hidden_authority() -> None:
    for marker in (
        "≠ factual truth proof",
        "≠ Mentaury autobiography",
        "≠ identity / M3 authority",
        "≠ relationship / commitment / consent authority",
        "≠ capability",
        "≠ Action Gate PASS",
        "≠ retrieval permission",
        "≠ tool / execution permission",
        "≠ deployment permission",
    ):
        assert marker in SELECTION


def test_self_attribution_cannot_be_manufactured() -> None:
    for marker in (
        "The selected candidate must not manufacture `VERIFIED_SELF`",
        'caller says "this is you"           ≠ VERIFIED_SELF',
        "creator authority                    ≠ VERIFIED_SELF",
        "narrative similarity                 ≠ VERIFIED_SELF",
        "same model/provider                  ≠ VERIFIED_SELF",
        "shared project lineage               ≠ VERIFIED_SELF",
        "pre-fork shared history alone        ≠ current-branch VERIFIED_SELF",
    ):
        assert marker in SELECTION


def test_p1_character_and_canon_boundaries_remain_closed() -> None:
    for marker in (
        "P1-001 contract = unchanged",
        "P1-002 contract = unchanged",
        "P1-003 contract = unchanged",
        "MENTAURY_CANON_V0.1 = unchanged",
        "P1_003_ELIGIBLE_FOR_NEXT_GATE\n+ PASS_ATTRIBUTED\n≠ Action Gate PASS",
        "presentation policy\n→ cannot change provenance, evidence or Non-Projection result",
    ):
        assert marker in SELECTION


def test_candidate_selection_does_not_freeze_implementation_details() -> None:
    for marker in (
        "exact Python package path",
        "exact public API/function name",
        "concrete dataclasses/enums",
        "canonical serialization/fingerprint domain",
        "exact reason codes",
        "deterministic budgets",
        "exact executable test IDs",
    ):
        assert marker in SELECTION


def test_next_bounded_work_is_contract_freeze_only() -> None:
    assert "NEXT_BOUNDED_WORK = NON_PROJECTION_IMPLEMENTATION_CONTRACT_FREEZE" in SELECTION
    assert "MODE              = DOCS_ONLY" in SELECTION
    assert "P1_004            = NOT_ASSIGNED" in SELECTION
    assert "OWNER_GO          = NOT_GRANTED" in SELECTION
    assert "IMPLEMENTATION    = NOT_AUTHORIZED" in SELECTION


def test_candidate_selection_requires_separate_authority_ladder() -> None:
    for marker in (
        "CANDIDATE_SELECTED_DOCS_ONLY",
        "→ NON_PROJECTION_IMPLEMENTATION_CONTRACT_FROZEN_DOCS_ONLY",
        "→ explicit separate NON_PROJECTION_OWNER_GO_AUTHORIZED_BOUNDED",
        "→ clean Tier A bounded implementation PR",
    ):
        assert marker in SELECTION
