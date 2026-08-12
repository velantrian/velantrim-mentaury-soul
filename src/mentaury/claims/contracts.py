"""Immutable contracts for the bounded PCR-v0.1 provenance-claim primitive."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from mentaury.epistemic_types import ClaimType
from mentaury.non_projection import (
    ClaimClass,
    ProvenanceState,
    Sensitivity,
    SourceClass,
    SourceOrigin,
    SubjectRelation,
)

PROVENANCE_CLAIM_CONTRACT_VERSION: Final[str] = "PCR-v0.1"
CANONICAL_PROFILE: Final[str] = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN: Final[str] = "MENTAURY_PROVENANCE_CLAIM_INPUT_V1"
SOURCE_SCOPE: Final[str] = "CALLER_SUPPLIED_REFERENCES_ONLY"

HARD_MAX_STRING_BYTES: Final[int] = 4096
HARD_MAX_TUPLE_ITEMS: Final[int] = 512
HARD_MAX_CANONICAL_INPUT_BYTES: Final[int] = 262144


class ProvenanceClaimContractError(ValueError):
    """Raised when input violates the frozen PCR-v0.1 contract or hard caps."""


class ProvenanceClaimBudgetExceeded(ValueError):
    """Raised when valid hard-cap input exceeds the caller's local budget."""


class EpistemicRole(StrEnum):
    OBSERVATION = "OBSERVATION"
    TESTIMONY = "TESTIMONY"
    EVIDENCE_CANDIDATE = "EVIDENCE_CANDIDATE"
    HYPOTHESIS = "HYPOTHESIS"
    INFERENCE = "INFERENCE"
    INTERPRETATION = "INTERPRETATION"
    METAPHORICAL_EXPRESSION = "METAPHORICAL_EXPRESSION"
    UNKNOWN = "UNKNOWN"


def _require_exact_type(value: object, expected: type[object], name: str) -> None:
    if type(value) is not expected:
        raise ProvenanceClaimContractError(
            f"{name} must be exact {expected.__name__}"
        )


def _require_exact_enum(value: object, expected: type[StrEnum], name: str) -> None:
    if type(value) is not expected:
        raise ProvenanceClaimContractError(
            f"{name} must be exact {expected.__name__} member"
        )


def _require_string(
    value: object, name: str, *, optional: bool = False
) -> str | None:
    if optional and value is None:
        return None
    if type(value) is not str or not value or value != value.strip():
        raise ProvenanceClaimContractError(
            f"{name} must be a non-empty unpadded string"
        )
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ProvenanceClaimContractError(
            f"{name} must be valid UTF-8"
        ) from exc
    if len(encoded) > HARD_MAX_STRING_BYTES:
        raise ProvenanceClaimContractError(
            f"{name} exceeds HARD_MAX_STRING_BYTES"
        )
    return value


def _require_bool(value: object, name: str) -> bool:
    if type(value) is not bool:
        raise ProvenanceClaimContractError(f"{name} must be exact bool")
    return value


def _require_positive_int(value: object, name: str, hard_cap: int) -> int:
    if type(value) is not int or value <= 0:
        raise ProvenanceClaimContractError(f"{name} must be a positive integer")
    if value > hard_cap:
        raise ProvenanceClaimContractError(f"{name} exceeds frozen hard cap")
    return value


def _require_string_tuple(value: object, name: str) -> tuple[str, ...]:
    if type(value) is not tuple:
        raise ProvenanceClaimContractError(f"{name} must be exact tuple")
    if len(value) > HARD_MAX_TUPLE_ITEMS:
        raise ProvenanceClaimContractError(
            f"{name} exceeds HARD_MAX_TUPLE_ITEMS"
        )
    checked = tuple(
        _require_string(item, f"{name}[{index}]")
        for index, item in enumerate(value)
    )
    if tuple(sorted(checked)) != checked:
        raise ProvenanceClaimContractError(
            f"{name} must already be lexically sorted"
        )
    if len(set(checked)) != len(checked):
        raise ProvenanceClaimContractError(f"{name} must be unique")
    return checked


@dataclass(frozen=True, slots=True)
class ProvenanceSource:
    source_ref: str
    source_actor_ref: str | None
    source_class: SourceClass
    source_origin: SourceOrigin
    provenance_state: ProvenanceState
    publication_or_capture_context_ref: str | None
    sensitivity: Sensitivity
    usage_boundary_ref: str
    material_gaps: tuple[str, ...]
    derivation_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_string(self.source_ref, "source_ref")
        _require_string(self.source_actor_ref, "source_actor_ref", optional=True)
        _require_exact_enum(self.source_class, SourceClass, "source_class")
        _require_exact_enum(self.source_origin, SourceOrigin, "source_origin")
        _require_exact_enum(
            self.provenance_state, ProvenanceState, "provenance_state"
        )
        _require_string(
            self.publication_or_capture_context_ref,
            "publication_or_capture_context_ref",
            optional=True,
        )
        _require_exact_enum(self.sensitivity, Sensitivity, "sensitivity")
        _require_string(self.usage_boundary_ref, "usage_boundary_ref")
        _require_string_tuple(self.material_gaps, "material_gaps")
        _require_string_tuple(self.derivation_refs, "derivation_refs")

    def to_value(self) -> dict[str, object]:
        return {
            "source_ref": self.source_ref,
            "source_actor_ref": self.source_actor_ref,
            "source_class": self.source_class.value,
            "source_origin": self.source_origin.value,
            "provenance_state": self.provenance_state.value,
            "publication_or_capture_context_ref": self.publication_or_capture_context_ref,
            "sensitivity": self.sensitivity.value,
            "usage_boundary_ref": self.usage_boundary_ref,
            "material_gaps": list(self.material_gaps),
            "derivation_refs": list(self.derivation_refs),
        }


@dataclass(frozen=True, slots=True)
class ClaimRepresentation:
    claim_id: str
    statement_ref: str
    claim_class: ClaimClass
    claim_type: ClaimType
    epistemic_role: EpistemicRole
    directly_stated: bool
    speaker_ref: str
    subject_ref: str
    subject_relation: SubjectRelation
    basis_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_string(self.claim_id, "claim_id")
        _require_string(self.statement_ref, "statement_ref")
        _require_exact_enum(self.claim_class, ClaimClass, "claim_class")
        _require_exact_enum(self.claim_type, ClaimType, "claim_type")
        _require_exact_enum(self.epistemic_role, EpistemicRole, "epistemic_role")
        _require_bool(self.directly_stated, "directly_stated")
        _require_string(self.speaker_ref, "speaker_ref")
        _require_string(self.subject_ref, "subject_ref")
        _require_exact_enum(
            self.subject_relation, SubjectRelation, "subject_relation"
        )
        _require_string_tuple(self.basis_refs, "basis_refs")
        _require_string_tuple(self.evidence_refs, "evidence_refs")
        if self.epistemic_role is EpistemicRole.INFERENCE and not self.basis_refs:
            raise ProvenanceClaimContractError(
                "INFERENCE requires non-empty basis_refs"
            )

    def to_value(self) -> dict[str, object]:
        return {
            "claim_id": self.claim_id,
            "statement_ref": self.statement_ref,
            "claim_class": self.claim_class.value,
            "claim_type": self.claim_type.value,
            "epistemic_role": self.epistemic_role.value,
            "directly_stated": self.directly_stated,
            "speaker_ref": self.speaker_ref,
            "subject_ref": self.subject_ref,
            "subject_relation": self.subject_relation.value,
            "basis_refs": list(self.basis_refs),
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class ClaimScope:
    applies_to: tuple[str, ...]
    may_support: tuple[str, ...]
    does_not_establish: tuple[str, ...]
    unknowns: tuple[str, ...]
    transfer_limits: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_string_tuple(self.applies_to, "applies_to")
        _require_string_tuple(self.may_support, "may_support")
        _require_string_tuple(self.does_not_establish, "does_not_establish")
        _require_string_tuple(self.unknowns, "unknowns")
        _require_string_tuple(self.transfer_limits, "transfer_limits")

    def to_value(self) -> dict[str, object]:
        return {
            "applies_to": list(self.applies_to),
            "may_support": list(self.may_support),
            "does_not_establish": list(self.does_not_establish),
            "unknowns": list(self.unknowns),
            "transfer_limits": list(self.transfer_limits),
        }


@dataclass(frozen=True, slots=True)
class RepresentationBudget:
    max_string_bytes: int
    max_tuple_items: int
    max_canonical_input_bytes: int

    def __post_init__(self) -> None:
        _require_positive_int(
            self.max_string_bytes, "max_string_bytes", HARD_MAX_STRING_BYTES
        )
        _require_positive_int(
            self.max_tuple_items, "max_tuple_items", HARD_MAX_TUPLE_ITEMS
        )
        _require_positive_int(
            self.max_canonical_input_bytes,
            "max_canonical_input_bytes",
            HARD_MAX_CANONICAL_INPUT_BYTES,
        )

    def to_value(self) -> dict[str, object]:
        return {
            "max_string_bytes": self.max_string_bytes,
            "max_tuple_items": self.max_tuple_items,
            "max_canonical_input_bytes": self.max_canonical_input_bytes,
        }


@dataclass(frozen=True, slots=True)
class ProvenanceClaimRecord:
    contract_version: str
    source: ProvenanceSource
    claim: ClaimRepresentation
    scope: ClaimScope
    input_fingerprint: str

    def __post_init__(self) -> None:
        if self.contract_version != PROVENANCE_CLAIM_CONTRACT_VERSION:
            raise ProvenanceClaimContractError(
                "contract_version must equal PCR-v0.1"
            )
        _require_exact_type(self.source, ProvenanceSource, "source")
        _require_exact_type(self.claim, ClaimRepresentation, "claim")
        _require_exact_type(self.scope, ClaimScope, "scope")
        fingerprint = _require_string(
            self.input_fingerprint, "input_fingerprint"
        )
        assert fingerprint is not None
        if len(fingerprint) != 64 or any(
            character not in "0123456789abcdef" for character in fingerprint
        ):
            raise ProvenanceClaimContractError(
                "input_fingerprint must be lowercase sha256 hex"
            )

    def to_value(self) -> dict[str, object]:
        return {
            "contract_version": self.contract_version,
            "source": self.source.to_value(),
            "claim": self.claim.to_value(),
            "scope": self.scope.to_value(),
            "input_fingerprint": self.input_fingerprint,
        }
