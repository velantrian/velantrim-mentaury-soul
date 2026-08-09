"""P1-001 pure Capability Lease resolution contracts."""

from __future__ import annotations

import copy
import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from mentaury.contracts import AuthorityRef, canonical_timestamp
from mentaury.validation import SHA256_DIGEST_PATTERN

RESOLVER_CONTRACT_VERSION: Final[str] = "P1-001-v0.2"
REGISTRY_SCHEMA_VERSION: Final[int] = 1

_SHA256_RE = re.compile(f"{SHA256_DIGEST_PATTERN}\\Z")


class RegistryAvailability(StrEnum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"


class LeaseStatus(StrEnum):
    PROPOSED = "PROPOSED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"
    SUPERSEDED = "SUPERSEDED"
    UNVERIFIED = "UNVERIFIED"


class ResolutionDecision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class ResolutionReason(StrEnum):
    REQUEST_INVALID = "REQUEST_INVALID"
    BUDGET_MISSING = "BUDGET_MISSING"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    REGISTRY_UNAVAILABLE = "REGISTRY_UNAVAILABLE"
    REGISTRY_CONTRACT_VIOLATION = "REGISTRY_CONTRACT_VIOLATION"
    UNKNOWN_LEASE = "UNKNOWN_LEASE"
    REVISION_MISMATCH = "REVISION_MISMATCH"
    LEASE_CONTRACT_VIOLATION = "LEASE_CONTRACT_VIOLATION"
    LEASE_DIGEST_MISMATCH = "LEASE_DIGEST_MISMATCH"
    LEASE_REVOKED = "LEASE_REVOKED"
    LEASE_EXPIRED = "LEASE_EXPIRED"
    LEASE_NOT_ACTIVE = "LEASE_NOT_ACTIVE"
    NOT_YET_VALID = "NOT_YET_VALID"
    PURPOSE_MISMATCH = "PURPOSE_MISMATCH"
    OPERATION_NOT_ALLOWED = "OPERATION_NOT_ALLOWED"
    DATA_SCOPE_VIOLATION = "DATA_SCOPE_VIOLATION"
    SIDE_EFFECT_NOT_ALLOWED = "SIDE_EFFECT_NOT_ALLOWED"
    ALLOW = "ALLOW"


def _require_non_empty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _require_positive(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _canonical_utc_z(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    try:
        canonical = canonical_timestamp(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a canonical UTC timestamp") from exc
    if canonical != value or not value.endswith("Z"):
        raise ValueError(f"{name} must use canonical UTC Z form")
    return canonical


def _canonical_strings(
    values: object,
    name: str,
    *,
    require_sorted: bool,
) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise TypeError(f"{name} must be an array")
    result = tuple(_require_non_empty(item, name) for item in values)
    if len(set(result)) != len(result):
        raise ValueError(f"{name} must be unique")
    canonical = tuple(sorted(result))
    if require_sorted and canonical != result:
        raise ValueError(f"{name} must be sorted")
    return result if require_sorted else canonical


@dataclass(frozen=True, slots=True, order=True)
class ScopeItem:
    kind: str
    identifier: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _require_non_empty(self.kind, "kind"))
        object.__setattr__(
            self, "identifier", _require_non_empty(self.identifier, "identifier")
        )

    def to_value(self) -> dict[str, object]:
        return {"kind": self.kind, "identifier": self.identifier}


@dataclass(frozen=True, slots=True)
class GrantedBy:
    actor_type: str
    actor_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "actor_type", _require_non_empty(self.actor_type, "actor_type")
        )
        object.__setattr__(
            self, "actor_id", _require_non_empty(self.actor_id, "actor_id")
        )

    def to_value(self) -> dict[str, object]:
        return {"actor_type": self.actor_type, "actor_id": self.actor_id}


@dataclass(frozen=True, slots=True)
class ActionIntent:
    purpose_id: str
    operation_id: str
    data_scope: tuple[ScopeItem, ...]
    requested_side_effects: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "purpose_id", _require_non_empty(self.purpose_id, "purpose_id")
        )
        object.__setattr__(
            self, "operation_id", _require_non_empty(self.operation_id, "operation_id")
        )
        scope = tuple(self.data_scope)
        if any(not isinstance(item, ScopeItem) for item in scope):
            raise TypeError("data_scope must contain ScopeItem values")
        if len(set(scope)) != len(scope):
            raise ValueError("data_scope must be unique")
        object.__setattr__(self, "data_scope", tuple(sorted(scope)))
        object.__setattr__(
            self,
            "requested_side_effects",
            _canonical_strings(
                self.requested_side_effects,
                "requested_side_effects",
                require_sorted=False,
            ),
        )

    def to_value(self) -> dict[str, object]:
        return {
            "purpose_id": self.purpose_id,
            "operation_id": self.operation_id,
            "data_scope": [item.to_value() for item in self.data_scope],
            "requested_side_effects": list(self.requested_side_effects),
        }


@dataclass(frozen=True, slots=True)
class ResolutionBudget:
    max_registry_lookups: int
    max_record_bytes: int
    max_scope_items: int

    def __post_init__(self) -> None:
        for name in (
            "max_registry_lookups",
            "max_record_bytes",
            "max_scope_items",
        ):
            object.__setattr__(self, name, _require_positive(getattr(self, name), name))

    def to_value(self) -> dict[str, object]:
        return {
            "max_registry_lookups": self.max_registry_lookups,
            "max_record_bytes": self.max_record_bytes,
            "max_scope_items": self.max_scope_items,
        }


@dataclass(frozen=True, slots=True)
class CapabilityLeaseRecord:
    lease_id: str
    revision: int
    supersedes_revision: int | None
    status: LeaseStatus
    tool_id: str | None
    granted_by: GrantedBy
    purpose_id: str
    allowed_operations: tuple[str, ...]
    data_scope: tuple[ScopeItem, ...]
    allowed_side_effects: tuple[str, ...]
    not_before: str
    expires_at: str
    revocation_conditions: tuple[str, ...]
    revoked_at: str | None
    delegation_allowed: bool
    branch_transfer_allowed: bool
    audit_required: bool
    identity_authority: str
    direct_m3_write: bool
    content_digest: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "lease_id", _require_non_empty(self.lease_id, "lease_id")
        )
        object.__setattr__(self, "revision", _require_positive(self.revision, "revision"))
        if self.supersedes_revision is not None:
            object.__setattr__(
                self,
                "supersedes_revision",
                _require_positive(self.supersedes_revision, "supersedes_revision"),
            )
        if not isinstance(self.status, LeaseStatus):
            raise TypeError("status must be a LeaseStatus")
        if self.tool_id is not None:
            object.__setattr__(self, "tool_id", _require_non_empty(self.tool_id, "tool_id"))
        if not isinstance(self.granted_by, GrantedBy):
            raise TypeError("granted_by must be GrantedBy")
        object.__setattr__(
            self, "purpose_id", _require_non_empty(self.purpose_id, "purpose_id")
        )
        object.__setattr__(
            self,
            "allowed_operations",
            _canonical_strings(
                self.allowed_operations,
                "allowed_operations",
                require_sorted=True,
            ),
        )
        scope = tuple(self.data_scope)
        if any(not isinstance(item, ScopeItem) for item in scope):
            raise TypeError("data_scope must contain ScopeItem values")
        if tuple(sorted(set(scope))) != scope:
            raise ValueError("data_scope must be sorted and unique")
        object.__setattr__(self, "data_scope", scope)
        object.__setattr__(
            self,
            "allowed_side_effects",
            _canonical_strings(
                self.allowed_side_effects,
                "allowed_side_effects",
                require_sorted=True,
            ),
        )
        object.__setattr__(self, "not_before", _canonical_utc_z(self.not_before, "not_before"))
        object.__setattr__(self, "expires_at", _canonical_utc_z(self.expires_at, "expires_at"))
        object.__setattr__(
            self,
            "revocation_conditions",
            _canonical_strings(
                self.revocation_conditions,
                "revocation_conditions",
                require_sorted=True,
            ),
        )
        if self.revoked_at is not None:
            object.__setattr__(self, "revoked_at", _canonical_utc_z(self.revoked_at, "revoked_at"))
        for name in (
            "delegation_allowed",
            "branch_transfer_allowed",
            "audit_required",
            "direct_m3_write",
        ):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be boolean")
        object.__setattr__(
            self,
            "identity_authority",
            _require_non_empty(self.identity_authority, "identity_authority"),
        )
        if (
            not isinstance(self.content_digest, str)
            or not _SHA256_RE.fullmatch(self.content_digest)
        ):
            raise ValueError("content_digest must be a lowercase sha256 digest")

    def to_value(self, *, include_content_digest: bool = True) -> dict[str, object]:
        value: dict[str, object] = {
            "lease_id": self.lease_id,
            "revision": self.revision,
            "supersedes_revision": self.supersedes_revision,
            "status": self.status.value,
            "tool_id": self.tool_id,
            "granted_by": self.granted_by.to_value(),
            "purpose_id": self.purpose_id,
            "allowed_operations": list(self.allowed_operations),
            "data_scope": [item.to_value() for item in self.data_scope],
            "allowed_side_effects": list(self.allowed_side_effects),
            "not_before": self.not_before,
            "expires_at": self.expires_at,
            "revocation_conditions": list(self.revocation_conditions),
            "revoked_at": self.revoked_at,
            "delegation_allowed": self.delegation_allowed,
            "branch_transfer_allowed": self.branch_transfer_allowed,
            "audit_required": self.audit_required,
            "identity_authority": self.identity_authority,
            "direct_m3_write": self.direct_m3_write,
        }
        if include_content_digest:
            value["content_digest"] = self.content_digest
        return value


@dataclass(frozen=True, slots=True)
class RegistrySnapshot:
    availability: RegistryAvailability
    unavailable_reason: str | None
    registry_schema_version: int
    live_heads: Mapping[str, int]
    records: tuple[Mapping[str, object], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.availability, RegistryAvailability):
            raise TypeError("availability must be RegistryAvailability")
        if (
            isinstance(self.registry_schema_version, bool)
            or not isinstance(self.registry_schema_version, int)
            or self.registry_schema_version != REGISTRY_SCHEMA_VERSION
        ):
            raise ValueError("unsupported registry_schema_version")
        if not isinstance(self.live_heads, Mapping):
            raise TypeError("live_heads must be an object")
        heads: dict[str, int] = {}
        for lease_id, revision in self.live_heads.items():
            lease_key = _require_non_empty(lease_id, "live_heads lease_id")
            heads[lease_key] = _require_positive(revision, "live head revision")

        raw_records = tuple(self.records)
        indexed: dict[tuple[str, int], Mapping[str, object]] = {}
        frozen_records: list[Mapping[str, object]] = []
        for raw in raw_records:
            if not isinstance(raw, Mapping):
                raise TypeError("records must contain objects")
            lease_id = _require_non_empty(raw.get("lease_id"), "record lease_id")
            revision = _require_positive(raw.get("revision"), "record revision")
            key = (lease_id, revision)
            if key in indexed:
                raise ValueError("duplicate registry record key")
            detached = copy.deepcopy(dict(raw))
            frozen = MappingProxyType(detached)
            indexed[key] = frozen
            frozen_records.append(frozen)

        if self.availability is RegistryAvailability.AVAILABLE:
            if self.unavailable_reason is not None:
                raise ValueError("AVAILABLE snapshot must not carry unavailable_reason")
            for lease_id, revision in heads.items():
                if (lease_id, revision) not in indexed:
                    raise ValueError("live head must point to an exact record")
        else:
            _require_non_empty(self.unavailable_reason, "unavailable_reason")
            if heads or frozen_records:
                raise ValueError("UNAVAILABLE snapshot cannot carry grantable records")

        object.__setattr__(
            self, "live_heads", MappingProxyType(dict(sorted(heads.items())))
        )
        object.__setattr__(self, "records", tuple(frozen_records))

    def record_for(self, lease_id: str, revision: int) -> Mapping[str, object] | None:
        for record in self.records:
            if record.get("lease_id") == lease_id and record.get("revision") == revision:
                return record
        return None


@dataclass(frozen=True, slots=True)
class ResolutionResult:
    decision: ResolutionDecision
    primary_reason: ResolutionReason
    lease_id: str | None
    requested_revision: int | None
    observed_live_revision: int | None
    observed_status: LeaseStatus | None
    observed_digest: str | None
    evaluated_at: str | None
    resolver_contract_version: str = RESOLVER_CONTRACT_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.decision, ResolutionDecision):
            raise TypeError("decision must be ResolutionDecision")
        if not isinstance(self.primary_reason, ResolutionReason):
            raise TypeError("primary_reason must be ResolutionReason")
        if self.decision is ResolutionDecision.ALLOW:
            if self.primary_reason is not ResolutionReason.ALLOW:
                raise ValueError("ALLOW decision requires ALLOW primary_reason")
        elif self.primary_reason is ResolutionReason.ALLOW:
            raise ValueError("DENY decision cannot carry ALLOW primary_reason")
        if self.lease_id is not None:
            _require_non_empty(self.lease_id, "lease_id")
        for name in ("requested_revision", "observed_live_revision"):
            value = getattr(self, name)
            if value is not None:
                _require_positive(value, name)
        if self.observed_status is not None and not isinstance(
            self.observed_status, LeaseStatus
        ):
            raise TypeError("observed_status must be LeaseStatus")
        if self.observed_digest is not None and (
            not isinstance(self.observed_digest, str)
            or not _SHA256_RE.fullmatch(self.observed_digest)
        ):
            raise ValueError("observed_digest must be a lowercase sha256 digest")
        if self.evaluated_at is not None:
            _canonical_utc_z(self.evaluated_at, "evaluated_at")
        if self.resolver_contract_version != RESOLVER_CONTRACT_VERSION:
            raise ValueError("unsupported resolver contract version")

    def to_value(self) -> dict[str, object]:
        return {
            "decision": self.decision.value,
            "primary_reason": self.primary_reason.value,
            "lease_id": self.lease_id,
            "requested_revision": self.requested_revision,
            "observed_live_revision": self.observed_live_revision,
            "observed_status": (
                None if self.observed_status is None else self.observed_status.value
            ),
            "observed_digest": self.observed_digest,
            "evaluated_at": self.evaluated_at,
            "resolver_contract_version": self.resolver_contract_version,
        }


__all__ = [
    "ActionIntent",
    "AuthorityRef",
    "CapabilityLeaseRecord",
    "GrantedBy",
    "LeaseStatus",
    "REGISTRY_SCHEMA_VERSION",
    "RESOLVER_CONTRACT_VERSION",
    "RegistryAvailability",
    "RegistrySnapshot",
    "ResolutionBudget",
    "ResolutionDecision",
    "ResolutionReason",
    "ResolutionResult",
    "ScopeItem",
]
