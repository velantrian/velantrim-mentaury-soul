"""#173 Track B regressions: role-aware Environment Manifest freshness.

docs/ENVIRONMENT_MANIFEST.md is classified `historical_or_reconcile_before_use`
in docs/ai/project_manifest.json (#160) and carries a direct-file currentness
marker (#176). These tests confirm the freshness gate respects that role
instead of silently treating it as a complete active current implementation
ledger, and fails closed if the role or its marker drift.
"""

from __future__ import annotations

import json
from pathlib import Path

from check_doc_freshness import (
    ACTIVE_DERIVED_DOC_PATHS,
    ENVIRONMENT_MANIFEST_PATH,
    ENVIRONMENT_MANIFEST_RELATIVE_PATH,
    PROJECT_MANIFEST_PATH,
    evaluate,
    evaluate_environment_manifest_role,
)

ROOT = Path(__file__).resolve().parents[1]

_ACTIVE_PATHS = tuple(str(p.relative_to(ROOT)) for p in ACTIVE_DERIVED_DOC_PATHS)

_MARKED_RECONCILE_TEXT = """# ⚙️ Mentaury Environment Manifest

> **Currentness:** historical / `RECONCILE_BEFORE_USE`.
> This file is a bounded environment / P-stage inventory checkpoint, not a complete current implementation ledger.
> Reconcile against docs/CURRENT_STATUS.md and live GitHub before treating the source list below as exhaustive.

```text
P0-001…P0-008_IMPLEMENTED_IN_MAIN
```
"""


def _manifest(*, reconcile_paths: list[str]) -> dict[str, object]:
    return {"historical_or_reconcile_before_use": reconcile_paths}


def test_current_repository_environment_manifest_role_passes() -> None:
    """Test A: real repository shape passes as-is."""

    project_manifest = json.loads(PROJECT_MANIFEST_PATH.read_text(encoding="utf-8"))
    environment_manifest_text = ENVIRONMENT_MANIFEST_PATH.read_text(encoding="utf-8")

    problems = evaluate_environment_manifest_role(
        project_manifest,
        environment_manifest_text,
        active_derived_relative_paths=_ACTIVE_PATHS,
    )
    assert problems == []
    assert ENVIRONMENT_MANIFEST_RELATIVE_PATH not in _ACTIVE_PATHS


def test_historical_incomplete_p_stage_inventory_does_not_fail() -> None:
    """Test B: an old/incomplete P-stage inventory is not a defect once marked."""

    problems = evaluate_environment_manifest_role(
        _manifest(reconcile_paths=[ENVIRONMENT_MANIFEST_RELATIVE_PATH]),
        _MARKED_RECONCILE_TEXT,
        active_derived_relative_paths=_ACTIVE_PATHS,
    )
    assert problems == []


def test_missing_currentness_marker_fails_closed() -> None:
    """Test C: RECONCILE_BEFORE_USE role without its marker fails closed."""

    unmarked_text = "# ⚙️ Mentaury Environment Manifest\n\nP0-001…P0-015_IMPLEMENTED_IN_MAIN\n"

    problems = evaluate_environment_manifest_role(
        _manifest(reconcile_paths=[ENVIRONMENT_MANIFEST_RELATIVE_PATH]),
        unmarked_text,
        active_derived_relative_paths=_ACTIVE_PATHS,
    )
    assert len(problems) == 1
    assert "missing required" in problems[0]
    assert "Currentness:" in problems[0]


def test_dual_role_contradiction_fails() -> None:
    """Test D: active-current AND historical/reconcile-before-use is a conflict."""

    problems = evaluate_environment_manifest_role(
        _manifest(reconcile_paths=[ENVIRONMENT_MANIFEST_RELATIVE_PATH]),
        _MARKED_RECONCILE_TEXT,
        active_derived_relative_paths=(*_ACTIVE_PATHS, ENVIRONMENT_MANIFEST_RELATIVE_PATH),
    )
    assert any("classified both as" in problem for problem in problems)


def test_silent_role_promotion_out_of_reconcile_fails() -> None:
    """Losing the RECONCILE_BEFORE_USE classification must not go unnoticed."""

    problems = evaluate_environment_manifest_role(
        _manifest(reconcile_paths=[]),
        _MARKED_RECONCILE_TEXT,
        active_derived_relative_paths=_ACTIVE_PATHS,
    )
    assert any("is no longer listed under" in problem for problem in problems)


def test_malformed_manifest_role_list_fails_closed() -> None:
    problems = evaluate_environment_manifest_role(
        {"historical_or_reconcile_before_use": "not-a-list"},
        _MARKED_RECONCILE_TEXT,
        active_derived_relative_paths=_ACTIVE_PATHS,
    )
    assert len(problems) == 1
    assert "must be a list" in problems[0]


def test_active_surfaces_retain_legacy_p_stage_protection() -> None:
    """Test E: README/Quick Reference still fail on a stale P-stage marker."""

    authoritative = (
        "| P0-014 Minimal Belief Lifecycle | ✅ Implemented | belief status ≠ truth |\n"
        "| P0-015 Deterministic Evidence Gate | ✅ Implemented | gate receipt ≠ fact |\n"
    )
    problems = evaluate(
        authoritative,
        {
            "README.md": "P0-001…P0-015_IMPLEMENTED_IN_MAIN",
            "docs/MENTAURY_QUICK_REFERENCE.md": "P0-001…P0-008_IMPLEMENTED_IN_MAIN",
        },
    )
    assert len(problems) == 1
    assert "docs/MENTAURY_QUICK_REFERENCE.md" in problems[0]


def test_active_derived_doc_paths_excludes_environment_manifest() -> None:
    assert ENVIRONMENT_MANIFEST_PATH not in ACTIVE_DERIVED_DOC_PATHS
