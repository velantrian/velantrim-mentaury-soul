"""#173 Track C regressions: active navigation final-V1 semantic freshness.

README.md, docs/MENTAURY_QUICK_REFERENCE.md and docs/ai/COMPONENT_MAP.md are
derived navigation surfaces. These tests bind them to
docs/CURRENT_STATUS.md ``## 1. Current checkpoint`` only. They do not make
those pages authoritative, and they do not place
docs/ENVIRONMENT_MANIFEST.md under Track C.
"""

from __future__ import annotations

import json

import check_doc_freshness
from check_doc_freshness import (
    ACTIVE_DERIVED_DOC_PATHS,
    ACTIVE_NAVIGATION_DOC_PATHS,
    CURRENT_STATUS_PATH,
    ENVIRONMENT_MANIFEST_PATH,
    ENVIRONMENT_MANIFEST_RELATIVE_PATH,
    PROJECT_MANIFEST_PATH,
    ROOT,
    evaluate,
    evaluate_active_navigation_semantics,
    evaluate_environment_manifest_role,
    evaluate_machine_snapshot,
)


_QR = "docs/MENTAURY_QUICK_REFERENCE.md"
_COMPONENT_MAP = "docs/ai/COMPONENT_MAP.md"


def _real_status() -> str:
    return CURRENT_STATUS_PATH.read_text(encoding="utf-8")


def _real_manifest() -> dict[str, object]:
    parsed = json.loads(PROJECT_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    return parsed


def _real_navigation() -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)): path.read_text(encoding="utf-8")
        for path in ACTIVE_NAVIGATION_DOC_PATHS
    }


def _real_p_stage_texts() -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)): path.read_text(encoding="utf-8")
        for path in ACTIVE_DERIVED_DOC_PATHS
    }


def _mutate_lines(text: str, predicate, mutator) -> str:
    out: list[str] = []
    for line in text.splitlines():
        out.append(mutator(line) if predicate(line) else line)
    return "\n".join(out)


def _lower(line: str) -> str:
    return line.casefold()


def _rewrite_cbp_implemented(text: str) -> str:
    def hit(line: str) -> bool:
        folded = _lower(line)
        return "cbp-v0.1" in folded or "claim_to_belief_binding" in folded

    def mutate(line: str) -> str:
        return (
            line.replace("IMPLEMENTED_BOUNDED", "ABSENT")
            .replace("implemented bounded", "absent")
            .replace("Implemented bounded", "Absent")
        )

    return _mutate_lines(text, hit, mutate)


def _rewrite_epr_implemented(text: str) -> str:
    def hit(line: str) -> bool:
        return "epr-v0.1" in _lower(line)

    def mutate(line: str) -> str:
        return (
            line.replace("IMPLEMENTED_BOUNDED", "ABSENT")
            .replace("implemented bounded", "absent")
            .replace("Implemented bounded", "Absent")
            .replace("routing only", "")
            .replace("next-owner routing", "")
            .replace("routes to the next owner only", "")
        )

    rewritten = _mutate_lines(text, hit, mutate)
    return (
        rewritten.replace("routing ≠ mutation authority", "")
        .replace("no mutation/execution authority", "")
        .replace("pure next-owner routing", "")
    )


def _rewrite_v1_final(text: str) -> str:
    return (
        text.replace("FINAL_ACCEPTANCE", "RELEASE_CANDIDATE")
        .replace("final acceptance", "release candidate")
        .replace("FINAL ACCEPTANCE", "release candidate")
        .replace("E2E verified", "E2E unverified")
        .replace("VERIFIED", "UNVERIFIED")
    )


def _rewrite_terminal_backlog(text: str) -> str:
    def hit(line: str) -> bool:
        return "terminal reconsideration" in _lower(line).replace("_", " ")

    def mutate(line: str) -> str:
        return (
            line.replace("NOT_IMPLEMENTED", "IMPLEMENTED")
            .replace("NOT IMPLEMENTED", "IMPLEMENTED")
            .replace("V1.1/V2_BACKLOG", "")
            .replace("V1.1/V2 BACKLOG", "")
            .replace("V1.1 / V2 BACKLOG", "")
        )

    return _mutate_lines(text, hit, mutate)


def _rewrite_action_ceiling(text: str) -> str:
    def hit(line: str) -> bool:
        folded = _lower(line)
        return (
            "action gate" in folded
            or "retrieval" in folded
            or "tools" in folded
            or "tool_execution" in folded
        )

    def mutate(line: str) -> str:
        return (
            line.replace("NOT_AUTHORIZED", "AUTHORIZED")
            .replace("Not authorized", "Authorized")
            .replace("NOT AUTHORIZED", "AUTHORIZED")
        )

    return _mutate_lines(text, hit, mutate)


def _rewrite_deployment(text: str) -> str:
    def hit(line: str) -> bool:
        folded = _lower(line)
        return "deployment" in folded

    def mutate(line: str) -> str:
        return (
            line.replace("NOT_AUTHORIZED", "AUTHORIZED")
            .replace("Not authorized", "Authorized")
        )

    return _mutate_lines(text, hit, mutate)


def _evaluate_nav(
    status: str | None = None,
    navigation: dict[str, str] | None = None,
    manifest: dict[str, object] | None = None,
) -> list[str]:
    return evaluate_active_navigation_semantics(
        _real_status() if status is None else status,
        _real_navigation() if navigation is None else navigation,
        _real_manifest() if manifest is None else manifest,
    )


def test_c_a_current_repository_navigation_semantics_pass() -> None:
    """C-A: current correct final-V1 navigation surfaces pass as-is."""

    assert _evaluate_nav() == []
    assert ENVIRONMENT_MANIFEST_PATH not in ACTIVE_NAVIGATION_DOC_PATHS
    assert check_doc_freshness.main() == 0


def test_c_b_cbp_drift_fails_while_p_stage_remains_valid() -> None:
    """C-B: CBP drift fails Track C; legacy P-stage markers stay valid."""

    navigation = _real_navigation()
    navigation[_QR] = _rewrite_cbp_implemented(navigation[_QR])

    problems = _evaluate_nav(navigation=navigation)
    assert any("C1 CBP" in problem and _QR in problem for problem in problems)

    p_stage_texts = _real_p_stage_texts()
    p_stage_texts[_QR] = navigation[_QR]
    assert evaluate(_real_status(), p_stage_texts) == []


def test_c_c_epr_drift_fails() -> None:
    """C-C: EPR implemented/routing drift fails Track C."""

    navigation = _real_navigation()
    navigation[_COMPONENT_MAP] = _rewrite_epr_implemented(navigation[_COMPONENT_MAP])

    problems = _evaluate_nav(navigation=navigation)
    assert any("C2 EPR" in problem and _COMPONENT_MAP in problem for problem in problems)


def test_c_d_v1_final_release_candidate_drift_fails() -> None:
    """C-D: V1 final → release-candidate / unverified drift fails."""

    navigation = _real_navigation()
    navigation[_QR] = _rewrite_v1_final(navigation[_QR])

    problems = _evaluate_nav(navigation=navigation)
    assert any("C3 V1" in problem and _QR in problem for problem in problems)


def test_c_e_terminal_backlog_drift_fails() -> None:
    """C-E: terminal reconsideration must stay NOT_IMPLEMENTED + V1.1/V2 backlog."""

    navigation = _real_navigation()
    navigation["README.md"] = _rewrite_terminal_backlog(navigation["README.md"])

    problems = _evaluate_nav(navigation=navigation)
    assert any(
        "C4 terminal backlog" in problem and "README.md" in problem
        for problem in problems
    )


def test_c_f_action_execution_ceiling_drift_fails() -> None:
    """C-F: Action Gate / retrieval / tools must remain NOT_AUTHORIZED."""

    navigation = _real_navigation()
    navigation[_QR] = _rewrite_action_ceiling(navigation[_QR])

    problems = _evaluate_nav(navigation=navigation)
    assert any(
        "C5 action/execution" in problem and _QR in problem for problem in problems
    )


def test_c_g_deployment_drift_fails() -> None:
    """C-G: runtime/deployment must remain NOT_AUTHORIZED."""

    navigation = _real_navigation()
    navigation[_COMPONENT_MAP] = _rewrite_deployment(navigation[_COMPONENT_MAP])

    problems = _evaluate_nav(navigation=navigation)
    assert any(
        "C6 deployment" in problem and _COMPONENT_MAP in problem for problem in problems
    )


def test_c_h_contradictory_stale_plus_current_fails() -> None:
    """C-H: current correct claims plus known stale inverses must fail."""

    navigation = _real_navigation()
    stale_block = (
        "Claim→belief binding = NOT_IMPLEMENTED\n"
        "EPR-v0.1 = FROZEN_DOCS · NOT_IMPLEMENTED\n"
        "Current project state | V1 Research/Core release candidate\n"
    )
    navigation[_QR] = stale_block + navigation[_QR]

    problems = _evaluate_nav(navigation=navigation)
    assert any("C1 CBP contradictory" in problem for problem in problems)
    assert any("C2 EPR contradictory" in problem for problem in problems)
    assert any("C3 V1 contradictory" in problem for problem in problems)


def test_c_i_current_checkpoint_isolation_ignores_history_only_markers() -> None:
    """C-I: a marker only outside ## 1. Current checkpoint does not satisfy auth."""

    status = _real_status().replace(
        "CLAIM_TO_BELIEF_BINDING_IMPLEMENTED_BOUNDED\n",
        "",
        1,
    )
    status = (
        status
        + "\nCLAIM_TO_BELIEF_BINDING_IMPLEMENTED_BOUNDED\n"
    )
    assert "CLAIM_TO_BELIEF_BINDING_IMPLEMENTED_BOUNDED" not in (
        check_doc_freshness.current_checkpoint(status) or ""
    )
    assert "CLAIM_TO_BELIEF_BINDING_IMPLEMENTED_BOUNDED" in status

    problems = _evaluate_nav(status=status)
    assert any(
        "C1 CBP" in problem and "no longer has" in problem for problem in problems
    )


def test_c_j_active_role_conflict_fails_closed() -> None:
    """C-J: Track C surface reclassified historical/reconcile-before-use fails closed."""

    manifest = _real_manifest()
    historical = list(manifest["historical_or_reconcile_before_use"])
    historical.append("README.md")
    manifest["historical_or_reconcile_before_use"] = historical

    problems = _evaluate_nav(manifest=manifest)
    assert any(
        "README.md" in problem
        and "fail closed" in problem
        and "historical_or_reconcile_before_use" in problem
        for problem in problems
    )
    assert not any("silently skipping" in problem and "PASS" in problem for problem in problems)


def test_c_k_environment_manifest_remains_track_b() -> None:
    """C-K: Environment Manifest is not a Track C CBP/EPR/ATR/HDE/V1 surface."""

    assert ENVIRONMENT_MANIFEST_PATH not in ACTIVE_NAVIGATION_DOC_PATHS
    assert ENVIRONMENT_MANIFEST_RELATIVE_PATH not in {
        str(path.relative_to(ROOT)) for path in ACTIVE_NAVIGATION_DOC_PATHS
    }

    historical_body = """# ⚙️ Mentaury Environment Manifest

> **Currentness:** historical / `RECONCILE_BEFORE_USE`.
> This file is a bounded environment / P-stage inventory checkpoint, not a complete current implementation ledger.
> Reconcile against docs/CURRENT_STATUS.md and live GitHub before treating the source list below as exhaustive.

```text
P0-001…P0-008_IMPLEMENTED_IN_MAIN
src/mentaury/capabilities/lease/
```
"""
    assert "CBP-v0.1" not in historical_body
    assert "EPR-v0.1" not in historical_body
    assert "ATR-v0.1" not in historical_body
    assert "HDE-v0.1" not in historical_body
    assert "1.0.0" not in historical_body

    problems = evaluate_environment_manifest_role(
        _real_manifest(),
        historical_body,
        active_derived_relative_paths=tuple(
            str(path.relative_to(ROOT)) for path in ACTIVE_DERIVED_DOC_PATHS
        ),
    )
    assert problems == []

    nav_on_manifest = evaluate_active_navigation_semantics(
        _real_status(),
        {ENVIRONMENT_MANIFEST_RELATIVE_PATH: historical_body},
        _real_manifest(),
        track_c_relative_paths=tuple(
            str(path.relative_to(ROOT)) for path in ACTIVE_NAVIGATION_DOC_PATHS
        ),
    )
    assert nav_on_manifest != []


def test_c_l_existing_track_a_b_and_stale_p_stage_still_fail() -> None:
    """C-L: Track A/B and the legacy P-stage guard remain fail-closed."""

    stale_p_stage = evaluate(
        _real_status(),
        {
            "README.md": "P0-001…P0-008_IMPLEMENTED_IN_MAIN",
            _QR: "P0-001…P0-008_IMPLEMENTED_IN_MAIN",
        },
    )
    assert stale_p_stage
    assert any("P0-008" in problem for problem in stale_p_stage)

    snapshot = json.loads(
        (ROOT / "docs" / "state" / "project_state.json").read_text(encoding="utf-8")
    )
    snapshot["implemented_bounded"]["claim_to_belief_binding_cbp_v0_1"] = False
    machine_problems = evaluate_machine_snapshot(_real_status(), json.dumps(snapshot))
    assert any("claim_to_belief_binding_cbp_v0_1" in problem for problem in machine_problems)

    unmarked = "# Environment Manifest\n\nP0-001…P0-015_IMPLEMENTED_IN_MAIN\n"
    role_problems = evaluate_environment_manifest_role(
        _real_manifest(),
        unmarked,
        active_derived_relative_paths=tuple(
            str(path.relative_to(ROOT)) for path in ACTIVE_DERIVED_DOC_PATHS
        ),
    )
    assert any("missing required" in problem for problem in role_problems)

    assert _evaluate_nav() == []


def test_missing_current_checkpoint_fails_closed() -> None:
    problems = _evaluate_nav(status="CLAIM_TO_BELIEF_BINDING_IMPLEMENTED_BOUNDED\n")
    assert len(problems) == 1
    assert "Current checkpoint" in problems[0]


def test_malformed_manifest_role_list_does_not_skip_track_c() -> None:
    problems = _evaluate_nav(
        manifest={"historical_or_reconcile_before_use": {"README.md": "historical"}}
    )
    assert any("must be a list" in problem for problem in problems)
    assert any("cannot skip" in problem for problem in problems)
