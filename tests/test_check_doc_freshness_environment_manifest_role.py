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

import check_doc_freshness
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


def test_historical_ledger_without_p_stage_marker_does_not_fail() -> None:
    """Track B must not require a historical P-stage ledger at all."""

    marked_without_p_stage = """# ⚙️ Mentaury Environment Manifest

> **Currentness:** historical / `RECONCILE_BEFORE_USE`.
> This file is a bounded environment checkpoint, not a complete current implementation ledger.
> Reconcile against docs/CURRENT_STATUS.md and live GitHub before use.
"""
    problems = evaluate_environment_manifest_role(
        _manifest(reconcile_paths=[ENVIRONMENT_MANIFEST_RELATIVE_PATH]),
        marked_without_p_stage,
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


def test_partial_currentness_marker_loss_fails_closed() -> None:
    """A plausible-looking but incomplete reconciliation marker must fail."""

    degraded_text = _MARKED_RECONCILE_TEXT.replace(
        "docs/CURRENT_STATUS.md", "docs/STALE_STATUS.md"
    )
    problems = evaluate_environment_manifest_role(
        _manifest(reconcile_paths=[ENVIRONMENT_MANIFEST_RELATIVE_PATH]),
        degraded_text,
        active_derived_relative_paths=_ACTIVE_PATHS,
    )
    assert len(problems) == 1
    assert "CURRENT_STATUS.md" in problems[0]


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


def test_manifest_role_object_instead_of_list_fails_closed() -> None:
    """JSON object keys must not accidentally act like a valid role list."""

    problems = evaluate_environment_manifest_role(
        {
            "historical_or_reconcile_before_use": {
                ENVIRONMENT_MANIFEST_RELATIVE_PATH: {"role": "RECONCILE_BEFORE_USE"}
            }
        },
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


def test_main_fails_closed_when_environment_manifest_marker_is_missing(
    monkeypatch, tmp_path: Path
) -> None:
    """End-to-end wiring: main() must actually execute the new Track B guard."""

    unmarked_path = tmp_path / "ENVIRONMENT_MANIFEST.md"
    unmarked_path.write_text(
        "# ⚙️ Mentaury Environment Manifest\n\nP0-001…P0-015_IMPLEMENTED_IN_MAIN\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        check_doc_freshness, "ENVIRONMENT_MANIFEST_PATH", unmarked_path
    )

    assert check_doc_freshness.main() == 1


def test_main_fails_closed_on_malformed_manifest_role_shape(
    monkeypatch, tmp_path: Path
) -> None:
    """End-to-end wiring: malformed routing metadata must not pass via iteration."""

    malformed_manifest_path = tmp_path / "project_manifest.json"
    malformed_manifest_path.write_text(
        json.dumps(
            {
                "historical_or_reconcile_before_use": {
                    ENVIRONMENT_MANIFEST_RELATIVE_PATH: {
                        "role": "RECONCILE_BEFORE_USE"
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        check_doc_freshness, "PROJECT_MANIFEST_PATH", malformed_manifest_path
    )

    assert check_doc_freshness.main() == 1
