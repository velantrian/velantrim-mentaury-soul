"""Structural consistency checks for the P1-001 contract and owner GO.

These tests do not implement or validate a capability resolver. They preserve
three distinct states:

- the immutable frozen contract receipt;
- the later bounded implementation authorization;
- implementation completion, which is still not claimed.
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
AUTH = (ROOT / "docs" / "P1_001_IMPLEMENTATION_AUTHORIZATION.md").read_text(
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

_AUTHORIZED_PATHS = (
    "src/mentaury/capabilities/__init__.py",
    "src/mentaury/capabilities/lease/__init__.py",
    "src/mentaury/capabilities/lease/contracts.py",
    "src/mentaury/capabilities/lease/resolver.py",
    "tests/test_capability_lease_resolution.py",
)


def _deny_results() -> list[str]:
    section = LEASE.split("## 7. 🚦 Normative deny precedence", 1)[1].split(
        "## 8. 📤 ResolutionResult", 1
    )[0]
    return re.findall(
        r"^\|\s*\d+\s*\|.*?\|\s*`([A-Z_]+)`\s*\|$", section, re.MULTILINE
    )


def _scenario_ids() -> list[int]:
    section = LEASE.split("## 9. 🧪 Scenario contract", 1)[1].split(
        "## 10. 🧱 P0 compatibility", 1
    )[0]
    return [int(value) for value in re.findall(r"`CAP-SC-(\d{3})`", section)]


def test_frozen_contract_and_later_owner_go_are_distinct() -> None:
    assert "FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED" in LEASE
    assert "Implementation in src/:       NOT AUTHORIZED" in LEASE

    assert "P1_001_IMPLEMENTATION_AUTHORIZED_BOUNDED" in STATUS
    assert "P1_001_IMPLEMENTATION_NOT_STARTED" in STATUS
    assert "P1_001_COMPLETION_NOT_CLAIMED" in STATUS
    assert "AUTHORIZED_BOUNDED · NOT_STARTED" in ROADMAP
    assert "OWNER_GO · AUTHORIZED_BOUNDED · NOT_STARTED" in AUTH

    combined_current = "\n".join((STATUS, ROADMAP, INDEX, AUTH))
    assert "Implementation completion:    NOT CLAIMED" in combined_current
    assert "ACTION_GATE_NOT_AUTHORIZED" in combined_current
    assert "DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN" in combined_current


def test_authorization_scope_is_exact_and_bounded() -> None:
    for path in _AUTHORIZED_PATHS:
        assert AUTH.count(path) == 1, path
        assert path in STATUS
        assert path in ROADMAP

    for forbidden in (
        "registry persistence",
        "network access",
        "ambient system clock",
        "event append",
        "replay or projection integration",
        "direct or indirect M3 write",
        "Action Gate",
        "tool execution",
        "backend selection or migration",
        "production deployment",
    ):
        assert forbidden.lower() in AUTH.lower(), forbidden


def test_current_governance_is_solo_tier_a_without_fake_independence() -> None:
    assert "Review mode:                  SOLO_MAINTAINER · TIER_A" in LEASE
    assert "Current review mode:          SOLO_MAINTAINER · TIER_A" in ROADMAP
    assert "Current governance:           SOLO_MAINTAINER" in INDEX
    assert "Governance:                   SOLO_MAINTAINER · TIER_A" in AUTH
    assert "**Current operating mode:** SOLO MAINTAINER" in GOVERNANCE

    combined = "\n".join((LEASE, ROADMAP, INDEX, AUTH)).lower()
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
    assert "CAP-SC-001…CAP-SC-025" in AUTH


def test_lifecycle_ambiguity_is_closed_fail_closed() -> None:
    assert "status EXPIRED while evaluated_at < expires_at" in LEASE
    assert "→ LEASE_CONTRACT_VIOLATION" in LEASE
    assert "status ACTIVE while evaluated_at >= expires_at" in LEASE
    assert "→ LEASE_EXPIRED" in LEASE
    assert "premature materialized `EXPIRED` status" in LEASE


def test_budget_vocabulary_is_consistent() -> None:
    combined = "\n".join((LEASE, ROADMAP, AUTH))
    assert "max_record_bytes" in LEASE
    assert "max_record_bytes" in ROADMAP
    assert "max_canonical_bytes" not in combined


def test_p0_and_execution_boundaries_remain_explicit() -> None:
    for document in (LEASE, ROADMAP, INDEX, AUTH):
        assert "Action Gate" in document
        assert "M3" in document
    assert "P0 events remain replayable without a registry" in LEASE
    assert "no backend selected" in INDEX.lower()
    assert "DOMAIN_RUNTIME_NOT_AUTHORIZED" in ROADMAP
    assert "ALLOW executes nothing" in AUTH


def test_owning_documents_link_to_each_other() -> None:
    assert "POST_P0_ROADMAP_V0.1.md" in LEASE
    assert "RESEARCH_INDEX.md" in LEASE
    assert "MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md" in ROADMAP
    assert "P1_001_IMPLEMENTATION_AUTHORIZATION.md" in ROADMAP
    assert "MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md" in INDEX
    assert "P1_001_IMPLEMENTATION_AUTHORIZATION.md" in INDEX
    assert "MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md" in AUTH
    assert "docs/CURRENT_STATUS.md" in AUTH
    assert "docs/GOVERNANCE.md" in INDEX or "../GOVERNANCE.md" in INDEX
