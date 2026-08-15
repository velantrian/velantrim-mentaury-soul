"""Doc-freshness gates for derived Mentaury status surfaces.

Human-readable derived documents are checked in two deliberately small ways:
compact milestone markers preserve the historical P-stage compatibility guard,
while the root human landing pages must also mirror a bounded set of explicit
current semantic facts from ``docs/CURRENT_STATUS.md``. The machine snapshot is
checked separately because it is structured data: it must declare itself derived
and must agree with the authoritative current-status markers for the bounded
implementation and authority fields it mirrors.

None of these checks makes a derived surface authoritative. Live merged GitHub
state plus ``docs/CURRENT_STATUS.md`` remain the conflict resolver.
"""

from __future__ import annotations

import json
import pathlib
import re
from collections.abc import Mapping
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CURRENT_STATUS_PATH = ROOT / "docs" / "CURRENT_STATUS.md"
MACHINE_STATE_PATH = ROOT / "docs" / "state" / "project_state.json"
DERIVED_DOC_PATHS = (
    ROOT / "README.md",
    ROOT / "docs" / "MENTAURY_QUICK_REFERENCE.md",
    ROOT / "docs" / "ENVIRONMENT_MANIFEST.md",
)
HUMAN_SEMANTIC_DOC_PATHS = (
    ROOT / "README.md",
    ROOT / "SYSTEM_OVERVIEW.md",
)

Milestone = tuple[int, int]

_AUTHORITATIVE_IMPLEMENTED_ROW = re.compile(
    r"P(\d+)-(\d{3})[^\n|]*\|\s*✅\s*Implemented",
    re.IGNORECASE,
)
_DERIVED_IMPLEMENTED_RANGE = re.compile(
    r"P(\d+)-\d{3}\s*…\s*P(\d+)-(\d{3})[ _]IMPLEMENTED[ _]IN[ _]MAIN",
    re.IGNORECASE,
)

_MACHINE_ROLE = "DERIVED_MACHINE_SNAPSHOT"
_MACHINE_CONFLICT_RULE = "LIVE_GITHUB_AND_CURRENT_STATUS_OVERRIDE_THIS_SNAPSHOT"

# Visible human-facing facts mirrored by README/System Overview. These exact
# phrases are intentionally simple: a stale pre-HDE landing page must not pass
# merely because it still carries an old P-stage compatibility marker.
_HUMAN_SEMANTIC_FACTS = (
    ("PHASE_4_IMPLEMENTATION_NOT_STARTED", "PHASE_4_IMPLEMENTATION = NOT_STARTED"),
    ("PHASE_4_OWNER_GO_NOT_GRANTED", "PHASE_4_OWNER_GO = NOT_GRANTED"),
    ("PHASE_4_RUNTIME_NOT_AUTHORIZED", "PHASE_4_RUNTIME = NOT_AUTHORIZED"),
    (
        "PHASE_5_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
        "PHASE_5_IMPLEMENTATION = IMPLEMENTED_BOUNDED",
    ),
    ("PHASE_5_OWNER_GO_CONSUMED_BY_PR_119", "PHASE_5_OWNER_GO = CONSUMED_BY_PR_119"),
    ("PHASE_5_RUNTIME_NOT_AUTHORIZED", "PHASE_5_RUNTIME = NOT_AUTHORIZED"),
    (
        "PHASE_6_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
        "PHASE_6_IMPLEMENTATION = IMPLEMENTED_BOUNDED",
    ),
    ("PHASE_6_OWNER_GO_CONSUMED_BY_PR_127", "PHASE_6_OWNER_GO = CONSUMED_BY_PR_127"),
    ("PHASE_6_RUNTIME_NOT_AUTHORIZED", "PHASE_6_RUNTIME = NOT_AUTHORIZED"),
)

# Snapshot booleans that mirror explicit current-status markers.
_IMPLEMENTED_MARKERS = {
    "phase_2_npg_shadow_composition": "PHASE_2_NPG_SHADOW_COMPOSITION_IMPLEMENTED_BOUNDED",
    "phase_3_provenance_claim_record": "PHASE_3_PROVENANCE_CLAIM_REPRESENTATION_IMPLEMENTED_BOUNDED",
    "phase_5_anchored_typed_relation_atr_v0_1": "PHASE_5_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
    "phase_6_hypothesis_discrimination_hde_v0_1": "PHASE_6_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
}
_FROZEN_NOT_IMPLEMENTED_MARKERS = {
    "phase_4_epistemic_change_router_epr_v0_1": (
        "PHASE_4_CONTRACT_VERSION_EPR_V0_1",
        "PHASE_4_IMPLEMENTATION_NOT_STARTED",
    ),
}
_AUTHORITY_NOT_AUTHORIZED_MARKERS = {
    "action_gate_authorized": "ACTION_GATE_NOT_AUTHORIZED",
    "retrieval_execution_authorized": "RETRIEVAL_EXECUTION_NOT_AUTHORIZED",
    "tool_execution_authorized": "TOOL_EXECUTION_NOT_AUTHORIZED",
    "identity_runtime_authorized": "IDENTITY_RUNTIME_NOT_AUTHORIZED",
    "relationship_runtime_authorized": "RELATIONSHIP_RUNTIME_NOT_AUTHORIZED",
    "runtime_deployment_authorized": "RUNTIME_DEPLOYMENT_NOT_AUTHORIZED",
    "phase_5_runtime_authorized": "PHASE_5_RUNTIME_NOT_AUTHORIZED",
    "phase_6_runtime_authorized": "PHASE_6_RUNTIME_NOT_AUTHORIZED",
}


def format_milestone(milestone: Milestone) -> str:
    stage, number = milestone
    return f"P{stage}-{number:03d}"


def authoritative_milestones(text: str) -> list[Milestone]:
    """Every ``P<stage>-<number>`` marked ``✅ Implemented``."""

    return [
        (int(stage), int(number))
        for stage, number in _AUTHORITATIVE_IMPLEMENTED_ROW.findall(text)
    ]


def derived_milestones(text: str) -> list[Milestone]:
    """Every coherent derived ``IMPLEMENTED IN MAIN`` range marker."""

    milestones: list[Milestone] = []
    for start_stage, end_stage, end_number in _DERIVED_IMPLEMENTED_RANGE.findall(text):
        if start_stage != end_stage:
            continue
        milestones.append((int(end_stage), int(end_number)))
    return milestones


def current_checkpoint(text: str) -> str | None:
    """Return only the authoritative current-checkpoint section, not history."""

    anchor = "## 1. 🧭 Current checkpoint"
    if anchor not in text:
        return None
    remainder = text.split(anchor, 1)[1]
    if "---" not in remainder:
        return None
    return remainder.split("---", 1)[0]


def evaluate(
    current_status_text: str, derived_doc_texts: Mapping[str, str]
) -> list[str]:
    """Check human-readable derived milestone markers."""

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


def evaluate_human_semantic_status(
    current_status_text: str, derived_doc_texts: Mapping[str, str]
) -> list[str]:
    """Check visible current Phase 4–6 facts on the root human landing pages."""

    checkpoint = current_checkpoint(current_status_text)
    if checkpoint is None:
        return [
            "docs/CURRENT_STATUS.md: could not isolate the authoritative "
            "'## 1. 🧭 Current checkpoint' section"
        ]

    problems: list[str] = []
    for name, doc_text in derived_doc_texts.items():
        for status_marker, derived_marker in _HUMAN_SEMANTIC_FACTS:
            authoritative_present = status_marker in checkpoint
            derived_present = derived_marker in doc_text
            if derived_present != authoritative_present:
                problems.append(
                    f"{name}: visible semantic marker {derived_marker!r} "
                    f"disagrees with CURRENT_STATUS current-checkpoint marker "
                    f"{status_marker!r} (present={authoritative_present})"
                )
    return problems


def _expect_mapping(snapshot: Mapping[str, Any], key: str) -> Mapping[str, Any] | None:
    value = snapshot.get(key)
    return value if isinstance(value, Mapping) else None


def evaluate_machine_snapshot(
    current_status_text: str, machine_state_text: str
) -> list[str]:
    """Fail closed when the derived JSON snapshot disagrees with current status."""

    try:
        parsed = json.loads(machine_state_text)
    except json.JSONDecodeError as exc:
        return [f"docs/state/project_state.json: invalid JSON: {exc.msg}"]

    if not isinstance(parsed, dict):
        return ["docs/state/project_state.json: top-level JSON value must be an object"]

    problems: list[str] = []
    if parsed.get("document_role") != _MACHINE_ROLE:
        problems.append(
            "docs/state/project_state.json: document_role must be "
            f"{_MACHINE_ROLE!r}"
        )
    if parsed.get("independent_truth_authority") is not False:
        problems.append(
            "docs/state/project_state.json: independent_truth_authority must be false"
        )
    if parsed.get("conflict_rule") != _MACHINE_CONFLICT_RULE:
        problems.append(
            "docs/state/project_state.json: conflict_rule must preserve live GitHub + "
            "CURRENT_STATUS precedence"
        )

    implemented = _expect_mapping(parsed, "implemented_bounded")
    if implemented is None:
        problems.append("docs/state/project_state.json: implemented_bounded must be an object")
    else:
        for key, marker in _IMPLEMENTED_MARKERS.items():
            snapshot_value = implemented.get(key)
            authoritative_value = marker in current_status_text
            if not isinstance(snapshot_value, bool):
                problems.append(f"implemented_bounded.{key}: expected boolean")
            elif snapshot_value != authoritative_value:
                problems.append(
                    f"implemented_bounded.{key}={snapshot_value} disagrees with "
                    f"CURRENT_STATUS marker {marker!r} (present={authoritative_value})"
                )

    frozen = _expect_mapping(parsed, "frozen_not_implemented")
    if frozen is None:
        problems.append(
            "docs/state/project_state.json: frozen_not_implemented must be an object"
        )
    else:
        for key, markers in _FROZEN_NOT_IMPLEMENTED_MARKERS.items():
            snapshot_value = frozen.get(key)
            authoritative_value = all(marker in current_status_text for marker in markers)
            if not isinstance(snapshot_value, bool):
                problems.append(f"frozen_not_implemented.{key}: expected boolean")
            elif snapshot_value != authoritative_value:
                problems.append(
                    f"frozen_not_implemented.{key}={snapshot_value} disagrees with "
                    f"CURRENT_STATUS markers {markers!r} (all_present={authoritative_value})"
                )

    authority = _expect_mapping(parsed, "authority")
    if authority is None:
        problems.append("docs/state/project_state.json: authority must be an object")
    else:
        for key, not_authorized_marker in _AUTHORITY_NOT_AUTHORIZED_MARKERS.items():
            snapshot_value = authority.get(key)
            authoritative_authorized = not_authorized_marker not in current_status_text
            if not isinstance(snapshot_value, bool):
                problems.append(f"authority.{key}: expected boolean")
            elif snapshot_value != authoritative_authorized:
                problems.append(
                    f"authority.{key}={snapshot_value} disagrees with CURRENT_STATUS "
                    f"marker {not_authorized_marker!r} "
                    f"(authorized={authoritative_authorized})"
                )

    return problems


def main() -> int:
    current_status_text = CURRENT_STATUS_PATH.read_text(encoding="utf-8")
    derived_doc_texts = {
        str(doc_path.relative_to(ROOT)): doc_path.read_text(encoding="utf-8")
        for doc_path in DERIVED_DOC_PATHS
    }
    semantic_doc_texts = {
        str(doc_path.relative_to(ROOT)): doc_path.read_text(encoding="utf-8")
        for doc_path in HUMAN_SEMANTIC_DOC_PATHS
    }

    problems = evaluate(current_status_text, derived_doc_texts)
    problems.extend(evaluate_human_semantic_status(current_status_text, semantic_doc_texts))
    problems.extend(
        evaluate_machine_snapshot(
            current_status_text,
            MACHINE_STATE_PATH.read_text(encoding="utf-8"),
        )
    )
    if problems:
        print("doc freshness gate: derived surfaces are out of sync:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    authoritative_max = max(authoritative_milestones(current_status_text))
    print(
        "doc freshness gate: milestone markers, human semantic state and machine "
        f"snapshot match {format_milestone(authoritative_max)} / CURRENT_STATUS PASS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
