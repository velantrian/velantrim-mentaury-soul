"""Doc-freshness gates for derived Mentaury status surfaces.

Human-readable derived documents are checked in role-aware ways: active
current surfaces (README, Quick Reference) preserve the historical P-stage
compatibility guard via compact milestone markers, and the root human landing
pages must also mirror a bounded set of explicit current semantic facts from
``docs/CURRENT_STATUS.md``. ``docs/ENVIRONMENT_MANIFEST.md`` is a
``historical_or_reconcile_before_use`` surface (per
``docs/ai/project_manifest.json``), not an active current implementation
inventory, so it is checked only for its declared role and direct-file
currentness marker, never for full P-stage/semantic currency. The machine
snapshot is checked separately because it is structured data: it must declare
itself derived and must agree with the authoritative current-checkpoint
markers for the bounded implementation and authority fields it mirrors.

None of these checks makes a derived surface authoritative. Live merged GitHub
state plus ``docs/CURRENT_STATUS.md`` remain the conflict resolver.
"""

from __future__ import annotations

import json
import pathlib
import re
from collections.abc import Iterable, Mapping
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CURRENT_STATUS_PATH = ROOT / "docs" / "CURRENT_STATUS.md"
MACHINE_STATE_PATH = ROOT / "docs" / "state" / "project_state.json"
PROJECT_MANIFEST_PATH = ROOT / "docs" / "ai" / "project_manifest.json"

# Active derived surfaces: expected to keep mirroring the highest implemented
# P-stage milestone. Environment Manifest is intentionally NOT here — see
# ENVIRONMENT_MANIFEST_RELATIVE_PATH below.
ACTIVE_DERIVED_DOC_PATHS = (
    ROOT / "README.md",
    ROOT / "docs" / "MENTAURY_QUICK_REFERENCE.md",
)
HUMAN_SEMANTIC_DOC_PATHS = (
    ROOT / "README.md",
    ROOT / "SYSTEM_OVERVIEW.md",
)

# docs/ai/project_manifest.json (#160) already classifies this file as
# historical_or_reconcile_before_use, and the file itself already carries a
# direct-file currentness marker (#176). Treating it through the same
# P-stage-range guard as an active surface would silently require it to
# mirror every later semantic/versioned V1 surface (CBP/EPR/ATR/HDE/E2E),
# which is exactly the #173 Track B blind spot. It is checked separately by
# evaluate_environment_manifest_role() below instead.
ENVIRONMENT_MANIFEST_PATH = ROOT / "docs" / "ENVIRONMENT_MANIFEST.md"
ENVIRONMENT_MANIFEST_RELATIVE_PATH = "docs/ENVIRONMENT_MANIFEST.md"

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

# Visible human-facing facts mirrored by README/System Overview. Historical
# Phase-4 pre-implementation markers remain useful here as negative sentinels:
# once absent from the current checkpoint they must also disappear from the
# visible landing pages.
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

_IMPLEMENTED_MARKERS = {
    "phase_2_npg_shadow_composition": "PHASE_2_NPG_SHADOW_COMPOSITION_IMPLEMENTED_BOUNDED",
    "phase_3_provenance_claim_record": "PHASE_3_PROVENANCE_CLAIM_REPRESENTATION_IMPLEMENTED_BOUNDED",
    "claim_to_belief_binding_cbp_v0_1": "CLAIM_TO_BELIEF_BINDING_IMPLEMENTED_BOUNDED",
    "phase_4_epistemic_change_router_epr_v0_1": "PHASE_4_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
    "phase_5_anchored_typed_relation_atr_v0_1": "PHASE_5_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
    "phase_6_hypothesis_discrimination_hde_v0_1": "PHASE_6_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
}
_FROZEN_NOT_IMPLEMENTED_MARKERS = {
    "phase_4_epistemic_change_router_epr_v0_1": (
        "PHASE_4_CONTRACT_VERSION_EPR_V0_1",
        "PHASE_4_IMPLEMENTATION_NOT_STARTED",
    ),
    "terminal_reconsideration_lineage": (
        "TERMINAL_RECONSIDERATION_LINEAGE_NOT_IMPLEMENTED",
    ),
}
_AUTHORITY_NOT_AUTHORIZED_MARKERS = {
    "action_gate_authorized": "ACTION_GATE_NOT_AUTHORIZED",
    "retrieval_execution_authorized": "RETRIEVAL_EXECUTION_NOT_AUTHORIZED",
    "tool_execution_authorized": "TOOL_EXECUTION_NOT_AUTHORIZED",
    "identity_runtime_authorized": "IDENTITY_RUNTIME_NOT_AUTHORIZED",
    "relationship_runtime_authorized": "RELATIONSHIP_RUNTIME_NOT_AUTHORIZED",
    "runtime_deployment_authorized": "RUNTIME_DEPLOYMENT_NOT_AUTHORIZED",
    "phase_4_runtime_authorized": "PHASE_4_RUNTIME_NOT_AUTHORIZED",
    "phase_5_runtime_authorized": "PHASE_5_RUNTIME_NOT_AUTHORIZED",
    "phase_6_runtime_authorized": "PHASE_6_RUNTIME_NOT_AUTHORIZED",
}
_V1_RESEARCH_CORE_EXPECTATIONS = {
    "final_version": ("V1_RESEARCH_CORE_VERSION_1_0_0", "1.0.0"),
    "release_status": (
        "V1_STAGE_5_FINAL_ACCEPTANCE_COMPLETE",
        "FINAL_ACCEPTANCE_COMPLETE",
    ),
    "offline_e2e_verified": ("V1_OFFLINE_EPISTEMIC_E2E_VERIFIED", True),
    "license_distribution_posture": (
        "V1_DISTRIBUTION_PROPRIETARY_ALL_RIGHTS_RESERVED",
        "PROPRIETARY_ALL_RIGHTS_RESERVED",
    ),
}
_V1_DISTRIBUTION_MARKER = "V1_DISTRIBUTION_PROPRIETARY_ALL_RIGHTS_RESERVED"

_RECONCILE_BEFORE_USE_MANIFEST_KEY = "historical_or_reconcile_before_use"

# Bounded direct-file evidence that Environment Manifest still declares its
# RECONCILE_BEFORE_USE role (added in #176). Intentionally a short substring
# check near the top of the file, not a regex over the preserved historical
# body.
_ENVIRONMENT_MANIFEST_CURRENTNESS_MARKERS = (
    "Currentness:",
    "RECONCILE_BEFORE_USE",
    "CURRENT_STATUS.md",
    "live GitHub",
    "not a complete current implementation ledger",
)
_ENVIRONMENT_MANIFEST_MARKER_WINDOW_CHARS = 2500


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


def evaluate_environment_manifest_role(
    project_manifest: Mapping[str, Any],
    environment_manifest_text: str,
    *,
    active_derived_relative_paths: Iterable[str],
) -> list[str]:
    """Fail closed on Environment Manifest role drift or a missing marker.

    Environment Manifest is deliberately excluded from ``evaluate()``'s active
    P-stage range check (see ``ACTIVE_DERIVED_DOC_PATHS``): its preserved
    historical P-stage/source inventory is not required to mirror later
    semantic/versioned V1 surfaces (CBP/EPR/ATR/HDE/E2E) that are not
    expressible as a newer P-number. That exclusion is only safe as long as
    ``docs/ai/project_manifest.json`` (the routing/role contract, not an
    engineering-truth authority) still classifies it
    ``historical_or_reconcile_before_use`` and the file itself still carries
    its direct-file currentness marker. Losing either silently would let it
    drift back into being treated as a complete active current implementation
    ledger without this gate noticing.
    """

    problems: list[str] = []

    reconcile_list = project_manifest.get(_RECONCILE_BEFORE_USE_MANIFEST_KEY)
    if not isinstance(reconcile_list, list):
        return [
            "docs/ai/project_manifest.json: "
            f"{_RECONCILE_BEFORE_USE_MANIFEST_KEY!r} must be a list"
        ]

    is_classified_reconcile = ENVIRONMENT_MANIFEST_RELATIVE_PATH in reconcile_list
    is_active_surface = ENVIRONMENT_MANIFEST_RELATIVE_PATH in set(
        active_derived_relative_paths
    )

    if is_active_surface and is_classified_reconcile:
        problems.append(
            f"{ENVIRONMENT_MANIFEST_RELATIVE_PATH}: classified both as an "
            "active P-stage freshness surface and as "
            f"{_RECONCILE_BEFORE_USE_MANIFEST_KEY!r} in "
            "docs/ai/project_manifest.json; these roles are mutually "
            "exclusive without an explicit dual-role rule"
        )

    if not is_classified_reconcile:
        problems.append(
            "docs/ai/project_manifest.json: "
            f"{ENVIRONMENT_MANIFEST_RELATIVE_PATH!r} is no longer listed "
            f"under {_RECONCILE_BEFORE_USE_MANIFEST_KEY!r}; if it was "
            "promoted back to an active current surface, add it to the "
            "active P-stage freshness set explicitly instead of leaving "
            "this reconcile-before-use guard silently unchecked"
        )

    marker_window = environment_manifest_text[
        :_ENVIRONMENT_MANIFEST_MARKER_WINDOW_CHARS
    ]
    missing_markers = [
        marker
        for marker in _ENVIRONMENT_MANIFEST_CURRENTNESS_MARKERS
        if marker not in marker_window
    ]
    if missing_markers:
        problems.append(
            f"{ENVIRONMENT_MANIFEST_RELATIVE_PATH}: missing required "
            "reconcile-before-use currentness marker text near the top of "
            f"the file: {missing_markers!r}"
        )

    return problems


def _expect_mapping(snapshot: Mapping[str, Any], key: str) -> Mapping[str, Any] | None:
    value = snapshot.get(key)
    return value if isinstance(value, Mapping) else None


def _marker_or_snapshot_key_is_material(
    snapshot: Mapping[str, Any], key: str, markers: tuple[str, ...], checkpoint: str
) -> bool:
    return key in snapshot or any(marker in checkpoint for marker in markers)


def evaluate_machine_snapshot(
    current_status_text: str, machine_state_text: str
) -> list[str]:
    """Fail closed when the derived JSON snapshot disagrees with current state.

    Repository execution always supplies the real ``CURRENT_STATUS`` and thus
    isolates its current-checkpoint section. Tiny synthetic unit fixtures from
    the original freshness suite intentionally contain marker text only; those
    remain supported as direct semantic fixtures without weakening the real
    repository path.
    """

    checkpoint = current_checkpoint(current_status_text) or current_status_text

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
            if not _marker_or_snapshot_key_is_material(implemented, key, (marker,), checkpoint):
                continue
            snapshot_value = implemented.get(key)
            authoritative_value = marker in checkpoint
            if not isinstance(snapshot_value, bool):
                problems.append(f"implemented_bounded.{key}: expected boolean")
            elif snapshot_value != authoritative_value:
                problems.append(
                    f"implemented_bounded.{key}={snapshot_value} disagrees with "
                    f"CURRENT_STATUS current marker {marker!r} "
                    f"(present={authoritative_value})"
                )

    frozen = _expect_mapping(parsed, "frozen_not_implemented")
    if frozen is None:
        problems.append(
            "docs/state/project_state.json: frozen_not_implemented must be an object"
        )
    else:
        for key, markers in _FROZEN_NOT_IMPLEMENTED_MARKERS.items():
            if not _marker_or_snapshot_key_is_material(frozen, key, markers, checkpoint):
                continue
            snapshot_value = frozen.get(key)
            authoritative_value = all(marker in checkpoint for marker in markers)
            if not isinstance(snapshot_value, bool):
                problems.append(f"frozen_not_implemented.{key}: expected boolean")
            elif snapshot_value != authoritative_value:
                problems.append(
                    f"frozen_not_implemented.{key}={snapshot_value} disagrees with "
                    f"CURRENT_STATUS current markers {markers!r} "
                    f"(all_present={authoritative_value})"
                )

    v1_markers_present = any(
        marker in checkpoint for marker, _expected in _V1_RESEARCH_CORE_EXPECTATIONS.values()
    ) or _V1_DISTRIBUTION_MARKER in checkpoint
    v1 = _expect_mapping(parsed, "v1_research_core")
    if v1_markers_present or "v1_research_core" in parsed:
        if v1 is None:
            problems.append("docs/state/project_state.json: v1_research_core must be an object")
        else:
            for key, (marker, expected_value) in _V1_RESEARCH_CORE_EXPECTATIONS.items():
                marker_present = marker in checkpoint
                snapshot_value = v1.get(key)
                if marker_present and snapshot_value != expected_value:
                    problems.append(
                        f"v1_research_core.{key}={snapshot_value!r} disagrees with "
                        f"CURRENT_STATUS current marker {marker!r}; expected "
                        f"{expected_value!r}"
                    )
                elif not marker_present and snapshot_value == expected_value:
                    problems.append(
                        f"v1_research_core.{key} claims {expected_value!r} ahead of "
                        f"CURRENT_STATUS current marker {marker!r}"
                    )

            if _V1_DISTRIBUTION_MARKER in checkpoint:
                owner_decision_required = v1.get(
                    "license_distribution_owner_decision_required"
                )
                if owner_decision_required is not False:
                    problems.append(
                        "v1_research_core.license_distribution_owner_decision_required="
                        f"{owner_decision_required!r} disagrees with CURRENT_STATUS final "
                        f"distribution marker {_V1_DISTRIBUTION_MARKER!r}; expected False"
                    )

    authority = _expect_mapping(parsed, "authority")
    if authority is None:
        problems.append("docs/state/project_state.json: authority must be an object")
    else:
        for key, not_authorized_marker in _AUTHORITY_NOT_AUTHORIZED_MARKERS.items():
            if not _marker_or_snapshot_key_is_material(
                authority, key, (not_authorized_marker,), checkpoint
            ):
                continue
            snapshot_value = authority.get(key)
            authoritative_authorized = not_authorized_marker not in checkpoint
            if not isinstance(snapshot_value, bool):
                problems.append(f"authority.{key}: expected boolean")
            elif snapshot_value != authoritative_authorized:
                problems.append(
                    f"authority.{key}={snapshot_value} disagrees with CURRENT_STATUS "
                    f"current marker {not_authorized_marker!r} "
                    f"(authorized={authoritative_authorized})"
                )

    return problems


def main() -> int:
    current_status_text = CURRENT_STATUS_PATH.read_text(encoding="utf-8")
    active_derived_relative_paths = [
        str(doc_path.relative_to(ROOT)) for doc_path in ACTIVE_DERIVED_DOC_PATHS
    ]
    derived_doc_texts = {
        relative_path: doc_path.read_text(encoding="utf-8")
        for relative_path, doc_path in zip(
            active_derived_relative_paths, ACTIVE_DERIVED_DOC_PATHS
        )
    }
    semantic_doc_texts = {
        str(doc_path.relative_to(ROOT)): doc_path.read_text(encoding="utf-8")
        for doc_path in HUMAN_SEMANTIC_DOC_PATHS
    }
    project_manifest = json.loads(
        PROJECT_MANIFEST_PATH.read_text(encoding="utf-8")
    )

    problems = evaluate(current_status_text, derived_doc_texts)
    problems.extend(evaluate_human_semantic_status(current_status_text, semantic_doc_texts))
    problems.extend(
        evaluate_environment_manifest_role(
            project_manifest,
            ENVIRONMENT_MANIFEST_PATH.read_text(encoding="utf-8"),
            active_derived_relative_paths=active_derived_relative_paths,
        )
    )
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
