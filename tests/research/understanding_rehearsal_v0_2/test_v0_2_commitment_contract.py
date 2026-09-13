from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "public_commitment_manifest.json"

EXPECTED_SHARED = "65cd3d34c1242c4176e1688fa368bfa45e8998600135814b27e299b12947e0bf"
EXPECTED_ARMS = {
    "B0": "064c05d2d15b2bea5cb097eee0b77d6013e40d1266f3d348d6ffc80a58c2ca0f",
    "B1": "1478c42f0472abf9e44532d577655fc95aec24018873bfc9b2724d0e6d9a84ab",
    "C1": "6344b7441c9971898182d144dfa5116984f2caa54f4059bd79ea354a236003fe",
}
EXPECTED_BUNDLE = "6d9a84bccb5272479ff5a21089c1cb9ba5a1d3261761240a3a6820b157fe89e7"
EXPECTED_PRIVATE_MANIFEST = "658f2b38485f9266e8e5647e564b84b96f955598bb8dc3dc7d50d7f55a9e7cdd"
EXPECTED_PACKAGE = "f6b73a6508ca96c85e1d8ac0678796d5909265ba6d0d2ad95553071a2c1f3d24"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_v0_2_identity_and_counts() -> None:
    manifest = load_manifest()
    assert manifest["schema"] == "understanding-rehearsal-commitment-v0.2"
    assert manifest["experiment_version"] == "0.2"
    assert manifest["canonicalization"] == "mentaury-canonical-json-v0.2"
    assert manifest["scenario_count"] == 12
    assert manifest["development_count"] == 6
    assert manifest["hidden_count"] == 6
    assert len(manifest["items"]) == 12
    assert len({item["scenario_id"] for item in manifest["items"]}) == 12
    assert [item["scenario_id"] for item in manifest["items"][:6]] == [f"V02-DEV-0{i}" for i in range(1, 7)]
    assert [item["scenario_id"] for item in manifest["items"][6:]] == [f"V02-HID-0{i}" for i in range(1, 7)]


def test_v0_2_profile_bindings_still_match_landed_bytes() -> None:
    manifest = load_manifest()
    shared = ROOT / "tests/research/understanding_rehearsal/shared_governance_profile.txt"
    arm_paths = {
        "B0": ROOT / "tests/research/understanding_rehearsal/b0_profile.txt",
        "B1": ROOT / "tests/research/understanding_b1/fixtures/b1_instruction_profile.txt",
        "C1": ROOT / "tests/research/understanding_rehearsal/c1_profile.txt",
    }
    assert digest(shared) == EXPECTED_SHARED == manifest["shared_governance_sha256"]
    for arm, path in arm_paths.items():
        assert digest(path) == EXPECTED_ARMS[arm] == manifest["arm_profile_sha256"][arm]


def test_v0_2_private_commitments_are_new_and_recoverable() -> None:
    manifest = load_manifest()
    assert manifest["private_bundle_sha256"] == EXPECTED_BUNDLE
    assert manifest["private_manifest_sha256"] == EXPECTED_PRIVATE_MANIFEST
    assert manifest["custody_package_sha256"] == EXPECTED_PACKAGE
    assert manifest["custody_recovery_test"] == "PASS"
    assert manifest["provider_calls"] == 0
    assert manifest["execution_authority"] == "NOT_GRANTED"
    assert manifest["independent_human_semantic_validation"] == "ABSENT"
    assert EXPECTED_BUNDLE != "ec34fdcfcdb545acf5f903d08a3113364f47e2742aefd7c8e59357336e244805"
    assert EXPECTED_PRIVATE_MANIFEST != "5ad0036a0ea086241df87a10cb9ee85be9d04b7036a6f6f1920dad635c6bdeaa"


def test_v0_2_public_manifest_contains_commitments_not_private_plaintext() -> None:
    manifest = load_manifest()
    forbidden_keys = {
        "model_input",
        "evaluator_reference",
        "material_constraints",
        "meaningful_alternatives",
        "consequences",
        "critical_unknowns",
        "expected_behavior",
        "evaluator_rationale",
        "gold_answer",
        "gold_rationale",
    }

    def walk(value):
        if isinstance(value, dict):
            assert forbidden_keys.isdisjoint(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(manifest)
    for item in manifest["items"]:
        assert len(item["semantic_input_sha256"]) == 64
        assert len(item["reference_commitment_sha256"]) == 64


def test_v0_2_preregistration_preserves_authority_ceiling() -> None:
    text = (ROOT / "docs/research/UNDERSTANDING_B0_B1_C1_PREREGISTRATION_V0_2.md").read_text(encoding="utf-8")
    required = [
        "RECOVERABILITY BEFORE EXECUTABILITY",
        "CUSTODY_RECOVERY_TEST = PASS",
        "PROVIDER_CALLS = 0",
        "EXECUTION_AUTHORITY = NOT_GRANTED",
        "OWNER_GO_EXPLORATORY_OUTPUT_ACQUISITION_V0_2",
        "POSSIBLE_COGNITIVE_POLICY_GAP",
        "B1 - B0 = neutral structure / elicitation effect",
        "C1 - B1 = candidate cognition-policy effect",
    ]
    for marker in required:
        assert marker in text
    assert "UNDERSTANDING_PROVEN" not in text
