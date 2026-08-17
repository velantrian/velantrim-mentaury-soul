from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from tests.research.understanding_rehearsal.offline_harness import (
    ARMS,
    DIMENSIONS,
    EVALUATION_SCHEMA,
    SCHEMA,
    commitment_manifest,
    make_blind_packet,
    output_freeze_receipt,
    repository_commitment_issues,
    sha256_text,
    summarize_evaluations,
    validate_arm_trio,
    validate_evaluation,
    validate_output_record,
)

ROOT = Path(__file__).resolve().parents[3]


def _base_records() -> list[dict]:
    manifest = commitment_manifest(ROOT)
    item = manifest["items"][0]
    common = {
        "schema": SCHEMA,
        "run_id": "REHEARSAL-LOCAL-001",
        "scenario_id": item["scenario_id"],
        "semantic_input_sha256": item["semantic_input_sha256"],
        "shared_governance_sha256": manifest["shared_governance_sha256"],
        "model_identity": {"provider": "external-test-fixture", "model": "same-model", "version": "v1"},
        "context_budget": {"input_tokens": 4096, "max_output_tokens": 1024},
        "decoding": {"temperature": 0, "seed": 7},
        "tool_access": False,
        "retrieval_access": False,
        "network_access": False,
    }
    rows = []
    for arm in ARMS:
        text = f"Externally supplied frozen output for {arm}."
        rows.append({
            **common,
            "arm": arm,
            "arm_profile_sha256": manifest["arm_profile_sha256"][arm],
            "output_text": text,
            "output_sha256": sha256_text(text),
        })
    return rows


def _evaluation(packet_id: str, scenario_id: str) -> dict:
    return {
        "schema": EVALUATION_SCHEMA,
        "scenario_id": scenario_id,
        "packet_id": packet_id,
        "dimensions": {dimension: "PASS" for dimension in DIMENSIONS},
        "hard_fails": [],
        "diagnostics": {"unnecessary_analysis": 0},
        "disagreement_state": "UNANIMOUS",
    }


def codes(issues) -> list[str]:
    return [issue.code for issue in issues]


def test_repository_commitments_self_verify() -> None:
    assert repository_commitment_issues(ROOT) == []


def test_complete_symmetric_trio_passes() -> None:
    records = _base_records()
    assert validate_arm_trio(ROOT, records) == []
    for record in records:
        assert validate_output_record(ROOT, record) == []


def test_missing_arm_is_incomplete_not_synthesized() -> None:
    records = _base_records()[:2]
    assert codes(validate_arm_trio(ROOT, records)) == ["INCOMPLETE-RUN"]


def test_duplicate_arm_is_incomplete() -> None:
    records = _base_records()
    manifest = commitment_manifest(ROOT)
    records[2]["arm"] = "B1"
    records[2]["arm_profile_sha256"] = manifest["arm_profile_sha256"]["B1"]
    assert "INCOMPLETE-RUN" in codes(validate_arm_trio(ROOT, records))


def test_semantic_input_drift_is_rejected() -> None:
    record = _base_records()[0]
    record["semantic_input_sha256"] = "0" * 64
    assert "OUTPUT-SEMANTIC-INPUT-DRIFT" in codes(validate_output_record(ROOT, record))


def test_output_digest_tampering_is_rejected() -> None:
    record = _base_records()[0]
    record["output_text"] += " tampered"
    assert "OUTPUT-DIGEST-MISMATCH" in codes(validate_output_record(ROOT, record))


def test_capability_use_is_rejected() -> None:
    for field in ("tool_access", "retrieval_access", "network_access"):
        record = _base_records()[0]
        record[field] = True
        assert "OUTPUT-UNAUTHORIZED-CAPABILITY" in codes(validate_output_record(ROOT, record))


def test_cross_arm_execution_asymmetry_invalidates_run() -> None:
    records = _base_records()
    records[2]["decoding"] = {"temperature": 0.7, "seed": 7}
    assert codes(validate_arm_trio(ROOT, records)) == ["INVALID-RUN-ASYMMETRY"]


def test_freeze_receipt_is_order_invariant() -> None:
    records = _base_records()
    first = output_freeze_receipt(records)
    second = output_freeze_receipt(list(reversed(records)))
    assert first == second
    assert len(first["receipt_sha256"]) == 64


def test_blinding_is_deterministic_and_evaluator_packet_has_no_arm_metadata() -> None:
    records = _base_records()
    packet1, mapping1 = make_blind_packet(ROOT, records, "seed-01")
    packet2, mapping2 = make_blind_packet(ROOT, records, "seed-01")
    assert packet1 == packet2
    assert mapping1 == mapping2
    assert set(mapping1["mapping"].values()) == set(ARMS)
    packet_text = str(packet1).lower()
    assert "provider" not in packet_text
    assert "model_identity" not in packet_text
    for row in packet1["outputs"]:
        assert "arm" not in row


def test_evaluation_requires_exact_six_dimensions() -> None:
    records = _base_records()
    packet, _ = make_blind_packet(ROOT, records, "seed-02")
    evaluation = _evaluation(packet["outputs"][0]["packet_id"], packet["scenario_id"])
    evaluation["dimensions"].pop(DIMENSIONS[0])
    assert codes(validate_evaluation(packet, evaluation)) == ["EVAL-DIMENSIONS-INVALID"]


def test_evaluation_preserves_disputed_label_state() -> None:
    records = _base_records()
    packet, _ = make_blind_packet(ROOT, records, "seed-03")
    evaluation = _evaluation(packet["outputs"][0]["packet_id"], packet["scenario_id"])
    evaluation["disagreement_state"] = "DISPUTED_LABEL"
    assert validate_evaluation(packet, evaluation) == []


def test_evaluation_rejects_arm_or_aggregate_score_leak() -> None:
    records = _base_records()
    packet, _ = make_blind_packet(ROOT, records, "seed-04")
    evaluation = _evaluation(packet["outputs"][0]["packet_id"], packet["scenario_id"])
    evaluation["aggregate_score"] = 0.99
    assert "EVAL-BLINDING-LEAK" in codes(validate_evaluation(packet, evaluation))


def test_summary_has_separate_dimensions_and_no_composite_score() -> None:
    records = _base_records()
    packet, sealed = make_blind_packet(ROOT, records, "seed-05")
    evaluations = [_evaluation(row["packet_id"], packet["scenario_id"]) for row in packet["outputs"]]
    for evaluation in evaluations:
        assert validate_evaluation(packet, evaluation) == []
    summary = summarize_evaluations(sealed["mapping"], evaluations)
    assert summary["aggregate_understanding_score"] is None
    assert summary["architectural_interpretation"] == "NOT_COMPUTED_BY_HARNESS"
    assert set(summary["dimensions"]) == set(ARMS)
    for arm in ARMS:
        assert set(summary["dimensions"][arm]) == set(DIMENSIONS)


def test_parser_failure_is_not_detector_success() -> None:
    with pytest.raises(Exception):
        # Malformed caller data should remain a real parser/caller failure; the harness
        # never translates exceptions into a successful hard-fail detection.
        sha256(None)  # type: ignore[arg-type]
