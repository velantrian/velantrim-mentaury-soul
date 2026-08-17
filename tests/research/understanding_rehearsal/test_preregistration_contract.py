from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

EXPECTED_SHARED_SHA256 = "65cd3d34c1242c4176e1688fa368bfa45e8998600135814b27e299b12947e0bf"
EXPECTED_PROFILE_SHA256 = {
    "B0": "064c05d2d15b2bea5cb097eee0b77d6013e40d1266f3d348d6ffc80a58c2ca0f",
    "B1": "1478c42f0472abf9e44532d577655fc95aec24018873bfc9b2724d0e6d9a84ab",
    "C1": "6344b7441c9971898182d144dfa5116984f2caa54f4059bd79ea354a236003fe",
}


def _sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _manifest() -> dict:
    return json.loads((HERE / "corpus_commitment_manifest.json").read_text(encoding="utf-8"))


def test_shared_governance_profile_is_frozen() -> None:
    assert _sha(HERE / "shared_governance_profile.txt") == EXPECTED_SHARED_SHA256


def test_arm_profile_hashes_are_frozen() -> None:
    paths = {
        "B0": HERE / "b0_profile.txt",
        "B1": ROOT / "tests/research/understanding_b1/fixtures/b1_instruction_profile.txt",
        "C1": HERE / "c1_profile.txt",
    }
    observed = {arm: _sha(path) for arm, path in paths.items()}
    assert observed == EXPECTED_PROFILE_SHA256


def test_b0_delta_contains_no_structured_cognition_procedure() -> None:
    text = (HERE / "b0_profile.txt").read_text(encoding="utf-8").lower()
    assert "no additional experimental" in text
    for token in ("alternatives", "critical unknowns", "consequences", "probability", "verdict"):
        assert token not in text


def test_commitment_manifest_matches_frozen_profiles() -> None:
    manifest = _manifest()
    assert manifest["schema"] == "understanding-rehearsal-commitment-v0.1"
    assert manifest["mode"] == "RESEARCH_ONLY_OFFLINE"
    assert manifest["confirmatory"] is False
    assert manifest["shared_governance_sha256"] == EXPECTED_SHARED_SHA256
    assert manifest["arm_profile_sha256"] == EXPECTED_PROFILE_SHA256


def test_corpus_split_is_exact_and_unique() -> None:
    manifest = _manifest()
    items = manifest["items"]
    ids = [item["scenario_id"] for item in items]
    assert len(items) == manifest["scenario_count"] == 12
    assert len(ids) == len(set(ids))
    assert sum(item["split"] == "development" for item in items) == manifest["development_count"] == 6
    assert sum(item["split"] == "hidden" for item in items) == manifest["hidden_count"] == 6


def test_all_commitments_are_sha256_hex() -> None:
    manifest = _manifest()
    for item in manifest["items"]:
        for key in ("semantic_input_sha256", "reference_commitment_sha256"):
            value = item[key]
            assert len(value) == 64
            int(value, 16)
    for key in ("owner_custody_bundle_sha256", "canonical_bundle_manifest_sha256", "shared_governance_sha256"):
        value = manifest[key]
        assert len(value) == 64
        int(value, 16)


def test_public_manifest_contains_commitments_not_reference_plaintext() -> None:
    manifest_text = (HERE / "corpus_commitment_manifest.json").read_text(encoding="utf-8").lower()
    forbidden = (
        '"reference_text"',
        '"reference_frame"',
        '"gold_answer"',
        '"expected_answer"',
        '"notes"',
        '"constraints"',
        '"unknowns"',
        '"alternatives"',
    )
    for token in forbidden:
        assert token not in manifest_text


def test_research_artifacts_do_not_claim_confirmatory_authority() -> None:
    doc = (ROOT / "docs/research/UNDERSTANDING_B0_B1_C1_PREREGISTRATION_V0_1.md").read_text(encoding="utf-8")
    assert "Confirmatory interpretation:** BLOCKED" in doc
    assert "rehearsal not executed" in doc
    assert "NO_RUNTIME_AUTHORITY" in doc
