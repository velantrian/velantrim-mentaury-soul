"""Structural checks for governance risk-tier contract alignment.

Эти тесты проверяют согласованность docs/GOVERNANCE.md и CODEOWNERS,
а не GitHub branch-protection (которая остаётся административной).
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = (ROOT / "docs" / "GOVERNANCE.md").read_text(encoding="utf-8")
CODEOWNERS = (ROOT / "CODEOWNERS").read_text(encoding="utf-8")
CURRENT_STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")

_APPROVED_STATUSES = {
    "READY_FOR_REVIEW",
    "BLOCKED_BY_CI",
    "BLOCKED_BY_CHANGES_REQUESTED",
    "BLOCKED_BY_INDEPENDENT_REVIEW",
    "BLOCKED_BY_STALE_REVIEW",
    "BLOCKED_BY_ADMIN_ENFORCEMENT",
    "ACCEPTED_FOR_MERGE",
}

# Existing Tier A paths that must be present now (not if/when).
_EXISTING_TIER_A = (
    "src/mentaury/storage/**",
    "src/mentaury/replay/**",
    "src/mentaury/beliefs/**",
    "src/mentaury/evidence/**",
    "src/mentaury/contracts/canonical_json.py",
    "scripts/validate.py",
    "scripts/check_doc_freshness.py",
    ".github/workflows/**",
    "requirements*.lock",
    "pyproject.toml",
    "CODEOWNERS",
    "docs/CURRENT_STATUS.md",
    "docs/GOVERNANCE.md",
    "docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md",
    "docs/research/POST_P0_ROADMAP_V0.1.md",
)

_IF_WHEN_TIER_A = (
    "src/mentaury/**/authority/**",
    "src/mentaury/**/lease/**",
    "src/mentaury/schema/**",
    "src/mentaury/canonical.py",
    "src/mentaury/canonical/**",
    "src/mentaury/integrity/**",
    "src/mentaury/redaction/**",
)

# CODEOWNERS active (non-comment) entries mapped from existing Tier A surfaces.
_CODEOWNERS_EXISTING = (
    "/src/mentaury/storage/",
    "/src/mentaury/replay/",
    "/src/mentaury/beliefs/",
    "/src/mentaury/evidence/",
    "/src/mentaury/contracts/canonical_json.py",
    "/scripts/validate.py",
    "/scripts/check_doc_freshness.py",
    "/.github/workflows/",
    "/requirements*.lock",
    "/pyproject.toml",
    "/CODEOWNERS",
    "/docs/CURRENT_STATUS.md",
    "/docs/GOVERNANCE.md",
    "/docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md",
    "/docs/research/POST_P0_ROADMAP_V0.1.md",
)


def _active_codeowner_paths(text: str) -> list[str]:
    paths: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        paths.append(stripped.split()[0])
    return paths


def test_current_status_is_classified_tier_a() -> None:
    assert "docs/CURRENT_STATUS.md" in GOVERNANCE
    assert "Tier A" in GOVERNANCE
    section = GOVERNANCE.split("### 3.2 Tier A")[1].split("### 3.3 Tier B")[0]
    assert "docs/CURRENT_STATUS.md" in section


def test_storage_and_workflows_are_tier_a() -> None:
    section = GOVERNANCE.split("### 3.2 Tier A")[1].split("### 3.3 Tier B")[0]
    assert "src/mentaury/storage/**" in section
    assert ".github/workflows/**" in section
    assert "requirements*.lock" in section


def test_existing_tier_a_paths_are_listed_without_duplicates() -> None:
    section = GOVERNANCE.split("#### Existing protected / high-risk paths")[1]
    section = section.split("#### Paths reserved if/when created")[0]
    fence = section.split("```text", 1)[1].split("```", 1)[0]
    listed = [line.strip() for line in fence.splitlines() if line.strip()]
    assert listed == list(_EXISTING_TIER_A)
    assert len(listed) == len(set(listed))


def test_reserved_paths_are_marked_if_when_created() -> None:
    section = GOVERNANCE.split("#### Paths reserved if/when created")[1]
    section = section.split("#### Tier A requirements")[0]
    lines = [line.strip() for line in section.splitlines() if line.strip()]
    for path in _IF_WHEN_TIER_A:
        matching = [line for line in lines if line.startswith(path)]
        assert len(matching) == 1, path
        assert "if/when created" in matching[0], path


def test_every_existing_tier_a_path_exists_on_disk() -> None:
    for pattern in _EXISTING_TIER_A:
        if pattern.endswith("/**"):
            root = ROOT / pattern[:-3]
            assert root.exists(), pattern
        elif "*" in pattern:
            # Glob lockfiles: at least one requirements*.lock must exist.
            matches = list(ROOT.glob(pattern))
            assert matches, pattern
        else:
            assert (ROOT / pattern).exists(), pattern


def test_codeowners_aligns_with_existing_tier_a_surfaces() -> None:
    active = _active_codeowner_paths(CODEOWNERS)
    assert active == list(_CODEOWNERS_EXISTING)
    assert len(active) == len(set(active))


def test_codeowners_keeps_if_when_paths_commented() -> None:
    # Reserved globs must not be active CODEOWNERS entries until created.
    active = set(_active_codeowner_paths(CODEOWNERS))
    for reserved in (
        "/src/mentaury/schema/",
        "/src/mentaury/canonical.py",
        "/src/mentaury/canonical/",
        "/src/mentaury/integrity/",
        "/src/mentaury/redaction/",
    ):
        assert reserved not in active
    assert "# /src/mentaury/**/authority/" in CODEOWNERS
    assert "# /src/mentaury/**/lease/" in CODEOWNERS


def test_pr_local_status_vocabulary_is_enumerated() -> None:
    for status in _APPROVED_STATUSES:
        assert status in GOVERNANCE
    # Vague status must be constrained, not promoted as standalone vocabulary.
    assert "BLOCKED_BY_GOVERNANCE_IDENTITY" in GOVERNANCE
    assert "must not be used without specifying" in GOVERNANCE


def test_automatic_escalation_rule_present() -> None:
    assert "entire PR becomes Tier A" in GOVERNANCE
    assert "Highest-risk file/effect classifies the whole PR" in CURRENT_STATUS or (
        "highest-risk" in GOVERNANCE.lower()
    )


def test_current_status_points_to_governance_authority() -> None:
    assert "docs/GOVERNANCE.md" in CURRENT_STATUS
    assert "NOT ESTABLISHED for #45/#46/#50/#51" in CURRENT_STATUS
    assert "CONFIRMED for #50/#51" in CURRENT_STATUS
