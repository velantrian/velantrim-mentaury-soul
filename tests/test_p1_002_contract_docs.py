"""Structural tests for the frozen P1-002 privacy reconciliation contract.

These checks prove document consistency and authorization boundaries only. They
must remain green before any separate implementation authorization is proposed.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md"
).read_text(encoding="utf-8")
CURRENT_STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
ROADMAP = (
    ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md"
).read_text(encoding="utf-8")
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


def test_contract_is_frozen_without_implementation_authority() -> None:
    assert "FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED" in CONTRACT
    assert "Implementation authorization: NOT GRANTED BY THIS DOCUMENT" in CONTRACT
    assert "P1_002_CONTRACT_FROZEN_DOCS" in CONTRACT
    assert "P1_002_IMPLEMENTATION_NOT_AUTHORIZED" in CONTRACT
    assert "P1_002_RUNTIME_DEPLOYMENT_NOT_AUTHORIZED" in CONTRACT
    assert "NO_STORAGE_OR_DOMAIN_MUTATION_AUTHORIZED" in CONTRACT


def test_authoritative_surfaces_select_the_same_bounded_contract() -> None:
    for document in (CURRENT_STATUS, ROADMAP, INDEX):
        assert "P1-002 Privacy Reconciliation Classifier" in document
        assert "P1_002_IMPLEMENTATION_NOT_AUTHORIZED" in document
    assert "P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md" in CURRENT_STATUS
    assert "P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md" in ROADMAP
    assert "P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md" in INDEX


def test_result_vocabulary_is_exact_and_non_executing() -> None:
    bounded_scope = _between(CONTRACT, "## 2. 🧱 Exact bounded scope", "## 3. 🧩 Contract vocabulary")
    decisions = re.findall(
        r"^(ALLOW_REFERENCE|DENY_RETRIEVAL|QUARANTINE_REQUIRED|REBUILD_REQUIRED)$",
        bounded_scope,
        re.MULTILINE,
    )
    assert decisions == [
        "ALLOW_REFERENCE",
        "DENY_RETRIEVAL",
        "QUARANTINE_REQUIRED",
        "REBUILD_REQUIRED",
    ]
    assert "classification data only" in CONTRACT
    assert "does not delete" in CONTRACT
    assert "performs no retrieval" in CONTRACT
    assert "grants no capability" in CONTRACT


def test_all_frozen_scenarios_are_present_once_and_in_order() -> None:
    scenario_section = _between(CONTRACT, "## 7. 🧪 Frozen scenarios", "## 8. 🔬 Required validation properties")
    found = tuple(re.findall(r"^(PRIV-SC-\d{3})\s", scenario_section, re.MULTILINE))
    assert found == _EXPECTED_SCENARIOS
    assert len(found) == len(set(found))


def test_normative_precedence_is_exact() -> None:
    precedence_section = _between(CONTRACT, "## 5. 🔁 Deterministic precedence", "### 5.1 Surface-specific remediation mapping")
    found = tuple(
        value.strip()
        for value in re.findall(r"^\d{2}\s+(.+)$", precedence_section, re.MULTILINE)
    )
    assert found == _EXPECTED_PRECEDENCE
    assert "The first matching reason wins" in precedence_section


def test_surface_remediation_mapping_is_explicit() -> None:
    mapping = _between(CONTRACT, "### 5.1 Surface-specific remediation mapping", "## 6. 🧾 Minimal result")
    assert "`BACKUP`, `FORK` | `QUARANTINE_REQUIRED`" in mapping
    assert "`INDEX`, `EMBEDDING`, `GRAPH_EDGE`, `CACHE`, `DERIVED_SUMMARY` | `REBUILD_REQUIRED`" in mapping
    assert "`PRIMARY` | `DENY_RETRIEVAL`" in mapping
    assert "`COPY_ABSENT` | `DENY_RETRIEVAL`" in mapping
    assert "`COPY_ALREADY_QUARANTINED` | `QUARANTINE_REQUIRED`" in mapping


def test_privacy_vocabulary_and_budget_guards_are_frozen() -> None:
    for value in (
        "PUBLIC",
        "PERSONAL",
        "SENSITIVE",
        "INTIMATE",
        "RESTRICTED",
        "THIRD_PARTY",
        "REDACTED",
        "PRIMARY",
        "BACKUP",
        "INDEX",
        "EMBEDDING",
        "GRAPH_EDGE",
        "CACHE",
        "DERIVED_SUMMARY",
        "FORK",
    ):
        assert value in CONTRACT
    assert "max_serialized_bytes" in CONTRACT
    assert "max_purposes" in CONTRACT
    assert "max_branches" in CONTRACT
    assert "booleans are rejected" in CONTRACT
    assert "sorted, unique tuples" in CONTRACT


def test_p0_p1_and_identity_boundaries_remain_separate() -> None:
    compatibility = _between(CONTRACT, "## 10. 🔗 Compatibility boundaries", "## 11. 🚫 Explicit non-goals")
    assert "P0 redaction executor" in compatibility
    assert "P1-002 classifier" in compatibility
    assert "Neither result authorizes execution" in compatibility
    assert "must not call P1-001 internally" in CONTRACT
    assert "privacy classification" in compatibility
    assert "≠ relationship decision" in compatibility
    assert "≠ identity continuity decision" in compatibility
    assert "≠ M2 or M3 mutation" in compatibility


def test_non_goals_block_hidden_runtime_promotion() -> None:
    non_goals = _between(CONTRACT, "## 11. 🚫 Explicit non-goals", "## 12. ⛔ Authorization boundary")
    for phrase in (
        "content deletion",
        "quarantine execution",
        "retrieval execution",
        "network lookup",
        "filesystem or database access",
        "relationship reconciliation",
        "identity continuity runtime",
        "M3 nomination or write",
        "Capability Lease validation",
        "Action Gate",
        "Tool Receipt runtime",
        "tool execution",
        "backend selection or migration",
        "production deployment",
    ):
        assert phrase in non_goals


def test_governance_and_codeowners_keep_source_path_reserved() -> None:
    contract_path = "docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md"
    assert contract_path in GOVERNANCE
    assert f"/{contract_path} @velantrian" in CODEOWNERS
    assert "src/mentaury/privacy/reconciliation/**" in GOVERNANCE
    assert "inactive until Owner GO" in GOVERNANCE
    assert "# /src/mentaury/privacy/reconciliation/ @velantrian" in CODEOWNERS


def test_no_implementation_or_authorization_receipt_exists_yet() -> None:
    assert not (ROOT / "docs" / "P1_002_IMPLEMENTATION_AUTHORIZATION.md").exists()
    assert not (ROOT / "src" / "mentaury" / "privacy").exists()
    assert not (ROOT / "tests" / "test_privacy_reconciliation_classifier.py").exists()
