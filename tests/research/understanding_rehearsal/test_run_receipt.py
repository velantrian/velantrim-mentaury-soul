from __future__ import annotations

from pathlib import Path

from tests.research.understanding_rehearsal.offline_harness import commitment_manifest
from tests.research.understanding_rehearsal.run_receipt import (
    build_run_receipt,
    build_scenario_evaluation_summary,
    summarize_diagnostics,
)

ROOT = Path(__file__).resolve().parents[3]


def _valid_summary() -> dict:
    return {
        "schema": "understanding-evaluation-summary-v0.1",
        "dimensions": {},
        "hard_fails": {},
        "disagreement_states": {},
        "diagnostics": {},
        "aggregate_understanding_score": None,
        "architectural_interpretation": "NOT_COMPUTED_BY_HARNESS",
    }


def test_diagnostics_are_reported_separately_by_arm_and_name() -> None:
    mapping = {"P1": "B0", "P2": "B1", "P3": "C1"}
    evaluations = [
        {"packet_id": "P1", "diagnostics": {"unnecessary_analysis": 0, "invented_alternative": False}},
        {"packet_id": "P2", "diagnostics": {"unnecessary_analysis": 1, "invented_alternative": False}},
        {"packet_id": "P3", "diagnostics": {"unnecessary_analysis": 0, "invented_alternative": True}},
    ]
    summary = summarize_diagnostics(mapping, evaluations)
    assert summary["B0"]["unnecessary_analysis"] == {"0": 1}
    assert summary["B1"]["unnecessary_analysis"] == {"1": 1}
    assert summary["C1"]["invented_alternative"] == {"true": 1}
    assert "aggregate" not in str(summary).lower()


def test_scenario_summary_binds_diagnostics_without_architectural_interpretation() -> None:
    mapping = {"P1": "B0"}
    evaluations = [{"packet_id": "P1", "diagnostics": {"missed_constraint": 1}}]
    base = _valid_summary()
    base.pop("diagnostics")
    combined = build_scenario_evaluation_summary(
        evaluation_summary=base,
        mapping=mapping,
        evaluations=evaluations,
    )
    assert combined["diagnostics"]["B0"]["missed_constraint"] == {"1": 1}
    assert combined["aggregate_understanding_score"] is None
    assert combined["architectural_interpretation"] == "NOT_COMPUTED_BY_HARNESS"


def test_partial_run_receipt_is_explicitly_incomplete() -> None:
    manifest = commitment_manifest(ROOT)
    first = manifest["items"][0]["scenario_id"]
    receipt = build_run_receipt(
        repository_sha="a" * 40,
        commitment_manifest=manifest,
        scenario_receipts=[{"scenario_id": first, "receipt_sha256": "b" * 64}],
        scenario_summaries={first: _valid_summary()},
    )
    assert receipt["status"] == "INCOMPLETE_RUN"
    assert receipt["observed_scenario_count"] == 1
    assert len(receipt["missing_scenarios"]) == 11
    assert receipt["aggregate_understanding_score"] is None
    assert receipt["architectural_interpretation"] == "NOT_COMPUTED_BY_HARNESS"


def test_complete_run_receipt_requires_all_committed_scenarios_and_summaries() -> None:
    manifest = commitment_manifest(ROOT)
    scenario_receipts = [
        {"scenario_id": item["scenario_id"], "receipt_sha256": f"{index:064x}"}
        for index, item in enumerate(manifest["items"], start=1)
    ]
    scenario_summaries = {item["scenario_id"]: _valid_summary() for item in manifest["items"]}
    receipt = build_run_receipt(
        repository_sha="c" * 40,
        commitment_manifest=manifest,
        scenario_receipts=scenario_receipts,
        scenario_summaries=scenario_summaries,
    )
    assert receipt["status"] == "COMPLETE"
    assert receipt["expected_scenario_count"] == 12
    assert receipt["observed_scenario_count"] == 12
    assert receipt["missing_scenarios"] == []
    assert len(receipt["items"]) == 12
    assert len(receipt["receipt_sha256"]) == 64


def test_missing_evaluation_summary_keeps_run_incomplete() -> None:
    manifest = commitment_manifest(ROOT)
    scenario_receipts = [
        {"scenario_id": item["scenario_id"], "receipt_sha256": f"{index:064x}"}
        for index, item in enumerate(manifest["items"], start=1)
    ]
    scenario_summaries = {item["scenario_id"]: _valid_summary() for item in manifest["items"][:-1]}
    receipt = build_run_receipt(
        repository_sha="d" * 40,
        commitment_manifest=manifest,
        scenario_receipts=scenario_receipts,
        scenario_summaries=scenario_summaries,
    )
    assert receipt["status"] == "INCOMPLETE_RUN"


def test_run_receipt_rejects_composite_or_missing_diagnostics_summary() -> None:
    manifest = commitment_manifest(ROOT)
    first = manifest["items"][0]["scenario_id"]
    bad = _valid_summary()
    bad["aggregate_understanding_score"] = 0.8
    try:
        build_run_receipt(
            repository_sha="e" * 40,
            commitment_manifest=manifest,
            scenario_receipts=[{"scenario_id": first, "receipt_sha256": "f" * 64}],
            scenario_summaries={first: bad},
        )
    except ValueError as exc:
        assert str(exc) == "COMPOSITE-SCORE-FORBIDDEN"
    else:
        raise AssertionError("composite score must be rejected")
