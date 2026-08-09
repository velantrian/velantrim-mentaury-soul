"""Structural checks for the P1-001 contract and completion evidence.

These tests preserve four distinct facts:

- the immutable frozen contract receipt;
- the later bounded owner authorization;
- the verified bounded implementation completion;
- the absence of authority for any subsequent runtime milestone.
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
README = (ROOT / "README.md").read_text(encoding="utf-8")
QUICK = (ROOT / "docs" / "MENTAURY_QUICK_REFERENCE.md").read_text(
    encoding="utf-8"
)
ENVIRONMENT = (ROOT / "docs" / "ENVIRONMENT_MANIFEST.md").read_text(
    encoding="utf-8"
)

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

_IMPLEMENTED_PATHS = (
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


def test_frozen_contract_remains_historical_while_current_state_is_implemented() -> None:
    assert "FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED" in LEASE
    assert "Implementation in src/:       NOT AUTHORIZED" in LEASE

    assert "P1_001_CAPABILITY_LEASE_RESOLUTION_IMPLEMENTED_BOUNDED" in STATUS
    assert "P1_001_PURE_RESOLVER_VALIDATED" in STATUS
    assert "P1-001 implementation:        IMPLEMENTED_BOUNDED" in ROADMAP
    assert "OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED" in AUTH
    assert "Completed execution milestone:P1-001 · IMPLEMENTED_BOUNDED" in INDEX

    for document in (STATUS, ROADMAP, INDEX, AUTH, README, QUICK, ENVIRONMENT):
        assert "NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED" in document


def test_implementation_scope_exists_and_matches_receipt() -> None:
    for path in _IMPLEMENTED_PATHS:
        assert (ROOT / path).exists(), path
        assert path in STATUS
        assert path in AUTH

    for path in _IMPLEMENTED_PATHS[:4]:
        assert path in ROADMAP or path in ENVIRONMENT


def test_completion_evidence_is_consistent() -> None:
    evidence_documents = (STATUS, ROADMAP, INDEX, AUTH, README, QUICK, ENVIRONMENT)
    immutable_evidence = (
        "53b3eec436d4dbfd2c13050a9966fb84ef0b7b3a",
        "31322108100",
        "d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98",
        "31322210843",
        "e873e43331fa7273b92f896b371707e4779b17d4",
        "31323051934",
        "f21809d8f31a457bd7acfe1d766230973ba9ecf5",
        "31323138053",
    )
    combined = "\n".join(evidence_documents)
    for receipt in immutable_evidence:
        assert receipt in combined

    for document in (STATUS, ROADMAP, AUTH, README, QUICK):
        assert "387 passed" in document


def test_authorization_is_consumed_and_does_not_roll_forward() -> None:
    combined = "\n".join((STATUS, ROADMAP, INDEX, AUTH)).lower()
    for forbidden in (
        "registry persistence",
        "registry service",
        "network",
        "ambient clock",
        "action gate",
        "tool execution",
        "event append",
        "replay",
        "m3",
        "backend selection",
        "production deployment",
    ):
        assert forbidden in combined, forbidden

    assert "authorization does not roll forward" in AUTH.lower()
    assert "owner go is consumed" in INDEX.lower()
    assert "no registry service, action gate, p1-002" in ROADMAP.lower()


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


def test_scenario_ids_are_unique_contiguous_and_implemented() -> None:
    ids = _scenario_ids()
    assert ids == list(range(1, 26))
    assert len(ids) == len(set(ids))
    assert "CAP-SC-001…CAP-SC-025" in AUTH
    implementation_tests = (ROOT / "tests" / "test_capability_lease_resolution.py").read_text(
        encoding="utf-8"
    )
    for scenario in range(1, 26):
        assert f"test_cap_sc_{scenario:03d}" in implementation_tests


def test_lifecycle_ambiguity_is_closed_fail_closed() -> None:
    assert "status EXPIRED while evaluated_at < expires_at" in LEASE
    assert "→ LEASE_CONTRACT_VIOLATION" in LEASE
    assert "status ACTIVE while evaluated_at >= expires_at" in LEASE
    assert "→ LEASE_EXPIRED" in LEASE
    assert "premature materialized `EXPIRED` status" in LEASE


def test_budget_vocabulary_is_consistent() -> None:
    combined = "\n".join((LEASE, ROADMAP, AUTH))
    assert "max_record_bytes" in LEASE
    assert "max_record_bytes" in AUTH
    assert "max_canonical_bytes" not in combined


def test_p0_and_execution_boundaries_remain_explicit() -> None:
    for document in (LEASE, ROADMAP, INDEX, AUTH):
        assert "Action Gate" in document
        assert "M3" in document
    assert "P0 events remain replayable without a registry" in LEASE
    assert "no backend" in INDEX.lower()
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
    assert "../GOVERNANCE.md" in INDEX
