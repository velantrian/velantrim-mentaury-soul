"""Structural checks for the adopted solo-maintainer governance contract."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = (ROOT / "docs" / "GOVERNANCE.md").read_text(encoding="utf-8")
CODEOWNERS = (ROOT / "CODEOWNERS").read_text(encoding="utf-8")
CURRENT_STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
SOLO_MODE = (ROOT / "docs" / "governance" / "solo-maintainer-mode.md").read_text(
    encoding="utf-8"
)
REVIEW_CHECKLIST = (
    ROOT / "docs" / "governance" / "solo-maintainer-review-checklist.md"
).read_text(encoding="utf-8")
P1_001_AUTH = (ROOT / "docs" / "P1_001_IMPLEMENTATION_AUTHORIZATION.md").read_text(
    encoding="utf-8"
)
P1_002_AUTH = (ROOT / "docs" / "P1_002_IMPLEMENTATION_AUTHORIZATION.md").read_text(
    encoding="utf-8"
)
P1_002_CONTRACT = (
    ROOT / "docs" / "research" / "P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md"
).read_text(encoding="utf-8")

_ACTIVE_STATUSES = (
    "DRAFT",
    "READY_FOR_MAINTAINER_REVIEW",
    "BLOCKED_BY_CI",
    "BLOCKED_BY_CONFLICT",
    "BLOCKED_BY_CHANGES_REQUESTED",
    "BLOCKED_BY_UNRESOLVED_CONVERSATION",
    "BLOCKED_BY_AUTHORIZATION_BOUNDARY",
    "ACCEPTED_FOR_MERGE",
    "MERGED",
)

_EXISTING_TIER_A = (
    "src/mentaury/storage/**",
    "src/mentaury/replay/**",
    "src/mentaury/beliefs/**",
    "src/mentaury/evidence/**",
    "src/mentaury/capabilities/lease/**",
    "src/mentaury/privacy/reconciliation/**",
    "src/mentaury/contracts/canonical_json.py",
    "scripts/validate.py",
    "scripts/check_doc_freshness.py",
    ".github/workflows/**",
    "requirements*.lock",
    "pyproject.toml",
    "CODEOWNERS",
    "docs/CURRENT_STATUS.md",
    "docs/GOVERNANCE.md",
    "docs/governance/**",
    "docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md",
    "docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md",
    "docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md",
    "docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md",
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

_CODEOWNERS_EXISTING = (
    "/src/mentaury/storage/",
    "/src/mentaury/replay/",
    "/src/mentaury/beliefs/",
    "/src/mentaury/evidence/",
    "/src/mentaury/capabilities/lease/",
    "/src/mentaury/privacy/reconciliation/",
    "/src/mentaury/contracts/canonical_json.py",
    "/scripts/validate.py",
    "/scripts/check_doc_freshness.py",
    "/.github/workflows/",
    "/requirements*.lock",
    "/pyproject.toml",
    "/CODEOWNERS",
    "/docs/CURRENT_STATUS.md",
    "/docs/GOVERNANCE.md",
    "/docs/governance/",
    "/docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md",
    "/docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md",
    "/docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md",
    "/docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md",
    "/docs/research/POST_P0_ROADMAP_V0.1.md",
)


def _active_codeowner_paths(text: str) -> list[str]:
    return [
        line.strip().split()[0]
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def _between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def _first_text_fence(section: str) -> list[str]:
    fence = section.split("```text", 1)[1].split("```", 1)[0]
    return [line.strip() for line in fence.splitlines() if line.strip()]


def test_solo_mode_is_the_current_operating_contract() -> None:
    assert "**Current operating mode:** SOLO MAINTAINER" in GOVERNANCE
    assert "required approvals = 0" in GOVERNANCE
    assert "no genuinely independent human reviewer" in GOVERNANCE
    assert "solo maintainer mode" in SOLO_MODE.lower()


def test_active_status_vocabulary_is_exact() -> None:
    section = _between(
        GOVERNANCE, "## 2. Standard merge statuses", "## 3. Risk classification"
    )
    assert _first_text_fence(section) == list(_ACTIVE_STATUSES)
    assert "BLOCKED_BY_INDEPENDENT_REVIEW" not in _first_text_fence(section)


def test_existing_tier_a_paths_are_exact_and_unique() -> None:
    section = _between(
        GOVERNANCE,
        "#### Existing protected / high-risk paths",
        "#### Paths reserved if/when created",
    )
    listed = _first_text_fence(section)
    assert listed == list(_EXISTING_TIER_A)
    assert len(listed) == len(set(listed))


def test_reserved_tier_a_paths_are_exact() -> None:
    section = _between(
        GOVERNANCE,
        "#### Paths reserved if/when created",
        "#### Tier A requirements",
    )
    lines = _first_text_fence(section)
    for path in _IF_WHEN_TIER_A:
        assert sum(line.startswith(path) for line in lines) == 1


def test_every_existing_tier_a_path_exists_in_candidate_tree() -> None:
    for pattern in _EXISTING_TIER_A:
        if pattern.endswith("/**"):
            assert (ROOT / pattern[:-3]).exists(), pattern
        elif "*" in pattern:
            assert list(ROOT.glob(pattern)), pattern
        else:
            assert (ROOT / pattern).exists(), pattern


def test_codeowners_aligns_with_tier_a_surfaces() -> None:
    active = _active_codeowner_paths(CODEOWNERS)
    assert active == list(_CODEOWNERS_EXISTING)
    assert len(active) == len(set(active))


def test_p1_001_scope_remains_bounded() -> None:
    assert "OWNER_GO · AUTHORIZED_BOUNDED · NOT_STARTED" in P1_001_AUTH
    assert "/src/mentaury/capabilities/lease/ @velantrian" in CODEOWNERS
    assert "P1-001 authority outside the pure resolver scope" in GOVERNANCE
    assert "Capability Lease registry persistence or service" in GOVERNANCE


def test_p1_002_authorization_activates_only_exact_pure_path() -> None:
    assert "OWNER_GO · AUTHORIZED_BOUNDED · NOT_STARTED" in P1_002_AUTH
    assert "P1_002_OWNER_GO_AUTHORIZED_BOUNDED" in P1_002_AUTH
    assert "P1_002_MUTATION_AUTHORITY_NONE" in P1_002_AUTH
    assert "P1_002_RETRIEVAL_AUTHORITY_NONE" in P1_002_AUTH
    assert "/src/mentaury/privacy/reconciliation/ @velantrian" in CODEOWNERS
    assert "/docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md @velantrian" in CODEOWNERS
    assert "src/mentaury/privacy/reconciliation/**" in GOVERNANCE
    assert "P1-002 authority outside the pure classifier scope" in GOVERNANCE
    assert "P1_002_IMPLEMENTATION_NOT_AUTHORIZED" in P1_002_CONTRACT
    assert (ROOT / "src" / "mentaury" / "privacy" / "reconciliation").is_dir()
    assert (ROOT / "tests" / "test_privacy_reconciliation_classifier.py").is_file()


def test_other_reserved_codeowner_paths_remain_commented() -> None:
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


def test_tier_a_requires_distinct_reviews_and_post_merge_ci() -> None:
    section = _between(GOVERNANCE, "#### Tier A requirements", "### 3.3 Tier B")
    assert "two-pass maintainer review" in section
    assert "**Correctness pass**" in section
    assert "**Adversarial pass**" in section
    assert "post-merge `main` CI" in section
    assert "Correctness pass" in REVIEW_CHECKLIST
    assert "Adversarial pass" in REVIEW_CHECKLIST


def test_automatic_escalation_and_historical_gate_rules_remain() -> None:
    assert "the entire PR becomes Tier A" in GOVERNANCE
    assert "highest-risk file or semantic effect" in GOVERNANCE
    assert "Any older repository text" in GOVERNANCE
    assert "superseded by this policy" in GOVERNANCE
    assert "BLOCKED_BY_INDEPENDENT_REVIEW" in GOVERNANCE


def test_future_team_transition_remains_explicit() -> None:
    assert "## 7. Transition to public or team operation" in GOVERNANCE
    assert "set required approvals to `1`" in GOVERNANCE
    assert "Issue #39" in GOVERNANCE
    assert "future lifecycle trigger" in GOVERNANCE


def test_current_status_points_to_governance_and_p1_002_receipt() -> None:
    assert "docs/GOVERNANCE.md" in CURRENT_STATUS
    assert "docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md" in CURRENT_STATUS
