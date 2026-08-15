"""Structural guards for authoritative Phase 6 readiness status.

The benchmark document remains historical preparation evidence. CURRENT_STATUS is
allowed to advance after the separate HDE-v0.1 readiness/selection merge.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
BENCHMARK = (
    ROOT
    / "docs"
    / "research"
    / "INFERENCE_BRIDGE_HYPOTHESIS_DISCRIMINATION_BENCHMARK.md"
).read_text(encoding="utf-8")
READINESS = (
    ROOT
    / "docs"
    / "research"
    / "PHASE_6_HYPOTHESIS_DISCRIMINATION_READINESS.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT
    / "docs"
    / "research"
    / "HYPOTHESIS_DISCRIMINATION_EVALUATOR_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")


def test_current_status_records_phase6_selected_but_not_implemented() -> None:
    for marker in (
        "PHASE_6_RESEARCH_PREPARATION_PREPARED_DOCS_TESTS_ONLY",
        "PHASE_6_INFERENCE_BRIDGE_AUDIT_PREPARED_DOCS_TESTS_ONLY",
        "PHASE_6_HYPOTHESIS_DISCRIMINATION_BENCHMARK_PREPARED_DOCS_TESTS_ONLY",
        "PHASE_6_BENCHMARK_PR_121_VERIFIED",
        "PHASE_6_READINESS_SELECTED_CANDIDATE_CONTRACT_FROZEN_DOCS_TESTS_ONLY",
        "PHASE_6_CANDIDATE_PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR",
        "PHASE_6_IMPLEMENTATION_CONTRACT_HDE_V0_1_FROZEN_DOCS_TESTS_ONLY",
        "PHASE_6_READINESS_PR_124_VERIFIED",
        "PHASE_6_IMPLEMENTATION_NOT_STARTED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION_NOT_GRANTED",
        "PHASE_6_RUNTIME_NOT_AUTHORIZED",
    ):
        assert marker in STATUS


def test_current_status_links_verified_benchmark_and_hde_evidence() -> None:
    for marker in (
        "#121",
        "af49fc90f88b34f54ebeaa8d1afd45ab76173763",
        "31871208558",
        "1074 passed",
        "4943195249",
        "147b456d7cbb56022a4234a0ca3f1cc861662fec",
        "31871247296",
        "#124",
        "a41394de254c9920d8829cd9bda73de4e95a82a0",
        "31877329002",
        "1088 passed",
        "c45bdc12bb3f25f38982554d4b96de3084c22815",
        "31877392090",
        "INFERENCE_BRIDGE_HYPOTHESIS_DISCRIMINATION_BENCHMARK.md",
        "PHASE_6_HYPOTHESIS_DISCRIMINATION_READINESS.md",
        "HYPOTHESIS_DISCRIMINATION_EVALUATOR_CONTRACT_V0_1.md",
    ):
        assert marker in STATUS


def test_historical_benchmark_retains_old_stop_while_current_status_advances() -> None:
    for marker in (
        "NON_DISCRIMINATING_EVIDENCE_COLLECTION",
        "PHASE_6_IMPLEMENTATION_MILESTONE = NOT_SELECTED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = NOT_GRANTED",
        "PHASE_6_RUNTIME = NOT_AUTHORIZED",
    ):
        assert marker in BENCHMARK

    for marker in (
        "PHASE_6_READINESS = SELECTED_CANDIDATE_CONTRACT_FROZEN_DOCS_TESTS_ONLY",
        "PHASE_6_CANDIDATE = PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR",
        "PHASE_6_IMPLEMENTATION_CONTRACT = HDE-v0.1 · FROZEN_DOCS_TESTS_ONLY",
        "PHASE_6_IMPLEMENTATION = NOT_STARTED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = NOT_GRANTED",
        "PHASE_6_RUNTIME = NOT_AUTHORIZED",
    ):
        assert marker in STATUS
        assert marker in READINESS or marker in CONTRACT


def test_historical_current_status_snapshot_is_preserved() -> None:
    snapshot = ROOT / "docs" / "history" / "CURRENT_STATUS_PRE_HDE_READINESS_2026_08_15.md"
    assert snapshot.exists()
    text = snapshot.read_text(encoding="utf-8")
    assert "PHASE_6_IMPLEMENTATION_MILESTONE_NOT_SELECTED" in text
    assert "PHASE_6_BENCHMARK_PR_121_VERIFIED" in text


def test_no_phase6_runtime_source_package_exists() -> None:
    for path in (
        ROOT / "src" / "mentaury" / "inference_bridge",
        ROOT / "src" / "mentaury" / "hypothesis_discrimination",
        ROOT / "src" / "mentaury" / "discrimination",
        ROOT / "src" / "mentaury" / "inquiry",
        ROOT / "src" / "mentaury" / "scheduler",
    ):
        assert not path.exists()
