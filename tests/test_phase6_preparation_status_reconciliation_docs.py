"""Structural guards for authoritative Phase 6 research-preparation status."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
BENCHMARK = (
    ROOT
    / "docs"
    / "research"
    / "INFERENCE_BRIDGE_HYPOTHESIS_DISCRIMINATION_BENCHMARK.md"
).read_text(encoding="utf-8")


def test_current_status_records_phase6_prepared_not_runtime() -> None:
    for marker in (
        "PHASE_6_RESEARCH_PREPARATION_PREPARED_DOCS_TESTS_ONLY",
        "PHASE_6_INFERENCE_BRIDGE_AUDIT_PREPARED_DOCS_TESTS_ONLY",
        "PHASE_6_HYPOTHESIS_DISCRIMINATION_BENCHMARK_PREPARED_DOCS_TESTS_ONLY",
        "PHASE_6_BENCHMARK_PR_121_VERIFIED",
        "PHASE_6_IMPLEMENTATION_MILESTONE_NOT_SELECTED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION_NOT_GRANTED",
        "PHASE_6_RUNTIME_NOT_AUTHORIZED",
    ):
        assert marker in STATUS


def test_current_status_links_verified_benchmark_evidence() -> None:
    for marker in (
        "#121",
        "af49fc90f88b34f54ebeaa8d1afd45ab76173763",
        "31871208558",
        "1074 passed",
        "4943195249",
        "147b456d7cbb56022a4234a0ca3f1cc861662fec",
        "31871247296",
        "INFERENCE_BRIDGE_HYPOTHESIS_DISCRIMINATION_BENCHMARK.md",
    ):
        assert marker in STATUS


def test_status_and_benchmark_share_failure_mode_and_stop_boundary() -> None:
    for marker in (
        "NON_DISCRIMINATING_EVIDENCE_COLLECTION",
        "PHASE_6_IMPLEMENTATION_MILESTONE = NOT_SELECTED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = NOT_GRANTED",
        "PHASE_6_RUNTIME = NOT_AUTHORIZED",
    ):
        assert marker in STATUS
        assert marker in BENCHMARK


def test_no_phase6_runtime_source_package_exists() -> None:
    for path in (
        ROOT / "src" / "mentaury" / "inference_bridge",
        ROOT / "src" / "mentaury" / "hypothesis_discrimination",
        ROOT / "src" / "mentaury" / "inquiry",
        ROOT / "src" / "mentaury" / "scheduler",
    ):
        assert not path.exists()
