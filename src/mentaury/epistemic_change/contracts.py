"""Immutable EPR-v0.1 routing-only contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from mentaury.beliefs.contracts import BeliefStatus
from mentaury.epistemic_types import ClaimType

EPISTEMIC_CHANGE_CONTRACT_VERSION: Final[str] = "EPR-v0.1"
CANONICAL_PROFILE: Final[str] = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN: Final[str] = "MENTAURY_EPISTEMIC_CHANGE_INPUT_V1"

HARD_MAX_STRING_BYTES: Final[int] = 4096
HARD_MAX_TUPLE_ITEMS: Final[int] = 512
HARD_MAX_CANONICAL_INPUT_BYTES: Final[int] = 262144


class EpistemicChangeContractError(ValueError):
    """Raised when EPR-v0.1 input violates the frozen contract or hard caps."""


class EpistemicChangeBudgetExceeded(ValueError):
    """Raised when valid hard-cap input exceeds caller-local EPR limits."""


class EpistemicChangeBindingError(ValueError):
    """Raised when a caller-supplied belief binding mismatches the PCR record."""


class EpistemicIntent(StrEnum):
    RETAIN_CLAIM = "RETAIN_CLAIM"
    CREATE_BELIEF_FROM_CLAIM = "CREATE_BELIEF_FROM_CLAIM"
    REVISE_EXISTING_BELIEF = "REVISE_EXISTING_BELIEF"
    SEEK_EVIDENCE_GATE_DECISION = "SEEK_EVIDENCE_GATE_DECISION"
    RECONSIDER_TERMINAL_BELIEF = "RECONSIDER_TERMINAL_BELIEF"
    DEFER = "DEFER"


class EpistemicRoute(StrEnum):
    RETAIN_CLAIM_ONLY = "RETAIN_CLAIM_ONLY"
    CLAIM_TO_BELIEF_BINDING_REQUIRED = "CLAIM_TO_BELIEF_BINDING_REQUIRED"
    P0_014_NON_TERMINAL_REVISION_REQUIRED = "P0_014_NON_TERMINAL_REVISION_REQUIRED"
    P0_015_EVIDENCE_GATE_REQUIRED = "P0_015_EVIDENCE_GATE_REQUIRED"
    TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED = "TERMINAL_RECONSIDERATION_LINEAGE_REQUIRED"
    DEFER = "DEFER"


class EpistemicOwner(StrEnum):
    PCR_V0_1 = "PCR_V0_1"
    FUTURE_CLAIM_TO_BELIEF_BINDING = "FUTURE_CLAIM_TO_BELIEF_BINDING"
    P0_014_BELIEF_LIFECYCLE = "P0_014_BELIEF_LIFECYCLE"
    P0_015_EVIDENCE_GATE = "P0_015_EVIDENCE_GATE"
    FUTURE_TERMINAL_RECONSIDERATION_LINEAGE = "FUTURE_TERMINAL_RECONSIDERATION_LINEAGE"
    NONE = "NONE"


class EpistemicRouteReason(StrEnum):
    CALLER_RETAINED_CLAIM = "CALLER_RETAINED_CLAIM"
    CLAIM_BINDING_PREREQUISITE = "CLAIM_BINDING_PREREQUISITE"
    NON_TERMINAL_REVISION_OWNER = "NON_TERMINAL_REVISION_OWNER"
    EVIDENCE_GATE_OWNER = "EVIDENCE_GATE_OWNER"
    TERMINAL_LINEAGE_PREREQUISITE = "TERMINAL_LINEAGE_PREREQUISITE"
    CALLER_DEFERRED = "CALLER_DEFERRED"
    INTENT_PRECONDITION_UNMET = "INTENT_PRECONDITION_UNMET"


def _require_string(value: object, name: str, *, optional: bool = False) -> str | None:
    if optional and value is None:
        return None
    if type(value) is not str or not value or value != value.strip():
        raise EpistemicChangeContractError(
            f"{name} must be a non-empty unpadded string"
        )
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise EpistemicChangeContractError(f"{name} must be valid UTF-8") from exc
    if len(encoded) > HARD_MAX_STRING_BYTES:
        raise EpistemicChangeContractError(f"{name} exceeds HARD_MAX_STRING_BYTES")
    return value


def _require_sha256(value: object, name: str) -> str:
    text = _require_string(value, name)
    assert text is not None
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise EpistemicChangeContractError(
            f"{name} must be lowercase 64-character sha256 hex"
        )
    return text


def _require_positive_int(value: object, name: str, hard_cap: int | None = None) -> int:
    if type(value) is not int or value <= 0:
        raise EpistemicChangeContractError(f"{name} must be a positive integer")
    if hard_cap is not None and value > hard_cap:
        raise EpistemicChangeContractError(f"{name} exceeds frozen hard cap")
    return value


def _require_exact_enum(value: object, enum_type: type[StrEnum], name: str) -> None:
    if type(value) is not enum_type:
        raise EpistemicChangeContractError(
            f"{name} must be exact {enum_type.__name__} member"
        )


def _require_string_tuple(value: object, name: str) -> tuple[str, ...]:
    if type(value) is not tuple:
        raise EpistemicChangeContractError(f"{name} must be exact tuple")
    if len(value) > HARD_MAX_TUPLE_ITEMS:
        raise EpistemicChangeContractError(f"{name} exceeds HARD_MAX_TUPLE_ITEMS")
    checked = tuple(
        _require_string(item, f"{name}[{index}]")
        for index, item in enumerate(value)
    )
    assert all(item is not None for item in checked)
    result = tuple(str(item) for item in checked)
    if tuple(sorted(result)) != result:
        raise EpistemicChangeContractError(f"{name} must already be lexically sorted")
    if len(set(result)) != len(result):
        raise EpistemicChangeContractError(f"{name} must be unique")
    return result


@dataclass(frozen=True, slots=True)
class BeliefBinding:
    belief_id: str
    belief_revision: int
    belief_status: BeliefStatus
    belief_claim_type: ClaimType
    claim_id: str
    claim_record_fingerprint: str

    def __post_init__(self) -> None:
        _require_string(self.belief_id, "belief_id")
        _require_positive_int(self.belief_revision, "belief_revision")
        _require_exact_enum(self.belief_status, BeliefStatus, "belief_status")
        _require_exact_enum(self.belief_claim_type, ClaimType, "belief_claim_type")
        _require_string(self.claim_id, "claim_id")
        _require_sha256(self.claim_record_fingerprint, "claim_record_fingerprint")

    def to_value(self) -> dict[str, object]:
        return {
            "belief_id": self.belief_id,
            "belief_revision": self.belief_revision,
            "belief_status": self.belief_status.value,
            "belief_claim_type": self.belief_claim_type.value,
            "claim_id": self.claim_id,
            "claim_record_fingerprint": self.claim_record_fingerprint,
        }


@dataclass(frozen=True, slots=True)
class EpistemicChangeRequest:
    request_id: str
    intent: EpistemicIntent
    reason_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_string(self.request_id, "request_id")
        _require_exact_enum(self.intent, EpistemicIntent, "intent")
        _require_string_tuple(self.reason_refs, "reason_refs")

    def to_value(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "intent": self.intent.value,
            "reason_refs": list(self.reason_refs),
        }


@dataclass(frozen=True, slots=True)
class EpistemicChangeBudget:
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
class EpistemicChangePlan:
    contract_version: str
    request_id: str
    route: EpistemicRoute
    next_owner: EpistemicOwner
    reason: EpistemicRouteReason
    record_fingerprint: str
    belief_id: str | None
    belief_revision: int | None
    routing_input_fingerprint: str

    def __post_init__(self) -> None:
        if self.contract_version != EPISTEMIC_CHANGE_CONTRACT_VERSION:
            raise EpistemicChangeContractError(
                "contract_version must equal EPR-v0.1"
            )
        _require_string(self.request_id, "request_id")
        _require_exact_enum(self.route, EpistemicRoute, "route")
        _require_exact_enum(self.next_owner, EpistemicOwner, "next_owner")
        _require_exact_enum(self.reason, EpistemicRouteReason, "reason")
        _require_sha256(self.record_fingerprint, "record_fingerprint")
        if (self.belief_id is None) != (self.belief_revision is None):
            raise EpistemicChangeContractError(
                "belief_id and belief_revision must both be present or absent"
            )
        _require_string(self.belief_id, "belief_id", optional=True)
        if self.belief_revision is not None:
            _require_positive_int(self.belief_revision, "belief_revision")
        _require_sha256(self.routing_input_fingerprint, "routing_input_fingerprint")

    def to_value(self) -> dict[str, object]:
        return {
            "contract_version": self.contract_version,
            "request_id": self.request_id,
            "route": self.route.value,
            "next_owner": self.next_owner.value,
            "reason": self.reason.value,
            "record_fingerprint": self.record_fingerprint,
            "belief_id": self.belief_id,
            "belief_revision": self.belief_revision,
            "routing_input_fingerprint": self.routing_input_fingerprint,
        }
