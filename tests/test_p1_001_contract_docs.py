"""Structural consistency checks for the docs-only P1-001 contract.

These tests do not implement or validate a capability resolver. They prevent the
three owning documents from drifting across governance, deny precedence, scenario
numbering, and explicit non-authorization boundaries.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEASE = (
    ROOT / "docs" / "research" / "MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md"
).read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "research" / "POST_P0_ROADMAP_V0.1.md").read_text(
    encoding="utf-8"
)
INDEX = (ROOT / "docs" / "research" / "RESEARCH_INDEX.md").read_text(
    encoding="utf-8"
)
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
GOVERNANCE = (ROOT / "docs" / "GOVERNANCE.md").read_text(encoding="utf-8")

_EXPECTED_DENY_ORDER = [
    "REQUEST_INVALID",
    "BUDGET_MISSING",
    "BUDGET_EXHAUSTED",
    "REGISTRY_UNAVAILABLE",
    "REGISTRY_CONTRACT_VIOLATION",
    "UNKNOWN_LEASE",
    "REVISION_MISMATCH",
    "BUDGET_EXHAUSTED",
    "LEASE_CONTRACT_VIOLATION",
    "LEASE_DIGEST_MISMATCH",
    "LEASE_CONTRACT_VIOLATION",
    "LEASE_CONTRACT_VIOLATION",
    "LEASE_REVOKED",
    "LEASE_EXPIRED",
    "LEASE_NOT_ACTIVE",
    "NOT_YET_VALID",
    "PURPOSE_MISMATCH",
    "OPERATION_NOT_ALLOWED",
    "BUDGET_EXHAUSTED",
    "DATA_SCOPE_VIOLATION",
    "SIDE_EFFECT_NOT_ALLOWED",
    "ALLOW",
]


def _deny_results() -> list[str]:
    section = LEASE.split("## 7. 🚦 Normative deny precedence", 1)[1].split(
        "## 8. 📤 ResolutionResult", 1
    )[0]
    rows = re.findall(r"^\|\s*\d+\s*\|.*?\|\s*`([A-Z_]+)`\s*\|$", section, re.MULTILINE)
    return rows


def _scenario_ids() -> list[int]:
    section = LEASE.split("## 9. 🧪 Scenario contract", 1)[1].split(
        "## 10. 🧱 P0 compatibility boundary", 1
    )[0]
    return [int(value) for value in re.findall(r"`CAP-SC-(\d{3})`", section)]


def test_p1_001_remains_docs_only_and_not_authorized() -> None:
    assert "CONTRACT_DRAFT · DOCS_ONLY" in LEASE or "FROZEN_DOCS · DOCS_ONLY" in LEASE
    assert "Implementation in src/:       NOT AUTHORIZED" in LEASE
    assert "CAPABILITY_LEASE_RESOLVER_NOT_AUTHORIZED" in ROADMAP
    assert "P1_001_CAPABILITY_LEASE_RESOLUTION_DOCS_ONLY_NOT_IMPLEMENTED" in STATUS
    assert "CAPABILITY_LEASE_RESOLVER_NOT_AUTHORIZED" in STATUS


def test_current_governance_is_solo_tier_a_without_fake_independence() -> None:
    assert "Review mode:                  SOLO_MAINTAINER · TIER_A" in LEASE
    assert "Current review mode:          SOLO_MAINTAINER · TIER_A" in ROADMAP
    assert "Current governance:           SOLO_MAINTAINER" in INDEX
    assert "**Current operating mode:** SOLO MAINTAINER" in GOVERNANCE

    combined = "\n".join((LEASE, ROADMAP, INDEX)).lower()
    for obsolete_gate in (
        "independent exact-head review",
        "independent docs review",
        "independent architecture review",
        "merge-blocking independent review",
        "awaiting qualifying approval",
    ):
        assert obsolete_gate not in combined


def test_registry_and_lease_admission_are_distinct() -> None:
    assert "### 3.1 RegistrySnapshot admission" in LEASE
    assert "REGISTRY_CONTRACT_VIOLATION" in LEASE
    assert "### 4.1 Record admission" in LEASE
    assert "LEASE_CONTRACT_VIOLATION" in LEASE
    assert "REGISTRY_UNAVAILABLE ≠ REGISTRY_CONTRACT_VIOLATION" in LEASE
    assert "REGISTRY_CONTRACT_VIOLATION ≠ UNKNOWN_LEASE" in LEASE


def test_deny_precedence_is_exact_and_complete() -> None:
    assert _deny_results() == _EXPECTED_DENY_ORDER


def test_scenario_ids_are_unique_and_contiguous() -> None:
    ids = _scenario_ids()
    assert ids == list(range(1, 26))
    assert len(ids) == len(set(ids))


def test_lifecycle_ambiguity_is_closed_fail_closed() -> None:
    assert "status EXPIRED while evaluated_at < expires_at" in LEASE
    assert "→ LEASE_CONTRACT_VIOLATION" in LEASE
    assert "status ACTIVE while evaluated_at >= expires_at" in LEASE
    assert "→ LEASE_EXPIRED" in LEASE
    assert "premature materialized `EXPIRED` status" in LEASE


def test_budget_vocabulary_is_consistent() -> None:
    combined = "\n".join((LEASE, ROADMAP))
    assert "max_record_bytes" in LEASE
    assert "max_record_bytes" in ROADMAP
    assert "max_canonical_bytes" not in combined


def test_p0_and_execution_boundaries_remain_explicit() -> None:
    for document in (LEASE, ROADMAP, INDEX):
        assert "Action Gate" in document
        assert "M3" in document
    assert "P0 events remain replayable without a registry" in LEASE
    assert "no backend selected" in INDEX.lower()
    assert "DOMAIN_RUNTIME_NOT_AUTHORIZED" in ROADMAP


def test_owning_documents_link_to_each_other() -> None:
    assert "POST_P0_ROADMAP_V0.1.md" in LEASE
    assert "RESEARCH_INDEX.md" in LEASE
    assert "MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md" in ROADMAP
    assert "MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md" in INDEX
    assert "docs/GOVERNANCE.md" in INDEX or "../GOVERNANCE.md" in INDEX
