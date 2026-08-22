"""Docs-only guards for the Stage 3A TRL-v0.1 contract freeze."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "research" / "TERMINAL_RECONSIDERATION_LINEAGE_CONTRACT_V0_1.md"
PACKAGE = ROOT / "src" / "mentaury" / "terminal_lineage"


def _text() -> str:
    return CONTRACT.read_text(encoding="utf-8")


def test_trl_contract_exists_and_freezes_exact_version_and_candidate() -> None:
    text = _text()
    assert 'Contract version:                    TRL-v0.1' in text
    assert 'PURE_TERMINAL_SUCCESSOR_LINEAGE_PLANNER' in text
    assert 'Implementation:                      NOT_STARTED' in text
    assert 'Implementation Owner GO:             NOT_GRANTED' in text


def test_trl_contract_preserves_existing_owner_boundaries() -> None:
    text = _text()
    required = (
        'P0-014 authority:                    UNCHANGED',
        'P0-015 Evidence Gate authority:      UNCHANGED',
        'Terminal belief in-place mutation:   FORBIDDEN',
        'Successor creation authority:        NONE',
        'Runtime activation:                  NOT_AUTHORIZED',
    )
    for marker in required:
        assert marker in text


def test_trl_contract_reuses_existing_terminality_rule() -> None:
    text = _text()
    assert 'belief_status_transition_allowed(status, status)' in text
    for status in ('SUPPORTED', 'CONTRADICTED', 'SUPERSEDED'):
        assert status in text


def test_trl_contract_forbids_successor_creation_fields_and_predecessor_mutation() -> None:
    text = _text()
    assert 'successor_belief_id' in text
    assert 'requested BeliefStatus' in text
    assert 'CREATE_BELIEF command' in text
    assert 'A terminal belief is never reopened in place.' in text
    assert 'store append' in text


def test_trl_contract_freeze_creates_no_source_package() -> None:
    assert not PACKAGE.exists()


def test_trl_contract_has_finite_stage3_definition_of_done() -> None:
    text = _text()
    assert '3A CONTRACT FREEZE' in text
    assert '3B BOUNDED IMPLEMENTATION' in text
    assert 'TRL-T01…T16 executable PASS' in text
    assert 'new explicit Owner GO after this contract is\nmerged' in text
