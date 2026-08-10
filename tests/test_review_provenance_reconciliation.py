from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT / "docs" / "governance" / "PR36_REVIEW_PROVENANCE_RECONCILIATION.md"
).read_text(encoding="utf-8")


def test_pr36_review_provenance_is_reconciled_without_runtime_authority() -> None:
    assert "HISTORICAL_REVIEW_LABEL_RECONCILED" in NOTE
    assert "INDEPENDENT_HUMAN_REVIEW_CLAIMED: NO" in NOTE
    assert "PR36_TECHNICAL_FINDINGS_RETAINED: YES" in NOTE
    assert "RUNTIME_AUTHORITY_CREATED: NO" in NOTE
    assert "same operator self-review ≠ independent review" in NOTE
    assert "NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED" in NOTE
    assert "CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION" in NOTE


def test_known_pr36_legacy_surfaces_are_named_explicitly() -> None:
    expected_paths = {
        "docs/MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md",
        "docs/research/MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md",
        "docs/research/GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md",
        "docs/research/MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md",
    }
    for path in expected_paths:
        assert path in NOTE
