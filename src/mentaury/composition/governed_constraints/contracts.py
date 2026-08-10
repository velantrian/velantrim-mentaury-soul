"""Frozen value contracts for the pure P1-003 governed constraint composer."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from mentaury.capabilities import (
    RegistrySnapshot,
    ResolutionBudget,
    ResolutionDecision,
    ResolutionReason,
    ResolutionResult,
    ScopeItem,
)
from mentaury.contracts import AuthorityRef, canonical_timestamp
from mentaury.privacy.reconciliation import (
    PrivacyCopy,
    PrivacyDecision,
    PrivacyMaterial,
    PrivacyReason,
    PrivacyReconciliationBudget,
    PrivacyReconciliationResult,
)

COMPOSER_CONTRACT_VERSION: Final[str] = "P1-003-v0.1"
BINDING_CONTRACT_VERSION: Final[str] = "CROSS-GATE-BINDING-v0.1"
CANONICAL_PROFILE: Final[str] = "MENTAURY_CANONICAL_JSON_V1"
COMMON_REQUEST_DOMAIN: Final[str] = "MENTAURY_P1_003_COMMON_REQUEST_V1"
EVALUATION_EVIDENCE_DOMAIN: Final[str] = "MENTAURY_P1_003_EVALUATION_EVIDENCE_V1"
P1_001_EXPECTED_VERSION: Final[str] = "P1-001-v0.2"
P1_002_EXPECTED_VERSION: Final[str] = "P1-002-v0.1"
SOURCE_PROVENANCE_SCOPE: Final[str] = "CALLER_SUPPLIED_VALUE_EVIDENCE_ONLY"

_SHA256_HEX_RE = re.compile(r"[0-9a-f]{64}\Z")


class GovernedConstraintContractError(ValueError):
    """Raised when a P1-003 public value violates the frozen contract."""


class GovernedConstraintDecision(StrEnum):
    ELIGIBLE_FOR_NEXT_GATE = "ELIGIBLE_FOR_NEXT_GATE"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"
    DEFER = "DEFER"


class GovernedConstraintReason(StrEnum):
    ELIGIBLE_FOR_NEXT_GATE = "ELIGIBLE_FOR_NEXT_GATE"
    COMMON_BINDING_MISMATCH = "COMMON_BINDING_MISMATCH"
    BINDING_CANONICALIZATION_FAILED = "BINDING_CANONICALIZATION_FAILED"
    EVIDENCE_CANONICALIZATION_FAILED = "EVIDENCE_CANONICALIZATION_FAILED"
    COMPOSITION_BUDGET_EXHAUSTED = "COMPOSITION_BUDGET_EXHAUSTED"
    GATE_VERSION_UNVERIFIED = "GATE_VERSION_UNVERIFIED"
    GATE_CONTRACT_UNVERIFIED = "GATE_CONTRACT_UNVERIFIED"
    CAPABILITY_BLOCKED = "CAPABILITY_BLOCKED"
    PRIVACY_BLOCKED = "PRIVACY_BLOCKED"
    CAPABILITY_AND_PRIVACY_BLOCKED = "CAPABILITY_AND_PRIVACY_BLOCKED"
    CAPABILITY_DEFERRED = "CAPABILITY_DEFERRED"
    PRIVACY_DEFERRED = "PRIVACY_DEFERRED"
    CAPABILITY_AND_PRIVACY_DEFERRED = "CAPABILITY_AND_PRIVACY_DEFERRED"


def _require_unpadded_string(value: object, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise GovernedConstraintContractError(
            f"{name} must be a non-empty unpadded string"
        )
    return value


def _require_positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise GovernedConstraintContractError(f"{name} must be a positive integer")
    return value


@dataclass(frozen=True, slots=True)
class CompositionBudget:
    max_common_request_bytes: int
    max_evidence_bytes: int
    max_scope_items: int
    max_side_effects: int

    def __post_init__(self) -> None:
        for name in (
            "max_common_request_bytes",
            "max_evidence_bytes",
            "max_scope_items",
            "max_side_effects",
        ):
            object.__setattr__(
                self,
                name,
                _require_positive_int(getattr(self, name), name),
            )

    def to_value(self) -> dict[str, int]:
        return {
            "max_common_request_bytes": self.max_common_request_bytes,
            "max_evidence_bytes": self.max_evidence_bytes,
            "max_scope_items": self.max_scope_items,
            "max_side_effects": self.max_side_effects,
        }


@dataclass(frozen=True, slots=True)
class CrossGateEvaluationContext:
    request_id: str
    purpose_id: str
    operation_id: str
    data_scope: tuple[ScopeItem, ...]
    requested_side_effects: tuple[str, ...]
    branch_id: str
    evaluated_at: str
    authority_ref: AuthorityRef
    registry_snapshot: RegistrySnapshot
    privacy_material: PrivacyMaterial
    privacy_copy: PrivacyCopy
    capability_budget: ResolutionBudget
    privacy_budget: PrivacyReconciliationBudget
    composition_budget: CompositionBudget

    def __post_init__(self) -> None:
        for name in ("request_id", "purpose_id", "operation_id", "branch_id"):
            _require_unpadded_string(getattr(self, name), name)

        if not isinstance(self.data_scope, tuple):
            raise GovernedConstraintContractError("data_scope must be a tuple")
        if any(type(item) is not ScopeItem for item in self.data_scope):
            raise GovernedConstraintContractError(
                "data_scope must contain only ScopeItem values"
            )
        if len(set(self.data_scope)) != len(self.data_scope):
            raise GovernedConstraintContractError("data_scope must be unique")
        if tuple(sorted(self.data_scope)) != self.data_scope:
            raise GovernedConstraintContractError("data_scope must already be sorted")

        if not isinstance(self.requested_side_effects, tuple):
            raise GovernedConstraintContractError(
                "requested_side_effects must be a tuple"
            )
        for side_effect in self.requested_side_effects:
            _require_unpadded_string(side_effect, "requested_side_effects")
        if len(set(self.requested_side_effects)) != len(self.requested_side_effects):
            raise GovernedConstraintContractError(
                "requested_side_effects must be unique"
            )
        if tuple(sorted(self.requested_side_effects)) != self.requested_side_effects:
            raise GovernedConstraintContractError(
                "requested_side_effects must already be sorted"
            )

        if not isinstance(self.evaluated_at, str):
            raise GovernedConstraintContractError("evaluated_at must be a string")
        try:
            canonical = canonical_timestamp(self.evaluated_at)
        except (TypeError, ValueError) as exc:
            raise GovernedConstraintContractError(
                "evaluated_at must be canonical UTC Z form"
            ) from exc
        if canonical != self.evaluated_at or not self.evaluated_at.endswith("Z"):
            raise GovernedConstraintContractError(
                "evaluated_at must be canonical UTC Z form"
            )

        exact_types = (
            ("authority_ref", self.authority_ref, AuthorityRef),
            ("registry_snapshot", self.registry_snapshot, RegistrySnapshot),
            ("privacy_material", self.privacy_material, PrivacyMaterial),
            ("privacy_copy", self.privacy_copy, PrivacyCopy),
            ("capability_budget", self.capability_budget, ResolutionBudget),
            (
                "privacy_budget",
                self.privacy_budget,
                PrivacyReconciliationBudget,
            ),
            ("composition_budget", self.composition_budget, CompositionBudget),
        )
        for name, value, expected_type in exact_types:
            if type(value) is not expected_type:
                raise GovernedConstraintContractError(
                    f"{name} must be exact {expected_type.__name__}"
                )

        if self.privacy_copy.material_id != self.privacy_material.material_id:
            raise GovernedConstraintContractError(
                "privacy_copy.material_id must equal privacy_material.material_id"
            )
        if self.privacy_copy.branch_id != self.branch_id:
            raise GovernedConstraintContractError(
                "privacy_copy.branch_id must equal branch_id"
            )
        if self.privacy_copy.policy_revision > self.privacy_material.policy_revision:
            raise GovernedConstraintContractError(
                "privacy_copy.policy_revision cannot be ahead of privacy_material"
            )


_NOT_ELIGIBLE_REASONS: Final[frozenset[GovernedConstraintReason]] = frozenset(
    {
        GovernedConstraintReason.COMMON_BINDING_MISMATCH,
        GovernedConstraintReason.BINDING_CANONICALIZATION_FAILED,
        GovernedConstraintReason.EVIDENCE_CANONICALIZATION_FAILED,
        GovernedConstraintReason.CAPABILITY_BLOCKED,
        GovernedConstraintReason.PRIVACY_BLOCKED,
        GovernedConstraintReason.CAPABILITY_AND_PRIVACY_BLOCKED,
    }
)
_DEFER_REASONS: Final[frozenset[GovernedConstraintReason]] = frozenset(
    {
        GovernedConstraintReason.COMPOSITION_BUDGET_EXHAUSTED,
        GovernedConstraintReason.GATE_VERSION_UNVERIFIED,
        GovernedConstraintReason.GATE_CONTRACT_UNVERIFIED,
        GovernedConstraintReason.CAPABILITY_DEFERRED,
        GovernedConstraintReason.PRIVACY_DEFERRED,
        GovernedConstraintReason.CAPABILITY_AND_PRIVACY_DEFERRED,
    }
)


@dataclass(frozen=True, slots=True)
class GovernedConstraintResult:
    decision: GovernedConstraintDecision
    primary_reason: GovernedConstraintReason
    common_request_fingerprint: str | None
    evaluation_evidence_fingerprint: str | None
    capability_result: ResolutionResult | None
    privacy_result: PrivacyReconciliationResult | None
    composer_contract_version: str = COMPOSER_CONTRACT_VERSION
    binding_contract_version: str = BINDING_CONTRACT_VERSION
    canonical_profile: str = CANONICAL_PROFILE

    def __post_init__(self) -> None:
        if type(self.decision) is not GovernedConstraintDecision:
            raise GovernedConstraintContractError(
                "decision must be GovernedConstraintDecision"
            )
        if type(self.primary_reason) is not GovernedConstraintReason:
            raise GovernedConstraintContractError(
                "primary_reason must be GovernedConstraintReason"
            )
        if self.composer_contract_version != COMPOSER_CONTRACT_VERSION:
            raise GovernedConstraintContractError("unsupported composer_contract_version")
        if self.binding_contract_version != BINDING_CONTRACT_VERSION:
            raise GovernedConstraintContractError("unsupported binding_contract_version")
        if self.canonical_profile != CANONICAL_PROFILE:
            raise GovernedConstraintContractError("unsupported canonical_profile")

        for name in (
            "common_request_fingerprint",
            "evaluation_evidence_fingerprint",
        ):
            value = getattr(self, name)
            if value is not None and (
                not isinstance(value, str) or not _SHA256_HEX_RE.fullmatch(value)
            ):
                raise GovernedConstraintContractError(
                    f"{name} must be lowercase SHA-256 hex or None"
                )

        if self.capability_result is not None and type(self.capability_result) is not ResolutionResult:
            raise GovernedConstraintContractError(
                "capability_result must be exact ResolutionResult or None"
            )
        if self.privacy_result is not None and type(self.privacy_result) is not PrivacyReconciliationResult:
            raise GovernedConstraintContractError(
                "privacy_result must be exact PrivacyReconciliationResult or None"
            )

        if self.decision is GovernedConstraintDecision.ELIGIBLE_FOR_NEXT_GATE:
            if self.primary_reason is not GovernedConstraintReason.ELIGIBLE_FOR_NEXT_GATE:
                raise GovernedConstraintContractError(
                    "eligible decision requires ELIGIBLE_FOR_NEXT_GATE reason"
                )
            if (
                self.common_request_fingerprint is None
                or self.evaluation_evidence_fingerprint is None
                or self.capability_result is None
                or self.privacy_result is None
            ):
                raise GovernedConstraintContractError(
                    "eligible result requires both fingerprints and gate results"
                )
            if not (
                self.capability_result.decision is ResolutionDecision.ALLOW
                and self.capability_result.primary_reason is ResolutionReason.ALLOW
                and self.capability_result.resolver_contract_version
                == P1_001_EXPECTED_VERSION
                and self.privacy_result.decision is PrivacyDecision.ALLOW_REFERENCE
                and self.privacy_result.reason is PrivacyReason.ALLOW_REFERENCE
            ):
                raise GovernedConstraintContractError(
                    "eligible result requires exact positive nested gate results"
                )
        elif self.primary_reason is GovernedConstraintReason.ELIGIBLE_FOR_NEXT_GATE:
            raise GovernedConstraintContractError(
                "non-eligible decision cannot carry eligible reason"
            )
        elif self.decision is GovernedConstraintDecision.NOT_ELIGIBLE:
            if self.primary_reason not in _NOT_ELIGIBLE_REASONS:
                raise GovernedConstraintContractError(
                    "NOT_ELIGIBLE decision has incompatible reason"
                )
        elif self.decision is GovernedConstraintDecision.DEFER:
            if self.primary_reason not in _DEFER_REASONS:
                raise GovernedConstraintContractError(
                    "DEFER decision has incompatible reason"
                )


__all__ = [
    "BINDING_CONTRACT_VERSION",
    "CANONICAL_PROFILE",
    "COMMON_REQUEST_DOMAIN",
    "COMPOSER_CONTRACT_VERSION",
    "CompositionBudget",
    "CrossGateEvaluationContext",
    "EVALUATION_EVIDENCE_DOMAIN",
    "GovernedConstraintContractError",
    "GovernedConstraintDecision",
    "GovernedConstraintReason",
    "GovernedConstraintResult",
    "P1_001_EXPECTED_VERSION",
    "P1_002_EXPECTED_VERSION",
    "SOURCE_PROVENANCE_SCOPE",
]
