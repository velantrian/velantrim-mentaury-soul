"""Pure deterministic P1-001 Capability Lease resolver."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from datetime import datetime

from mentaury.contracts import (
    AuthorityRef,
    CanonicalJSONError,
    canonical_json_bytes,
    canonical_timestamp,
)

from .contracts import (
    ActionIntent,
    CapabilityLeaseRecord,
    GrantedBy,
    LeaseStatus,
    RegistryAvailability,
    RegistrySnapshot,
    ResolutionBudget,
    ResolutionDecision,
    ResolutionReason,
    ResolutionResult,
    ScopeItem,
)


def resolve_capability_lease(
    *,
    registry_snapshot: object,
    authority_ref: object,
    action_intent: object,
    evaluated_at: object,
    resolution_budget: object,
) -> ResolutionResult:
    """Resolve one explicit intent without ambient authority or side effects.

    The function follows the frozen P1-001 first-match deny precedence. It
    performs no network, filesystem, database, event, replay, belief, identity,
    relationship, M3, tool, or external-effect operation.
    """

    parsed_ref: AuthorityRef | None = None
    parsed_intent: ActionIntent | None = None
    canonical_evaluated_at: str | None = None

    try:
        if not isinstance(registry_snapshot, (RegistrySnapshot, Mapping)):
            raise TypeError("registry_snapshot must be an object")
        parsed_ref = _parse_authority_ref(authority_ref)
        parsed_intent = _parse_action_intent(action_intent)
        canonical_evaluated_at = _parse_evaluated_at(evaluated_at)
    except (KeyError, TypeError, ValueError):
        return _result(
            ResolutionReason.REQUEST_INVALID,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
        )

    if resolution_budget is None:
        return _result(
            ResolutionReason.BUDGET_MISSING,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
        )

    try:
        budget = _parse_budget(resolution_budget)
    except (KeyError, TypeError, ValueError):
        return _result(
            ResolutionReason.BUDGET_EXHAUSTED,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
        )

    availability = _peek_registry_availability(registry_snapshot)
    if availability is RegistryAvailability.UNAVAILABLE:
        return _result(
            ResolutionReason.REGISTRY_UNAVAILABLE,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
        )
    if availability is None:
        return _result(
            ResolutionReason.REGISTRY_CONTRACT_VIOLATION,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
        )

    try:
        snapshot = _parse_registry_snapshot(registry_snapshot)
    except (KeyError, TypeError, ValueError):
        return _result(
            ResolutionReason.REGISTRY_CONTRACT_VIOLATION,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
        )

    live_revision = snapshot.live_heads.get(parsed_ref.capability_lease_id)
    if live_revision is None:
        return _result(
            ResolutionReason.UNKNOWN_LEASE,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
        )
    if parsed_ref.capability_revision != live_revision:
        return _result(
            ResolutionReason.REVISION_MISMATCH,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
        )

    raw_record = snapshot.record_for(
        parsed_ref.capability_lease_id,
        parsed_ref.capability_revision,
    )
    if raw_record is None:  # Registry admission makes this unreachable.
        return _result(
            ResolutionReason.REGISTRY_CONTRACT_VIOLATION,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
        )

    try:
        raw_record_bytes = canonical_json_bytes(raw_record)
    except (CanonicalJSONError, TypeError, ValueError):
        raw_record_bytes = None
    if raw_record_bytes is not None and len(raw_record_bytes) > budget.max_record_bytes:
        return _result(
            ResolutionReason.BUDGET_EXHAUSTED,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
        )

    try:
        record = _parse_record(raw_record)
    except (KeyError, TypeError, ValueError):
        return _result(
            ResolutionReason.LEASE_CONTRACT_VIOLATION,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
        )

    if raw_record_bytes is None:
        return _result(
            ResolutionReason.LEASE_CONTRACT_VIOLATION,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if capability_lease_digest(record) != record.content_digest:
        return _result(
            ResolutionReason.LEASE_DIGEST_MISMATCH,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if not _semantic_invariants_hold(record):
        return _result(
            ResolutionReason.LEASE_CONTRACT_VIOLATION,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    evaluated = _as_datetime(canonical_evaluated_at)
    not_before = _as_datetime(record.not_before)
    expires_at = _as_datetime(record.expires_at)

    if record.status is LeaseStatus.EXPIRED and evaluated < expires_at:
        return _result(
            ResolutionReason.LEASE_CONTRACT_VIOLATION,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if record.status is LeaseStatus.REVOKED:
        return _result(
            ResolutionReason.LEASE_REVOKED,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if evaluated >= expires_at:
        return _result(
            ResolutionReason.LEASE_EXPIRED,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if record.status is not LeaseStatus.ACTIVE:
        return _result(
            ResolutionReason.LEASE_NOT_ACTIVE,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if evaluated < not_before:
        return _result(
            ResolutionReason.NOT_YET_VALID,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if parsed_intent.purpose_id != record.purpose_id:
        return _result(
            ResolutionReason.PURPOSE_MISMATCH,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if parsed_intent.operation_id not in record.allowed_operations:
        return _result(
            ResolutionReason.OPERATION_NOT_ALLOWED,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if (
        len(record.data_scope) > budget.max_scope_items
        or len(parsed_intent.data_scope) > budget.max_scope_items
    ):
        return _result(
            ResolutionReason.BUDGET_EXHAUSTED,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if not set(parsed_intent.data_scope).issubset(record.data_scope):
        return _result(
            ResolutionReason.DATA_SCOPE_VIOLATION,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    if not set(parsed_intent.requested_side_effects).issubset(
        record.allowed_side_effects
    ):
        return _result(
            ResolutionReason.SIDE_EFFECT_NOT_ALLOWED,
            authority_ref=parsed_ref,
            evaluated_at=canonical_evaluated_at,
            observed_live_revision=live_revision,
            record=record,
        )

    return _result(
        ResolutionReason.ALLOW,
        authority_ref=parsed_ref,
        evaluated_at=canonical_evaluated_at,
        observed_live_revision=live_revision,
        record=record,
    )


def capability_lease_digest(record: CapabilityLeaseRecord) -> str:
    """Recompute the frozen lease digest domain, excluding content_digest."""

    if not isinstance(record, CapabilityLeaseRecord):
        raise TypeError("record must be a CapabilityLeaseRecord")
    payload = record.to_value(include_content_digest=False)
    return f"sha256:{hashlib.sha256(canonical_json_bytes(payload)).hexdigest()}"


def _result(
    reason: ResolutionReason,
    *,
    authority_ref: AuthorityRef | None,
    evaluated_at: str | None,
    observed_live_revision: int | None = None,
    record: CapabilityLeaseRecord | None = None,
) -> ResolutionResult:
    decision = (
        ResolutionDecision.ALLOW
        if reason is ResolutionReason.ALLOW
        else ResolutionDecision.DENY
    )
    return ResolutionResult(
        decision=decision,
        primary_reason=reason,
        lease_id=None if authority_ref is None else authority_ref.capability_lease_id,
        requested_revision=(
            None if authority_ref is None else authority_ref.capability_revision
        ),
        observed_live_revision=observed_live_revision,
        observed_status=None if record is None else record.status,
        observed_digest=None if record is None else record.content_digest,
        evaluated_at=evaluated_at,
    )


def _require_exact_keys(
    value: Mapping[str, object], expected: set[str], name: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{name} keys must be exact; missing={sorted(expected - actual)!r}, "
            f"extra={sorted(actual - expected)!r}"
        )


def _parse_authority_ref(value: object) -> AuthorityRef:
    if isinstance(value, AuthorityRef):
        result = value
    else:
        mapping = _mapping(value, "authority_ref")
        _require_exact_keys(
            mapping,
            {"capability_lease_id", "capability_revision"},
            "authority_ref",
        )
        result = AuthorityRef(
            capability_lease_id=_string(
                mapping["capability_lease_id"], "capability_lease_id"
            ),
            capability_revision=_positive(
                mapping["capability_revision"], "capability_revision"
            ),
        )
    if result.capability_revision <= 0:
        raise ValueError("capability_revision must be positive")
    return result


def _parse_action_intent(value: object) -> ActionIntent:
    if isinstance(value, ActionIntent):
        return value
    mapping = _mapping(value, "action_intent")
    _require_exact_keys(
        mapping,
        {"purpose_id", "operation_id", "data_scope", "requested_side_effects"},
        "action_intent",
    )
    scope = tuple(
        _parse_scope_item(item, "action_intent.data_scope")
        for item in _array(mapping["data_scope"], "data_scope")
    )
    side_effects = tuple(
        _string(item, "requested_side_effects")
        for item in _array(
            mapping["requested_side_effects"], "requested_side_effects"
        )
    )
    return ActionIntent(
        purpose_id=_string(mapping["purpose_id"], "purpose_id"),
        operation_id=_string(mapping["operation_id"], "operation_id"),
        data_scope=scope,
        requested_side_effects=side_effects,
    )


def _parse_budget(value: object) -> ResolutionBudget:
    if isinstance(value, ResolutionBudget):
        return value
    mapping = _mapping(value, "resolution_budget")
    _require_exact_keys(
        mapping,
        {"max_registry_lookups", "max_record_bytes", "max_scope_items"},
        "resolution_budget",
    )
    return ResolutionBudget(
        max_registry_lookups=_positive(
            mapping["max_registry_lookups"], "max_registry_lookups"
        ),
        max_record_bytes=_positive(mapping["max_record_bytes"], "max_record_bytes"),
        max_scope_items=_positive(mapping["max_scope_items"], "max_scope_items"),
    )


def _peek_registry_availability(value: object) -> RegistryAvailability | None:
    if isinstance(value, RegistrySnapshot):
        return value.availability
    if not isinstance(value, Mapping):
        return None
    try:
        return RegistryAvailability(value.get("availability"))
    except (TypeError, ValueError):
        return None


def _parse_registry_snapshot(value: object) -> RegistrySnapshot:
    if isinstance(value, RegistrySnapshot):
        return value
    mapping = _mapping(value, "registry_snapshot")
    _require_exact_keys(
        mapping,
        {
            "availability",
            "unavailable_reason",
            "registry_schema_version",
            "live_heads",
            "records",
        },
        "registry_snapshot",
    )
    heads_mapping = _mapping(mapping["live_heads"], "live_heads")
    heads: dict[str, int] = {}
    for lease_id, revision in heads_mapping.items():
        heads[_string(lease_id, "live_heads lease_id")] = _positive(
            revision, "live head revision"
        )
    return RegistrySnapshot(
        availability=RegistryAvailability(mapping["availability"]),
        unavailable_reason=_optional_string(
            mapping["unavailable_reason"], "unavailable_reason"
        ),
        registry_schema_version=_integer(
            mapping["registry_schema_version"], "registry_schema_version"
        ),
        live_heads=heads,
        records=tuple(_array(mapping["records"], "records")),
    )


def _parse_record(value: object) -> CapabilityLeaseRecord:
    if isinstance(value, CapabilityLeaseRecord):
        return value
    mapping = _mapping(value, "capability_lease_record")
    _require_exact_keys(
        mapping,
        {
            "lease_id",
            "revision",
            "supersedes_revision",
            "status",
            "tool_id",
            "granted_by",
            "purpose_id",
            "allowed_operations",
            "data_scope",
            "allowed_side_effects",
            "not_before",
            "expires_at",
            "revocation_conditions",
            "revoked_at",
            "delegation_allowed",
            "branch_transfer_allowed",
            "audit_required",
            "identity_authority",
            "direct_m3_write",
            "content_digest",
        },
        "capability_lease_record",
    )
    granted = _mapping(mapping["granted_by"], "granted_by")
    _require_exact_keys(granted, {"actor_type", "actor_id"}, "granted_by")
    scope = tuple(
        _parse_scope_item(item, "capability_lease_record.data_scope")
        for item in _array(mapping["data_scope"], "data_scope")
    )
    return CapabilityLeaseRecord(
        lease_id=_string(mapping["lease_id"], "lease_id"),
        revision=_positive(mapping["revision"], "revision"),
        supersedes_revision=_optional_positive(
            mapping["supersedes_revision"], "supersedes_revision"
        ),
        status=LeaseStatus(mapping["status"]),
        tool_id=_optional_string(mapping["tool_id"], "tool_id"),
        granted_by=GrantedBy(
            actor_type=_string(granted["actor_type"], "actor_type"),
            actor_id=_string(granted["actor_id"], "actor_id"),
        ),
        purpose_id=_string(mapping["purpose_id"], "purpose_id"),
        allowed_operations=tuple(
            _string(item, "allowed_operations")
            for item in _array(mapping["allowed_operations"], "allowed_operations")
        ),
        data_scope=scope,
        allowed_side_effects=tuple(
            _string(item, "allowed_side_effects")
            for item in _array(
                mapping["allowed_side_effects"], "allowed_side_effects"
            )
        ),
        not_before=_string(mapping["not_before"], "not_before"),
        expires_at=_string(mapping["expires_at"], "expires_at"),
        revocation_conditions=tuple(
            _string(item, "revocation_conditions")
            for item in _array(
                mapping["revocation_conditions"], "revocation_conditions"
            )
        ),
        revoked_at=_optional_string(mapping["revoked_at"], "revoked_at"),
        delegation_allowed=_boolean(
            mapping["delegation_allowed"], "delegation_allowed"
        ),
        branch_transfer_allowed=_boolean(
            mapping["branch_transfer_allowed"], "branch_transfer_allowed"
        ),
        audit_required=_boolean(mapping["audit_required"], "audit_required"),
        identity_authority=_string(
            mapping["identity_authority"], "identity_authority"
        ),
        direct_m3_write=_boolean(mapping["direct_m3_write"], "direct_m3_write"),
        content_digest=_string(mapping["content_digest"], "content_digest"),
    )


def _parse_scope_item(value: object, name: str) -> ScopeItem:
    if isinstance(value, ScopeItem):
        return value
    mapping = _mapping(value, name)
    _require_exact_keys(mapping, {"kind", "identifier"}, name)
    return ScopeItem(
        kind=_string(mapping["kind"], "kind"),
        identifier=_string(mapping["identifier"], "identifier"),
    )


def _parse_evaluated_at(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("evaluated_at must be a string")
    canonical = canonical_timestamp(value)
    if canonical != value or not value.endswith("Z"):
        raise ValueError("evaluated_at must use canonical UTC Z form")
    return canonical


def _semantic_invariants_hold(record: CapabilityLeaseRecord) -> bool:
    if record.revision == 1:
        if record.supersedes_revision is not None:
            return False
    elif record.supersedes_revision != record.revision - 1:
        return False
    if _as_datetime(record.not_before) >= _as_datetime(record.expires_at):
        return False
    if record.delegation_allowed or record.branch_transfer_allowed:
        return False
    if not record.audit_required:
        return False
    if record.identity_authority != "NONE" or record.direct_m3_write:
        return False
    if (record.status is LeaseStatus.REVOKED) != (record.revoked_at is not None):
        return False
    return True


def _as_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value[:-1] + "+00:00")


def _mapping(value: object, name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be an object")
    if any(not isinstance(key, str) for key in value):
        raise TypeError(f"{name} keys must be strings")
    return value


def _array(value: object, name: str) -> Sequence[object]:
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"{name} must be an array")
    return value


def _string(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _optional_string(value: object, name: str) -> str | None:
    if value is None:
        return None
    return _string(value, name)


def _integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    return value


def _positive(value: object, name: str) -> int:
    result = _integer(value, name)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _optional_positive(value: object, name: str) -> int | None:
    if value is None:
        return None
    return _positive(value, name)


def _boolean(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be boolean")
    return value


__all__ = ["capability_lease_digest", "resolve_capability_lease"]
