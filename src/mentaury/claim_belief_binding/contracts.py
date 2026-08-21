"""CBP-v0.1 immutable contracts for provenance-preserving belief genesis binding."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from mentaury.epistemic_types import ClaimType

CLAIM_BELIEF_BINDING_CONTRACT_VERSION: Final[str] = "CBP-v0.1"
CREATE_BELIEF_FROM_CLAIM: Final[str] = "CREATE_BELIEF_FROM_CLAIM"
CREATE_BELIEF_FROM_CLAIM_SCHEMA: Final[str] = "create-belief-from-claim/v1"
BELIEF_CLAIM_BOUND: Final[str] = "BELIEF_CLAIM_BOUND"
BELIEF_CLAIM_BOUND_SCHEMA: Final[str] = "belief-claim-bound/v1"
CANONICAL_PROFILE: Final[str] = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN: Final[str] = "MENTAURY_CLAIM_BELIEF_BINDING_INPUT_V1"

HARD_MAX_STRING_BYTES: Final[int] = 4096
HARD_MAX_TUPLE_ITEMS: Final[int] = 512
HARD_MAX_CANONICAL_INPUT_BYTES: Final[int] = 262144


class ClaimBeliefBindingContractError(ValueError):
    """Raised when CBP-v0.1 input violates the bounded contract."""


class ClaimBeliefBindingBudgetExceeded(ValueError):
    """Raised when valid CBP-v0.1 input exceeds caller-local limits."""


class StatementEquivalence(StrEnum):
    """What CBP-v0.1 proves about PCR statement_ref vs belief statement text."""

    NOT_ESTABLISHED = "NOT_ESTABLISHED"


def _require_string(value: object, name: str) -> str:
    if type(value) is not str or not value or value != value.strip():
        raise ClaimBeliefBindingContractError(
            f"{name} must be a non-empty unpadded string"
        )
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ClaimBeliefBindingContractError(f"{name} must be valid UTF-8") from exc
    if len(encoded) > HARD_MAX_STRING_BYTES:
        raise ClaimBeliefBindingContractError(
            f"{name} exceeds HARD_MAX_STRING_BYTES"
        )
    return value


def _require_positive_int(value: object, name: str, hard_cap: int) -> int:
    if type(value) is not int or value <= 0:
        raise ClaimBeliefBindingContractError(f"{name} must be a positive integer")
    if value > hard_cap:
        raise ClaimBeliefBindingContractError(f"{name} exceeds frozen hard cap")
    return value


def _require_sha256(value: object, name: str) -> str:
    text = _require_string(value, name)
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise ClaimBeliefBindingContractError(
            f"{name} must be lowercase 64-character sha256 hex"
        )
    return text


@dataclass(frozen=True, slots=True)
class ClaimBeliefBindingBudget:
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

    def to_value(self) -> dict[str, int]:
        return {
            "max_string_bytes": self.max_string_bytes,
            "max_tuple_items": self.max_tuple_items,
            "max_canonical_input_bytes": self.max_canonical_input_bytes,
        }


@dataclass(frozen=True, slots=True)
class ClaimBeliefBinding:
    contract_version: str
    belief_id: str
    belief_revision: int
    claim_id: str
    claim_record_fingerprint: str
    claim_type: ClaimType
    statement_ref: str
    statement_equivalence: StatementEquivalence
    binding_input_fingerprint: str

    def __post_init__(self) -> None:
        if self.contract_version != CLAIM_BELIEF_BINDING_CONTRACT_VERSION:
            raise ClaimBeliefBindingContractError(
                "contract_version must equal CBP-v0.1"
            )
        _require_string(self.belief_id, "belief_id")
        if self.belief_revision != 1:
            raise ClaimBeliefBindingContractError(
                "belief_revision must equal creation revision 1"
            )
        _require_string(self.claim_id, "claim_id")
        _require_sha256(self.claim_record_fingerprint, "claim_record_fingerprint")
        if type(self.claim_type) is not ClaimType:
            raise ClaimBeliefBindingContractError(
                "claim_type must be exact ClaimType member"
            )
        _require_string(self.statement_ref, "statement_ref")
        if self.statement_equivalence is not StatementEquivalence.NOT_ESTABLISHED:
            raise ClaimBeliefBindingContractError(
                "statement_equivalence must remain NOT_ESTABLISHED in CBP-v0.1"
            )
        _require_sha256(self.binding_input_fingerprint, "binding_input_fingerprint")

    def to_value(self) -> dict[str, object]:
        return {
            "contract_version": self.contract_version,
            "belief_id": self.belief_id,
            "belief_revision": self.belief_revision,
            "claim_id": self.claim_id,
            "claim_record_fingerprint": self.claim_record_fingerprint,
            "claim_type": self.claim_type.value,
            "statement_ref": self.statement_ref,
            "statement_equivalence": self.statement_equivalence.value,
            "binding_input_fingerprint": self.binding_input_fingerprint,
        }
