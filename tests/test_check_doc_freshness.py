"""Tests for scripts/check_doc_freshness.py.

``scripts`` is not part of the installed ``mentaury`` package (it holds
standalone CI/dev utilities), so this module is only importable because
``pyproject.toml`` adds ``scripts`` to ``[tool.pytest.ini_options].pythonpath``
for the test session.
"""

from __future__ import annotations

from check_doc_freshness import (
    authoritative_milestones,
    derived_milestones,
    evaluate,
    format_milestone,
)

_AUTHORITATIVE_P0_015 = (
    "| P0-014 Minimal Belief Lifecycle | ✅ Implemented | belief status ≠ truth |\n"
    "| P0-015 Deterministic Evidence Gate | ✅ Implemented | gate receipt ≠ fact |\n"
)


def _derived(marker: str) -> str:
    return f"Синхронно: GitHub main after merged PR #31\n\n{marker}\n"


def test_authoritative_milestones_reads_only_implemented_rows() -> None:
    text = (
        "| P0-013 R1 Replay | ✅ Implemented | replay ≠ truth |\n"
        "| P0-014 Belief Lifecycle | 🔴 NOT IMPLEMENTED | n/a |\n"
    )
    assert authoritative_milestones(text) == [(0, 13)]


def test_derived_milestones_accepts_underscore_and_space_variants() -> None:
    assert derived_milestones("P0-001…P0-015_IMPLEMENTED_IN_MAIN") == [(0, 15)]
    assert derived_milestones("P0-001…P0-015 IMPLEMENTED IN MAIN") == [(0, 15)]


def test_derived_milestones_rejects_cross_stage_range() -> None:
    # A range whose start and end stage disagree is not a coherent claim
    # about either stage, so it must not be silently treated as either one.
    assert derived_milestones("P0-001…P1-002_IMPLEMENTED_IN_MAIN") == []


def test_format_milestone_pads_the_number() -> None:
    assert format_milestone((0, 5)) == "P0-005"
    assert format_milestone((1, 2)) == "P1-002"


def test_evaluate_passes_when_derived_matches_authoritative_exactly() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"docs/A.md": _derived("P0-001…P0-015_IMPLEMENTED_IN_MAIN")},
    )
    assert problems == []


def test_evaluate_fails_when_derived_lags_behind_authoritative() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"docs/A.md": _derived("P0-001…P0-008_IMPLEMENTED_IN_MAIN")},
    )
    assert len(problems) == 1
    assert "docs/A.md" in problems[0]
    assert "P0-008" in problems[0] and "P0-015" in problems[0]
    assert "ahead of" not in problems[0]


def test_evaluate_fails_when_derived_overshoots_authoritative() -> None:
    # A derived document must not be allowed to claim an unimplemented
    # future milestone (e.g. "P0-001...P0-999") just because that number is
    # numerically >= the authoritative maximum.
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"docs/A.md": _derived("P0-001…P0-999_IMPLEMENTED_IN_MAIN")},
    )
    assert len(problems) == 1
    assert "ahead of" in problems[0]


def test_evaluate_fails_when_marker_is_missing() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"docs/A.md": "No freshness marker in this document at all."},
    )
    assert len(problems) == 1
    assert "missing a well-formed" in problems[0]


def test_evaluate_fails_when_marker_is_malformed_cross_stage() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"docs/A.md": _derived("P0-001…P1-002_IMPLEMENTED_IN_MAIN")},
    )
    assert len(problems) == 1
    assert "missing a well-formed" in problems[0]


def test_evaluate_fails_when_authoritative_table_is_missing() -> None:
    problems = evaluate(
        "Nothing implemented is recorded here.",
        {"docs/A.md": _derived("P0-001…P0-015_IMPLEMENTED_IN_MAIN")},
    )
    assert len(problems) == 1
    assert "authoritative" in problems[0].lower()


def test_evaluate_uses_the_highest_of_several_markers_in_one_document() -> None:
    # If a document (accidentally or intentionally) contains more than one
    # range marker, the highest one is treated as its current claim.
    text = _derived("P0-001…P0-008_IMPLEMENTED_IN_MAIN") + "\n" + _derived(
        "P0-001…P0-015_IMPLEMENTED_IN_MAIN"
    )
    assert derived_milestones(text) == [(0, 8), (0, 15)]
    problems = evaluate(_AUTHORITATIVE_P0_015, {"docs/A.md": text})
    assert problems == []


def test_evaluate_reports_each_derived_document_independently() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {
            "docs/FRESH.md": _derived("P0-001…P0-015_IMPLEMENTED_IN_MAIN"),
            "docs/STALE.md": _derived("P0-001…P0-008_IMPLEMENTED_IN_MAIN"),
        },
    )
    assert len(problems) == 1
    assert "docs/STALE.md" in problems[0]


def test_evaluate_is_stage_generic_beyond_p0() -> None:
    # Once the project moves to a POST-P0 roadmap numbered P1-XXX, the
    # authoritative table gains P1 rows; a derived document still parked on
    # a P0-only marker must be flagged, even though its milestone *number*
    # (15) is numerically larger than the new stage's (2).
    authoritative = _AUTHORITATIVE_P0_015 + (
        "| P1-002 Post-P0 Roadmap Step | ✅ Implemented | roadmap ≠ runtime |\n"
    )
    stale_on_old_stage = evaluate(
        authoritative,
        {"docs/A.md": _derived("P0-001…P0-015_IMPLEMENTED_IN_MAIN")},
    )
    assert len(stale_on_old_stage) == 1
    assert "P0-015" in stale_on_old_stage[0] and "P1-002" in stale_on_old_stage[0]

    caught_up = evaluate(
        authoritative,
        {"docs/A.md": _derived("P1-001…P1-002_IMPLEMENTED_IN_MAIN")},
    )
    assert caught_up == []


def test_readme_marker_behind_current_status_fails() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"README.md": _derived("P0-001…P0-008_IMPLEMENTED_IN_MAIN")},
    )
    assert len(problems) == 1
    assert "README.md" in problems[0]
    assert "P0-008" in problems[0] and "P0-015" in problems[0]


def test_readme_marker_ahead_of_current_status_fails() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"README.md": _derived("P0-001…P0-999_IMPLEMENTED_IN_MAIN")},
    )
    assert len(problems) == 1
    assert "README.md" in problems[0]
    assert "ahead of" in problems[0]


def test_readme_marker_equal_passes() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"README.md": _derived("P0-001…P0-015_IMPLEMENTED_IN_MAIN")},
    )
    assert problems == []


def test_readme_missing_marker_fails() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"README.md": "README without a freshness marker."},
    )
    assert len(problems) == 1
    assert "README.md" in problems[0]
    assert "missing a well-formed" in problems[0]
