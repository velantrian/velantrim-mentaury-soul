"""P1-002 privacy classifier contract, scenario, and adversarial tests."""

from __future__ import annotations

import dataclasses
import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from mentaury.contracts import canonical_json_bytes
from mentaury.privacy.reconciliation import (
    CopyState,
    MaterialState,
    PrivacyAccessIntent,
    PrivacyClass,
    PrivacyContractError,
    PrivacyCopy,
    PrivacyDecision,
    PrivacyMaterial,
    PrivacyReason,
    PrivacyReconciliationBudget,
    PrivacyReconciliationResult,
    SurfaceKind,
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


def test_priv_sc_001_deleted_data_present_in_backup() -> None:
    assert _outcome(
        material=_material(state="DELETED"),
        copy=_copy(surface="BACKUP"),
    ) == (
        PrivacyDecision.QUARANTINE_REQUIRED,
        PrivacyReason.DELETED_OR_REDACTED_MATERIAL,
    )


def test_priv_sc_002_third_party_testimony_without_permission() -> None:
    assert _outcome(
        material=_material(privacy_class="THIRD_PARTY")
    ) == (
        PrivacyDecision.DENY_RETRIEVAL,
        PrivacyReason.THIRD_PARTY_PERMISSION_MISSING,
    )


def test_priv_sc_003_fork_retains_withdrawn_data() -> None:
    assert _outcome(
        material=_material(
            permitted_purposes=[], withdrawn_purposes=[PURPOSE]
        ),
        copy=_copy(surface="FORK"),
    ) == (
        PrivacyDecision.QUARANTINE_REQUIRED,
        PrivacyReason.PURPOSE_WITHDRAWN,
    )


def test_priv_sc_004_derived_summary_exposes_redacted_material() -> None:
    assert _outcome(
        material=_material(privacy_class="REDACTED", state="REDACTED"),
        copy=_copy(surface="DERIVED_SUMMARY"),
    ) == (
        PrivacyDecision.REBUILD_REQUIRED,
        PrivacyReason.DELETED_OR_REDACTED_MATERIAL,
    )


def test_priv_sc_005_active_primary_copy_is_allowed_for_exact_policy() -> None:
    assert _outcome() == (
        PrivacyDecision.ALLOW_REFERENCE,
        PrivacyReason.ALLOW_REFERENCE,
    )


def test_priv_sc_006_stale_primary_policy_revision() -> None:
    assert _outcome(
        material=_material(policy_revision=2),
        copy=_copy(policy_revision=1),
    ) == (
        PrivacyDecision.DENY_RETRIEVAL,
        PrivacyReason.STALE_POLICY_REVISION,
    )


def test_priv_sc_007_stale_index_policy_revision() -> None:
    assert _outcome(
        material=_material(policy_revision=2),
        copy=_copy(policy_revision=1, surface="INDEX"),
    ) == (
        PrivacyDecision.REBUILD_REQUIRED,
        PrivacyReason.STALE_POLICY_REVISION,
    )


def test_priv_sc_008_copy_links_to_another_material() -> None:
    with pytest.raises(PrivacyContractError, match="material_id"):
        _classify(copy=_copy(material_id="MAT-OTHER"))


def test_priv_sc_009_copy_material_is_absent() -> None:
    assert _outcome(
        copy=_copy(state="ABSENT", contains_material=False)
    ) == (
        PrivacyDecision.DENY_RETRIEVAL,
        PrivacyReason.COPY_ABSENT,
    )


def test_priv_sc_010_copy_is_already_quarantined() -> None:
    assert _outcome(copy=_copy(state="QUARANTINED")) == (
        PrivacyDecision.QUARANTINE_REQUIRED,
        PrivacyReason.COPY_ALREADY_QUARANTINED,
    )


def test_priv_sc_011_budget_is_exhausted() -> None:
    assert _outcome(budget=_budget(max_serialized_bytes=1)) == (
        PrivacyDecision.DENY_RETRIEVAL,
        PrivacyReason.BUDGET_EXHAUSTED,
    )


def test_priv_sc_012_fork_branch_is_not_permitted() -> None:
    branch = "branch:fork"
    assert _outcome(
        copy=_copy(branch_id=branch, surface="FORK"),
        intent=_intent(branch_id=branch),
    ) == (
        PrivacyDecision.QUARANTINE_REQUIRED,
        PrivacyReason.BRANCH_NOT_PERMITTED,
    )


def test_priv_sc_013_mapping_contains_unknown_field() -> None:
    value = _material()
    value["unexpected_authority"] = True
    with pytest.raises(PrivacyContractError, match="unknown fields"):
        _classify(material=value)


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
            _material(
                permitted_purposes=[], withdrawn_purposes=[PURPOSE]
            ),
            _copy(branch_id="branch:other"),
            _intent(branch_id="branch:other"),
            _budget(),
            PrivacyReason.PURPOSE_WITHDRAWN,
        ),
        (
            _material(
                policy_revision=2,
                permitted_purposes=["archive"],
            ),
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
    for _ in range(20):
        assert _classify() == first
        assert canonical_json_bytes(_classify().to_value()) == canonical_json_bytes(
            first.to_value()
        )


@pytest.mark.parametrize(
    "material",
    [
        _material(policy_revision=True),
        _material(privacy_class="UNKNOWN"),
        _material(permitted_purposes=[PURPOSE, PURPOSE]),
        _material(permitted_purposes=[PURPOSE, "archive"]),
        _material(
            permitted_purposes=[PURPOSE], withdrawn_purposes=[PURPOSE]
        ),
        _material(third_party_permission="yes"),
        _material(material_id=" padded "),
    ],
)
def test_strict_material_admission_rejects_wrong_or_noncanonical_values(
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


def test_intent_linkage_is_checked_before_budget() -> None:
    with pytest.raises(PrivacyContractError, match="intent.copy_id"):
        _classify(
            intent=_intent(copy_id="COPY-OTHER"),
            budget=_budget(max_serialized_bytes=1),
        )


def test_purpose_and_branch_collection_budgets_fail_closed() -> None:
    purpose_result = _classify(
        material=_material(permitted_purposes=["archive", PURPOSE]),
        budget=_budget(max_purposes=1),
    )
    branch_result = _classify(
        material=_material(
            permitted_branches=[BRANCH_ID, "branch:secondary"]
        ),
        budget=_budget(max_branches=1),
    )
    assert purpose_result.reason is PrivacyReason.BUDGET_EXHAUSTED
    assert branch_result.reason is PrivacyReason.BUDGET_EXHAUSTED


def test_public_material_without_explicit_lists_can_be_referenced() -> None:
    result = _classify(
        material=_material(
            privacy_class="PUBLIC",
            permitted_purposes=[],
            permitted_branches=[],
        )
    )
    assert result.decision is PrivacyDecision.ALLOW_REFERENCE


def test_restricted_material_requires_explicit_purpose_and_branch() -> None:
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


def test_third_party_permission_does_not_bypass_purpose_or_branch() -> None:
    result = _classify(
        material=_material(
            privacy_class="THIRD_PARTY",
            third_party_permission=True,
            permitted_purposes=["archive"],
        )
    )
    assert result.reason is PrivacyReason.PURPOSE_NOT_PERMITTED


def test_result_is_exactly_two_fields_and_contains_no_permission_material() -> None:
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


def test_result_rejects_incoherent_allow_pairs() -> None:
    with pytest.raises(PrivacyContractError):
        PrivacyReconciliationResult(
            PrivacyDecision.ALLOW_REFERENCE,
            PrivacyReason.PURPOSE_NOT_PERMITTED,
        )
    with pytest.raises(PrivacyContractError):
        PrivacyReconciliationResult(
            PrivacyDecision.DENY_RETRIEVAL,
            PrivacyReason.ALLOW_REFERENCE,
        )


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
        (ROOT / "src" / "mentaury" / "privacy" / "reconciliation" / name).read_text(
            encoding="utf-8"
        )
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
