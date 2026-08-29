"""Final-V1 machine-snapshot regressions for the documentation freshness gate."""

from __future__ import annotations

import copy
import json

from check_doc_freshness import evaluate_machine_snapshot


_CURRENT_V1_STATUS = """
# 🚦 Mentaury Soul — Current Status

## 1. 🧭 Current checkpoint

```text
CLAIM_TO_BELIEF_BINDING_IMPLEMENTED_BOUNDED
PHASE_4_IMPLEMENTATION_IMPLEMENTED_BOUNDED
PHASE_4_RUNTIME_NOT_AUTHORIZED
V1_OFFLINE_EPISTEMIC_E2E_VERIFIED
V1_RESEARCH_CORE_VERSION_1_0_0
V1_STAGE_5_FINAL_ACCEPTANCE_COMPLETE
V1_DISTRIBUTION_PROPRIETARY_ALL_RIGHTS_RESERVED
TERMINAL_RECONSIDERATION_LINEAGE_NOT_IMPLEMENTED
```

---
"""


def _snapshot() -> dict[str, object]:
    return {
        "schema": "mentaury-project-state/1",
        "project": "Mentaury Soul",
        "document_role": "DERIVED_MACHINE_SNAPSHOT",
        "conflict_rule": "LIVE_GITHUB_AND_CURRENT_STATUS_OVERRIDE_THIS_SNAPSHOT",
        "independent_truth_authority": False,
        "v1_research_core": {
            "final_version": "1.0.0",
            "release_status": "FINAL_ACCEPTANCE_COMPLETE",
            "offline_e2e_verified": True,
            "license_distribution_owner_decision_required": False,
            "license_distribution_posture": "PROPRIETARY_ALL_RIGHTS_RESERVED",
        },
        "implemented_bounded": {
            "claim_to_belief_binding_cbp_v0_1": True,
            "phase_4_epistemic_change_router_epr_v0_1": True,
        },
        "frozen_not_implemented": {
            "phase_4_epistemic_change_router_epr_v0_1": False,
            "terminal_reconsideration_lineage": True,
        },
        "authority": {
            "phase_4_runtime_authorized": False,
        },
    }


def _evaluate(snapshot: dict[str, object]) -> list[str]:
    return evaluate_machine_snapshot(_CURRENT_V1_STATUS, json.dumps(snapshot))


def test_current_v1_machine_snapshot_fields_pass() -> None:
    assert _evaluate(_snapshot()) == []


def test_machine_snapshot_detects_cbp_and_epr_drift() -> None:
    snapshot = _snapshot()
    implemented = snapshot["implemented_bounded"]
    assert isinstance(implemented, dict)
    implemented["claim_to_belief_binding_cbp_v0_1"] = False
    implemented["phase_4_epistemic_change_router_epr_v0_1"] = False

    problems = _evaluate(snapshot)
    assert any("claim_to_belief_binding_cbp_v0_1" in problem for problem in problems)
    assert any(
        "phase_4_epistemic_change_router_epr_v0_1" in problem for problem in problems
    )


def test_machine_snapshot_detects_terminal_lineage_drift() -> None:
    snapshot = _snapshot()
    frozen = snapshot["frozen_not_implemented"]
    assert isinstance(frozen, dict)
    frozen["terminal_reconsideration_lineage"] = False

    problems = _evaluate(snapshot)
    assert any("terminal_reconsideration_lineage" in problem for problem in problems)


def test_machine_snapshot_detects_phase4_runtime_authority_drift() -> None:
    snapshot = _snapshot()
    authority = snapshot["authority"]
    assert isinstance(authority, dict)
    authority["phase_4_runtime_authorized"] = True

    problems = _evaluate(snapshot)
    assert any("phase_4_runtime_authorized" in problem for problem in problems)


def test_machine_snapshot_detects_v1_completion_drift() -> None:
    snapshot = _snapshot()
    v1 = snapshot["v1_research_core"]
    assert isinstance(v1, dict)
    v1["final_version"] = "0.0.0"
    v1["release_status"] = "RELEASE_CANDIDATE"
    v1["offline_e2e_verified"] = False
    v1["license_distribution_owner_decision_required"] = True
    v1["license_distribution_posture"] = "UNDECIDED"

    problems = _evaluate(snapshot)
    for field in (
        "final_version",
        "release_status",
        "offline_e2e_verified",
        "license_distribution_owner_decision_required",
        "license_distribution_posture",
    ):
        assert any(f"v1_research_core.{field}" in problem for problem in problems)


def test_machine_snapshot_requires_v1_block_when_current_status_is_final() -> None:
    snapshot = _snapshot()
    snapshot.pop("v1_research_core")

    problems = _evaluate(snapshot)
    assert any("v1_research_core must be an object" in problem for problem in problems)


def test_machine_snapshot_detects_forward_v1_claim_without_current_marker() -> None:
    status = _CURRENT_V1_STATUS.replace("V1_STAGE_5_FINAL_ACCEPTANCE_COMPLETE", "")
    snapshot = copy.deepcopy(_snapshot())

    problems = evaluate_machine_snapshot(status, json.dumps(snapshot))
    assert any(
        "v1_research_core.release_status" in problem and "ahead of" in problem
        for problem in problems
    )
