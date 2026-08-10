"""Structural assertions for the NPG-v0.1 bounded implementation receipt."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = (ROOT / "docs" / "NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md").read_text(
    encoding="utf-8"
)
CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_completion_is_bound_to_exact_frozen_contract_and_pr() -> None:
    for marker in (
        "Status:                           OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED",
        "Milestone:                        Pure Non-Projection Classifier · NPG-v0.1",
        "NON_PROJECTION_CONTRACT_VERSION = NPG-v0.1 · UNCHANGED",
        "ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION = AIE-v0.1 · UNCHANGED",
        "NON_PROJECTION_CANDIDATE = PURE_NON_PROJECTION_CLASSIFIER",
        "NON_PROJECTION_OWNER_GO = CONSUMED_BY_PR_90",
        "IMPLEMENTATION_AUTHORIZATION = CONSUMED · NPG-v0.1_ONLY",
        "NON_PROJECTION_IMPLEMENTATION = IMPLEMENTED_BOUNDED",
        "Implementation PR:             #90",
        "Reviewed exact head:           a61427f85c70531b329894d5dc310e43bcc9d7de",
        "Exact-head CI:                 31438692348 · SUCCESS · 762 passed",
        "Protected squash merge/main:   cfb59fb7a49166d55360c6a8843269ab8f18b9e0",
        "Resulting-main CI:             31438898049 · SUCCESS · 762 passed",
    ):
        assert marker in RECEIPT


def test_exact_completed_package_is_recorded() -> None:
    for path in (
        "src/mentaury/non_projection/__init__.py",
        "src/mentaury/non_projection/contracts.py",
        "src/mentaury/non_projection/classifier.py",
        "tests/test_non_projection_classifier.py",
        "tests/test_non_projection_classifier_conformance.py",
    ):
        assert path in RECEIPT
        assert (ROOT / path).exists()


def test_frozen_semantics_remain_bound() -> None:
    for marker in (
        "VERIFIED_SELF → DEFER · SELF_BASIS_UNVERIFIED",
        "REJECT\n> DEFER\n> CONTESTED\n> REVISE_REQUIRED\n> PASS_ATTRIBUTED",
        "hard-cap overflow\n→ NonProjectionContractError",
        "local-budget overflow while still inside hard caps\n→ DEFER · BUDGET_EXHAUSTED",
        "6e0d6105651b905626ae1552d6ac58baf0f238520ce16eed31bece91bf9e4150",
    ):
        assert marker in RECEIPT
    assert "Contract version:                    NPG-v0.1" in CONTRACT
    assert "Envelope version:                    AIE-v0.1" in CONTRACT


def test_all_executable_families_remain_recorded() -> None:
    for marker in (
        "NPC-CTX-001…022",
        "NPC-FP-001…008",
        "NPC-DEC-001…016",
        "NPC-T-001…012",
        "NPC-SC-001…012",
        "NPC-SC-CONTESTED-001",
        "NPC-M-001…008",
        "NPC-PURE-001…010",
    ):
        assert marker in RECEIPT
        assert marker in CONTRACT


def test_runtime_and_authority_boundaries_remain_closed() -> None:
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
        "IMPLEMENTED_BOUNDED\n≠ RUNTIME_ASSIGNED\n≠ RUNTIME_ENABLED\n≠ ACTION_AUTHORITY\n≠ DEPLOYMENT",
    ):
        assert marker in RECEIPT


def test_stale_summary_state_is_not_promoted_or_bulk_rewritten() -> None:
    assert "historical summary state" in RECEIPT
    assert "#86 → #87 → #88 → #89 → #90" in RECEIPT
    assert "not bulk-rewritten" in RECEIPT
    assert "Any such transition requires a new explicit bounded milestone" in RECEIPT
