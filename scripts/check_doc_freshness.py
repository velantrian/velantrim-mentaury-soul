"""Doc-freshness gate for derived Mentaury status documents.

Added during the 2026-08-06 audit after ``docs/MENTAURY_QUICK_REFERENCE.md``
and ``docs/ENVIRONMENT_MANIFEST.md`` were found several P0 milestones behind
the authoritative ``docs/CURRENT_STATUS.md`` (one still referenced a merged
PR by number, the other still said "Permanent CI: NOT PRESENT" after P0-012
shipped). Both derived documents declare their own claimed status as an
explicit ``P0-XXX…P0-YYY IMPLEMENTED IN MAIN`` marker; this script fails
closed whenever that marker is missing or lags behind the highest milestone
``docs/CURRENT_STATUS.md`` marks "Implemented" in its status table.

This does not replace human judgement about *content* drift. It only proves
that nobody forgot to bump the one-line status marker on the next merged
P0 milestone.
"""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
CURRENT_STATUS_PATH = ROOT / "docs" / "CURRENT_STATUS.md"
DERIVED_DOC_PATHS = (
    ROOT / "docs" / "MENTAURY_QUICK_REFERENCE.md",
    ROOT / "docs" / "ENVIRONMENT_MANIFEST.md",
)

_AUTHORITATIVE_IMPLEMENTED_ROW = re.compile(
    r"P0-(\d{3})[^\n|]*\|\s*✅\s*Implemented",
    re.IGNORECASE,
)
_DERIVED_IMPLEMENTED_RANGE = re.compile(
    r"P0-\d{3}\s*…\s*P0-(\d{3})[ _]IMPLEMENTED[ _]IN[ _]MAIN",
    re.IGNORECASE,
)


def _max_milestone(text: str, pattern: re.Pattern[str]) -> int | None:
    numbers = [int(match.group(1)) for match in pattern.finditer(text)]
    return max(numbers) if numbers else None


def main() -> int:
    current_status_text = CURRENT_STATUS_PATH.read_text(encoding="utf-8")
    authoritative_max = _max_milestone(
        current_status_text, _AUTHORITATIVE_IMPLEMENTED_ROW
    )
    if authoritative_max is None:
        print(
            "doc freshness gate: could not find any '✅ Implemented' P0 "
            f"milestone row in {CURRENT_STATUS_PATH.relative_to(ROOT)}"
        )
        return 1

    problems: list[str] = []
    for doc_path in DERIVED_DOC_PATHS:
        doc_text = doc_path.read_text(encoding="utf-8")
        doc_max = _max_milestone(doc_text, _DERIVED_IMPLEMENTED_RANGE)
        relative = doc_path.relative_to(ROOT)
        if doc_max is None:
            problems.append(
                f"{relative}: missing a 'P0-XXX…P0-YYY IMPLEMENTED IN MAIN' "
                "freshness marker"
            )
        elif doc_max < authoritative_max:
            problems.append(
                f"{relative} declares up to P0-{doc_max:03d} implemented, "
                f"but {CURRENT_STATUS_PATH.relative_to(ROOT)} (authoritative) "
                f"already has P0-{authoritative_max:03d} implemented"
            )

    if problems:
        print("doc freshness gate: derived documents lag the authoritative status:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(
        "doc freshness gate: derived documents match "
        f"P0-{authoritative_max:03d} PASS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
