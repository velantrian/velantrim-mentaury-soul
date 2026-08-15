"""Immutable contracts for the bounded ATR-v0.1 typed-relation primitive."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

TYPED_RELATION_CONTRACT_VERSION: Final[str] = "ATR-v0.1"
CANONICAL_PROFILE: Final[str] = "MENTAURY_CANONICAL_JSON_V1"
INPUT_FINGERPRINT_DOMAIN: Final[str] = "MENTAURY_ANCHORED_TYPED_RELATION_INPUT_V1"

HARD_MAX_STRING_BYTES: Final[int] = 4096
HARD_MAX_TUPLE_ITEMS: Final[int] = 512
HARD_MAX_CANONICAL_INPUT_BYTES: Final[int] = 262144


class TypedRelationContractError(ValueError):
    """Raised when input violates the frozen ATR-v0.1 contract or hard caps."""


class TypedRelationBudgetExceeded(ValueError):
    """Raised when valid hard-cap input exceeds the caller's local budget."""


class RelationType(StrEnum):
    CAUSAL = "CAUSAL"
    CORRELATIONAL = "CORRELATIONAL"
    TEMPORAL = "TEMPORAL"
    ANALOGICAL = "ANALOGICAL"
    TAXONOMIC = "TAXONOMIC"
    MECHANISTIC = "MECHANISTIC"
    EVIDENTIAL = "EVIDENTIAL"
    CONTRADICTORY = "CONTRADICTORY"
    UNKNOWN = "UNKNOWN"


class RelationOrientation(StrEnum):
    DIRECTED = "DIRECTED"
    SYMMETRIC = "SYMMETRIC"
    UNKNOWN = "UNKNOWN"


class RelationOrigin(StrEnum):
    SOURCE_ASSERTED = "SOURCE_ASSERTED"
    MENTAURY_DERIVED = "MENTAURY_DERIVED"
    EXTERNAL_DERIVED = "EXTERNAL_DERIVED"
    UNKNOWN = "UNKNOWN"


class ScopeReferenceKind(StrEnum):
    CLAIM_ANCHOR = "CLAIM_ANCHOR"
    CONTEXT_REF = "CONTEXT_REF"


def _require_exact_type(value: object, expected: type[object], name: str) -> None:
    if type(value) is not expected:
        raise TypedRelationContractError(
            f"{name} must be exact {expected.__name__}"
        )


def _require_exact_enum(value: object, expected: type[StrEnum], name: str) -> None:
    if type(value) is not expected:
        raise TypedRelationContractError(
            f"{name} must be exact {expected.__name__} member"
        )


def _require_string(
    value: object, name: str, *, optional: bool = False
) -> str | None:
    if optional and value is None:
        return None
    if type(value) is not str or not value or value != value.strip():
        raise TypedRelationContractError(
            f"{name} must be a non-empty unpadded string"
        )
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise TypedRelationContractError(f"{name} must be valid UTF-8") from exc
    if len(encoded) > HARD_MAX_STRING_BYTES:
        raise TypedRelationContractError(f"{name} exceeds HARD_MAX_STRING_BYTES")
    return value


def _require_fingerprint(value: object, name: str) -> str:
    checked = _require_string(value, name)
    assert checked is not None
    if len(checked) != 64 or any(
        character not in "0123456789abcdef" for character in checked
    ):
        raise TypedRelationContractError(
            f"{name} must be lowercase sha256 hex"
        )
    return checked


def _require_positive_int(value: object, name: str, hard_cap: int) -> int:
    if type(value) is not int or value <= 0:
        raise TypedRelationContractError(f"{name} must be a positive integer")
    if value > hard_cap:
        raise TypedRelationContractError(f"{name} exceeds frozen hard cap")
    return value


@dataclass(frozen=True, slots=True)
class ClaimAnchor:
    claim_id: str
    claim_input_fingerprint: str

    def __post_init__(self) -> None:
        _require_string(self.claim_id, "claim_id")
        _require_fingerprint(
            self.claim_input_fingerprint, "claim_input_fingerprint"
        )

    def to_value(self) -> dict[str, object]:
        return {
            "claim_id": self.claim_id,
            "claim_input_fingerprint": self.claim_input_fingerprint,
        }


@dataclass(frozen=True, slots=True)
class RelationEndpoints:
    left_anchor: ClaimAnchor
    right_anchor: ClaimAnchor

    def __post_init__(self) -> None:
        _require_exact_type(self.left_anchor, ClaimAnchor, "left_anchor")
        _require_exact_type(self.right_anchor, ClaimAnchor, "right_anchor")
        if self.left_anchor == self.right_anchor:
            raise TypedRelationContractError("exact self-relations are forbidden")

    def to_value(self) -> dict[str, object]:
        return {
            "left_anchor": self.left_anchor.to_value(),
            "right_anchor": self.right_anchor.to_value(),
        }


_COMPATIBLE_ORIENTATIONS: Final[dict[RelationType, frozenset[RelationOrientation]]] = {
    RelationType.CAUSAL: frozenset({RelationOrientation.DIRECTED}),
    RelationType.CORRELATIONAL: frozenset({RelationOrientation.SYMMETRIC}),
    RelationType.TEMPORAL: frozenset({RelationOrientation.DIRECTED}),
    RelationType.ANALOGICAL: frozenset({RelationOrientation.SYMMETRIC}),
    RelationType.TAXONOMIC: frozenset({RelationOrientation.DIRECTED}),
    RelationType.MECHANISTIC: frozenset({RelationOrientation.DIRECTED}),
    RelationType.EVIDENTIAL: frozenset({RelationOrientation.DIRECTED}),
    RelationType.CONTRADICTORY: frozenset({RelationOrientation.SYMMETRIC}),
    RelationType.UNKNOWN: frozenset(
        {
            RelationOrientation.UNKNOWN,
            RelationOrientation.DIRECTED,
            RelationOrientation.SYMMETRIC,
        }
    ),
}


@dataclass(frozen=True, slots=True)
class RelationSemantics:
    relation_type: RelationType
    orientation: RelationOrientation

    def __post_init__(self) -> None:
        _require_exact_enum(self.relation_type, RelationType, "relation_type")
        _require_exact_enum(self.orientation, RelationOrientation, "orientation")
        if self.orientation not in _COMPATIBLE_ORIENTATIONS[self.relation_type]:
            raise TypedRelationContractError(
                "relation_type and orientation are incompatible"
            )

    def to_value(self) -> dict[str, object]:
        return {
            "relation_type": self.relation_type.value,
            "orientation": self.orientation.value,
        }


@dataclass(frozen=True, slots=True)
class ScopeReference:
    kind: ScopeReferenceKind
    reference_id: str
    claim_input_fingerprint: str | None

    def __post_init__(self) -> None:
        _require_exact_enum(self.kind, ScopeReferenceKind, "kind")
        _require_string(self.reference_id, "reference_id")
        if self.kind is ScopeReferenceKind.CLAIM_ANCHOR:
            _require_fingerprint(
                self.claim_input_fingerprint, "claim_input_fingerprint"
            )
        elif self.claim_input_fingerprint is not None:
            raise TypedRelationContractError(
                "CONTEXT_REF claim_input_fingerprint must be None"
            )

    def to_value(self) -> dict[str, object]:
        return {
            "kind": self.kind.value,
            "reference_id": self.reference_id,
            "claim_input_fingerprint": self.claim_input_fingerprint,
        }


def _claim_anchor_key(anchor: ClaimAnchor) -> tuple[str, str]:
    return (anchor.claim_id, anchor.claim_input_fingerprint)


def _scope_reference_key(reference: ScopeReference) -> tuple[str, str, str]:
    return (
        reference.kind.value,
        reference.reference_id,
        reference.claim_input_fingerprint or "",
    )


def _require_claim_anchor_tuple(
    value: object, name: str
) -> tuple[ClaimAnchor, ...]:
    if type(value) is not tuple:
        raise TypedRelationContractError(f"{name} must be exact tuple")
    if len(value) > HARD_MAX_TUPLE_ITEMS:
        raise TypedRelationContractError(f"{name} exceeds HARD_MAX_TUPLE_ITEMS")
    for index, item in enumerate(value):
        _require_exact_type(item, ClaimAnchor, f"{name}[{index}]")
    checked = value
    keys = tuple(_claim_anchor_key(item) for item in checked)
    if tuple(sorted(keys)) != keys:
        raise TypedRelationContractError(f"{name} must already be canonically sorted")
    if len(set(keys)) != len(keys):
        raise TypedRelationContractError(f"{name} must be unique")
    return checked


def _require_scope_reference_tuple(
    value: object, name: str
) -> tuple[ScopeReference, ...]:
    if type(value) is not tuple:
        raise TypedRelationContractError(f"{name} must be exact tuple")
    if len(value) > HARD_MAX_TUPLE_ITEMS:
        raise TypedRelationContractError(f"{name} exceeds HARD_MAX_TUPLE_ITEMS")
    for index, item in enumerate(value):
        _require_exact_type(item, ScopeReference, f"{name}[{index}]")
    checked = value
    keys = tuple(_scope_reference_key(item) for item in checked)
    if tuple(sorted(keys)) != keys:
        raise TypedRelationContractError(f"{name} must already be canonically sorted")
    if len(set(keys)) != len(keys):
        raise TypedRelationContractError(f"{name} must be unique")
    return checked


@dataclass(frozen=True, slots=True)
class RelationProvenance:
    origin: RelationOrigin
    origin_actor_ref: str | None
    source_assertion_anchor: ClaimAnchor | None
    basis_anchors: tuple[ClaimAnchor, ...]

    def __post_init__(self) -> None:
        _require_exact_enum(self.origin, RelationOrigin, "origin")
        _require_claim_anchor_tuple(self.basis_anchors, "basis_anchors")

        if self.origin is RelationOrigin.SOURCE_ASSERTED:
            _require_string(self.origin_actor_ref, "origin_actor_ref")
            _require_exact_type(
                self.source_assertion_anchor,
                ClaimAnchor,
                "source_assertion_anchor",
            )
        elif self.origin in (
            RelationOrigin.MENTAURY_DERIVED,
            RelationOrigin.EXTERNAL_DERIVED,
        ):
            _require_string(self.origin_actor_ref, "origin_actor_ref")
            if self.source_assertion_anchor is not None:
                raise TypedRelationContractError(
                    "derived origin source_assertion_anchor must be None"
                )
            if not self.basis_anchors:
                raise TypedRelationContractError(
                    "derived origin requires non-empty basis_anchors"
                )
        else:
            if self.origin_actor_ref is not None:
                raise TypedRelationContractError(
                    "UNKNOWN origin_actor_ref must be None"
                )
            if self.source_assertion_anchor is not None:
                raise TypedRelationContractError(
                    "UNKNOWN source_assertion_anchor must be None"
                )

    def to_value(self) -> dict[str, object]:
        return {
            "origin": self.origin.value,
            "origin_actor_ref": self.origin_actor_ref,
            "source_assertion_anchor": (
                None
                if self.source_assertion_anchor is None
                else self.source_assertion_anchor.to_value()
            ),
            "basis_anchors": [anchor.to_value() for anchor in self.basis_anchors],
        }


@dataclass(frozen=True, slots=True)
class RelationScope:
    conditions: tuple[ScopeReference, ...]
    moderators: tuple[ScopeReference, ...]
    exceptions: tuple[ScopeReference, ...]
    unknowns: tuple[ScopeReference, ...]
    transfer_limits: tuple[ScopeReference, ...]

    def __post_init__(self) -> None:
        _require_scope_reference_tuple(self.conditions, "conditions")
        _require_scope_reference_tuple(self.moderators, "moderators")
        _require_scope_reference_tuple(self.exceptions, "exceptions")
        _require_scope_reference_tuple(self.unknowns, "unknowns")
        _require_scope_reference_tuple(self.transfer_limits, "transfer_limits")

    def to_value(self) -> dict[str, object]:
        return {
            "conditions": [reference.to_value() for reference in self.conditions],
            "moderators": [reference.to_value() for reference in self.moderators],
            "exceptions": [reference.to_value() for reference in self.exceptions],
            "unknowns": [reference.to_value() for reference in self.unknowns],
            "transfer_limits": [
                reference.to_value() for reference in self.transfer_limits
            ],
        }


@dataclass(frozen=True, slots=True)
class RelationRepresentationBudget:
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
class AnchoredTypedRelationRecord:
    contract_version: str
    endpoints: RelationEndpoints
    semantics: RelationSemantics
    provenance: RelationProvenance
    scope: RelationScope
    input_fingerprint: str

    def __post_init__(self) -> None:
        if self.contract_version != TYPED_RELATION_CONTRACT_VERSION:
            raise TypedRelationContractError(
                "contract_version must equal ATR-v0.1"
            )
        _require_exact_type(self.endpoints, RelationEndpoints, "endpoints")
        _require_exact_type(self.semantics, RelationSemantics, "semantics")
        _require_exact_type(self.provenance, RelationProvenance, "provenance")
        _require_exact_type(self.scope, RelationScope, "scope")
        _require_fingerprint(self.input_fingerprint, "input_fingerprint")

    def to_value(self) -> dict[str, object]:
        return {
            "contract_version": self.contract_version,
            "endpoints": self.endpoints.to_value(),
            "semantics": self.semantics.to_value(),
            "provenance": self.provenance.to_value(),
            "scope": self.scope.to_value(),
            "input_fingerprint": self.input_fingerprint,
        }
