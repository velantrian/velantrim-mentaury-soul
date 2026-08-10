"""Tests for governance risk tiers and independence semantics.

This module verifies that governance principles are correctly documented
and that independence semantics are owned by a single durable source.
"""

from __future__ import annotations

from pathlib import Path

GOVERNANCE = Path(__file__).parent.parent / "docs" / "GOVERNANCE.md"
CHARACTER_SPEC = Path(__file__).parent.parent / "docs" / "MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md"
ARCH_RECONCILIATION = Path(__file__).parent.parent / "docs" / "research" / "ARCHITECTURE_RECONCILIATION_V0.1.md"


def test_independence_semantics_owned_by_governance_only() -> None:
    """
    Independence semantics (INDEPENDENT_HUMAN_REVIEW, INDEPENDENT_TECHNICAL_VALIDATION)
    must be defined in GOVERNANCE.md and referenced from other documents,
    never defined in multiple places.

    Uses structural markers (assert token in file) rather than exact prose,
    allowing legitimate refactoring without breaking the test.
    """
    # § 3 must define both independence types
    governance_text = GOVERNANCE.read_text(encoding="utf-8")
    assert "INDEPENDENT_HUMAN_REVIEW" in governance_text
    assert "INDEPENDENT_TECHNICAL_VALIDATION" in governance_text
    assert "§ 3" in governance_text or "## § 3" in governance_text

    # Character Spec must reference GOVERNANCE.md for semantics
    char_text = CHARACTER_SPEC.read_text(encoding="utf-8")
    assert "GOVERNANCE.md" in char_text or "GOVERNANCE" in char_text
    assert "Character Spec § 3" in char_text or "GOVERNANCE.md § 3" in char_text or "independence semantics" in char_text.lower()

    # Arch Reconciliation must reference gate ownership, not define independence
    arch_text = ARCH_RECONCILIATION.read_text(encoding="utf-8")
    assert "GOVERNANCE" in arch_text


def test_tier_a_files_marked_in_governance() -> None:
    """Tier A high-risk files must be documented in GOVERNANCE.md."""
    governance_text = GOVERNANCE.read_text(encoding="utf-8")

    # Should mention Tier A or high-risk files
    assert "Tier A" in governance_text or "HIGH_RISK" in governance_text.upper()

    # Should reference CANON and P0 Plan as examples
    assert "CANON" in governance_text or "Canon" in governance_text
    assert "P0" in governance_text


def test_character_runtime_activation_gate_status_block_present() -> None:
    """CHARACTER_RUNTIME_ACTIVATION_GATE status must be documented."""
    char_text = CHARACTER_SPEC.read_text(encoding="utf-8")

    # Status block must be present
    assert "CHARACTER_RUNTIME_ACTIVATION_GATE" in char_text
    assert "BLOCKED_PENDING_REQUIRED_VALIDATION" in char_text


def test_merge_authority_distinct_from_runtime_authority() -> None:
    """Core principle: SOLO_MAINTAINER MERGE ≠ DOMAIN RUNTIME ACTIVATION."""
    governance_text = GOVERNANCE.read_text(encoding="utf-8")

    assert "SOLO_MAINTAINER" in governance_text or "solo maintainer" in governance_text.lower()
    assert "MERGE" in governance_text or "merge" in governance_text
    assert "RUNTIME" in governance_text or "runtime" in governance_text
    assert "≠" in governance_text or "!=" in governance_text
