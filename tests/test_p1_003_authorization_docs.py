"""Structural assertions for the completed bounded P1-003 receipt."""

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


def test_frozen_contract_remains_historical_no_go_freeze_receipt() -> None:
    assert "P1-003 contract:                FROZEN_DOCS" in CONTRACT
    assert "Owner GO:                       NOT_GRANTED" in CONTRACT
    assert "Implementation authorization:   NONE" in CONTRACT
    assert "CONTRACT FROZEN ≠ OWNER GO" in CONTRACT
    assert "P1_003_OWNER_GO_CONSUMED" not in CONTRACT
    assert "IMPLEMENTED_BOUNDED" not in CONTRACT


def test_receipt_records_consumed_bounded_completion() -> None:
    assert "OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED" in AUTH
    assert "P1_003_OWNER_GO = CONSUMED" in AUTH
    assert "P1_003_OWNER_GO_CONSUMED" in AUTH
    assert "P1_003_IMPLEMENTATION = IMPLEMENTED_BOUNDED" in AUTH
    assert "P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_IMPLEMENTED_BOUNDED" in AUTH
    assert "P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED" in AUTH
    assert "NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED" in AUTH
    assert "Implementation authorization: CONSUMED · P1-003-v0.1 ONLY" in AUTH


def test_completion_evidence_is_exact_and_reviewed() -> None:
    for marker in (
        "Implementation PR:         #79",
        "9855f766f2bf801c8297c4f870b21d3ed37911fb",
        "31394829487 · SUCCESS · 552 passed",
        "4897445251",
        "59f2caa4deacd06aee0bbfc8dae1221edcb666eb",
        "31395291622 · SUCCESS · 552 passed",
        "Correctness pass:          PASS",
        "Adversarial pass:          PASS",
        "Authorization boundary:    PRESERVED",
        "Independent human review:  NO",
    ):
        assert marker in AUTH


def test_authoritative_surfaces_share_completed_state() -> None:
    for document in (CURRENT_STATUS, ROADMAP, INDEX):
        assert "P1_003_IMPLEMENTATION_AUTHORIZATION.md" in document
        assert "IMPLEMENTED_BOUNDED" in document
        assert "P1_003_RUNTIME_ASSIGNMENT" in document or "P1-003 runtime assignment" in document
        assert "NOT_ASSIGNED" in document
        assert "NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED" in document

    assert "P1_003_OWNER_GO_CONSUMED" in CURRENT_STATUS
    assert "P1-003 Owner GO:               CONSUMED" in ROADMAP
    assert "P1-003 Owner GO:              CONSUMED" in INDEX


def test_historical_authorization_provenance_is_preserved_but_superseded() -> None:
    assert "Historical authorization provenance" in AUTH
    assert "P1_003_OWNER_GO_AUTHORIZED_BOUNDED" in AUTH
    assert "P1_003_IMPLEMENTATION_NOT_STARTED" in AUTH
    assert "superseded by the verified\ncompletion state" in AUTH
    assert "Historical pre-implementation markers" in CURRENT_STATUS


def test_completed_scope_is_exact_four_file_package() -> None:
    package = ROOT / "src" / "mentaury" / "composition"
    expected = {
        "__init__.py",
        "governed_constraints/__init__.py",
        "governed_constraints/contracts.py",
        "governed_constraints/composer.py",
    }
    actual = {
        path.relative_to(package).as_posix()
        for path in package.rglob("*.py")
    }
    assert actual == expected
    for path in expected:
        assert (package / path).is_file()


def test_full_frozen_matrix_remains_required_and_completed() -> None:
    for family in (
        "CGC-CTX-001…014",
        "CGC-FP-001…010",
        "CGC-DEC-001…014",
        "CGC-T-001…012",
        "CGC-M-001…010",
        "CGC-PURE-001…008",
    ):
        assert family in AUTH
        assert family in CONTRACT


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


def test_compatibility_stop_is_retained_after_completion() -> None:
    for marker in (
        "STOP_CURRENT_IMPLEMENTATION",
        "NEW_DOCS_ONLY_CONTRACT_REVISION",
        "NEW_OWNER_DECISION",
    ):
        assert marker in AUTH
