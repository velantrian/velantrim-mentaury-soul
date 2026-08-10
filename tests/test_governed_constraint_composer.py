"""Executable P1-003 frozen contract, threat, metamorphic and purity matrix."""

from __future__ import annotations

import builtins
import dataclasses
import inspect
import os
import socket
import sqlite3
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path

import pytest

import mentaury.composition.governed_constraints.composer as composer_module
from mentaury.capabilities import (
    CapabilityLeaseRecord,
    GrantedBy,
    LeaseStatus,
    RegistryAvailability,
    RegistrySnapshot,
    ResolutionBudget,
    ResolutionReason,
    ScopeItem,
    capability_lease_digest,
)
from mentaury.composition import (
    BINDING_CONTRACT_VERSION,
    CANONICAL_PROFILE,
    COMMON_REQUEST_DOMAIN,
    COMPOSER_CONTRACT_VERSION,
    EVALUATION_EVIDENCE_DOMAIN,
    P1_001_EXPECTED_VERSION,
    P1_002_EXPECTED_VERSION,
    SOURCE_PROVENANCE_SCOPE,
    CompositionBudget,
    CrossGateEvaluationContext,
    GovernedConstraintContractError,
    GovernedConstraintDecision,
    GovernedConstraintReason,
    compose_governed_constraints,
)
from mentaury.contracts import AuthorityRef, canonical_json_bytes
from mentaury.privacy.reconciliation import (
    CopyState,
    MaterialState,
    PrivacyAccessIntent,
    PrivacyClass,
    PrivacyContractError,
    PrivacyCopy,
    PrivacyMaterial,
    PrivacyReconciliationBudget,
    SurfaceKind,
)

ROOT = Path(__file__).resolve().parents[1]
LEASE_ID = "CAP-P1-003-001"
PURPOSE_ID = "research"
BRANCH_ID = "branch:main"
MATERIAL_ID = "MAT-P1-003-001"
COPY_ID = "COPY-P1-003-001"
REQUEST_ID = "REQ-P1-003-001"
EVALUATED_AT = "2026-08-09T12:00:00Z"
ZERO_DIGEST = "sha256:" + ("0" * 64)
EXPECTED_COMMON_SHA256 = "5d7f08c361d76784676128470715f3a9675e850115d2ca2a1c6f3cf05bc81e16"
EXPECTED_EVIDENCE_SHA256 = "a8c0439d616761f71de044361e9ae7db710d45c50b54df4aa049d8753e0f13b3"


def _record(**changes: object) -> CapabilityLeaseRecord:
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


def _snapshot(
    *,
    record: CapabilityLeaseRecord | None = None,
    records: tuple[dict[str, object], ...] | None = None,
    live_heads: dict[str, int] | None = None,
) -> RegistrySnapshot:
    selected = _record() if record is None else record
    actual_records = (selected.to_value(),) if records is None else records
    actual_heads = (
        {selected.lease_id: selected.revision}
        if live_heads is None
        else live_heads
    )
    return RegistrySnapshot(
        availability=RegistryAvailability.AVAILABLE,
        unavailable_reason=None,
        registry_schema_version=1,
        live_heads=actual_heads,
        records=actual_records,
    )


def _unavailable_snapshot() -> RegistrySnapshot:
    return RegistrySnapshot(
        availability=RegistryAvailability.UNAVAILABLE,
        unavailable_reason="registry offline",
        registry_schema_version=1,
        live_heads={},
        records=(),
    )


def _material(**changes: object) -> PrivacyMaterial:
    base = PrivacyMaterial(
        material_id=MATERIAL_ID,
        privacy_class=PrivacyClass.PERSONAL,
        state=MaterialState.ACTIVE,
        policy_revision=1,
        permitted_purposes=(PURPOSE_ID,),
        withdrawn_purposes=(),
        permitted_branches=(BRANCH_ID,),
        third_party_permission=False,
    )
    return replace(base, **changes)


def _copy(**changes: object) -> PrivacyCopy:
    base = PrivacyCopy(
        copy_id=COPY_ID,
        material_id=MATERIAL_ID,
        branch_id=BRANCH_ID,
        surface=SurfaceKind.PRIMARY,
        policy_revision=1,
        state=CopyState.PRESENT,
        contains_material=True,
    )
    return replace(base, **changes)


def _context(**changes: object) -> CrossGateEvaluationContext:
    values: dict[str, object] = {
        "request_id": REQUEST_ID,
        "purpose_id": PURPOSE_ID,
        "operation_id": "read",
        "data_scope": (ScopeItem("stream", "stream:test"),),
        "requested_side_effects": (),
        "branch_id": BRANCH_ID,
        "evaluated_at": EVALUATED_AT,
        "authority_ref": AuthorityRef(LEASE_ID, 1),
        "registry_snapshot": _snapshot(),
        "privacy_material": _material(),
        "privacy_copy": _copy(),
        "capability_budget": ResolutionBudget(1, 65_536, 128),
        "privacy_budget": PrivacyReconciliationBudget(16_384, 64, 64),
        "composition_budget": CompositionBudget(16_384, 131_072, 128, 64),
    }
    values.update(changes)
    return CrossGateEvaluationContext(**values)


def _compose(**changes: object):
    return compose_governed_constraints(context=_context(**changes))


def _expected_common(context: CrossGateEvaluationContext) -> dict[str, object]:
    return {
        "domain": COMMON_REQUEST_DOMAIN,
        "composer_contract_version": COMPOSER_CONTRACT_VERSION,
        "binding_contract_version": BINDING_CONTRACT_VERSION,
        "canonical_profile": CANONICAL_PROFILE,
        "request_id": context.request_id,
        "purpose_id": context.purpose_id,
        "operation_id": context.operation_id,
        "data_scope": [item.to_value() for item in context.data_scope],
        "requested_side_effects": list(context.requested_side_effects),
        "branch_id": context.branch_id,
        "material_id": context.privacy_material.material_id,
        "copy_id": context.privacy_copy.copy_id,
        "capability_lease_id": context.authority_ref.capability_lease_id,
        "capability_revision": context.authority_ref.capability_revision,
    }


def _expected_evidence(context: CrossGateEvaluationContext, result) -> dict[str, object]:
    assert result.capability_result is not None
    assert result.privacy_result is not None
    intent = PrivacyAccessIntent(COPY_ID, context.branch_id, context.purpose_id)
    return {
        "domain": EVALUATION_EVIDENCE_DOMAIN,
        "composer_contract_version": COMPOSER_CONTRACT_VERSION,
        "binding_contract_version": BINDING_CONTRACT_VERSION,
        "canonical_profile": CANONICAL_PROFILE,
        "source_provenance_scope": SOURCE_PROVENANCE_SCOPE,
        "common_request_fingerprint": result.common_request_fingerprint,
        "evaluated_at": context.evaluated_at,
        "p1_001_contract_version": P1_001_EXPECTED_VERSION,
        "p1_002_contract_version": P1_002_EXPECTED_VERSION,
        "capability_budget": context.capability_budget.to_value(),
        "privacy_budget": context.privacy_budget.to_value(),
        "composition_budget": context.composition_budget.to_value(),
        "targeted_capability_source": {
            "registry_availability": context.registry_snapshot.availability.value,
            "registry_unavailable_reason": context.registry_snapshot.unavailable_reason,
            "registry_schema_version": context.registry_snapshot.registry_schema_version,
            "requested_capability_lease_id": context.authority_ref.capability_lease_id,
            "requested_capability_revision": context.authority_ref.capability_revision,
            "observed_live_revision": context.registry_snapshot.live_heads.get(LEASE_ID),
            "requested_record": context.registry_snapshot.record_for(
                context.authority_ref.capability_lease_id,
                context.authority_ref.capability_revision,
            ),
        },
        "privacy_source": {
            "privacy_material": context.privacy_material.to_value(),
            "privacy_copy": context.privacy_copy.to_value(),
            "privacy_intent": intent.to_value(),
            "privacy_budget": context.privacy_budget.to_value(),
        },
        "capability_result": result.capability_result.to_value(),
        "privacy_result": result.privacy_result.to_value(),
    }


def _mutate_frozen_context() -> None:
    context = _context()
    context.purpose_id = "mutated"


def _unknown_api_argument() -> None:
    compose_governed_constraints(context=_context(), caller_digest="0" * 64)


CTX_IDS = [f"CGC-CTX-{index:03d}" for index in range(1, 15)]


@pytest.mark.parametrize("case_id", CTX_IDS, ids=CTX_IDS)
def test_context_contract_matrix(case_id: str) -> None:
    if case_id == "CGC-CTX-001":
        assert _compose().decision is GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE
    elif case_id == "CGC-CTX-002":
        with pytest.raises(GovernedConstraintContractError):
            _context(request_id=" padded ")
    elif case_id == "CGC-CTX-003":
        with pytest.raises(GovernedConstraintContractError, match="sorted"):
            _context(
                data_scope=(ScopeItem("stream", "z"), ScopeItem("stream", "a"))
            )
    elif case_id == "CGC-CTX-004":
        item = ScopeItem("stream", "same")
        with pytest.raises(GovernedConstraintContractError, match="unique"):
            _context(data_scope=(item, item))
    elif case_id == "CGC-CTX-005":
        with pytest.raises(GovernedConstraintContractError, match="sorted"):
            _context(requested_side_effects=("write", "network"))
    elif case_id == "CGC-CTX-006":
        with pytest.raises(GovernedConstraintContractError, match="unique"):
            _context(requested_side_effects=("network", "network"))
    elif case_id == "CGC-CTX-007":
        with pytest.raises(GovernedConstraintContractError, match="canonical"):
            _context(evaluated_at="2026-08-09T12:00:00+00:00")
    elif case_id == "CGC-CTX-008":
        with pytest.raises(GovernedConstraintContractError, match="material_id"):
            _context(privacy_copy=_copy(material_id="MAT-OTHER"))
    elif case_id == "CGC-CTX-009":
        with pytest.raises(GovernedConstraintContractError, match="branch_id"):
            _context(privacy_copy=_copy(branch_id="branch:other"))
    elif case_id == "CGC-CTX-010":
        with pytest.raises(GovernedConstraintContractError, match="ahead"):
            _context(privacy_copy=_copy(policy_revision=2))
    elif case_id == "CGC-CTX-011":
        with pytest.raises(GovernedConstraintContractError, match="capability_budget"):
            _context(capability_budget={"max_registry_lookups": 1})
    elif case_id == "CGC-CTX-012":
        with pytest.raises(GovernedConstraintContractError):
            CompositionBudget(True, 1, 1, 1)
    elif case_id == "CGC-CTX-013":
        with pytest.raises(dataclasses.FrozenInstanceError):
            _mutate_frozen_context()
    else:
        with pytest.raises(TypeError):
            _unknown_api_argument()


FP_IDS = [f"CGC-FP-{index:03d}" for index in range(1, 11)]


@pytest.mark.parametrize("case_id", FP_IDS, ids=FP_IDS)
def test_fingerprint_and_projection_matrix(case_id: str) -> None:
    context = _context()
    result = compose_governed_constraints(context=context)
    if case_id == "CGC-FP-001":
        assert canonical_json_bytes(
            composer_module._common_request_value(context)
        ) == canonical_json_bytes(_expected_common(context))
    elif case_id == "CGC-FP-002":
        assert result.common_request_fingerprint == EXPECTED_COMMON_SHA256
    elif case_id == "CGC-FP-003":
        assert result.capability_result is not None and result.privacy_result is not None
        intent = PrivacyAccessIntent(COPY_ID, BRANCH_ID, PURPOSE_ID)
        actual = composer_module._evaluation_evidence_value(
            context=context,
            common_request_fingerprint=result.common_request_fingerprint,
            privacy_intent=intent,
            capability_result=result.capability_result,
            privacy_result=result.privacy_result,
        )
        assert canonical_json_bytes(actual) == canonical_json_bytes(
            _expected_evidence(context, result)
        )
    elif case_id == "CGC-FP-004":
        assert result.evaluation_evidence_fingerprint == EXPECTED_EVIDENCE_SHA256
    elif case_id == "CGC-FP-005":
        assert _compose(
            request_id="REQ-OTHER"
        ).common_request_fingerprint != result.common_request_fingerprint
    elif case_id == "CGC-FP-006":
        changed = _compose(
            privacy_material=_material(policy_revision=2),
            privacy_copy=_copy(policy_revision=2),
        )
        assert changed.common_request_fingerprint == result.common_request_fingerprint
        assert (
            changed.evaluation_evidence_fingerprint
            != result.evaluation_evidence_fingerprint
        )
    elif case_id == "CGC-FP-007":
        unrelated = _record(lease_id="CAP-UNRELATED")
        primary = _record()
        expanded = _snapshot(
            record=primary,
            records=(primary.to_value(), unrelated.to_value()),
            live_heads={LEASE_ID: 1, "CAP-UNRELATED": 1},
        )
        changed = _compose(registry_snapshot=expanded)
        assert changed.common_request_fingerprint == result.common_request_fingerprint
        assert (
            changed.evaluation_evidence_fingerprint
            == result.evaluation_evidence_fingerprint
        )
    elif case_id == "CGC-FP-008":
        fields = {field.name for field in dataclasses.fields(CrossGateEvaluationContext)}
        assert {
            "composer_contract_version",
            "binding_contract_version",
            "canonical_profile",
        }.isdisjoint(fields)
    elif case_id == "CGC-FP-009":
        fields = {field.name for field in dataclasses.fields(CrossGateEvaluationContext)}
        assert {
            "common_request_fingerprint",
            "evaluation_evidence_fingerprint",
        }.isdisjoint(fields)
    else:
        rendered = canonical_json_bytes(_expected_evidence(context, result)).decode().lower()
        assert '"unrelated"' not in rendered
        assert '"relationship"' not in rendered
        assert '"m3"' not in rendered


DEC_IDS = [f"CGC-DEC-{index:03d}" for index in range(1, 15)]


@pytest.mark.parametrize("case_id", DEC_IDS, ids=DEC_IDS)
def test_decision_precedence_matrix(case_id: str, monkeypatch) -> None:
    if case_id == "CGC-DEC-001":
        result = _compose()
        expected = (
            GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE,
            GovernedConstraintReason.ELIGIBLE_FOR_NEXT_GATE,
        )
    elif case_id == "CGC-DEC-002":
        result = _compose(operation_id="write")
        expected = (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.CAPABILITY_BLOCKED,
        )
    elif case_id == "CGC-DEC-003":
        result = _compose(privacy_material=_material(permitted_purposes=()))
        expected = (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.PRIVACY_BLOCKED,
        )
    elif case_id == "CGC-DEC-004":
        result = _compose(
            operation_id="write",
            privacy_material=_material(permitted_purposes=()),
        )
        expected = (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.CAPABILITY_AND_PRIVACY_BLOCKED,
        )
    elif case_id == "CGC-DEC-005":
        result = _compose(registry_snapshot=_unavailable_snapshot())
        expected = (
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.CAPABILITY_DEFERRED,
        )
    elif case_id == "CGC-DEC-006":
        result = _compose(
            privacy_budget=PrivacyReconciliationBudget(1, 64, 64)
        )
        expected = (
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.PRIVACY_DEFERRED,
        )
    elif case_id == "CGC-DEC-007":
        result = _compose(
            registry_snapshot=_unavailable_snapshot(),
            privacy_budget=PrivacyReconciliationBudget(1, 64, 64),
        )
        expected = (
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.CAPABILITY_AND_PRIVACY_DEFERRED,
        )
    elif case_id == "CGC-DEC-008":
        result = _compose(
            operation_id="write",
            privacy_budget=PrivacyReconciliationBudget(1, 64, 64),
        )
        expected = (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.CAPABILITY_BLOCKED,
        )
    elif case_id == "CGC-DEC-009":
        record = _record(status=LeaseStatus.UNVERIFIED)
        result = _compose(registry_snapshot=_snapshot(record=record))
        expected = (
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.CAPABILITY_DEFERRED,
        )
    elif case_id == "CGC-DEC-010":
        record = _record(revision=2, supersedes_revision=1)
        result = _compose(
            registry_snapshot=_snapshot(
                record=record,
                records=(record.to_value(),),
                live_heads={LEASE_ID: 2},
            ),
            authority_ref=AuthorityRef(LEASE_ID, 1),
        )
        expected = (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.CAPABILITY_BLOCKED,
        )
    elif case_id == "CGC-DEC-011":
        result = _compose(
            privacy_material=_material(policy_revision=2),
            privacy_copy=_copy(policy_revision=1),
        )
        expected = (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.PRIVACY_BLOCKED,
        )
    elif case_id == "CGC-DEC-012":
        result = _compose(
            composition_budget=CompositionBudget(1, 131_072, 128, 64)
        )
        expected = (
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.COMPOSITION_BUDGET_EXHAUSTED,
        )
    elif case_id == "CGC-DEC-013":
        result = _compose(request_id=chr(0xD800))
        expected = (
            GovernedConstraintDecision.NOT_ELIGIBLE,
            GovernedConstraintReason.BINDING_CANONICALIZATION_FAILED,
        )
    else:
        monkeypatch.setattr(
            composer_module,
            "RESOLVER_CONTRACT_VERSION",
            "P1-001-v9",
        )
        result = _compose()
        expected = (
            GovernedConstraintDecision.DEFER,
            GovernedConstraintReason.GATE_VERSION_UNVERIFIED,
        )
    assert (result.decision, result.primary_reason) == expected


def test_binding_mismatch_and_gate_contract_fail_closed(monkeypatch) -> None:
    original_resolver = composer_module.resolve_capability_lease

    def forged(**kwargs):
        return replace(original_resolver(**kwargs), lease_id="CAP-FORGED")

    monkeypatch.setattr(composer_module, "resolve_capability_lease", forged)
    result = _compose()
    assert result.primary_reason is GovernedConstraintReason.COMMON_BINDING_MISMATCH

    monkeypatch.setattr(composer_module, "resolve_capability_lease", original_resolver)

    def broken(*args, **kwargs):
        raise PrivacyContractError("synthetic contract failure")

    monkeypatch.setattr(composer_module, "classify_privacy_reconciliation", broken)
    result = _compose()
    assert result.decision is GovernedConstraintDecision.DEFER
    assert result.primary_reason is GovernedConstraintReason.GATE_CONTRACT_UNVERIFIED


def test_evidence_canonicalization_failure_is_not_eligible() -> None:
    malformed = _record().to_value()
    malformed["unexpected_float"] = 1.5
    snapshot = RegistrySnapshot(
        availability=RegistryAvailability.AVAILABLE,
        unavailable_reason=None,
        registry_schema_version=1,
        live_heads={LEASE_ID: 1},
        records=(malformed,),
    )
    result = _compose(registry_snapshot=snapshot)
    assert result.decision is GovernedConstraintDecision.NOT_ELIGIBLE
    assert (
        result.primary_reason
        is GovernedConstraintReason.EVIDENCE_CANONICALIZATION_FAILED
    )


T_IDS = [f"CGC-T-{index:03d}" for index in range(1, 13)]


@pytest.mark.parametrize("case_id", T_IDS, ids=T_IDS)
def test_threat_matrix(case_id: str, monkeypatch) -> None:
    baseline = _compose()
    if case_id == "CGC-T-001":
        changed = _compose(request_id="REQ-OTHER")
        assert changed.common_request_fingerprint != baseline.common_request_fingerprint
        assert tuple(inspect.signature(compose_governed_constraints).parameters) == (
            "context",
        )
    elif case_id == "CGC-T-002":
        changed = _compose(purpose_id="archive")
        assert changed.decision is GovernedConstraintDecision.NOT_ELIGIBLE
        assert changed.capability_result.primary_reason is ResolutionReason.PURPOSE_MISMATCH
        assert changed.privacy_result.reason.value == "PURPOSE_NOT_PERMITTED"
        assert changed.common_request_fingerprint != baseline.common_request_fingerprint
    elif case_id == "CGC-T-003":
        changed = _compose(operation_id="write")
        assert changed.decision is GovernedConstraintDecision.NOT_ELIGIBLE
        assert changed.common_request_fingerprint != baseline.common_request_fingerprint
    elif case_id == "CGC-T-004":
        changed = _compose(
            data_scope=(
                ScopeItem("stream", "other"),
                ScopeItem("stream", "stream:test"),
            )
        )
        assert changed.decision is GovernedConstraintDecision.NOT_ELIGIBLE
        assert changed.common_request_fingerprint != baseline.common_request_fingerprint
    elif case_id == "CGC-T-005":
        changed = _compose(requested_side_effects=("network",))
        assert changed.decision is GovernedConstraintDecision.NOT_ELIGIBLE
        assert changed.common_request_fingerprint != baseline.common_request_fingerprint
    elif case_id == "CGC-T-006":
        record = _record(revision=2, supersedes_revision=1)
        changed = _compose(
            registry_snapshot=_snapshot(
                record=record,
                records=(record.to_value(),),
                live_heads={LEASE_ID: 2},
            ),
            authority_ref=AuthorityRef(LEASE_ID, 1),
        )
        assert changed.capability_result.primary_reason is ResolutionReason.REVISION_MISMATCH
        assert changed.decision is GovernedConstraintDecision.NOT_ELIGIBLE
    elif case_id == "CGC-T-007":
        changed = _compose(
            privacy_material=_material(policy_revision=2),
            privacy_copy=_copy(policy_revision=1),
        )
        assert changed.privacy_result.reason.value == "STALE_POLICY_REVISION"
        assert changed.decision is GovernedConstraintDecision.NOT_ELIGIBLE
    elif case_id == "CGC-T-008":
        with pytest.raises(GovernedConstraintContractError):
            _context(branch_id="branch:other", privacy_copy=_copy())
        changed = _compose(
            branch_id="branch:other",
            privacy_copy=_copy(branch_id="branch:other"),
        )
        assert changed.common_request_fingerprint != baseline.common_request_fingerprint
    elif case_id == "CGC-T-009":
        with pytest.raises(TypeError):
            compose_governed_constraints(
                context=_context(),
                common_request_fingerprint="0" * 64,
            )
    elif case_id == "CGC-T-010":
        fields = set(dataclasses.asdict(baseline))
        assert {
            "tool",
            "credential",
            "execution",
            "retrieval_permission",
            "action_gate_pass",
        }.isdisjoint(fields)
        assert baseline.decision.value != "ACTION_GATE_PASS"
    elif case_id == "CGC-T-011":
        def forbidden(*args, **kwargs):
            raise AssertionError("ambient authority accessed")

        monkeypatch.setattr(builtins, "open", forbidden)
        monkeypatch.setattr(socket, "socket", forbidden)
        monkeypatch.setattr(sqlite3, "connect", forbidden)
        monkeypatch.setattr(time, "time", forbidden)
        monkeypatch.setattr(os, "getenv", forbidden)
        assert _compose().decision is GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE
    else:
        context_fields = {
            field.name for field in dataclasses.fields(CrossGateEvaluationContext)
        }
        result_fields = {field.name for field in dataclasses.fields(type(baseline))}
        assert {
            "character",
            "identity",
            "relationship",
            "m3",
            "m3_write",
        }.isdisjoint(context_fields | result_fields)
        source = _p1_003_sources()
        for forbidden in (
            "mentaury.identity",
            "mentaury.relationship",
            "mentaury.beliefs",
        ):
            assert forbidden not in source


M_IDS = [f"CGC-M-{index:03d}" for index in range(1, 11)]


@pytest.mark.parametrize("case_id", M_IDS, ids=M_IDS)
def test_metamorphic_matrix(case_id: str) -> None:
    baseline = _compose()
    if case_id == "CGC-M-001":
        assert (
            _compose(request_id="REQ-MUTATED").common_request_fingerprint
            != baseline.common_request_fingerprint
        )
    elif case_id == "CGC-M-002":
        assert (
            _compose(requested_side_effects=("network",)).decision
            is GovernedConstraintDecision.NOT_ELIGIBLE
        )
    elif case_id == "CGC-M-003":
        assert (
            _compose(
                data_scope=(
                    ScopeItem("stream", "other"),
                    ScopeItem("stream", "stream:test"),
                )
            ).decision
            is GovernedConstraintDecision.NOT_ELIGIBLE
        )
    elif case_id == "CGC-M-004":
        assert (
            _compose(operation_id="write").decision
            is not GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE
        )
    elif case_id == "CGC-M-005":
        assert (
            _compose(registry_snapshot=_unavailable_snapshot()).decision
            is GovernedConstraintDecision.DEFER
        )
    elif case_id == "CGC-M-006":
        primary = _record()
        a = _record(lease_id="CAP-A")
        b = _record(lease_id="CAP-B")
        one = _snapshot(
            record=primary,
            records=(primary.to_value(), a.to_value(), b.to_value()),
            live_heads={LEASE_ID: 1, "CAP-A": 1, "CAP-B": 1},
        )
        two = _snapshot(
            record=primary,
            records=(b.to_value(), primary.to_value(), a.to_value()),
            live_heads={"CAP-B": 1, LEASE_ID: 1, "CAP-A": 1},
        )
        first = _compose(registry_snapshot=one)
        second = _compose(registry_snapshot=two)
        assert first == second
    elif case_id == "CGC-M-007":
        context = _context()
        assert compose_governed_constraints(
            context=context
        ) == compose_governed_constraints(context=context)
    elif case_id == "CGC-M-008":
        changed = _compose(
            privacy_material=_material(policy_revision=2),
            privacy_copy=_copy(policy_revision=2),
        )
        assert (
            changed.evaluation_evidence_fingerprint
            != baseline.evaluation_evidence_fingerprint
        )
    elif case_id == "CGC-M-009":
        primary = _record()
        unrelated = _record(lease_id="CAP-UNRELATED")
        expanded = _snapshot(
            record=primary,
            records=(primary.to_value(), unrelated.to_value()),
            live_heads={LEASE_ID: 1, "CAP-UNRELATED": 1},
        )
        assert _compose(registry_snapshot=expanded) == baseline
    else:
        assert baseline.decision is GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE
        assert "ACTION_GATE" not in repr(dataclasses.asdict(baseline))


def _p1_003_sources() -> str:
    package = ROOT / "src" / "mentaury" / "composition"
    return "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(package.rglob("*.py"))
    )


PURE_IDS = [f"CGC-PURE-{index:03d}" for index in range(1, 9)]


@pytest.mark.parametrize("case_id", PURE_IDS, ids=PURE_IDS)
def test_purity_matrix(case_id: str, monkeypatch) -> None:
    if case_id == "CGC-PURE-001":
        code = r'''
import builtins, os, socket, sqlite3, time

def forbidden(*args, **kwargs):
    raise AssertionError("ambient access")

builtins.open = forbidden
socket.socket = forbidden
sqlite3.connect = forbidden
time.time = forbidden
os.getenv = forbidden

from dataclasses import replace
from mentaury.capabilities import CapabilityLeaseRecord, GrantedBy, LeaseStatus, RegistryAvailability, RegistrySnapshot, ResolutionBudget, ScopeItem, capability_lease_digest
from mentaury.composition import CompositionBudget, CrossGateEvaluationContext, GovernedConstraintDecision, compose_governed_constraints
from mentaury.contracts import AuthorityRef
from mentaury.privacy.reconciliation import CopyState, MaterialState, PrivacyClass, PrivacyCopy, PrivacyMaterial, PrivacyReconciliationBudget, SurfaceKind

zero = "sha256:" + "0" * 64
record = CapabilityLeaseRecord(lease_id="CAP-P1-003-001", revision=1, supersedes_revision=None, status=LeaseStatus.ACTIVE, tool_id=None, granted_by=GrantedBy("operator", "operator:test"), purpose_id="research", allowed_operations=("read",), data_scope=(ScopeItem("stream", "stream:test"),), allowed_side_effects=(), not_before="2026-08-09T00:00:00Z", expires_at="2026-08-10T00:00:00Z", revocation_conditions=(), revoked_at=None, delegation_allowed=False, branch_transfer_allowed=False, audit_required=True, identity_authority="NONE", direct_m3_write=False, content_digest=zero)
record = replace(record, content_digest=capability_lease_digest(record))
snapshot = RegistrySnapshot(RegistryAvailability.AVAILABLE, None, 1, {record.lease_id: 1}, (record.to_value(),))
material = PrivacyMaterial("MAT-P1-003-001", PrivacyClass.PERSONAL, MaterialState.ACTIVE, 1, ("research",), (), ("branch:main",), False)
copy = PrivacyCopy("COPY-P1-003-001", material.material_id, "branch:main", SurfaceKind.PRIMARY, 1, CopyState.PRESENT, True)
context = CrossGateEvaluationContext("REQ-P1-003-001", "research", "read", (ScopeItem("stream", "stream:test"),), (), "branch:main", "2026-08-09T12:00:00Z", AuthorityRef(record.lease_id, 1), snapshot, material, copy, ResolutionBudget(1, 65536, 128), PrivacyReconciliationBudget(16384, 64, 64), CompositionBudget(16384, 131072, 128, 64))
result = compose_governed_constraints(context=context)
assert result.decision is GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE
print("ok")
'''
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == "ok"
    elif case_id == "CGC-PURE-002":
        def forbidden(*args, **kwargs):
            raise AssertionError("ambient I/O")

        monkeypatch.setattr(builtins, "open", forbidden)
        monkeypatch.setattr(socket, "socket", forbidden)
        monkeypatch.setattr(sqlite3, "connect", forbidden)
        assert _compose().decision is GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE
    elif case_id == "CGC-PURE-003":
        monkeypatch.setattr(
            time,
            "time",
            lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("clock")),
        )
        assert _compose().decision is GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE
    elif case_id == "CGC-PURE-004":
        monkeypatch.setattr(
            os,
            "getenv",
            lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("env")),
        )
        assert _compose().decision is GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE
    elif case_id == "CGC-PURE-005":
        source = _p1_003_sources()
        for forbidden in (
            "from mentaury.storage",
            "from mentaury.replay",
            "from mentaury.beliefs",
            "from mentaury.identity",
            "from mentaury.relationship",
            "append_event",
            "write_m3",
        ):
            assert forbidden not in source
    elif case_id == "CGC-PURE-006":
        source = _p1_003_sources()
        for forbidden in (
            "import subprocess",
            "import importlib",
            "tool_adapter",
            "sqlite3.connect",
            "socket.socket",
            "plugin",
        ):
            assert forbidden not in source
    elif case_id == "CGC-PURE-007":
        context = _context()
        first = compose_governed_constraints(context=context)
        second = compose_governed_constraints(context=context)
        assert first == second
        assert first.common_request_fingerprint == second.common_request_fingerprint
        assert (
            first.evaluation_evidence_fingerprint
            == second.evaluation_evidence_fingerprint
        )
    else:
        result = _compose()
        for field in dataclasses.fields(result):
            assert not callable(getattr(result, field.name))
        rendered = repr(dataclasses.asdict(result)).lower()
        for forbidden in (
            "password",
            "secret",
            "credential",
            "bearer",
            "tool_handle",
            "storage_locator",
            "mutation_command",
        ):
            assert forbidden not in rendered
