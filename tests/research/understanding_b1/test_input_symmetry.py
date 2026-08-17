from __future__ import annotations

import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from input_symmetry import (  # noqa: E402
    assert_input_symmetry,
    build_arm_packet,
    semantic_input_digest,
    verify_neutral_model_input,
)


def load(name: str):
    return json.loads((ROOT / "fixtures" / name).read_text())


def test_model_input_is_role_neutral():
    model_input = load("model_input.json")
    assert verify_neutral_model_input(model_input) == []
    assert set(model_input) == {"scenario_id", "atoms"}
    assert all(set(atom) == {"id", "text"} for atom in model_input["atoms"])


def test_b0_b1_c1_receive_identical_semantic_input():
    model_input = load("model_input.json")
    packets = [build_arm_packet(model_input, arm) for arm in ("B0", "B1", "C1")]
    assert_input_symmetry(packets)
    assert {packet["semantic_input_digest"] for packet in packets} == {
        semantic_input_digest(model_input)
    }


def test_reference_labels_are_not_model_facing():
    model_input = load("model_input.json")
    source = load("source_frame.json")
    serialized = json.dumps(model_input, sort_keys=True)
    for forbidden in (
        "situation_model",
        "material_constraints",
        "alternatives",
        "consequences",
        "critical_unknowns",
        "allowed_discrimination_kinds",
        "governed_conclusion_scope",
    ):
        assert forbidden not in serialized
    source_ids = {
        item["id"]
        for name in (
            "situation_model",
            "material_constraints",
            "alternatives",
            "consequences",
            "critical_unknowns",
        )
        for item in source["semantic_payload"][name]
    }
    assert source_ids == {atom["id"] for atom in model_input["atoms"]}


def test_role_leak_is_rejected():
    model_input = load("model_input.json")
    bad = copy.deepcopy(model_input)
    bad["material_constraints"] = ["A2"]
    assert verify_neutral_model_input(bad) == ["INPUT-SHAPE"]


def test_semantic_drift_across_arms_invalidates_run():
    model_input = load("model_input.json")
    packets = [build_arm_packet(model_input, arm) for arm in ("B0", "B1", "C1")]
    packets[1]["model_input"]["atoms"][1]["text"] = "Approval is optional."
    with pytest.raises(ValueError, match="INPUT-SYMMETRY-DRIFT"):
        assert_input_symmetry(packets)
