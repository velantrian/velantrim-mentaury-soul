"""Tests for scripts/check_doc_freshness.py."""

from __future__ import annotations

import json

from check_doc_freshness import (
    authoritative_milestones,
    derived_milestones,
    evaluate,
    evaluate_machine_snapshot,
    format_milestone,
)

_AUTHORITATIVE_P0_015 = (
    "| P0-014 Minimal Belief Lifecycle | ✅ Implemented | belief status ≠ truth |\n"
    "| P0-015 Deterministic Evidence Gate | ✅ Implemented | gate receipt ≠ fact |\n"
)

_MACHINE_STATUS = """
PHASE_2_NPG_SHADOW_COMPOSITION_IMPLEMENTED_BOUNDED
PHASE_3_PROVENANCE_CLAIM_REPRESENTATION_IMPLEMENTED_BOUNDED
PHASE_4_CONTRACT_VERSION_EPR_V0_1
PHASE_4_IMPLEMENTATION_NOT_STARTED
PHASE_5_CONTRACT_VERSION_ATR_V0_1
PHASE_5_IMPLEMENTATION_IMPLEMENTED_BOUNDED
PHASE_5_RUNTIME_NOT_AUTHORIZED
PHASE_6_IMPLEMENTATION_IMPLEMENTED_BOUNDED
PHASE_6_RUNTIME_NOT_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
RETRIEVAL_EXECUTION_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
IDENTITY_RUNTIME_NOT_AUTHORIZED
RELATIONSHIP_RUNTIME_NOT_AUTHORIZED
RUNTIME_DEPLOYMENT_NOT_AUTHORIZED
"""


def _derived(marker: str) -> str:
    return f"Синхронно: GitHub main after merged PR #31\n\n{marker}\n"


def _machine_snapshot() -> dict[str, object]:
    return {
        "schema": "mentaury-project-state/1",
        "project": "Mentaury Soul",
        "document_role": "DERIVED_MACHINE_SNAPSHOT",
        "conflict_rule": "LIVE_GITHUB_AND_CURRENT_STATUS_OVERRIDE_THIS_SNAPSHOT",
        "independent_truth_authority": False,
        "implemented_bounded": {
            "phase_2_npg_shadow_composition": True,
            "phase_3_provenance_claim_record": True,
            "phase_5_anchored_typed_relation_atr_v0_1": True,
            "phase_6_hypothesis_discrimination_hde_v0_1": True,
        },
        "frozen_not_implemented": {
            "phase_4_epistemic_change_router_epr_v0_1": True,
        },
        "authority": {
            "action_gate_authorized": False,
            "retrieval_execution_authorized": False,
            "tool_execution_authorized": False,
            "identity_runtime_authorized": False,
            "relationship_runtime_authorized": False,
            "runtime_deployment_authorized": False,
            "phase_5_runtime_authorized": False,
            "phase_6_runtime_authorized": False,
        },
    }


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
    text = _derived("P0-001…P0-008_IMPLEMENTED_IN_MAIN") + "\n" + _derived(
        "P0-001…P0-015_IMPLEMENTED_IN_MAIN"
    )
    assert derived_milestones(text) == [(0, 8), (0, 15)]
    assert evaluate(_AUTHORITATIVE_P0_015, {"docs/A.md": text}) == []


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
    authoritative = _AUTHORITATIVE_P0_015 + (
        "| P1-002 Post-P0 Roadmap Step | ✅ Implemented | roadmap ≠ runtime |\n"
    )
    stale_on_old_stage = evaluate(
        authoritative,
        {"docs/A.md": _derived("P0-001…P0-015_IMPLEMENTED_IN_MAIN")},
    )
    assert len(stale_on_old_stage) == 1
    assert "P0-015" in stale_on_old_stage[0] and "P1-002" in stale_on_old_stage[0]

    assert evaluate(
        authoritative,
        {"docs/A.md": _derived("P1-001…P1-002_IMPLEMENTED_IN_MAIN")},
    ) == []


def test_readme_marker_behind_current_status_fails() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"README.md": _derived("P0-001…P0-008_IMPLEMENTED_IN_MAIN")},
    )
    assert len(problems) == 1
    assert "README.md" in problems[0]


def test_readme_marker_ahead_of_current_status_fails() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"README.md": _derived("P0-001…P0-999_IMPLEMENTED_IN_MAIN")},
    )
    assert len(problems) == 1
    assert "ahead of" in problems[0]


def test_readme_marker_equal_passes() -> None:
    assert evaluate(
        _AUTHORITATIVE_P0_015,
        {"README.md": _derived("P0-001…P0-015_IMPLEMENTED_IN_MAIN")},
    ) == []


def test_readme_missing_marker_fails() -> None:
    problems = evaluate(
        _AUTHORITATIVE_P0_015,
        {"README.md": "README without a freshness marker."},
    )
    assert len(problems) == 1
    assert "missing a well-formed" in problems[0]


def test_machine_snapshot_matching_current_status_passes() -> None:
    problems = evaluate_machine_snapshot(
        _MACHINE_STATUS,
        json.dumps(_machine_snapshot()),
    )
    assert problems == []


def test_machine_snapshot_invalid_json_fails_closed() -> None:
    problems = evaluate_machine_snapshot(_MACHINE_STATUS, "{not-json")
    assert len(problems) == 1
    assert "invalid JSON" in problems[0]


def test_machine_snapshot_must_be_explicitly_derived() -> None:
    snapshot = _machine_snapshot()
    snapshot["document_role"] = "CURRENT_TRUTH"
    snapshot["independent_truth_authority"] = True
    snapshot["conflict_rule"] = "MACHINE_WINS"
    problems = evaluate_machine_snapshot(_MACHINE_STATUS, json.dumps(snapshot))
    assert len(problems) == 3
    assert any("document_role" in problem for problem in problems)
    assert any("independent_truth_authority" in problem for problem in problems)
    assert any("conflict_rule" in problem for problem in problems)


def test_machine_snapshot_detects_implemented_drift_both_directions() -> None:
    snapshot = _machine_snapshot()
    implemented = snapshot["implemented_bounded"]
    assert isinstance(implemented, dict)
    implemented["phase_2_npg_shadow_composition"] = False
    problems = evaluate_machine_snapshot(_MACHINE_STATUS, json.dumps(snapshot))
    assert any("phase_2_npg_shadow_composition" in problem for problem in problems)

    implemented["phase_2_npg_shadow_composition"] = True
    status_without_phase_2 = _MACHINE_STATUS.replace(
        "PHASE_2_NPG_SHADOW_COMPOSITION_IMPLEMENTED_BOUNDED", ""
    )
    problems = evaluate_machine_snapshot(status_without_phase_2, json.dumps(snapshot))
    assert any("phase_2_npg_shadow_composition" in problem for problem in problems)


def test_machine_snapshot_detects_phase5_implementation_drift() -> None:
    snapshot = _machine_snapshot()
    implemented = snapshot["implemented_bounded"]
    assert isinstance(implemented, dict)
    implemented["phase_5_anchored_typed_relation_atr_v0_1"] = False
    problems = evaluate_machine_snapshot(_MACHINE_STATUS, json.dumps(snapshot))
    assert any("phase_5_anchored_typed_relation_atr_v0_1" in problem for problem in problems)


def test_machine_snapshot_detects_phase6_hde_implementation_drift() -> None:
    snapshot = _machine_snapshot()
    implemented = snapshot["implemented_bounded"]
    assert isinstance(implemented, dict)
    implemented["phase_6_hypothesis_discrimination_hde_v0_1"] = False
    problems = evaluate_machine_snapshot(_MACHINE_STATUS, json.dumps(snapshot))
    assert any(
        "phase_6_hypothesis_discrimination_hde_v0_1" in problem for problem in problems
    )

    implemented["phase_6_hypothesis_discrimination_hde_v0_1"] = True
    status_without_hde = _MACHINE_STATUS.replace(
        "PHASE_6_IMPLEMENTATION_IMPLEMENTED_BOUNDED", ""
    )
    problems = evaluate_machine_snapshot(status_without_hde, json.dumps(snapshot))
    assert any(
        "phase_6_hypothesis_discrimination_hde_v0_1" in problem for problem in problems
    )


def test_machine_snapshot_detects_frozen_contract_drift() -> None:
    snapshot = _machine_snapshot()
    frozen = snapshot["frozen_not_implemented"]
    assert isinstance(frozen, dict)
    frozen["phase_4_epistemic_change_router_epr_v0_1"] = False
    problems = evaluate_machine_snapshot(_MACHINE_STATUS, json.dumps(snapshot))
    assert any("phase_4_epistemic_change_router_epr_v0_1" in problem for problem in problems)


def test_machine_snapshot_detects_authority_drift() -> None:
    snapshot = _machine_snapshot()
    authority = snapshot["authority"]
    assert isinstance(authority, dict)
    authority["tool_execution_authorized"] = True
    problems = evaluate_machine_snapshot(_MACHINE_STATUS, json.dumps(snapshot))
    assert any("tool_execution_authorized" in problem for problem in problems)


def test_machine_snapshot_detects_phase_runtime_authority_drift() -> None:
    snapshot = _machine_snapshot()
    authority = snapshot["authority"]
    assert isinstance(authority, dict)
    authority["phase_5_runtime_authorized"] = True
    authority["phase_6_runtime_authorized"] = True
    problems = evaluate_machine_snapshot(_MACHINE_STATUS, json.dumps(snapshot))
    assert any("phase_5_runtime_authorized" in problem for problem in problems)
    assert any("phase_6_runtime_authorized" in problem for problem in problems)


def test_machine_snapshot_requires_boolean_fields() -> None:
    snapshot = _machine_snapshot()
    authority = snapshot["authority"]
    assert isinstance(authority, dict)
    authority["action_gate_authorized"] = "false"
    problems = evaluate_machine_snapshot(_MACHINE_STATUS, json.dumps(snapshot))
    assert any("expected boolean" in problem for problem in problems)
