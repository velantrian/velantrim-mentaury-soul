"""P1-002 privacy classifier contract, scenario, and adversarial tests."""

from __future__ import annotations

import dataclasses
import os
import subprocess
import sys
from pathlib import Path

import pytest

from mentaury.contracts import canonical_json_bytes
from mentaury.privacy.reconciliation import (
    PrivacyAccessIntent,
    PrivacyContractError,
    PrivacyCopy,
    PrivacyDecision,
    PrivacyMaterial,
    PrivacyReason,
    PrivacyReconciliationBudget,
    PrivacyReconciliationResult,
    classify_privacy_reconciliation,
)

ROOT = Path(__file__).resolve().parents[1]
MATERIAL_ID = "MAT-TEST-001"
COPY_ID = "COPY-TEST-001"
BRANCH_ID = "branch:main"
PURPOSE = "research"


def _material(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "material_id": MATERIAL_ID,
        "privacy_class": "PERSONAL",
        "state": "ACTIVE",
        "policy_revision": 1,
        "permitted_purposes": [PURPOSE],
        "withdrawn_purposes": [],
        "permitted_branches": [BRANCH_ID],
        "third_party_permission": False,
    }
    value.update(changes)
    return value


def _copy(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "copy_id": COPY_ID,
        "material_id": MATERIAL_ID,
        "branch_id": BRANCH_ID,
        "surface": "PRIMARY",
        "policy_revision": 1,
        "state": "PRESENT",
        "contains_material": True,
    }
    value.update(changes)
    return value


def _intent(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "copy_id": COPY_ID,
        "branch_id": BRANCH_ID,
        "purpose": PURPOSE,
    }
    value.update(changes)
    return value


def _budget(**changes: object) -> dict[str, int]:
    value = {
        "max_serialized_bytes": 16_384,
        "max_purposes": 64,
        "max_branches": 64,
    }
    value.update(changes)
    return value


def _classify(
    *,
    material: object | None = None,
    copy: object | None = None,
    intent: object | None = None,
    budget: object | None = None,
) -> PrivacyReconciliationResult:
    return classify_privacy_reconciliation(
        _material() if material is None else material,
        _copy() if copy is None else copy,
        _intent() if intent is None else intent,
        _budget() if budget is None else budget,
    )


def _outcome(**kwargs: object) -> tuple[PrivacyDecision, PrivacyReason]:
    result = _classify(**kwargs)
    return result.decision, result.reason


@pytest.mark.parametrize(
    ("scenario", "material", "copy", "intent", "budget", "expected"),
    [
        (
            "PRIV-SC-001",
            _material(state="DELETED"),
            _copy(surface="BACKUP"),
            _intent(),
            _budget(),
            (
                PrivacyDecision.QUARANTINE_REQUIRED,
                PrivacyReason.DELETED_OR_REDACTED_MATERIAL,
            ),
        ),
        (
            "PRIV-SC-002",
            _material(privacy_class="THIRD_PARTY"),
            _copy(),
            _intent(),
            _budget(),
            (
                PrivacyDecision.DENY_RETRIEVAL,
                PrivacyReason.THIRD_PARTY_PERMISSION_MISSING,
            ),
        ),
        (
            "PRIV-SC-003",
            _material(permitted_purposes=[], withdrawn_purposes=[PURPOSE]),
            _copy(surface="FORK"),
            _intent(),
            _budget(),
            (
                PrivacyDecision.QUARANTINE_REQUIRED,
                PrivacyReason.PURPOSE_WITHDRAWN,
            ),
        ),
        (
            "PRIV-SC-004",
            _material(privacy_class="REDACTED", state="REDACTED"),
            _copy(surface="DERIVED_SUMMARY"),
            _intent(),
            _budget(),
            (
                PrivacyDecision.REBUILD_REQUIRED,
                PrivacyReason.DELETED_OR_REDACTED_MATERIAL,
            ),
        ),
        (
            "PRIV-SC-005",
            _material(),
            _copy(),
            _intent(),
            _budget(),
            (PrivacyDecision.ALLOW_REFERENCE, PrivacyReason.ALLOW_REFERENCE),
        ),
        (
            "PRIV-SC-006",
            _material(policy_revision=2),
            _copy(policy_revision=1),
            _intent(),
            _budget(),
            (
                PrivacyDecision.DENY_RETRIEVAL,
                PrivacyReason.STALE_POLICY_REVISION,
            ),
        ),
        (
            "PRIV-SC-007",
            _material(policy_revision=2),
            _copy(policy_revision=1, surface="INDEX"),
            _intent(),
            _budget(),
            (
                PrivacyDecision.REBUILD_REQUIRED,
                PrivacyReason.STALE_POLICY_REVISION,
            ),
        ),
        (
            "PRIV-SC-009",
            _material(),
            _copy(state="ABSENT", contains_material=False),
            _intent(),
            _budget(),
            (PrivacyDecision.DENY_RETRIEVAL, PrivacyReason.COPY_ABSENT),
        ),
        (
            "PRIV-SC-010",
            _material(),
            _copy(state="QUARANTINED"),
            _intent(),
            _budget(),
            (
                PrivacyDecision.QUARANTINE_REQUIRED,
                PrivacyReason.COPY_ALREADY_QUARANTINED,
            ),
        ),
        (
            "PRIV-SC-011",
            _material(),
            _copy(),
            _intent(),
            _budget(max_serialized_bytes=1),
            (
                PrivacyDecision.DENY_RETRIEVAL,
                PrivacyReason.BUDGET_EXHAUSTED,
            ),
        ),
        (
            "PRIV-SC-012",
            _material(),
            _copy(branch_id="branch:fork", surface="FORK"),
            _intent(branch_id="branch:fork"),
            _budget(),
            (
                PrivacyDecision.QUARANTINE_REQUIRED,
                PrivacyReason.BRANCH_NOT_PERMITTED,
            ),
        ),
    ],
    ids=lambda value: value if isinstance(value, str) and value.startswith("PRIV-") else None,
)
def test_frozen_semantic_scenarios(
    scenario: str,
    material: object,
    copy: object,
    intent: object,
    budget: object,
    expected: tuple[PrivacyDecision, PrivacyReason],
) -> None:
    assert scenario.startswith("PRIV-SC-")
    assert _outcome(
        material=material, copy=copy, intent=intent, budget=budget
    ) == expected


def test_priv_sc_008_copy_links_to_another_material() -> None:
    with pytest.raises(PrivacyContractError, match="material_id"):
        _classify(copy=_copy(material_id="MAT-OTHER"))


def test_priv_sc_013_mapping_contains_unknown_field() -> None:
    material = _material()
    material["unexpected_authority"] = True
    with pytest.raises(PrivacyContractError, match="unknown fields"):
        _classify(material=material)


def test_priv_sc_014_unrelated_additional_permitted_purpose_is_invariant() -> None:
    baseline = _classify()
    expanded = _classify(
        material=_material(permitted_purposes=["archive", PURPOSE])
    )
    assert expanded == baseline


def test_priv_sc_015_copy_policy_revision_ahead_of_material() -> None:
    with pytest.raises(PrivacyContractError, match="cannot be ahead"):
        _classify(copy=_copy(policy_revision=2))


@pytest.mark.parametrize(
    ("material", "copy", "intent", "budget", "reason"),
    [
        (
            _material(state="DELETED"),
            _copy(state="ABSENT", contains_material=False),
            _intent(),
            _budget(max_serialized_bytes=1),
            PrivacyReason.BUDGET_EXHAUSTED,
        ),
        (
            _material(state="DELETED"),
            _copy(state="ABSENT", contains_material=False),
            _intent(),
            _budget(),
            PrivacyReason.COPY_ABSENT,
        ),
        (
            _material(state="DELETED"),
            _copy(state="QUARANTINED"),
            _intent(),
            _budget(),
            PrivacyReason.COPY_ALREADY_QUARANTINED,
        ),
        (
            _material(
                privacy_class="THIRD_PARTY",
                state="DELETED",
                permitted_purposes=[],
                withdrawn_purposes=[PURPOSE],
            ),
            _copy(),
            _intent(),
            _budget(),
            PrivacyReason.DELETED_OR_REDACTED_MATERIAL,
        ),
        (
            _material(
                privacy_class="THIRD_PARTY",
                permitted_purposes=[],
                withdrawn_purposes=[PURPOSE],
            ),
            _copy(),
            _intent(),
            _budget(),
            PrivacyReason.THIRD_PARTY_PERMISSION_MISSING,
        ),
        (
            _material(permitted_purposes=[], withdrawn_purposes=[PURPOSE]),
            _copy(branch_id="branch:other"),
            _intent(branch_id="branch:other"),
            _budget(),
            PrivacyReason.PURPOSE_WITHDRAWN,
        ),
        (
            _material(policy_revision=2, permitted_purposes=["archive"]),
            _copy(policy_revision=1, branch_id="branch:other"),
            _intent(branch_id="branch:other"),
            _budget(),
            PrivacyReason.PURPOSE_NOT_PERMITTED,
        ),
        (
            _material(policy_revision=2),
            _copy(policy_revision=1, branch_id="branch:other"),
            _intent(branch_id="branch:other"),
            _budget(),
            PrivacyReason.BRANCH_NOT_PERMITTED,
        ),
    ],
)
def test_normative_first_match_precedence(
    material: object,
    copy: object,
    intent: object,
    budget: object,
    reason: PrivacyReason,
) -> None:
    assert _classify(
        material=material, copy=copy, intent=intent, budget=budget
    ).reason is reason


@pytest.mark.parametrize(
    ("surface", "decision"),
    [
        ("BACKUP", PrivacyDecision.QUARANTINE_REQUIRED),
        ("FORK", PrivacyDecision.QUARANTINE_REQUIRED),
        ("INDEX", PrivacyDecision.REBUILD_REQUIRED),
        ("EMBEDDING", PrivacyDecision.REBUILD_REQUIRED),
        ("GRAPH_EDGE", PrivacyDecision.REBUILD_REQUIRED),
        ("CACHE", PrivacyDecision.REBUILD_REQUIRED),
        ("DERIVED_SUMMARY", PrivacyDecision.REBUILD_REQUIRED),
        ("PRIMARY", PrivacyDecision.DENY_RETRIEVAL),
    ],
)
def test_surface_specific_remediation_mapping(
    surface: str, decision: PrivacyDecision
) -> None:
    result = _classify(
        material=_material(state="DELETED"), copy=_copy(surface=surface)
    )
    assert result.decision is decision
    assert result.reason is PrivacyReason.DELETED_OR_REDACTED_MATERIAL


def test_typed_and_mapping_inputs_are_byte_equivalent() -> None:
    typed = classify_privacy_reconciliation(
        PrivacyMaterial.from_value(_material()),
        PrivacyCopy.from_value(_copy()),
        PrivacyAccessIntent.from_value(_intent()),
        PrivacyReconciliationBudget.from_value(_budget()),
    )
    mapped = _classify()
    assert canonical_json_bytes(typed.to_value()) == canonical_json_bytes(
        mapped.to_value()
    )


def test_repeatability_is_deterministic() -> None:
    first = _classify()
    first_bytes = canonical_json_bytes(first.to_value())
    for _ in range(20):
        current = _classify()
        assert current == first
        assert canonical_json_bytes(current.to_value()) == first_bytes


@pytest.mark.parametrize(
    "material",
    [
        _material(policy_revision=True),
        _material(privacy_class="UNKNOWN"),
        _material(permitted_purposes=[PURPOSE, PURPOSE]),
        _material(permitted_purposes=[PURPOSE, "archive"]),
        _material(permitted_purposes=[PURPOSE], withdrawn_purposes=[PURPOSE]),
        _material(third_party_permission="yes"),
        _material(material_id=" padded "),
    ],
)
def test_material_admission_rejects_wrong_or_noncanonical_values(
    material: object,
) -> None:
    with pytest.raises(PrivacyContractError):
        _classify(material=material)


@pytest.mark.parametrize(
    ("copy", "intent", "budget"),
    [
        (_copy(policy_revision=True), _intent(), _budget()),
        (_copy(contains_material="yes"), _intent(), _budget()),
        (_copy(surface="UNKNOWN"), _intent(), _budget()),
        (_copy(), _intent(purpose=" "), _budget()),
        (_copy(), _intent(), _budget(max_purposes=True)),
        (_copy(), _intent(), {**_budget(), "unknown": 1}),
    ],
)
def test_other_contracts_reject_wrong_types_and_unknown_fields(
    copy: object, intent: object, budget: object
) -> None:
    with pytest.raises(PrivacyContractError):
        _classify(copy=copy, intent=intent, budget=budget)


@pytest.mark.parametrize(
    ("material", "copy"),
    [
        (_material(policy_revision=2**60), _copy()),
        (
            _material(material_id=chr(0xD800)),
            _copy(material_id=chr(0xD800)),
        ),
    ],
)
def test_noncanonical_json_values_become_contract_violations(
    material: object, copy: object
) -> None:
    with pytest.raises(PrivacyContractError, match="canonical JSON"):
        _classify(material=material, copy=copy)


def test_linkage_is_checked_before_budget() -> None:
    with pytest.raises(PrivacyContractError, match="intent.copy_id"):
        _classify(
            intent=_intent(copy_id="COPY-OTHER"),
            budget=_budget(max_serialized_bytes=1),
        )


def test_purpose_and_branch_collection_budgets_fail_closed() -> None:
    purpose = _classify(
        material=_material(permitted_purposes=["archive", PURPOSE]),
        budget=_budget(max_purposes=1),
    )
    branch = _classify(
        material=_material(permitted_branches=[BRANCH_ID, "branch:secondary"]),
        budget=_budget(max_branches=1),
    )
    assert purpose.reason is PrivacyReason.BUDGET_EXHAUSTED
    assert branch.reason is PrivacyReason.BUDGET_EXHAUSTED


def test_empty_allowlists_grant_nothing_even_for_public_material() -> None:
    result = _classify(
        material=_material(
            privacy_class="PUBLIC",
            permitted_purposes=[],
            permitted_branches=[],
        )
    )
    assert result.decision is PrivacyDecision.DENY_RETRIEVAL
    assert result.reason is PrivacyReason.PURPOSE_NOT_PERMITTED


def test_public_material_with_exact_allowlists_can_be_referenced() -> None:
    result = _classify(material=_material(privacy_class="PUBLIC"))
    assert result.decision is PrivacyDecision.ALLOW_REFERENCE
    assert result.reason is PrivacyReason.ALLOW_REFERENCE


def test_restricted_material_requires_exact_purpose_and_branch() -> None:
    missing_purpose = _classify(
        material=_material(
            privacy_class="RESTRICTED",
            state="RESTRICTED",
            permitted_purposes=[],
            permitted_branches=[],
        )
    )
    assert missing_purpose.reason is PrivacyReason.PURPOSE_NOT_PERMITTED

    missing_branch = _classify(
        material=_material(
            privacy_class="RESTRICTED",
            state="RESTRICTED",
            permitted_purposes=[PURPOSE],
            permitted_branches=[],
        )
    )
    assert missing_branch.reason is PrivacyReason.BRANCH_NOT_PERMITTED


def test_third_party_permission_does_not_bypass_purpose_policy() -> None:
    result = _classify(
        material=_material(
            privacy_class="THIRD_PARTY",
            third_party_permission=True,
            permitted_purposes=["archive"],
        )
    )
    assert result.reason is PrivacyReason.PURPOSE_NOT_PERMITTED


def test_result_is_exactly_two_fields_without_permission_material() -> None:
    result = _classify()
    assert tuple(field.name for field in dataclasses.fields(result)) == (
        "decision",
        "reason",
    )
    value = result.to_value()
    assert set(value) == {"decision", "reason"}
    assert {
        "material_id",
        "copy_id",
        "purpose",
        "branch_id",
        "capability",
        "token",
        "permission",
        "mutation",
        "instructions",
    }.isdisjoint(value)


def test_result_and_typed_inputs_are_immutable() -> None:
    material = PrivacyMaterial.from_value(_material())
    result = _classify(material=material)
    with pytest.raises(dataclasses.FrozenInstanceError):
        material.policy_revision = 2
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.reason = PrivacyReason.BUDGET_EXHAUSTED


@pytest.mark.parametrize(
    ("decision", "reason"),
    [
        (
            PrivacyDecision.ALLOW_REFERENCE,
            PrivacyReason.PURPOSE_NOT_PERMITTED,
        ),
        (
            PrivacyDecision.DENY_RETRIEVAL,
            PrivacyReason.ALLOW_REFERENCE,
        ),
        (
            PrivacyDecision.QUARANTINE_REQUIRED,
            PrivacyReason.BUDGET_EXHAUSTED,
        ),
        (
            PrivacyDecision.REBUILD_REQUIRED,
            PrivacyReason.COPY_ABSENT,
        ),
        (
            PrivacyDecision.DENY_RETRIEVAL,
            PrivacyReason.COPY_ALREADY_QUARANTINED,
        ),
        (
            PrivacyDecision.DENY_RETRIEVAL,
            PrivacyReason.INPUT_CONTRACT_VIOLATION,
        ),
    ],
)
def test_result_rejects_impossible_decision_reason_pairs(
    decision: PrivacyDecision, reason: PrivacyReason
) -> None:
    with pytest.raises(PrivacyContractError):
        PrivacyReconciliationResult(decision, reason)


def test_import_has_no_ambient_io_or_clock_side_effects() -> None:
    code = """
import builtins
import os
import socket
import sqlite3
import time

def forbidden(*args, **kwargs):
    raise AssertionError('ambient side effect during import')

builtins.open = forbidden
socket.socket = forbidden
sqlite3.connect = forbidden
time.time = forbidden
os.getenv = forbidden

import mentaury.privacy.reconciliation
from mentaury.privacy.reconciliation import classify_privacy_reconciliation
assert callable(classify_privacy_reconciliation)
print('ok')
"""
    env = dict(os.environ)
    src = str(ROOT / "src")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src if not existing else os.pathsep.join((src, existing))
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "ok"


def test_source_has_no_forbidden_runtime_integrations() -> None:
    sources = "\n".join(
        (
            ROOT
            / "src"
            / "mentaury"
            / "privacy"
            / "reconciliation"
            / name
        ).read_text(encoding="utf-8")
        for name in ("contracts.py", "classifier.py")
    )
    for forbidden_import in (
        "import os",
        "import socket",
        "import sqlite3",
        "import pathlib",
        "import subprocess",
        "import requests",
        "from mentaury.storage",
        "from mentaury.replay",
        "from mentaury.beliefs",
        "from mentaury.evidence",
        "from mentaury.capabilities",
        "from mentaury.identity",
    ):
        assert forbidden_import not in sources
