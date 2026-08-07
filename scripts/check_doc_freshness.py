"""Doc-freshness gate for derived Mentaury status documents.

Added during the 2026-08-06 audit after ``docs/MENTAURY_QUICK_REFERENCE.md``
and ``docs/ENVIRONMENT_MANIFEST.md`` were found several P0 milestones behind
the authoritative ``docs/CURRENT_STATUS.md`` (one still referenced a merged
PR by number, the other still said "Permanent CI: NOT PRESENT" after P0-012
shipped). Both derived documents declare their own claimed status as an
explicit ``P<stage>-XXX…P<stage>-YYY IMPLEMENTED IN MAIN`` marker; this
script fails closed whenever that marker is missing, lags behind, or
overshoots the highest milestone ``docs/CURRENT_STATUS.md`` marks
"Implemented" in its status table.

The milestone pattern is stage-generic (``P0-``, ``P1-``, ...): a milestone
is compared as the tuple ``(stage, number)``, so once the project moves past
the P0 line (e.g. into a POST-P0 roadmap numbered ``P1-001``, ``P1-002``,
...) this gate keeps working unmodified instead of silently staying green
against a frozen ``P0-015`` marker forever.

This does not replace human judgement about *content* drift. It only proves
that nobody forgot to bump the one-line status marker on the next merged
milestone.
"""

from __future__ import annotations

import pathlib
import re
from collections.abc import Mapping

ROOT = pathlib.Path(__file__).resolve().parents[1]
CURRENT_STATUS_PATH = ROOT / "docs" / "CURRENT_STATUS.md"
DERIVED_DOC_PATHS = (
    ROOT / "docs" / "MENTAURY_QUICK_REFERENCE.md",
    ROOT / "docs" / "ENVIRONMENT_MANIFEST.md",
)

Milestone = tuple[int, int]

# Authoritative rows look like:
#   | P0-015 Deterministic Evidence Gate | ✅ Implemented | ... |
_AUTHORITATIVE_IMPLEMENTED_ROW = re.compile(
    r"P(\d+)-(\d{3})[^\n|]*\|\s*✅\s*Implemented",
    re.IGNORECASE,
)

# Derived-document markers look like:
#   P0-001…P0-015_IMPLEMENTED_IN_MAIN
#   P0-001…P0-015 IMPLEMENTED IN MAIN
_DERIVED_IMPLEMENTED_RANGE = re.compile(
    r"P(\d+)-\d{3}\s*…\s*P(\d+)-(\d{3})[ _]IMPLEMENTED[ _]IN[ _]MAIN",
    re.IGNORECASE,
)


def format_milestone(milestone: Milestone) -> str:
    stage, number = milestone
    return f"P{stage}-{number:03d}"


def authoritative_milestones(text: str) -> list[Milestone]:
    """Every ``P<stage>-<number>`` marked "✅ Implemented" in an authoritative table."""

    return [
        (int(stage), int(number))
        for stage, number in _AUTHORITATIVE_IMPLEMENTED_ROW.findall(text)
    ]


def derived_milestones(text: str) -> list[Milestone]:
    """Every well-formed ``P<s>-XXX…P<s>-YYY IMPLEMENTED IN MAIN`` marker.

    A range whose start and end stage disagree (e.g. a corrupted
    ``P0-001…P1-002`` marker) is not a meaningful claim about either stage,
    so it is skipped rather than silently accepted as either one.
    """

    milestones: list[Milestone] = []
    for start_stage, end_stage, end_number in _DERIVED_IMPLEMENTED_RANGE.findall(
        text
    ):
        if start_stage != end_stage:
            continue
        milestones.append((int(end_stage), int(end_number)))
    return milestones


def evaluate(
    current_status_text: str, derived_doc_texts: Mapping[str, str]
) -> list[str]:
    """Return a list of human-readable problems, or an empty list if fresh.

    Pure function over document text, independent of the filesystem, so it
    can be unit-tested directly against synthetic document snippets instead
    of real files on disk.
    """

    authoritative = authoritative_milestones(current_status_text)
    if not authoritative:
        return [
            "could not find any '✅ Implemented' P<stage>-XXX milestone row "
            "in the authoritative status document"
        ]
    authoritative_max = max(authoritative)

    problems: list[str] = []
    for name, doc_text in derived_doc_texts.items():
        derived = derived_milestones(doc_text)
        if not derived:
            problems.append(
                f"{name}: missing a well-formed "
                "'P<stage>-XXX…P<stage>-YYY IMPLEMENTED IN MAIN' freshness marker"
            )
            continue
        derived_max = max(derived)
        if derived_max < authoritative_max:
            problems.append(
                f"{name} declares up to {format_milestone(derived_max)} "
                "implemented, but the authoritative status document already "
                f"has {format_milestone(authoritative_max)} implemented"
            )
        elif derived_max > authoritative_max:
            problems.append(
                f"{name} claims {format_milestone(derived_max)} implemented, "
                "which is ahead of the authoritative status document (only "
                f"has {format_milestone(authoritative_max)} implemented) — "
                "this looks like a typo or a premature status update"
            )
    return problems


def main() -> int:
    current_status_text = CURRENT_STATUS_PATH.read_text(encoding="utf-8")
    derived_doc_texts = {
        str(doc_path.relative_to(ROOT)): doc_path.read_text(encoding="utf-8")
        for doc_path in DERIVED_DOC_PATHS
    }

    problems = evaluate(current_status_text, derived_doc_texts)
    if problems:
        print("doc freshness gate: derived documents are out of sync:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    authoritative_max = max(authoritative_milestones(current_status_text))
    print(
        "doc freshness gate: derived documents match "
        f"{format_milestone(authoritative_max)} PASS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
