from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import json
from typing import Any


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return sha256(canonical_json(value)).hexdigest()


def summarize_diagnostics(mapping: dict[str, str], evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    """Preserve diagnostic distributions without turning them into a composite score."""
    counts: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    for evaluation in evaluations:
        packet_id = evaluation["packet_id"]
        arm = mapping[packet_id]
        diagnostics = evaluation["diagnostics"]
        if not isinstance(diagnostics, dict):
            raise ValueError("EVAL-DIAGNOSTICS-INVALID")
        for name, value in diagnostics.items():
            encoded = canonical_json(value).decode("utf-8")
            counts[arm][name][encoded] += 1
    return {
        arm: {name: dict(value_counts) for name, value_counts in by_name.items()}
        for arm, by_name in counts.items()
    }


def build_run_receipt(
    *,
    repository_sha: str,
    commitment_manifest: dict[str, Any],
    scenario_receipts: list[dict[str, Any]],
    scenario_summaries: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a deterministic whole-run receipt; never infer missing scenarios or conclusions."""
    expected = [item["scenario_id"] for item in commitment_manifest["items"]]
    observed = [receipt["scenario_id"] for receipt in scenario_receipts]
    if len(observed) != len(set(observed)):
        raise ValueError("DUPLICATE-SCENARIO-RECEIPT")
    unknown = sorted(set(observed) - set(expected))
    if unknown:
        raise ValueError(f"UNKNOWN-SCENARIO-RECEIPT:{','.join(unknown)}")
    missing = sorted(set(expected) - set(observed))
    extra_summaries = sorted(set(scenario_summaries) - set(observed))
    if extra_summaries:
        raise ValueError(f"SUMMARY-WITHOUT-RECEIPT:{','.join(extra_summaries)}")

    item_rows = []
    for receipt in sorted(scenario_receipts, key=lambda row: row["scenario_id"]):
        scenario_id = receipt["scenario_id"]
        summary = scenario_summaries.get(scenario_id)
        item_rows.append({
            "scenario_id": scenario_id,
            "output_freeze_receipt_sha256": receipt["receipt_sha256"],
            "evaluation_summary_sha256": sha256_json(summary) if summary is not None else None,
        })

    core = {
        "schema": "understanding-run-receipt-v0.1",
        "repository_sha": repository_sha,
        "commitment_manifest_sha256": sha256_json(commitment_manifest),
        "expected_scenario_count": len(expected),
        "observed_scenario_count": len(observed),
        "missing_scenarios": missing,
        "status": "COMPLETE" if not missing and len(scenario_summaries) == len(expected) else "INCOMPLETE_RUN",
        "items": item_rows,
        "aggregate_understanding_score": None,
        "architectural_interpretation": "NOT_COMPUTED_BY_HARNESS",
    }
    return {**core, "receipt_sha256": sha256_json(core)}
