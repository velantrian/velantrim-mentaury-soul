"""Regression guard for final V1 epistemic governance classification."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = ROOT / "docs" / "GOVERNANCE.md"


def test_final_v1_epistemic_surfaces_remain_tier_a() -> None:
    text = GOVERNANCE.read_text(encoding="utf-8")
    protected = text.split(
        "#### Existing protected / high-risk paths", 1
    )[1].split("#### Paths reserved if/when created", 1)[0]

    assert "src/mentaury/claim_belief_binding/**" in protected
    assert "src/mentaury/epistemic_change/**" in protected
