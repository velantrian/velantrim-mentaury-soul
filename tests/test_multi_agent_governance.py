"""Structural checks for serialized multi-agent execution governance."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = (ROOT / "docs" / "GOVERNANCE.md").read_text(encoding="utf-8")
SOLO_MODE = (ROOT / "docs" / "governance" / "solo-maintainer-mode.md").read_text(
    encoding="utf-8"
)
MULTI_AGENT = (
    ROOT / "docs" / "governance" / "multi-agent-serialized-execution.md"
).read_text(encoding="utf-8")
REVIEW_CHECKLIST = (
    ROOT / "docs" / "governance" / "solo-maintainer-review-checklist.md"
).read_text(encoding="utf-8")

_REQUIRED_MARKERS = (
    "MULTI_AGENT_EXECUTION_MODE = SERIALIZED_BY_BOUNDED_MILESTONE",
    "ONE_BOUNDED_MILESTONE = ONE_ACTIVE_WRITER",
    "PARALLEL_READ_AUDIT = ALLOWED",
    "PARALLEL_WRITE_SAME_MILESTONE = FORBIDDEN",
    "AUTHORITY_MILESTONES = STRICTLY_SERIALIZED",
    "MAIN_DRIFT = REVERIFY_BEFORE_CONTINUING",
)


def test_canonical_governance_adopts_serialized_multi_agent_execution() -> None:
    assert "docs/governance/multi-agent-serialized-execution.md" in GOVERNANCE
    for marker in _REQUIRED_MARKERS:
        assert marker in GOVERNANCE
        assert marker in MULTI_AGENT


def test_solo_mode_mirrors_the_active_writer_boundary() -> None:
    for marker in _REQUIRED_MARKERS:
        assert marker in SOLO_MODE
    assert "second AI session" in SOLO_MODE
    assert "not an independent" in SOLO_MODE


def test_same_milestone_parallel_writes_fail_closed() -> None:
    assert "UNKNOWN_OR_CONFLICTING_WRITER_STATE = STOP_AND_RECONCILE" in GOVERNANCE
    assert "UNKNOWN_OR_CONFLICTING_WRITER_STATE = STOP_AND_RECONCILE" in MULTI_AGENT
    assert "Do not race the other writer to merge" in MULTI_AGENT
    assert "NEW WRITE / MERGE = STOPPED_PENDING_RECONCILIATION" in MULTI_AGENT


def test_main_drift_requires_semantic_reconciliation() -> None:
    assert "STOP MUTATION" in MULTI_AGENT
    assert "READ NEW MAIN" in MULTI_AGENT
    assert "RE-EVALUATE SCOPE AND AUTHORIZATION" in MULTI_AGENT
    assert "clean textual merge" in MULTI_AGENT
    assert "clean textual merge" in GOVERNANCE


def test_authority_transitions_are_strictly_serialized() -> None:
    section = MULTI_AGENT.split("## 5. Strictly serialized authority milestones", 1)[1]
    for phrase in (
        "contract freeze or contract revision",
        "Owner GO",
        "implementation authorization",
        "runtime activation",
        "governance authority changes",
        "deployment authorization",
    ):
        assert phrase in section
    assert "merged `main` plus verified resulting-main CI" in section
    assert "CONTRACT FROZEN ≠ OWNER GO" in section
    assert "OWNER GO ≠ IMPLEMENTATION COMPLETE" in section


def test_writer_transfer_does_not_create_independent_review() -> None:
    section = MULTI_AGENT.split("## 6. Writer transfer", 1)[1]
    assert "previous active writer stops repository mutations" in section
    assert "new writer re-reads current `main`" in section
    assert "Transfer does not create independent review" in section


def test_tier_a_checklist_contains_multi_agent_preflight() -> None:
    assert "## 3. Multi-agent execution preflight" in REVIEW_CHECKLIST
    assert "Multi-agent writer state: SERIALIZED / NOT_APPLICABLE / CONCERN" in REVIEW_CHECKLIST
    assert "Competing same-scope PR/write detected: NO / YES" in REVIEW_CHECKLIST
    assert "Main drift reconciled: YES / NOT_APPLICABLE / NO" in REVIEW_CHECKLIST
    assert "Any unresolved `CONCERN`" in REVIEW_CHECKLIST


def test_governance_hardening_does_not_grant_p1_003_authority() -> None:
    section = MULTI_AGENT.split("## 8. Current P1-003 boundary", 1)[1]
    assert "P1_003_CONTRACT = FROZEN_DOCS" in section
    assert "P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED" in section
    assert "P1_003_OWNER_GO = NOT_GRANTED" in section
    assert "IMPLEMENTATION_AUTHORIZATION = NONE" in section
    assert "does not grant P1-003 Owner GO" in GOVERNANCE
