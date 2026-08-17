from __future__ import annotations

from hashlib import sha256
import json
import re
from typing import Any

ARM_IDS = ("B0", "B1", "C1")
FORBIDDEN_MODEL_INPUT_KEYS = {
    "situation_model",
    "material_constraints",
    "alternatives",
    "consequences",
    "critical_unknowns",
    "allowed_discrimination_kinds",
    "governed_conclusion_scope",
    "reference_frame",
    "gold",
    "label",
    "verdict",
    "selected",
    "probability",
}


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def semantic_input_digest(model_input: dict[str, Any]) -> str:
    return "sha256:" + sha256(canonical_json(model_input)).hexdigest()


def _neutral_atom_id(value: str) -> bool:
    return re.fullmatch(r"A[1-9][0-9]{0,3}", value) is not None


def verify_neutral_model_input(model_input: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(model_input, dict) or set(model_input) != {"scenario_id", "atoms"}:
        return ["INPUT-SHAPE"]

    if not isinstance(model_input["scenario_id"], str) or not model_input["scenario_id"]:
        errors.append("INPUT-SCENARIO-ID")

    atoms = model_input.get("atoms")
    if not isinstance(atoms, list) or not atoms:
        return errors + ["INPUT-ATOMS"]

    seen: set[str] = set()
    for idx, atom in enumerate(atoms):
        if not isinstance(atom, dict) or set(atom) != {"id", "text"}:
            errors.append(f"INPUT-ATOM-SHAPE:{idx}")
            continue

        atom_id = atom.get("id")
        if not isinstance(atom_id, str) or not _neutral_atom_id(atom_id):
            errors.append(f"INPUT-ATOM-ID:{idx}")
        elif atom_id in seen:
            errors.append("INPUT-DUPLICATE-ID")
        seen.add(atom_id)

        if not isinstance(atom.get("text"), str) or not atom["text"].strip():
            errors.append(f"INPUT-ATOM-TEXT:{idx}")

        for key in atom:
            if key in FORBIDDEN_MODEL_INPUT_KEYS:
                errors.append(f"INPUT-ROLE-LEAK:{idx}:{key}")

    for key in model_input:
        if key in FORBIDDEN_MODEL_INPUT_KEYS:
            errors.append(f"INPUT-ROLE-LEAK:{key}")

    return errors


def build_arm_packet(model_input: dict[str, Any], arm: str) -> dict[str, Any]:
    if arm not in ARM_IDS:
        raise ValueError("unknown arm")
    errors = verify_neutral_model_input(model_input)
    if errors:
        raise ValueError(",".join(errors))
    return {
        "arm": arm,
        "semantic_input_digest": semantic_input_digest(model_input),
        "model_input": json.loads(json.dumps(model_input)),
    }


def semantic_projection(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "semantic_input_digest": packet["semantic_input_digest"],
        "model_input": packet["model_input"],
    }


def assert_input_symmetry(packets: list[dict[str, Any]]) -> None:
    if {packet.get("arm") for packet in packets} != set(ARM_IDS):
        raise ValueError("INPUT-ARMS")
    projections = [canonical_json(semantic_projection(packet)) for packet in packets]
    if len(set(projections)) != 1:
        raise ValueError("INPUT-SYMMETRY-DRIFT")
