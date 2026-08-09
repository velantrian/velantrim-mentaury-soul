"""Immutable contracts for the bounded P1-002 privacy classifier."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Final, TypeVar

CLASSIFIER_CONTRACT_VERSION: Final[str] = "P1-002-v0.1"


class PrivacyContractError(ValueError):
    """Raised when caller-supplied privacy values violate the frozen contract."""


class PrivacyClass(StrEnum):
    PUBLIC = "PUBLIC"
    PERSONAL = "PERSONAL"
    SENSITIVE = "SENSITIVE"
    INTIMATE = "INTIMATE"
    RESTRICTED = "RESTRICTED"
    THIRD_PARTY = "THIRD_PARTY"
    REDACTED = "REDACTED"


class MaterialState(StrEnum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    REDACTED = "REDACTED"
    RESTRICTED = "RESTRICTED"


class SurfaceKind(StrEnum):
    PRIMARY = "PRIMARY"
    BACKUP = "BACKUP"
    INDEX = "INDEX"
    EMBEDDING = "EMBEDDING"
    GRAPH_EDGE = "GRAPH_EDGE"
    CACHE = "CACHE"
    DERIVED_SUMMARY = "DERIVED_SUMMARY"
    FORK = "FORK"


class CopyState(StrEnum):
    PRESENT = "PRESENT"
    QUARANTINED = "QUARANTINED"
    REBUILT = "REBUILT"
    ABSENT = "ABSENT"


class PrivacyDecision(StrEnum):
    ALLOW_REFERENCE = "ALLOW_REFERENCE"
    DENY_RETRIEVAL = "DENY_RETRIEVAL"
    QUARANTINE_REQUIRED = "QUARANTINE_REQUIRED"
    REBUILD_REQUIRED = "REBUILD_REQUIRED"


class PrivacyReason(StrEnum):
    INPUT_CONTRACT_VIOLATION = "INPUT_CONTRACT_VIOLATION"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    COPY_ABSENT = "COPY_ABSENT"
    COPY_ALREADY_QUARANTINED = "COPY_ALREADY_QUARANTINED"
    DELETED_OR_REDACTED_MATERIAL = "DELETED_OR_REDACTED_MATERIAL"
    THIRD_PARTY_PERMISSION_MISSING = "THIRD_PARTY_PERMISSION_MISSING"
    PURPOSE_WITHDRAWN = "PURPOSE_WITHDRAWN"
    PURPOSE_NOT_PERMITTED = "PURPOSE_NOT_PERMITTED"
    BRANCH_NOT_PERMITTED = "BRANCH_NOT_PERMITTED"
    STALE_POLICY_REVISION = "STALE_POLICY_REVISION"
    ALLOW_REFERENCE = "ALLOW_REFERENCE"


EnumT = TypeVar("EnumT", bound=StrEnum)


def _require_exact_mapping(
    value: object, *, name: str, fields: frozenset[str]
) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise PrivacyContractError(f"{name} must be an object")
    keys = set(value.keys())
    if any(not isinstance(key, str) for key in value.keys()):
        raise PrivacyContractError(f"{name} keys must be strings")
    missing = fields - keys
    unknown = keys - fields
    if missing:
        raise PrivacyContractError(f"{name} missing fields: {sorted(missing)}")
    if unknown:
        raise PrivacyContractError(f"{name} unknown fields: {sorted(unknown)}")
    return value


def _require_non_empty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise PrivacyContractError(f"{name} must be a non-empty unpadded string")
    return value


def _require_positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise PrivacyContractError(f"{name} must be a positive integer")
    return value


def _require_bool(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise PrivacyContractError(f"{name} must be boolean")
    return value


def _require_enum(value: object, enum_type: type[EnumT], name: str) -> EnumT:
    if isinstance(value, enum_type):
        return value
    if not isinstance(value, str):
        raise PrivacyContractError(f"{name} must be a string enum value")
    try:
        return enum_type(value)
    except ValueError as exc:
        raise PrivacyContractError(f"unsupported {name}: {value}") from exc


def _require_canonical_strings(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, (tuple, list)):
        raise PrivacyContractError(f"{name} must be an array")
    result = tuple(_require_non_empty(item, name) for item in value)
    if len(set(result)) != len(result):
        raise PrivacyContractError(f"{name} must be unique")
    if tuple(sorted(result)) != result:
        raise PrivacyContractError(f"{name} must be sorted")
    return result


@dataclass(frozen=True, slots=True)
class PrivacyMaterial:
    material_id: str
    privacy_class: PrivacyClass
    state: MaterialState
    policy_revision: int
    permitted_purposes: tuple[str, ...]
    withdrawn_purposes: tuple[str, ...]
    permitted_branches: tuple[str, ...]
    third_party_permission: bool

    _FIELDS: Final[frozenset[str]] = frozenset(
        {
            "material_id",
            "privacy_class",
            "state",
            "policy_revision",
            "permitted_purposes",
            "withdrawn_purposes",
            "permitted_branches",
            "third_party_permission",
        }
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "material_id", _require_non_empty(self.material_id, "material_id")
        )
        object.__setattr__(
            self,
            "privacy_class",
            _require_enum(self.privacy_class, PrivacyClass, "privacy_class"),
        )
        object.__setattr__(
            self, "state", _require_enum(self.state, MaterialState, "state")
        )
        object.__setattr__(
            self,
            "policy_revision",
            _require_positive_int(self.policy_revision, "policy_revision"),
        )
        permitted = _require_canonical_strings(
            self.permitted_purposes, "permitted_purposes"
        )
        withdrawn = _require_canonical_strings(
            self.withdrawn_purposes, "withdrawn_purposes"
        )
        branches = _require_canonical_strings(
            self.permitted_branches, "permitted_branches"
        )
        if set(permitted) & set(withdrawn):
            raise PrivacyContractError(
                "a purpose cannot be both permitted and withdrawn"
            )
        object.__setattr__(self, "permitted_purposes", permitted)
        object.__setattr__(self, "withdrawn_purposes", withdrawn)
        object.__setattr__(self, "permitted_branches", branches)
        object.__setattr__(
            self,
            "third_party_permission",
            _require_bool(self.third_party_permission, "third_party_permission"),
        )

    @classmethod
    def from_value(cls, value: object) -> "PrivacyMaterial":
        if isinstance(value, cls):
            return value
        mapping = _require_exact_mapping(value, name="material", fields=cls._FIELDS)
        return cls(
            material_id=mapping["material_id"],
            privacy_class=mapping["privacy_class"],
            state=mapping["state"],
            policy_revision=mapping["policy_revision"],
            permitted_purposes=mapping["permitted_purposes"],
            withdrawn_purposes=mapping["withdrawn_purposes"],
            permitted_branches=mapping["permitted_branches"],
            third_party_permission=mapping["third_party_permission"],
        )

    def to_value(self) -> dict[str, object]:
        return {
            "material_id": self.material_id,
            "privacy_class": self.privacy_class.value,
            "state": self.state.value,
            "policy_revision": self.policy_revision,
            "permitted_purposes": list(self.permitted_purposes),
            "withdrawn_purposes": list(self.withdrawn_purposes),
            "permitted_branches": list(self.permitted_branches),
            "third_party_permission": self.third_party_permission,
        }


@dataclass(frozen=True, slots=True)
class PrivacyCopy:
    copy_id: str
    material_id: str
    branch_id: str
    surface: SurfaceKind
    policy_revision: int
    state: CopyState
    contains_material: bool

    _FIELDS: Final[frozenset[str]] = frozenset(
        {
            "copy_id",
            "material_id",
            "branch_id",
            "surface",
            "policy_revision",
            "state",
            "contains_material",
        }
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "copy_id", _require_non_empty(self.copy_id, "copy_id"))
        object.__setattr__(
            self, "material_id", _require_non_empty(self.material_id, "material_id")
        )
        object.__setattr__(
            self, "branch_id", _require_non_empty(self.branch_id, "branch_id")
        )
        object.__setattr__(
            self, "surface", _require_enum(self.surface, SurfaceKind, "surface")
        )
        object.__setattr__(
            self,
            "policy_revision",
            _require_positive_int(self.policy_revision, "policy_revision"),
        )
        object.__setattr__(self, "state", _require_enum(self.state, CopyState, "state"))
        object.__setattr__(
            self,
            "contains_material",
            _require_bool(self.contains_material, "contains_material"),
        )
        if self.state is CopyState.ABSENT and self.contains_material:
            raise PrivacyContractError("ABSENT copy cannot contain material")
        if self.state is not CopyState.ABSENT and not self.contains_material:
            raise PrivacyContractError(
                "PRESENT, QUARANTINED, and REBUILT copies must contain material"
            )

    @classmethod
    def from_value(cls, value: object) -> "PrivacyCopy":
        if isinstance(value, cls):
            return value
        mapping = _require_exact_mapping(value, name="copy", fields=cls._FIELDS)
        return cls(
            copy_id=mapping["copy_id"],
            material_id=mapping["material_id"],
            branch_id=mapping["branch_id"],
            surface=mapping["surface"],
            policy_revision=mapping["policy_revision"],
            state=mapping["state"],
            contains_material=mapping["contains_material"],
        )

    def to_value(self) -> dict[str, object]:
        return {
            "copy_id": self.copy_id,
            "material_id": self.material_id,
            "branch_id": self.branch_id,
            "surface": self.surface.value,
            "policy_revision": self.policy_revision,
            "state": self.state.value,
            "contains_material": self.contains_material,
        }


@dataclass(frozen=True, slots=True)
class PrivacyAccessIntent:
    copy_id: str
    branch_id: str
    purpose: str

    _FIELDS: Final[frozenset[str]] = frozenset({"copy_id", "branch_id", "purpose"})

    def __post_init__(self) -> None:
        object.__setattr__(self, "copy_id", _require_non_empty(self.copy_id, "copy_id"))
        object.__setattr__(
            self, "branch_id", _require_non_empty(self.branch_id, "branch_id")
        )
        object.__setattr__(self, "purpose", _require_non_empty(self.purpose, "purpose"))

    @classmethod
    def from_value(cls, value: object) -> "PrivacyAccessIntent":
        if isinstance(value, cls):
            return value
        mapping = _require_exact_mapping(value, name="intent", fields=cls._FIELDS)
        return cls(
            copy_id=mapping["copy_id"],
            branch_id=mapping["branch_id"],
            purpose=mapping["purpose"],
        )

    def to_value(self) -> dict[str, object]:
        return {
            "copy_id": self.copy_id,
            "branch_id": self.branch_id,
            "purpose": self.purpose,
        }


@dataclass(frozen=True, slots=True)
class PrivacyReconciliationBudget:
    max_serialized_bytes: int
    max_purposes: int
    max_branches: int

    _FIELDS: Final[frozenset[str]] = frozenset(
        {"max_serialized_bytes", "max_purposes", "max_branches"}
    )

    def __post_init__(self) -> None:
        for name in self._FIELDS:
            object.__setattr__(
                self, name, _require_positive_int(getattr(self, name), name)
            )

    @classmethod
    def from_value(cls, value: object) -> "PrivacyReconciliationBudget":
        if isinstance(value, cls):
            return value
        mapping = _require_exact_mapping(value, name="budget", fields=cls._FIELDS)
        return cls(
            max_serialized_bytes=mapping["max_serialized_bytes"],
            max_purposes=mapping["max_purposes"],
            max_branches=mapping["max_branches"],
        )

    def to_value(self) -> dict[str, object]:
        return {
            "max_serialized_bytes": self.max_serialized_bytes,
            "max_purposes": self.max_purposes,
            "max_branches": self.max_branches,
        }


@dataclass(frozen=True, slots=True)
class PrivacyReconciliationResult:
    decision: PrivacyDecision
    reason: PrivacyReason

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "decision", _require_enum(self.decision, PrivacyDecision, "decision")
        )
        object.__setattr__(
            self, "reason", _require_enum(self.reason, PrivacyReason, "reason")
        )
        if self.decision is PrivacyDecision.ALLOW_REFERENCE:
            if self.reason is not PrivacyReason.ALLOW_REFERENCE:
                raise PrivacyContractError(
                    "ALLOW_REFERENCE decision requires ALLOW_REFERENCE reason"
                )
        elif self.reason is PrivacyReason.ALLOW_REFERENCE:
            raise PrivacyContractError(
                "non-allow decision cannot carry ALLOW_REFERENCE reason"
            )

    def to_value(self) -> dict[str, str]:
        return {"decision": self.decision.value, "reason": self.reason.value}
