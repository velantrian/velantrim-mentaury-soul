"""Synthetic tests for scripts/validate.py structural manifest.

Presence-check доказывает только наличие обязательных путей, не корректность
поведения. Тесты временно моделируют отсутствие пути и ожидают controlled
failure без динамического rglob вместо явного manifest.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from validate import (
    REQUIRED_PATHS,
    forbidden_runtime_modules,
    missing_required_paths,
)


def test_required_paths_cover_p0_015_surfaces() -> None:
    required = set(REQUIRED_PATHS)
    assert "src/mentaury/storage/redaction.py" in required
    assert "src/mentaury/replay/__init__.py" in required
    assert "src/mentaury/replay/engine.py" in required
    assert "src/mentaury/beliefs/lifecycle.py" in required
    assert "src/mentaury/beliefs/evidence_gate.py" in required
    assert "src/mentaury/evidence/gate.py" in required
    assert "tests/test_redaction.py" in required
    assert "tests/test_r1_replay.py" in required
    assert "tests/test_belief_lifecycle.py" in required
    assert "tests/test_evidence_gate.py" in required


def test_required_paths_cover_current_bounded_post_p0_surfaces() -> None:
    required = set(REQUIRED_PATHS)
    expected = {
        "src/mentaury/capabilities/lease/resolver.py",
        "src/mentaury/privacy/reconciliation/classifier.py",
        "src/mentaury/composition/governed_constraints/composer.py",
        "src/mentaury/non_projection/classifier.py",
        "src/mentaury/composition/non_projection_shadow/coordinator.py",
        "src/mentaury/claims/representation.py",
        "src/mentaury/relations/representation.py",
        "src/mentaury/discrimination/evaluator.py",
        "tests/test_capability_lease_resolution.py",
        "tests/test_privacy_reconciliation_classifier.py",
        "tests/test_governed_constraint_composer.py",
        "tests/test_non_projection_classifier.py",
        "tests/test_non_projection_shadow_composition.py",
        "tests/test_provenance_claim_representation.py",
        "tests/test_typed_relations.py",
        "tests/test_hypothesis_discrimination_evaluator.py",
    }
    assert expected <= required


def test_missing_required_paths_reports_absent_manifest_entry(
    tmp_path: Path,
) -> None:
    # Явный manifest entry, которого нет на диске → controlled failure.
    missing = missing_required_paths(
        root=tmp_path,
        required_paths=("src/mentaury/storage/redaction.py",),
    )
    assert missing == ["src/mentaury/storage/redaction.py"]


def test_missing_required_paths_empty_when_file_present(tmp_path: Path) -> None:
    target = tmp_path / "src" / "mentaury" / "storage" / "redaction.py"
    target.parent.mkdir(parents=True)
    target.write_text("# stub\n", encoding="utf-8")
    missing = missing_required_paths(
        root=tmp_path,
        required_paths=("src/mentaury/storage/redaction.py",),
    )
    assert missing == []


def test_forbidden_runtime_modules_detects_banned_names(tmp_path: Path) -> None:
    banned = tmp_path / "src" / "mentaury" / "identity_engine.py"
    banned.parent.mkdir(parents=True)
    banned.write_text("# forbidden stub\n", encoding="utf-8")
    assert "identity_engine.py" in forbidden_runtime_modules(tmp_path)


def test_repo_required_paths_currently_exist() -> None:
    assert missing_required_paths() == []
