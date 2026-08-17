from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PROFILE = ROOT / "fixtures" / "b1_instruction_profile.txt"
EXPECTED_SHA256 = "1478c42f0472abf9e44532d577655fc95aec24018873bfc9b2724d0e6d9a84ab"


def test_instruction_profile_is_frozen_by_hash():
    data = PROFILE.read_bytes()
    assert sha256(data).hexdigest() == EXPECTED_SHA256


def test_instruction_profile_has_no_positive_decision_heuristic():
    text = PROFILE.read_text().lower()
    forbidden_positive_patterns = (
        r"\bprefer\s+h[0-9]",
        r"\bchoose\s+h[0-9]",
        r"\bselect\s+h[0-9]",
        r"\bmost\s+likely\b",
        r"\bassign\s+probability\b",
        r"\bif\s+.*\bthen\s+(?:choose|select|prefer|publish|act)\b",
        r"\brecommend\s+(?:h[0-9]|publish|act)\b",
        r"\bauthorize\s+(?:publish|action|tool|retrieval)\b",
    )
    for pattern in forbidden_positive_patterns:
        assert re.search(pattern, text) is None, pattern


def test_instruction_profile_explicitly_denies_authority_channels():
    text = PROFILE.read_text().lower()
    for required in (
        "do not add facts",
        "do not select a preferred alternative",
        "do not infer or assert supported",
        "do not output final",
        "do not invent content",
    ):
        assert required in text
