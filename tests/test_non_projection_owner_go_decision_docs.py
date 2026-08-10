"""Structural assertions for the docs-only NPG-v0.1 Owner GO milestone."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION = (
    ROOT / "docs" / "research" / "NON_PROJECTION_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_owner_go_is_explicit_exact_and_bounded() -> None:
    for marker in (
        "OWNER GO DECISION: GO.",
        "OWNER_GO_DECISION = GO",
        "NON_PROJECTION_OWNER_GO = GRANTED",
        "OWNER_GO_SCOPE = NPG-v0.1_ONLY",
        "IMPLEMENTATION_AUTHORIZATION = GRANTED_FOR_NEXT_SEPARATE_BOUNDED_IMPLEMENTATION_MILESTONE",
        "Contract version:                    NPG-v0.1",
        "Envelope version:                    AIE-v0.1",
        "Candidate:                           PURE_NON_PROJECTION_CLASSIFIER",
        "Owning contract PR:                  #86",
        "Budget clarification PR:             #87",
    ):
        assert marker in DECISION


def test_owner_go_does_not_start_implementation_or_runtime() -> None:
    for marker in (
        "NON_PROJECTION_IMPLEMENTATION = NOT_STARTED",
        "NON_PROJECTION_RUNTIME = NOT_AUTHORIZED",
        "P1_004 = NOT_ASSIGNED",
        "ACTION_GATE = NOT_AUTHORIZED",
        "RETRIEVAL_EXECUTION = NOT_AUTHORIZED",
        "TOOL_EXECUTION = NOT_AUTHORIZED",
        "IDENTITY_RUNTIME = NOT_AUTHORIZED",
        "RELATIONSHIP_RUNTIME = NOT_AUTHORIZED",
        "DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN",
        "RUNTIME_DEPLOYMENT = NOT_AUTHORIZED",
        "OWNER_GO_GRANTED\n≠ IMPLEMENTATION_STARTED\n≠ IMPLEMENTATION_COMPLETED\n≠ RUNTIME_ENABLED\n≠ ACTION_AUTHORITY",
    ):
        assert marker in DECISION


def test_exact_frozen_contract_identity_and_api_are_preserved() -> None:
    for marker in (
        "Contract version:                    NPG-v0.1",
        "Envelope version:                    AIE-v0.1",
        "Candidate:                           PURE_NON_PROJECTION_CLASSIFIER",
        "def classify_non_projection(",
        "envelope: AttributedInterpretationEnvelope",
        "budget: NonProjectionBudget",
        ") -> NonProjectionResult:",
    ):
        assert marker in CONTRACT or marker in DECISION


def test_fail_closed_identity_result_precedence_and_budget_remain_frozen() -> None:
    for marker in (
        "VERIFIED_SELF → DEFER · SELF_BASIS_UNVERIFIED",
        "REJECT > DEFER > CONTESTED > REVISE_REQUIRED > PASS_ATTRIBUTED",
        "hard-cap overflow → NonProjectionContractError",
        "local-budget overflow while still inside hard caps → DEFER · BUDGET_EXHAUSTED",
        "Silent truncation, sampling, reordering, auto-upgrade and permissive fallback",
    ):
        assert marker in DECISION


def test_authority_ceiling_cannot_be_laundered() -> None:
    for marker in (
        "≠ factual truth proof",
        "≠ Mentaury autobiography",
        "≠ identity claim or stable M3 trait",
        "≠ relationship / commitment / consent authority",
        "≠ Action Gate PASS",
        "≠ retrieval permission",
        "≠ tool / execution permission",
        "≠ deployment permission",
    ):
        assert marker in DECISION


def test_all_frozen_safety_and_executable_families_remain_bound() -> None:
    for number in range(1, 13):
        assert f"NPG-T{number:02d}" in CONTRACT
    for number in range(1, 13):
        assert f"NPG-SC-{number:03d}" in CONTRACT
    for number in range(1, 9):
        assert f"MT-NPG-{number:03d}" in CONTRACT

    for marker in (
        "NPG-SC-CONTESTED-001",
        "NPC-CTX-001…022",
        "NPC-FP-001…008",
        "NPC-DEC-001…016",
        "NPC-T-001…012",
        "NPC-SC-001…012",
        "NPC-SC-CONTESTED-001",
        "NPC-M-001…008",
        "NPC-PURE-001…010",
    ):
        assert marker in CONTRACT
        assert marker in DECISION


def test_p1_canon_and_governance_boundaries_are_preserved() -> None:
    for marker in (
        "P1-001 contract = unchanged",
        "P1-002 contract = unchanged",
        "P1-003 contract = unchanged",
        "MENTAURY_CANON_V0.1 = unchanged",
        "SOLO_MAINTAINER = ACTIVE",
        "INDEPENDENT_HUMAN_REVIEW = NO",
        "Issue #39 remains open",
    ):
        assert marker in DECISION


def test_owner_go_pr_contains_no_non_projection_implementation_package_yet() -> None:
    assert not (ROOT / "src" / "mentaury" / "non_projection").exists()


def test_stop_boundary_is_explicit() -> None:
    for marker in (
        "CONTRACT FROZEN\n+ EXPLICIT OWNER GO\n≠ IMPLEMENTATION",
        "OWNER GO\n≠ RUNTIME ENABLEMENT",
        "OWNER GO\n≠ ACTION AUTHORITY",
        "fresh live preflight required before any code",
    ):
        assert marker in DECISION
