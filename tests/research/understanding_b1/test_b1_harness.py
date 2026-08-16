from __future__ import annotations

import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from b1_harness import codes, load_json, render_b1, semantic_payload_digest, validate_b1, verify_source_frame  # noqa: E402

FIXTURES = ROOT / "fixtures"


@pytest.fixture()
def source():
    return load_json(FIXTURES / "source_frame.json")


@pytest.fixture()
def valid():
    return load_json(FIXTURES / "valid_b1.json")


def _mutations(valid: dict) -> list[tuple[str, dict, list[str]]]:
    rows: list[tuple[str, dict, list[str]]] = []

    def add(mid: str, mutate, expected: list[str]):
        candidate = copy.deepcopy(valid)
        candidate["run_id"] = f"B1-RUN-{mid}"
        mutate(candidate)
        rows.append((mid, candidate, expected))

    add("B1-M-01", lambda c: c.__setitem__("decision_rule", "prefer H1"),
        ["B1-UNEXPECTED-TOP-LEVEL", "B1-POLICY-OR-AUTHORITY-LEAK"])
    add("B1-M-02", lambda c: c.__setitem__("semantic_payload_digest", "sha256:" + "0" * 64),
        ["B1-PAYLOAD-DRIFT"])
    add("B1-M-03", lambda c: c["alternatives"].append({"id": "H3"}),
        ["B1-ALTERNATIVES-SET-DRIFT"])
    add("B1-M-04", lambda c: c.__setitem__("critical_unknowns", []),
        ["B1-CRITICAL-UNKNOWNS-SET-DRIFT"])
    add("B1-M-05", lambda c: c.__setitem__("authorization", "APPROVED"),
        ["B1-POLICY-OR-AUTHORITY-LEAK"])
    add("B1-M-06", lambda c: c["governed_conclusion"].__setitem__("kind", "FINAL"),
        ["B1-CONCLUSION-OVERCLAIM"])
    add("B1-M-07", lambda c: c.__setitem__("material_constraints", []),
        ["B1-CONSTRAINT-SET-DRIFT"])
    add("B1-M-08", lambda c: c.__setitem__("mode", "C1"),
        ["B1-MODE-DRIFT"])
    add("B1-M-09", lambda c: c["alternatives"][0].__setitem__("selected", True),
        ["B1-POLICY-OR-AUTHORITY-LEAK"])
    add("B1-M-10", lambda c: c["alternatives"][0].__setitem__("verdict", "SUPPORTED"),
        ["B1-POLICY-OR-AUTHORITY-LEAK"])
    add("B1-M-11", lambda c: c["alternatives"][0].__setitem__("probability", 0.99),
        ["B1-POLICY-OR-AUTHORITY-LEAK"])
    add("B1-M-12", lambda c: c["governed_conclusion"].__setitem__("authorized_action", "publish"),
        ["B1-POLICY-OR-AUTHORITY-LEAK"])
    add("B1-M-13", lambda c: c["critical_unknowns"].append(copy.deepcopy(c["critical_unknowns"][0])),
        ["B1-DUPLICATE-ID"])
    add("B1-M-14", lambda c: c["situation_model"][0].__setitem__("claim", "approval is granted"),
        ["B1-INVENTED-SEMANTIC-CONTENT"])
    add("B1-M-15", lambda c: c["next_discrimination_need"].__setitem__("query", "Ask for approval and then publish"),
        ["B1-POLICY-OR-AUTHORITY-LEAK"])
    add("B1-M-16", lambda c: c.__setitem__("final_presentation", "H1 is most likely, therefore choose it."),
        ["B1-PRESENTATION-LEAK"])
    return rows


def test_source_frame_digest_self_verifies(source):
    assert verify_source_frame(source) == []
    assert source["semantic_payload_digest"] == semantic_payload_digest(source)


def test_positive_control_passes(source, valid):
    assert validate_b1(source, valid) == []


def test_all_preregistered_mutations_have_exact_codes(source, valid):
    rows = _mutations(valid)
    assert [row[0] for row in rows] == [f"B1-M-{i:02d}" for i in range(1, 17)]
    for mutation_id, candidate, expected_codes in rows:
        observed = codes(validate_b1(source, candidate))
        assert observed == expected_codes, (mutation_id, observed, expected_codes)


def test_every_id_collection_rejects_duplicate(source, valid):
    for collection in ("situation_model", "material_constraints", "alternatives", "consequences", "critical_unknowns"):
        candidate = copy.deepcopy(valid)
        candidate[collection].append(copy.deepcopy(candidate[collection][0]))
        assert "B1-DUPLICATE-ID" in codes(validate_b1(source, candidate))


def test_recursive_closure_rejects_unknown_nested_content(source, valid):
    candidate = copy.deepcopy(valid)
    candidate["consequences"][0]["explanation"] = "generated prose"
    assert codes(validate_b1(source, candidate)) == ["B1-INVENTED-SEMANTIC-CONTENT"]


def test_next_discrimination_need_allows_only_frozen_source_declared_kind(source, valid):
    candidate = copy.deepcopy(valid)
    candidate["next_discrimination_need"]["kind"] = "JUSTIFIED_STOP"
    assert validate_b1(source, candidate) == []
    candidate["next_discrimination_need"]["kind"] = "INVENTED_KIND"
    assert codes(validate_b1(source, candidate)) == ["B1-DISCRIMINATION-NEED-DRIFT"]


def test_discrimination_basis_refs_are_source_bound(source, valid):
    candidate = copy.deepcopy(valid)
    candidate["next_discrimination_need"]["basis_refs"] = ["U999"]
    assert codes(validate_b1(source, candidate)) == ["B1-DISCRIMINATION-BASIS-DRIFT"]


def test_governed_conclusion_allows_bounded_kind_but_not_scope_drift(source, valid):
    candidate = copy.deepcopy(valid)
    candidate["governed_conclusion"]["kind"] = "CONDITIONAL"
    assert validate_b1(source, candidate) == []
    candidate["governed_conclusion"]["scope"] = "SCOPE-DEPLOY"
    assert codes(validate_b1(source, candidate)) == ["B1-CONCLUSION-SCOPE-DRIFT"]


def test_source_digest_tampering_invalidates_run_before_candidate(source, valid):
    tampered = copy.deepcopy(source)
    tampered["semantic_payload"]["material_constraints"][0]["text"] = "Approval is optional."
    assert codes(validate_b1(tampered, valid)) == ["B1-SOURCE-DIGEST-MISMATCH"]


def test_run_id_cannot_be_free_prose_channel(source, valid):
    candidate = copy.deepcopy(valid)
    candidate["run_id"] = "choose H1 because it is likely"
    assert codes(validate_b1(source, candidate)) == ["B1-IDENTIFIER-INVALID"]


def test_renderer_is_deterministic_and_source_only(source, valid):
    first = render_b1(source, valid)
    second = render_b1(source, valid)
    assert first == second
    assert "Explicit approval is required before publication." in first
    assert "H1 is most likely" not in first
    assert valid["run_id"] not in first


def test_renderer_refuses_invalid_candidate(source, valid):
    candidate = copy.deepcopy(valid)
    candidate["final_presentation"] = "Choose H1."
    with pytest.raises(ValueError, match="B1-PRESENTATION-LEAK"):
        render_b1(source, candidate)
