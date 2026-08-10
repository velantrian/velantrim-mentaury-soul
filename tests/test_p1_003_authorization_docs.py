"""Structural assertions for the bounded P1-003 Owner GO receipt."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md"
).read_text(encoding="utf-8")
AUTH = (ROOT / "docs" / "P1_003_IMPLEMENTATION_AUTHORIZATION.md").read_text(
    encoding="utf-8"
)
CURRENT_STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)
INDEX = (ROOT / "docs" / "research" / "RESEARCH_INDEX.md").read_text(
    encoding="utf-8"
)


def test_frozen_contract_remains_the_no_go_freeze_receipt() -> None:
    """The contract-freeze document is historical evidence, not rewritten GO."""

    assert "P1-003 contract:                FROZEN_DOCS" in CONTRACT
    assert "Owner GO:                       NOT_GRANTED" in CONTRACT
    assert "Implementation authorization:   NONE" in CONTRACT
    assert "CONTRACT FROZEN ≠ OWNER GO" in CONTRACT
    assert "P1_003_OWNER_GO_AUTHORIZED_BOUNDED" not in CONTRACT


def test_owner_go_is_separate_bounded_and_not_started() -> None:
    assert "OWNER_GO · AUTHORIZED_BOUNDED · NOT_STARTED" in AUTH
    assert "P1_003_CONTRACT = FROZEN_DOCS" in AUTH
    assert "P1_003_OWNER_GO = AUTHORIZED_BOUNDED" in AUTH
    assert "P1_003_OWNER_GO_AUTHORIZED_BOUNDED" in AUTH
    assert "P1_003_IMPLEMENTATION_NOT_STARTED" in AUTH
    assert "P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED" in AUTH
    assert "AUTHORIZED_BOUNDED · P1-003-v0.1 ONLY" in AUTH
    assert "one-time / consumable" in AUTH
    assert "OWNER GO ≠ IMPLEMENTATION COMPLETE" in AUTH


def test_authoritative_surfaces_reference_the_receipt_and_same_state() -> None:
    for document in (CURRENT_STATUS, ROADMAP, INDEX):
        assert "P1_003_IMPLEMENTATION_AUTHORIZATION.md" in document
        assert "P1_003_OWNER_GO_AUTHORIZED_BOUNDED" in document
        assert "P1_003_IMPLEMENTATION_NOT_STARTED" in document
        assert "P1_003_RUNTIME_ASSIGNMENT" in document or "P1-003 assignment" in document
        assert "P1-003-v0.1" in document


def test_owner_go_preserves_frozen_implementation_contract() -> None:
    for token in (
        "P1-003-v0.1",
        "CROSS-GATE-BINDING-v0.1",
        "MENTAURY_CANONICAL_JSON_V1",
        "MENTAURY_P1_003_COMMON_REQUEST_V1",
        "MENTAURY_P1_003_EVALUATION_EVIDENCE_V1",
        "P1-001-v0.2",
        "P1-002-v0.1",
        "compose_governed_constraints",
        "CrossGateEvaluationContext",
    ):
        assert token in CONTRACT
        assert token in AUTH

    assert "CompositionBudget" in CONTRACT
    assert "exact frozen context and budget schemas remain unchanged" in AUTH

    for family in (
        "CGC-CTX-001…012",
        "CGC-FP-001…010",
        "CGC-DEC-001…012",
        "CGC-T-001…012",
        "CGC-M-001…010",
        "CGC-PURE-001…006",
    ):
        assert family in AUTH


def test_authorization_boundary_remains_non_executing() -> None:
    combined = f"{AUTH}\n{CURRENT_STATUS}\n{ROADMAP}\n{INDEX}"
    for marker in (
        "ACTION_GATE = NOT_AUTHORIZED",
        "RETRIEVAL_EXECUTION = NOT_AUTHORIZED",
        "TOOL_EXECUTION = NOT_AUTHORIZED",
        "IDENTITY_RUNTIME = NOT_AUTHORIZED",
        "RELATIONSHIP_RUNTIME = NOT_AUTHORIZED",
        "DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN",
        "RUNTIME_DEPLOYMENT = NOT_AUTHORIZED",
        "CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION",
    ):
        assert marker in combined


def test_owner_go_milestone_contains_no_p1_003_runtime_implementation() -> None:
    assert not (ROOT / "src" / "mentaury" / "composition").exists()
    assert "No `src/mentaury/composition/**` file is created" in AUTH


def test_compatibility_stop_is_explicit() -> None:
    for marker in (
        "STOP_CURRENT_IMPLEMENTATION",
        "NEW_DOCS_ONLY_CONTRACT_REVISION",
        "NEW_OWNER_DECISION",
    ):
        assert marker in AUTH
