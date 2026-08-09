"""Structural tests for the P1-002 contract and bounded authorization."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT / "docs" / "research" / "P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md"
).read_text(encoding="utf-8")
AUTH = (ROOT / "docs" / "P1_002_IMPLEMENTATION_AUTHORIZATION.md").read_text(
    encoding="utf-8"
)
CURRENT_STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)
INDEX = (ROOT / "docs" / "research" / "RESEARCH_INDEX.md").read_text(
    encoding="utf-8"
)
GOVERNANCE = (ROOT / "docs" / "GOVERNANCE.md").read_text(encoding="utf-8")
CODEOWNERS = (ROOT / "CODEOWNERS").read_text(encoding="utf-8")

_EXPECTED_SCENARIOS = tuple(f"PRIV-SC-{number:03d}" for number in range(1, 16))
_EXPECTED_PRECEDENCE = (
    "exact typed-or-mapping admission",
    "unknown-field / wrong-type / non-canonical collection rejection",
    "cross-record linkage invariants",
    "canonical serialized-size and collection budgets",
    "COPY_ABSENT",
    "COPY_ALREADY_QUARANTINED",
    "DELETED_OR_REDACTED_MATERIAL",
    "THIRD_PARTY_PERMISSION_MISSING",
    "PURPOSE_WITHDRAWN",
    "PURPOSE_NOT_PERMITTED",
    "BRANCH_NOT_PERMITTED",
    "STALE_POLICY_REVISION",
    "ALLOW_REFERENCE",
)


def _between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def test_frozen_contract_remains_historical() -> None:
    assert "FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED" in CONTRACT
    assert "Implementation authorization: NOT GRANTED BY THIS DOCUMENT" in CONTRACT
    assert "P1_002_CONTRACT_FROZEN_DOCS" in CONTRACT
    assert "P1_002_IMPLEMENTATION_NOT_AUTHORIZED" in CONTRACT
    assert "P1_002_RUNTIME_DEPLOYMENT_NOT_AUTHORIZED" in CONTRACT
    assert "NO_STORAGE_OR_DOMAIN_MUTATION_AUTHORIZED" in CONTRACT


def test_new_owner_go_is_separate_and_bounded() -> None:
    assert "OWNER_GO · AUTHORIZED_BOUNDED · NOT_STARTED" in AUTH
    for marker in (
        "P1_002_OWNER_GO_AUTHORIZED_BOUNDED",
        "P1_002_IMPLEMENTATION_NOT_STARTED",
        "P1_002_MUTATION_AUTHORITY_NONE",
        "P1_002_RETRIEVAL_AUTHORITY_NONE",
        "NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED",
    ):
        assert marker in AUTH
        assert marker in CURRENT_STATUS or marker in ROADMAP or marker in INDEX
    assert "does not reuse the consumed\nP1-001 authorization" in AUTH


def test_authoritative_surfaces_reference_contract_and_receipt() -> None:
    for document in (CURRENT_STATUS, ROADMAP, INDEX, AUTH):
        assert "P1-002 Privacy Reconciliation Classifier" in document
    for document in (CURRENT_STATUS, ROADMAP, INDEX):
        assert "P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md" in document
        assert "P1_002_IMPLEMENTATION_AUTHORIZATION.md" in document


def test_result_vocabulary_is_exact_and_non_executing() -> None:
    scope = _between(CONTRACT, "## 2. 🧱 Exact bounded scope", "## 3. 🧩 Contract vocabulary")
    assert re.findall(
        r"^(ALLOW_REFERENCE|DENY_RETRIEVAL|QUARANTINE_REQUIRED|REBUILD_REQUIRED)$",
        scope,
        re.MULTILINE,
    ) == [
        "ALLOW_REFERENCE",
        "DENY_RETRIEVAL",
        "QUARANTINE_REQUIRED",
        "REBUILD_REQUIRED",
    ]
    assert "classification data only" in CONTRACT
    assert "performs no retrieval" in CONTRACT
    assert "grants no capability" in CONTRACT
    assert "classification data only" in AUTH


def test_all_frozen_scenarios_are_present_once_and_in_order() -> None:
    section = _between(CONTRACT, "## 7. 🧪 Frozen scenarios", "## 8. 🔬 Required validation properties")
    found = tuple(re.findall(r"^(PRIV-SC-\d{3})\s", section, re.MULTILINE))
    assert found == _EXPECTED_SCENARIOS
    assert len(found) == len(set(found))


def test_normative_precedence_is_exact() -> None:
    section = _between(CONTRACT, "## 5. 🔁 Deterministic precedence", "### 5.1 Surface-specific remediation mapping")
    found = tuple(value.strip() for value in re.findall(r"^\d{2}\s+(.+)$", section, re.MULTILINE))
    assert found == _EXPECTED_PRECEDENCE
    assert "The first matching reason wins" in section


def test_surface_mapping_and_budget_vocabulary_are_frozen() -> None:
    mapping = _between(CONTRACT, "### 5.1 Surface-specific remediation mapping", "## 6. 🧾 Minimal result")
    assert "`BACKUP`, `FORK` | `QUARANTINE_REQUIRED`" in mapping
    assert "`INDEX`, `EMBEDDING`, `GRAPH_EDGE`, `CACHE`, `DERIVED_SUMMARY` | `REBUILD_REQUIRED`" in mapping
    assert "`PRIMARY` | `DENY_RETRIEVAL`" in mapping
    for token in ("max_serialized_bytes", "max_purposes", "max_branches"):
        assert token in CONTRACT
        assert token in AUTH or token == "max_serialized_bytes"
    assert "booleans are rejected" in CONTRACT
    assert "sorted, unique tuples" in CONTRACT


def test_p0_p1_identity_and_execution_boundaries_remain_separate() -> None:
    compatibility = _between(CONTRACT, "## 10. 🔗 Compatibility boundaries", "## 11. 🚫 Explicit non-goals")
    assert "P0 redaction executor" in compatibility
    assert "P1-002 classifier" in compatibility
    assert "Neither result authorizes execution" in compatibility
    assert "must not call P1-001 internally" in CONTRACT
    assert "≠ relationship decision" in compatibility
    assert "≠ identity continuity decision" in compatibility
    assert "≠ M2 or M3 mutation" in compatibility


def test_authorization_preserves_all_non_goals() -> None:
    combined = f"{CONTRACT}\n{AUTH}\n{GOVERNANCE}"
    for phrase in (
        "content deletion",
        "quarantine execution",
        "retrieval execution",
        "filesystem or database access",
        "relationship mutation",
        "identity continuity runtime",
        "M3",
        "Capability Lease validation",
        "Action Gate",
        "Tool Receipt runtime",
        "tool execution",
        "backend selection",
        "production deployment",
    ):
        assert phrase.lower() in combined.lower()


def test_governance_and_codeowners_activate_only_exact_path() -> None:
    assert "src/mentaury/privacy/reconciliation/**" in GOVERNANCE
    assert "/src/mentaury/privacy/reconciliation/ @velantrian" in CODEOWNERS
    assert "/docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md @velantrian" in CODEOWNERS
    assert "P1-002 authority outside the pure classifier scope" in GOVERNANCE


def test_authorization_exists_but_implementation_is_not_started() -> None:
    assert (ROOT / "docs" / "P1_002_IMPLEMENTATION_AUTHORIZATION.md").exists()
    assert not (ROOT / "src" / "mentaury" / "privacy").exists()
    assert not (ROOT / "tests" / "test_privacy_reconciliation_classifier.py").exists()
