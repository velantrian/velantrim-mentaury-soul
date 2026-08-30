"""Integrity tests for the AI/documentation routing manifest."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "ai" / "project_manifest.json"
AI_ENTRY_PATH = ROOT / "docs" / "ai" / "README.md"

SYMBOLIC_ROUTE_ENTRIES = {
    "OWNING_READINESS_OR_CONTRACT",
    "EXACT_PR_TEST_CI_EVIDENCE",
    "AFFECTED_COMPONENT_ONLY",
    "OWNING_CONTRACT",
    "SOURCE",
    "TESTS",
    "EXACT_CI_AND_REVIEW_EVIDENCE",
}


def _manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        parsed = json.load(handle)
    assert isinstance(parsed, dict)
    return parsed


def _required_ai_entries() -> set[str]:
    text = AI_ENTRY_PATH.read_text(encoding="utf-8")
    required_section = text.split("## 1. Required reading order", 1)[1].split("---", 1)[0]
    return {
        line.split("`", 2)[1]
        for line in required_section.splitlines()
        if line[:1].isdigit() and "`" in line
    }


def test_manifest_separates_authority_navigation_and_historical_inputs() -> None:
    manifest = _manifest()

    authority = set(manifest["authority_docs"])
    navigation = set(manifest["navigation_docs"])
    historical = set(manifest["historical_or_reconcile_before_use"])

    assert authority == {
        "docs/CURRENT_STATUS.md",
        "docs/GOVERNANCE.md",
        "docs/MENTAURY_CANON_V0.1.md",
    }
    assert navigation.isdisjoint(authority)
    assert historical.isdisjoint(authority | navigation)

    ledger = manifest["future_work_ledger"]
    assert ledger == "docs/ai/AUDIT_AND_FUTURE_WORK.md"
    assert manifest["future_work_ledger_usage"] == "RECONCILE_BEFORE_USE"
    assert ledger in historical

    expected_reconcile_before_use = {
        "docs/ai/AUDIT_AND_FUTURE_WORK.md",
        "docs/research/POST_P0_ROADMAP_V0.1.md",
        "docs/P0_010_ATOMIC_SAME_STREAM_REDACTION.md",
        "docs/V1_RELEASE_CANDIDATE_STATUS.md",
        "docs/ENVIRONMENT_MANIFEST.md",
    }
    assert expected_reconcile_before_use.issubset(historical)

    for historical_doc in historical:
        assert (ROOT / historical_doc).exists(), historical_doc
        for route_name, route in manifest["reading_routes"].items():
            assert historical_doc not in route, (
                f"{route_name} route must not treat {historical_doc} as active state"
            )


def test_ai_entry_mandatory_route_excludes_historical_inputs() -> None:
    manifest = _manifest()
    required_names = _required_ai_entries()
    historical_names = {
        Path(path).name for path in manifest["historical_or_reconcile_before_use"]
    }

    assert historical_names.isdisjoint(required_names)
    assert "RECONCILE_BEFORE_USE" in AI_ENTRY_PATH.read_text(encoding="utf-8")


def test_ai_entry_mandatory_route_paths_exist() -> None:
    missing = [
        entry
        for entry in _required_ai_entries()
        if not (AI_ENTRY_PATH.parent / entry).exists()
    ]
    assert missing == []


def test_active_reading_route_paths_exist() -> None:
    manifest = _manifest()
    missing: list[str] = []

    for route in manifest["reading_routes"].values():
        for entry in route:
            if entry in SYMBOLIC_ROUTE_ENTRIES:
                continue
            if not (ROOT / entry).exists():
                missing.append(entry)

    assert missing == []


def test_structural_path_hints_are_real_repository_paths() -> None:
    manifest = _manifest()
    hints = manifest["structural_path_hints"]
    missing = [hint for hint in hints if not (ROOT / hint).exists()]

    assert missing == []
    assert "src/mentaury/claim_belief_binding/" in hints
    assert "src/mentaury/epistemic_change/" in hints
    assert "src/mentaury/identity/" not in hints
