"""Immutable contracts for the bounded HDE-v0.1 discrimination primitive."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from mentaury.claims import EpistemicRole, ProvenanceClaimRecord

HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION: Final[str] = "HDE-v0.1"
CANONICAL_PROFILE: Final[str] = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN: Final[str] = "MENTAURY_HYPOTHESIS_DISCRIMINATION_INPUT_V1"

HARD_MAX_STRING_BYTES: Final[int] = 4096
HARD_MAX_TUPLE_ITEMS: Final[int] = 512
HARD_MAX_CANONICAL_INPUT_BYTES: Final[int] = 262144


class HypothesisDiscriminationContractError(ValueError):
    """Raised when input violates the frozen HDE-v0.1 contract."""


class PredictionState(StrEnum):
    PREDICTED = "PREDICTED"
    NOT_PREDICTED = "NOT_PREDICTED"
    UNKNOWN = "UNKNOWN"


class DiscriminationClass(StrEnum):
    DISCRIMINATING = "DISCRIMINATING"
    NON_DISCRIMINATING = "NON_DISCRIMINATING"
    INCONCLUSIVE_STRUCTURE = "INCONCLUSIVE_STRUCTURE"


def _require_exact_type(value: object, expected: type[object], name: str) -> None:
    if type(value) is not expected:
        raise HypothesisDiscriminationContractError(
            f"{name} must be exact {expected.__name__}"
        )


def _require_exact_enum(value: object, expected: type[StrEnum], name: str) -> None:
    if type(value) is not expected:
        raise HypothesisDiscriminationContractError(
            f"{name} must be exact {expected.__name__} member"
        )


def _require_string(value: object, name: str) -> str:
    if type(value) is not str or not value or value != value.strip():
        raise HypothesisDiscriminationContractError(
            f"{name} must be a non-empty unpadded string"
        )
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise HypothesisDiscriminationContractError(
            f"{name} must be valid UTF-8"
        ) from exc
    if len(encoded) > HARD_MAX_STRING_BYTES:
        raise HypothesisDiscriminationContractError(
            f"{name} exceeds HARD_MAX_STRING_BYTES"
        )
    return value


def _require_bool(value: object, name: str) -> bool:
    if type(value) is not bool:
        raise HypothesisDiscriminationContractError(f"{name} must be exact bool")
    return value


def _require_positive_int(value: object, name: str, hard_cap: int) -> int:
    if type(value) is not int or value <= 0:
        raise HypothesisDiscriminationContractError(f"{name} must be a positive integer")
    if value > hard_cap:
        raise HypothesisDiscriminationContractError(f"{name} exceeds frozen hard cap")
    return value


def _require_string_tuple(value: object, name: str) -> tuple[str, ...]:
    if type(value) is not tuple:
        raise HypothesisDiscriminationContractError(f"{name} must be exact tuple")
    if len(value) > HARD_MAX_TUPLE_ITEMS:
        raise HypothesisDiscriminationContractError(
            f"{name} exceeds HARD_MAX_TUPLE_ITEMS"
        )
    checked = tuple(
        _require_string(item, f"{name}[{index}]")
        for index, item in enumerate(value)
    )
    if not checked:
        raise HypothesisDiscriminationContractError(f"{name} must be non-empty")
    if tuple(sorted(checked)) != checked:
        raise HypothesisDiscriminationContractError(
            f"{name} must already be lexically sorted"
        )
    if len(set(checked)) != len(checked):
        raise HypothesisDiscriminationContractError(f"{name} must be unique")
    return checked


@dataclass(frozen=True, slots=True)
class OutcomePrediction:
    outcome_ref: str
    h1_prediction: PredictionState
    h2_prediction: PredictionState
    expectation_basis_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_string(self.outcome_ref, "outcome_ref")
        _require_exact_enum(self.h1_prediction, PredictionState, "h1_prediction")
        _require_exact_enum(self.h2_prediction, PredictionState, "h2_prediction")
        _require_string_tuple(self.expectation_basis_refs, "expectation_basis_refs")

    def to_value(self) -> dict[str, object]:
        return {
            "outcome_ref": self.outcome_ref,
            "h1_prediction": self.h1_prediction.value,
            "h2_prediction": self.h2_prediction.value,
            "expectation_basis_refs": list(self.expectation_basis_refs),
        }


def _require_outcome_tuple(
    value: object, name: str
) -> tuple[OutcomePrediction, ...]:
    if type(value) is not tuple:
        raise HypothesisDiscriminationContractError(f"{name} must be exact tuple")
    if not value:
        raise HypothesisDiscriminationContractError(f"{name} must be non-empty")
    if len(value) > HARD_MAX_TUPLE_ITEMS:
        raise HypothesisDiscriminationContractError(
            f"{name} exceeds HARD_MAX_TUPLE_ITEMS"
        )
    for index, item in enumerate(value):
        _require_exact_type(item, OutcomePrediction, f"{name}[{index}]")
    refs = tuple(item.outcome_ref for item in value)
    if tuple(sorted(refs)) != refs:
        raise HypothesisDiscriminationContractError(
            f"{name} must already be canonically sorted by outcome_ref"
        )
    if len(set(refs)) != len(refs):
        raise HypothesisDiscriminationContractError(
            "duplicate outcome_ref is forbidden"
        )
    return value


def _hypothesis_identity(record: ProvenanceClaimRecord) -> tuple[str, str]:
    return (record.claim.claim_id, record.input_fingerprint)


@dataclass(frozen=True, slots=True)
class DiscriminationProposal:
    contract_version: str
    h1: ProvenanceClaimRecord
    h2: ProvenanceClaimRecord
    proposed_observation_ref: str
    design_origin_ref: str
    design_basis_refs: tuple[str, ...]
    outcomes: tuple[OutcomePrediction, ...]
    partition_scope_ref: str
    partition_complete_for_scope: bool

    def __post_init__(self) -> None:
        if self.contract_version != HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION:
            raise HypothesisDiscriminationContractError(
                "contract_version must equal HDE-v0.1"
            )
        _require_exact_type(self.h1, ProvenanceClaimRecord, "h1")
        _require_exact_type(self.h2, ProvenanceClaimRecord, "h2")
        if self.h1.claim.epistemic_role is not EpistemicRole.HYPOTHESIS:
            raise HypothesisDiscriminationContractError(
                "h1 must have EpistemicRole.HYPOTHESIS"
            )
        if self.h2.claim.epistemic_role is not EpistemicRole.HYPOTHESIS:
            raise HypothesisDiscriminationContractError(
                "h2 must have EpistemicRole.HYPOTHESIS"
            )
        if _hypothesis_identity(self.h1) == _hypothesis_identity(self.h2):
            raise HypothesisDiscriminationContractError(
                "exact H1 and H2 PCR identities must differ"
            )
        _require_string(self.proposed_observation_ref, "proposed_observation_ref")
        _require_string(self.design_origin_ref, "design_origin_ref")
        _require_string_tuple(self.design_basis_refs, "design_basis_refs")
        _require_outcome_tuple(self.outcomes, "outcomes")
        _require_string(self.partition_scope_ref, "partition_scope_ref")
        _require_bool(
            self.partition_complete_for_scope,
            "partition_complete_for_scope",
        )

    def to_value(self) -> dict[str, object]:
        return {
            "contract_version": self.contract_version,
            "h1": self.h1.to_value(),
            "h2": self.h2.to_value(),
            "proposed_observation_ref": self.proposed_observation_ref,
            "design_origin_ref": self.design_origin_ref,
            "design_basis_refs": list(self.design_basis_refs),
            "outcomes": [outcome.to_value() for outcome in self.outcomes],
            "partition_scope_ref": self.partition_scope_ref,
            "partition_complete_for_scope": self.partition_complete_for_scope,
        }


@dataclass(frozen=True, slots=True)
class DiscriminationEvaluationBudget:
    max_string_bytes: int
    max_tuple_items: int
    max_canonical_input_bytes: int

    def __post_init__(self) -> None:
        _require_positive_int(
            self.max_string_bytes,
            "max_string_bytes",
            HARD_MAX_STRING_BYTES,
        )
        _require_positive_int(
            self.max_tuple_items,
            "max_tuple_items",
            HARD_MAX_TUPLE_ITEMS,
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
class DiscriminationEvaluation:
    contract_version: str
    classification: DiscriminationClass
    differential_outcome_refs: tuple[str, ...]
    unknown_outcome_refs: tuple[str, ...]
    input_fingerprint: str

    def __post_init__(self) -> None:
        if self.contract_version != HYPOTHESIS_DISCRIMINATION_CONTRACT_VERSION:
            raise HypothesisDiscriminationContractError(
                "contract_version must equal HDE-v0.1"
            )
        _require_exact_enum(
            self.classification,
            DiscriminationClass,
            "classification",
        )
        for name, value in (
            ("differential_outcome_refs", self.differential_outcome_refs),
            ("unknown_outcome_refs", self.unknown_outcome_refs),
        ):
            if type(value) is not tuple:
                raise HypothesisDiscriminationContractError(
                    f"{name} must be exact tuple"
                )
            checked = tuple(
                _require_string(item, f"{name}[{index}]")
                for index, item in enumerate(value)
            )
            if tuple(sorted(checked)) != checked or len(set(checked)) != len(checked):
                raise HypothesisDiscriminationContractError(
                    f"{name} must be sorted and unique"
                )
        fingerprint = _require_string(self.input_fingerprint, "input_fingerprint")
        if len(fingerprint) != 64 or any(
            character not in "0123456789abcdef" for character in fingerprint
        ):
            raise HypothesisDiscriminationContractError(
                "input_fingerprint must be lowercase sha256 hex"
            )

    def to_value(self) -> dict[str, object]:
        return {
            "contract_version": self.contract_version,
            "classification": self.classification.value,
            "differential_outcome_refs": list(self.differential_outcome_refs),
            "unknown_outcome_refs": list(self.unknown_outcome_refs),
            "input_fingerprint": self.input_fingerprint,
        }
