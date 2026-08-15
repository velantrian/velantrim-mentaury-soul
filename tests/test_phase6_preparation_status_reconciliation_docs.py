"""Structural guards for authoritative Phase 6 status after HDE-v0.1 completion.

Historical benchmark/readiness documents remain immutable provenance; current
status may advance after separate Owner GO and verified bounded implementation.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = (ROOT / "docs" / "CURRENT_STATUS.md").read_text(encoding="utf-8")
BENCHMARK = (
    ROOT / "docs" / "research" / "INFERENCE_BRIDGE_HYPOTHESIS_DISCRIMINATION_BENCHMARK.md"
).read_text(encoding="utf-8")
READINESS = (
    ROOT / "docs" / "research" / "PHASE_6_HYPOTHESIS_DISCRIMINATION_READINESS.md"
).read_text(encoding="utf-8")
CONTRACT = (
    ROOT / "docs" / "research" / "HYPOTHESIS_DISCRIMINATION_EVALUATOR_CONTRACT_V0_1.md"
).read_text(encoding="utf-8")
OWNER_GO = (
    ROOT / "docs" / "research" / "HYPOTHESIS_DISCRIMINATION_EVALUATOR_OWNER_GO_DECISION.md"
).read_text(encoding="utf-8")
RECEIPT = (
    ROOT / "docs" / "HYPOTHESIS_DISCRIMINATION_EVALUATOR_IMPLEMENTATION_AUTHORIZATION.md"
).read_text(encoding="utf-8")


def test_current_status_records_hde_implemented_bounded_not_runtime() -> None:
    for marker in (
        "PHASE_6_RESEARCH_PREPARATION_PREPARED_DOCS_TESTS_ONLY",
        "PHASE_6_INFERENCE_BRIDGE_AUDIT_PREPARED_DOCS_TESTS_ONLY",
        "PHASE_6_HYPOTHESIS_DISCRIMINATION_BENCHMARK_PREPARED_DOCS_TESTS_ONLY",
        "PHASE_6_BENCHMARK_PR_121_VERIFIED",
        "PHASE_6_READINESS_SELECTED_CANDIDATE_CONTRACT_FROZEN_DOCS_TESTS_ONLY",
        "PHASE_6_CANDIDATE_PURE_HYPOTHESIS_DISCRIMINATION_EVALUATOR",
        "PHASE_6_IMPLEMENTATION_CONTRACT_HDE_V0_1_FROZEN_DOCS_TESTS_ONLY",
        "PHASE_6_READINESS_PR_124_VERIFIED",
        "PHASE_6_OWNER_GO_CONSUMED_BY_PR_127",
        "PHASE_6_OWNER_GO_SCOPE_HDE_V0_1_ONLY",
        "PHASE_6_IMPLEMENTATION_AUTHORIZATION_CONSUMED_HDE_V0_1_ONLY",
        "PHASE_6_IMPLEMENTATION_IMPLEMENTED_BOUNDED",
        "PHASE_6_HDE_T01_T16_EXECUTABLE_PASS",
        "PHASE_6_HDE_M01_M10_EXECUTABLE_PASS",
        "PHASE_6_RUNTIME_NOT_AUTHORIZED",
    ):
        assert marker in STATUS


def test_current_status_links_complete_hde_evidence_chain() -> None:
    for marker in (
        "#121",
        "af49fc90f88b34f54ebeaa8d1afd45ab76173763",
        "31871208558",
        "#124",
        "a41394de254c9920d8829cd9bda73de4e95a82a0",
        "31877329002",
        "#126",
        "de0cbbce8fe0ffb50f60f622026cd3d427842e66",
        "#127",
        "6977d5696cf642653aaef56f4cbef73db35070ec",
        "31886102508",
        "1111 passed",
        "4943890604",
        "2c916e8ce44f623d1a1880f8e480ae2f13277615",
        "31886151205",
        "HYPOTHESIS_DISCRIMINATION_EVALUATOR_IMPLEMENTATION_AUTHORIZATION.md",
    ):
        assert marker in STATUS


def test_historical_docs_retain_preimplementation_authority_state() -> None:
    for marker in (
        "PHASE_6_IMPLEMENTATION_MILESTONE = NOT_SELECTED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = NOT_GRANTED",
        "PHASE_6_RUNTIME = NOT_AUTHORIZED",
    ):
        assert marker in BENCHMARK

    for marker in (
        "PHASE_6_IMPLEMENTATION = NOT_STARTED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = NOT_GRANTED",
        "PHASE_6_RUNTIME = NOT_AUTHORIZED",
    ):
        assert marker in READINESS or marker in CONTRACT
        assert marker in STATUS  # retained explicitly as historical compatibility provenance


def test_owner_go_is_consumed_only_by_verified_hde_implementation() -> None:
    assert "Owner GO scope:                 HDE-v0.1_ONLY" in OWNER_GO
    assert "Single-use authorization:       YES" in OWNER_GO
    for marker in (
        "PHASE_6_IMPLEMENTATION = IMPLEMENTED_BOUNDED",
        "PHASE_6_OWNER_GO_FOR_IMPLEMENTATION = CONSUMED_BY_PR_127",
        "PHASE_6_RUNTIME = NOT_AUTHORIZED",
    ):
        assert marker in RECEIPT


def test_historical_current_status_snapshot_is_preserved() -> None:
    snapshot = ROOT / "docs" / "history" / "CURRENT_STATUS_PRE_HDE_READINESS_2026_08_15.md"
    assert snapshot.exists()
    text = snapshot.read_text(encoding="utf-8")
    assert "PHASE_6_IMPLEMENTATION_MILESTONE_NOT_SELECTED" in text
    assert "PHASE_6_BENCHMARK_PR_121_VERIFIED" in text


def test_only_authorized_hde_package_exists_and_runtime_packages_remain_absent() -> None:
    for path in (
        ROOT / "src" / "mentaury" / "inference_bridge",
        ROOT / "src" / "mentaury" / "hypothesis_discrimination",
        ROOT / "src" / "mentaury" / "inquiry",
        ROOT / "src" / "mentaury" / "scheduler",
    ):
        assert not path.exists()

    discrimination = ROOT / "src" / "mentaury" / "discrimination"
    assert discrimination.is_dir()
    assert {path.name for path in discrimination.iterdir() if path.is_file()} == {
        "__init__.py",
        "contracts.py",
        "evaluator.py",
    }
    assert (ROOT / "tests" / "test_hypothesis_discrimination_evaluator.py").is_file()
