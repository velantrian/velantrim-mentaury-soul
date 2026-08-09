"""P1-001 Capability Lease resolver contract and adversarial tests."""

from __future__ import annotations

import copy
import dataclasses
import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from mentaury.capabilities import (
    ActionIntent,
    CapabilityLeaseRecord,
    GrantedBy,
    LeaseStatus,
    RegistryAvailability,
    RegistrySnapshot,
    ResolutionBudget,
    ResolutionDecision,
    ResolutionReason,
    ScopeItem,
    capability_lease_digest,
    resolve_capability_lease,
)
from mentaury.contracts import AuthorityRef, canonical_json_bytes

LEASE_ID = "CAP-TEST-001"
PURPOSE_ID = "PURPOSE-TEST-001"
EVALUATED_AT = "2026-08-09T12:00:00Z"
ZERO_DIGEST = "sha256:" + ("0" * 64)
ROOT = Path(__file__).resolve().parents[1]


def _typed_record(**changes: object) -> CapabilityLeaseRecord:
    base = CapabilityLeaseRecord(
        lease_id=LEASE_ID,
        revision=1,
        supersedes_revision=None,
        status=LeaseStatus.ACTIVE,
        tool_id=None,
        granted_by=GrantedBy(actor_type="operator", actor_id="operator:test"),
        purpose_id=PURPOSE_ID,
        allowed_operations=("read",),
        data_scope=(ScopeItem("stream", "stream:test"),),
        allowed_side_effects=(),
        not_before="2026-08-09T00:00:00Z",
        expires_at="2026-08-10T00:00:00Z",
        revocation_conditions=(),
        revoked_at=None,
        delegation_allowed=False,
        branch_transfer_allowed=False,
        audit_required=True,
        identity_authority="NONE",
        direct_m3_write=False,
        content_digest=ZERO_DIGEST,
    )
    candidate = replace(base, **changes, content_digest=ZERO_DIGEST)
    return replace(candidate, content_digest=capability_lease_digest(candidate))


def _record(**changes: object) -> dict[str, object]:
    return _typed_record(**changes).to_value()


def _snapshot(
    *,
    records: list[dict[str, object]] | None = None,
    live_heads: dict[str, int] | None = None,
    availability: str = "AVAILABLE",
    unavailable_reason: str | None = None,
    registry_schema_version: int = 1,
) -> dict[str, object]:
    actual_records = [_record()] if records is None else records
    if live_heads is None:
        if actual_records:
            selected = actual_records[0]
            actual_heads = {str(selected["lease_id"]): int(selected["revision"])}
        else:
            actual_heads = {}
    else:
        actual_heads = live_heads
    return {
        "availability": availability,
        "unavailable_reason": unavailable_reason,
        "registry_schema_version": registry_schema_version,
        "live_heads": actual_heads,
        "records": actual_records,
    }


def _intent(
    *,
    purpose_id: str = PURPOSE_ID,
    operation_id: str = "read",
    data_scope: list[dict[str, str]] | None = None,
    requested_side_effects: list[str] | None = None,
) -> dict[str, object]:
    return {
        "purpose_id": purpose_id,
        "operation_id": operation_id,
        "data_scope": (
            [{"kind": "stream", "identifier": "stream:test"}]
            if data_scope is None
            else data_scope
        ),
        "requested_side_effects": (
            [] if requested_side_effects is None else requested_side_effects
        ),
    }


def _budget(
    *,
    max_registry_lookups: int = 1,
    max_record_bytes: int = 65_536,
    max_scope_items: int = 128,
) -> dict[str, int]:
    return {
        "max_registry_lookups": max_registry_lookups,
        "max_record_bytes": max_record_bytes,
        "max_scope_items": max_scope_items,
    }


def _resolve(
    *,
    snapshot: object | None = None,
    ref: object | None = None,
    intent: object | None = None,
    evaluated_at: object = EVALUATED_AT,
    budget: object | None = None,
):
    return resolve_capability_lease(
        registry_snapshot=_snapshot() if snapshot is None else snapshot,
        authority_ref=AuthorityRef(LEASE_ID, 1) if ref is None else ref,
        action_intent=_intent() if intent is None else intent,
        evaluated_at=evaluated_at,
        resolution_budget=_budget() if budget is None else budget,
    )


def _reason(**kwargs: object) -> ResolutionReason:
    return _resolve(**kwargs).primary_reason


def test_cap_sc_001_unavailable_registry() -> None:
    snapshot = _snapshot(
        records=[],
        live_heads={},
        availability="UNAVAILABLE",
        unavailable_reason="registry offline",
    )
    assert _reason(snapshot=snapshot) is ResolutionReason.REGISTRY_UNAVAILABLE


def test_cap_sc_002_unsupported_registry_schema() -> None:
    assert (
        _reason(snapshot=_snapshot(registry_schema_version=2))
        is ResolutionReason.REGISTRY_CONTRACT_VIOLATION
    )


@pytest.mark.parametrize("mode", ["duplicate", "broken-head"])
def test_cap_sc_003_duplicate_key_or_broken_live_head(mode: str) -> None:
    record = _record()
    if mode == "duplicate":
        snapshot = _snapshot(records=[record, copy.deepcopy(record)])
    else:
        snapshot = _snapshot(records=[record], live_heads={LEASE_ID: 2})
    assert _reason(snapshot=snapshot) is ResolutionReason.REGISTRY_CONTRACT_VIOLATION


def test_cap_sc_004_unknown_lease() -> None:
    assert (
        _reason(snapshot=_snapshot(records=[], live_heads={}))
        is ResolutionReason.UNKNOWN_LEASE
    )


def test_cap_sc_005_revision_behind_live_head() -> None:
    record = _record(revision=2, supersedes_revision=1)
    snapshot = _snapshot(records=[record], live_heads={LEASE_ID: 2})
    assert (
        _reason(snapshot=snapshot, ref=AuthorityRef(LEASE_ID, 1))
        is ResolutionReason.REVISION_MISMATCH
    )


def test_cap_sc_006_revision_ahead_of_live_head() -> None:
    record = _record(revision=2, supersedes_revision=1)
    snapshot = _snapshot(records=[record], live_heads={LEASE_ID: 2})
    assert (
        _reason(snapshot=snapshot, ref=AuthorityRef(LEASE_ID, 3))
        is ResolutionReason.REVISION_MISMATCH
    )


def test_cap_sc_007_oversized_record() -> None:
    assert (
        _reason(budget=_budget(max_record_bytes=1))
        is ResolutionReason.BUDGET_EXHAUSTED
    )


def test_cap_sc_008_malformed_lease_schema() -> None:
    malformed = _record()
    malformed["unexpected"] = True
    assert (
        _reason(snapshot=_snapshot(records=[malformed]))
        is ResolutionReason.LEASE_CONTRACT_VIOLATION
    )


def test_cap_sc_009_forged_digest() -> None:
    forged = _record()
    forged["content_digest"] = "sha256:" + ("f" * 64)
    assert (
        _reason(snapshot=_snapshot(records=[forged]))
        is ResolutionReason.LEASE_DIGEST_MISMATCH
    )


def test_cap_sc_010_malformed_supersession() -> None:
    record = _record(revision=2, supersedes_revision=None)
    assert (
        _reason(
            snapshot=_snapshot(records=[record], live_heads={LEASE_ID: 2}),
            ref=AuthorityRef(LEASE_ID, 2),
        )
        is ResolutionReason.LEASE_CONTRACT_VIOLATION
    )


def test_cap_sc_011_premature_materialized_expired() -> None:
    record = _record(status=LeaseStatus.EXPIRED)
    assert (
        _reason(snapshot=_snapshot(records=[record]))
        is ResolutionReason.LEASE_CONTRACT_VIOLATION
    )


def test_cap_sc_012_revoked_lease() -> None:
    record = _record(
        status=LeaseStatus.REVOKED,
        revoked_at="2026-08-09T11:00:00Z",
    )
    assert (
        _reason(snapshot=_snapshot(records=[record]))
        is ResolutionReason.LEASE_REVOKED
    )


def test_cap_sc_013_active_at_expiry() -> None:
    assert (
        _reason(evaluated_at="2026-08-10T00:00:00Z")
        is ResolutionReason.LEASE_EXPIRED
    )


@pytest.mark.parametrize(
    "status",
    [
        LeaseStatus.PROPOSED,
        LeaseStatus.SUSPENDED,
        LeaseStatus.SUPERSEDED,
        LeaseStatus.UNVERIFIED,
    ],
)
def test_cap_sc_014_other_non_active_state(status: LeaseStatus) -> None:
    assert (
        _reason(snapshot=_snapshot(records=[_record(status=status)]))
        is ResolutionReason.LEASE_NOT_ACTIVE
    )


def test_cap_sc_015_before_not_before() -> None:
    assert (
        _reason(evaluated_at="2026-08-08T23:59:59Z")
        is ResolutionReason.NOT_YET_VALID
    )


def test_cap_sc_016_purpose_mismatch() -> None:
    assert (
        _reason(intent=_intent(purpose_id="PURPOSE-OTHER"))
        is ResolutionReason.PURPOSE_MISMATCH
    )


def test_cap_sc_017_operation_not_allowed() -> None:
    assert (
        _reason(intent=_intent(operation_id="write"))
        is ResolutionReason.OPERATION_NOT_ALLOWED
    )


def test_cap_sc_018_scope_budget_exceeded() -> None:
    record = _record(
        data_scope=(
            ScopeItem("stream", "stream:a"),
            ScopeItem("stream", "stream:b"),
        )
    )
    intent = _intent(
        data_scope=[
            {"kind": "stream", "identifier": "stream:a"},
            {"kind": "stream", "identifier": "stream:b"},
        ]
    )
    assert (
        _reason(
            snapshot=_snapshot(records=[record]),
            intent=intent,
            budget=_budget(max_scope_items=1),
        )
        is ResolutionReason.BUDGET_EXHAUSTED
    )


def test_cap_sc_019_typed_scope_violation() -> None:
    assert (
        _reason(
            intent=_intent(
                data_scope=[
                    {"kind": "stream", "identifier": "stream:other"}
                ]
            )
        )
        is ResolutionReason.DATA_SCOPE_VIOLATION
    )


def test_cap_sc_020_undeclared_side_effect() -> None:
    assert (
        _reason(intent=_intent(requested_side_effects=["network"]))
        is ResolutionReason.SIDE_EFFECT_NOT_ALLOWED
    )


def test_cap_sc_021_missing_budget() -> None:
    result = resolve_capability_lease(
        registry_snapshot=_snapshot(),
        authority_ref=AuthorityRef(LEASE_ID, 1),
        action_intent=_intent(),
        evaluated_at=EVALUATED_AT,
        resolution_budget=None,
    )
    assert result.primary_reason is ResolutionReason.BUDGET_MISSING


@pytest.mark.parametrize(
    "changes",
    [{"identity_authority": "M3"}, {"direct_m3_write": True}],
)
def test_cap_sc_022_identity_authority_or_direct_m3_write(
    changes: dict[str, object],
) -> None:
    assert (
        _reason(snapshot=_snapshot(records=[_record(**changes)]))
        is ResolutionReason.LEASE_CONTRACT_VIOLATION
    )


def test_cap_sc_023_identical_inputs_are_byte_equivalent() -> None:
    first = _resolve()
    second = _resolve()
    assert first.decision is ResolutionDecision.ALLOW
    assert canonical_json_bytes(first.to_value()) == canonical_json_bytes(
        second.to_value()
    )


def test_cap_sc_024_unrelated_admitted_record_does_not_change_result() -> None:
    primary = _record()
    unrelated = _record(lease_id="CAP-UNRELATED")
    baseline = _resolve(snapshot=_snapshot(records=[primary]))
    expanded = _resolve(snapshot=_snapshot(records=[primary, unrelated]))
    assert canonical_json_bytes(baseline.to_value()) == canonical_json_bytes(
        expanded.to_value()
    )


def test_cap_sc_025_fork_old_and_new_unverified_refs() -> None:
    restored = _record(
        revision=2,
        supersedes_revision=1,
        status=LeaseStatus.UNVERIFIED,
    )
    snapshot = _snapshot(records=[restored], live_heads={LEASE_ID: 2})
    old = _resolve(snapshot=snapshot, ref=AuthorityRef(LEASE_ID, 1))
    new = _resolve(snapshot=snapshot, ref=AuthorityRef(LEASE_ID, 2))
    assert old.primary_reason is ResolutionReason.REVISION_MISMATCH
    assert new.primary_reason is ResolutionReason.LEASE_NOT_ACTIVE


@pytest.mark.parametrize(
    "mutation",
    [
        lambda intent: {**intent, "unknown": True},
        lambda intent: {**intent, "purpose_id": ""},
        lambda intent: {
            **intent,
            "data_scope": [
                {"kind": "stream", "identifier": "stream:test"},
                {"kind": "stream", "identifier": "stream:test"},
            ],
        },
    ],
)
def test_request_admission_is_strict(mutation) -> None:
    assert _reason(intent=mutation(_intent())) is ResolutionReason.REQUEST_INVALID


def test_invalid_evaluated_at_is_request_invalid() -> None:
    assert (
        _reason(evaluated_at="2026-08-09T14:00:00+02:00")
        is ResolutionReason.REQUEST_INVALID
    )


@pytest.mark.parametrize(
    "budget",
    [
        {},
        {
            "max_registry_lookups": 0,
            "max_record_bytes": 1,
            "max_scope_items": 1,
        },
        {
            "max_registry_lookups": True,
            "max_record_bytes": 1,
            "max_scope_items": 1,
        },
        {
            "max_registry_lookups": 1,
            "max_record_bytes": 1,
            "max_scope_items": 1,
            "extra": 1,
        },
    ],
)
def test_malformed_budget_fails_as_budget_exhausted(budget: object) -> None:
    assert _reason(budget=budget) is ResolutionReason.BUDGET_EXHAUSTED


def test_budget_failure_precedes_registry_unavailable() -> None:
    snapshot = _snapshot(
        records=[],
        live_heads={},
        availability="UNAVAILABLE",
        unavailable_reason="offline",
    )
    assert _reason(snapshot=snapshot, budget={}) is ResolutionReason.BUDGET_EXHAUSTED


@pytest.mark.parametrize(
    "mutation",
    [
        lambda record: {
            key: value for key, value in record.items() if key != "purpose_id"
        },
        lambda record: {**record, "allowed_operations": ["read", "read"]},
        lambda record: {**record, "allowed_operations": ["write", "read"]},
        lambda record: {
            **record,
            "data_scope": [
                {"kind": "stream", "identifier": "stream:b"},
                {"kind": "stream", "identifier": "stream:a"},
            ],
        },
        lambda record: {
            **record,
            "not_before": "2026-08-09T02:00:00+02:00",
        },
        lambda record: {**record, "audit_required": "true"},
    ],
)
def test_record_admission_rejects_unknown_types_duplicates_and_order(
    mutation,
) -> None:
    malformed = mutation(_record())
    assert (
        _reason(snapshot=_snapshot(records=[malformed]))
        is ResolutionReason.LEASE_CONTRACT_VIOLATION
    )


def test_digest_precedes_semantic_and_lifecycle_denial() -> None:
    forged = _record(
        status=LeaseStatus.REVOKED,
        revoked_at="2026-08-09T11:00:00Z",
        identity_authority="M3",
    )
    forged["content_digest"] = "sha256:" + ("e" * 64)
    assert (
        _reason(snapshot=_snapshot(records=[forged]))
        is ResolutionReason.LEASE_DIGEST_MISMATCH
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"delegation_allowed": True},
        {"branch_transfer_allowed": True},
        {"audit_required": False},
        {"not_before": "2026-08-10T00:00:00Z"},
        {"status": LeaseStatus.REVOKED, "revoked_at": None},
        {
            "status": LeaseStatus.ACTIVE,
            "revoked_at": "2026-08-09T11:00:00Z",
        },
    ],
)
def test_semantic_invariants_fail_closed(changes: dict[str, object]) -> None:
    assert (
        _reason(snapshot=_snapshot(records=[_record(**changes)]))
        is ResolutionReason.LEASE_CONTRACT_VIOLATION
    )


def test_allow_result_contains_no_reusable_permission_material() -> None:
    value = _resolve().to_value()
    assert value["decision"] == "ALLOW"
    assert value["primary_reason"] == "ALLOW"
    assert set(value) == {
        "decision",
        "primary_reason",
        "lease_id",
        "requested_revision",
        "observed_live_revision",
        "observed_status",
        "observed_digest",
        "evaluated_at",
        "resolver_contract_version",
    }
    forbidden = {
        "allowed_operations",
        "data_scope",
        "allowed_side_effects",
        "tool_id",
        "capability",
        "token",
        "secret",
    }
    assert forbidden.isdisjoint(value)


def test_typed_and_mapping_inputs_are_equivalent() -> None:
    record = _typed_record()
    typed_snapshot = RegistrySnapshot(
        availability=RegistryAvailability.AVAILABLE,
        unavailable_reason=None,
        registry_schema_version=1,
        live_heads={LEASE_ID: 1},
        records=(record.to_value(),),
    )
    typed = resolve_capability_lease(
        registry_snapshot=typed_snapshot,
        authority_ref=AuthorityRef(LEASE_ID, 1),
        action_intent=ActionIntent(
            purpose_id=PURPOSE_ID,
            operation_id="read",
            data_scope=(ScopeItem("stream", "stream:test"),),
            requested_side_effects=(),
        ),
        evaluated_at=EVALUATED_AT,
        resolution_budget=ResolutionBudget(1, 65_536, 128),
    )
    mapped = _resolve()
    assert canonical_json_bytes(typed.to_value()) == canonical_json_bytes(
        mapped.to_value()
    )


def test_registry_snapshot_detaches_caller_records() -> None:
    raw = _record()
    snapshot = RegistrySnapshot(
        availability=RegistryAvailability.AVAILABLE,
        unavailable_reason=None,
        registry_schema_version=1,
        live_heads={LEASE_ID: 1},
        records=(raw,),
    )
    raw["purpose_id"] = "MUTATED"
    stored = snapshot.record_for(LEASE_ID, 1)
    assert stored is not None
    assert stored["purpose_id"] == PURPOSE_ID


def test_registry_snapshot_records_are_recursively_immutable() -> None:
    snapshot = RegistrySnapshot(
        availability=RegistryAvailability.AVAILABLE,
        unavailable_reason=None,
        registry_schema_version=1,
        live_heads={LEASE_ID: 1},
        records=(_record(),),
    )
    stored = snapshot.record_for(LEASE_ID, 1)
    assert stored is not None

    granted_by = stored["granted_by"]
    operations = stored["allowed_operations"]
    assert operations == ("read",)

    with pytest.raises(TypeError):
        granted_by["actor_id"] = "operator:mutated"
    with pytest.raises(TypeError):
        operations[0] = "write"


def test_authority_ref_shape_remains_p0_reference_only() -> None:
    assert tuple(field.name for field in dataclasses.fields(AuthorityRef)) == (
        "capability_lease_id",
        "capability_revision",
    )


def test_import_has_no_ambient_io_or_clock_side_effects() -> None:
    code = """
import builtins
import socket
import sqlite3
import time

def forbidden(*args, **kwargs):
    raise AssertionError('ambient side effect during import')

builtins.open = forbidden
socket.socket = forbidden
sqlite3.connect = forbidden
time.time = forbidden

import mentaury.capabilities
from mentaury.capabilities import resolve_capability_lease
assert callable(resolve_capability_lease)
print('ok')
"""
    env = dict(os.environ)
    src = str(ROOT / "src")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        src if not existing else os.pathsep.join((src, existing))
    )
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


def test_resolver_source_has_no_forbidden_runtime_integrations() -> None:
    source = (
        ROOT / "src" / "mentaury" / "capabilities" / "lease" / "resolver.py"
    ).read_text(encoding="utf-8")
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
    ):
        assert forbidden_import not in source
