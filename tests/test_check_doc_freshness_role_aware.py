"""Track B regression tests: role-aware Environment Manifest freshness (#173).

``docs/ai/project_manifest.json`` already classifies
``docs/ENVIRONMENT_MANIFEST.md`` as ``historical_or_reconcile_before_use``.
These tests lock in that the freshness gate no longer holds that surface to
the active-current P-stage full-currentness guard, while still fail-closing
on a missing role/marker or a role contradiction. See
``evaluate_role_conflicts`` and ``evaluate_reconcile_before_use_integrity``
in ``scripts/check_doc_freshness.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

import check_doc_freshness
from check_doc_freshness import (
    evaluate_reconcile_before_use_integrity,
    evaluate_role_conflicts,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "ai" / "project_manifest.json"
ENVIRONMENT_MANIFEST_PATH = ROOT / "docs" / "ENVIRONMENT_MANIFEST.md"
ENVIRONMENT_MANIFEST_NAME = "docs/ENVIRONMENT_MANIFEST.md"

_VALID_RECONCILE_MARKERS = (
    "> **Currentness:** historical / `RECONCILE_BEFORE_USE`.\n"
    "> Reconcile against docs/CURRENT_STATUS.md and live GitHub before use.\n"
    "> The preserved body is provenance and is not rewritten here.\n"
)


def _manifest_historical_paths() -> list[str]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    historical = manifest["historical_or_reconcile_before_use"]
    assert isinstance(historical, list)
    return historical


# --- Test A: current repository configuration passes -----------------------


def test_current_environment_manifest_role_passes() -> None:
    historical = _manifest_historical_paths()
    doc_texts = {
        ENVIRONMENT_MANIFEST_NAME: ENVIRONMENT_MANIFEST_PATH.read_text(encoding="utf-8")
    }
    assert evaluate_reconcile_before_use_integrity(historical, doc_texts) == []

    active_paths = ["README.md", "docs/MENTAURY_QUICK_REFERENCE.md"]
    assert evaluate_role_conflicts(active_paths, historical) == []


def test_full_gate_passes_on_real_repository() -> None:
    assert check_doc_freshness.main() == 0


def test_environment_manifest_is_not_an_active_derived_surface() -> None:
    active_names = {
        str(path.relative_to(ROOT)) for path in check_doc_freshness.ACTIVE_DERIVED_DOC_PATHS
    }
    assert ENVIRONMENT_MANIFEST_NAME not in active_names

    reconcile_names = {
        str(path.relative_to(ROOT))
        for path in check_doc_freshness.RECONCILE_BEFORE_USE_DOC_PATHS
    }
    assert ENVIRONMENT_MANIFEST_NAME in reconcile_names


# --- Test B: historical ledger may remain historically incomplete ----------


def test_historical_ledger_incomplete_p_stage_inventory_does_not_fail() -> None:
    # Deliberately omits final V1 CBP/EPR/ATR/HDE/E2E coverage — that is
    # exactly the historical-provenance gap Track B must tolerate.
    text = _VALID_RECONCILE_MARKERS + "\nP0-001…P0-008_IMPLEMENTED_IN_MAIN\n"
    problems = evaluate_reconcile_before_use_integrity(
        [ENVIRONMENT_MANIFEST_NAME],
        {ENVIRONMENT_MANIFEST_NAME: text},
    )
    assert problems == []


def test_historical_ledger_with_no_p_stage_marker_at_all_does_not_fail() -> None:
    text = _VALID_RECONCILE_MARKERS + "\nNo P-stage marker of any kind here.\n"
    problems = evaluate_reconcile_before_use_integrity(
        [ENVIRONMENT_MANIFEST_NAME],
        {ENVIRONMENT_MANIFEST_NAME: text},
    )
    assert problems == []


# --- Test C: missing currentness marker fails closed ------------------------


def test_missing_currentness_marker_fails_closed() -> None:
    stripped = "# Environment Manifest\n\nNo currentness marker here at all.\n"
    problems = evaluate_reconcile_before_use_integrity(
        [ENVIRONMENT_MANIFEST_NAME],
        {ENVIRONMENT_MANIFEST_NAME: stripped},
    )
    assert len(problems) == 1
    assert ENVIRONMENT_MANIFEST_NAME in problems[0]
    assert "currentness marker" in problems[0]


def test_partial_marker_loss_fails_closed() -> None:
    # Keeps "Currentness:"/"RECONCILE_BEFORE_USE" but drops the
    # CURRENT_STATUS.md/live-GitHub reconciliation pointer.
    degraded = "> **Currentness:** historical / `RECONCILE_BEFORE_USE`.\n"
    problems = evaluate_reconcile_before_use_integrity(
        [ENVIRONMENT_MANIFEST_NAME],
        {ENVIRONMENT_MANIFEST_NAME: degraded},
    )
    assert len(problems) == 1
    assert "CURRENT_STATUS.md" in problems[0]


def test_manifest_role_disagreement_fails_closed() -> None:
    # The freshness gate treats the file as reconcile-before-use, but the
    # manifest's role list no longer agrees.
    problems = evaluate_reconcile_before_use_integrity(
        [],
        {ENVIRONMENT_MANIFEST_NAME: _VALID_RECONCILE_MARKERS},
    )
    assert len(problems) == 1
    assert "does not classify it that way" in problems[0]


# --- Test D: active/historical role contradiction fails ---------------------


def test_dual_role_contradiction_fails() -> None:
    problems = evaluate_role_conflicts(
        [ENVIRONMENT_MANIFEST_NAME, "README.md"],
        [ENVIRONMENT_MANIFEST_NAME],
    )
    assert len(problems) == 1
    assert ENVIRONMENT_MANIFEST_NAME in problems[0]


def test_no_conflict_when_active_and_historical_sets_are_disjoint() -> None:
    assert (
        evaluate_role_conflicts(
            ["README.md", "docs/MENTAURY_QUICK_REFERENCE.md"],
            [ENVIRONMENT_MANIFEST_NAME],
        )
        == []
    )


def test_explicit_dual_role_allowlist_permits_the_exception() -> None:
    assert (
        evaluate_role_conflicts(
            [ENVIRONMENT_MANIFEST_NAME],
            [ENVIRONMENT_MANIFEST_NAME],
            dual_role_allowlist=[ENVIRONMENT_MANIFEST_NAME],
        )
        == []
    )


# --- Test E: active surfaces retain legacy P-stage protection ---------------


def test_active_surface_still_fails_when_stale() -> None:
    authoritative = "| P0-015 Deterministic Evidence Gate | ✅ Implemented | gate ≠ fact |\n"
    stale_readme = "P0-001…P0-008_IMPLEMENTED_IN_MAIN\n"
    problems = check_doc_freshness.evaluate(authoritative, {"README.md": stale_readme})
    assert len(problems) == 1
    assert "README.md" in problems[0]


def test_active_surface_set_excludes_reconcile_before_use_paths() -> None:
    active_names = {
        str(path.relative_to(ROOT)) for path in check_doc_freshness.ACTIVE_DERIVED_DOC_PATHS
    }
    historical = set(_manifest_historical_paths())
    assert active_names.isdisjoint(historical)
