"""P0-015 deterministic evidence-gate contracts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from mentaury.beliefs.contracts import ClaimType, EvidenceSide
from mentaury.contracts import PendingEvent, canonical_timestamp

EVIDENCE_GATE_PROFILE: Final[str] = "MENTAURY_EVIDENCE_GATE_V1"
APPLY_EVIDENCE_GATE: Final[str] = "APPLY_EVIDENCE_GATE"
BELIEF_EVIDENCE_GATED: Final[str] = "BELIEF_EVIDENCE_GATED"
BELIEF_EVIDENCE_GATED_SCHEMA: Final[str] = "belief-evidence-gated/v1"
EVIDENCE_GATE_REJECTED: Final[str] = "EVIDENCE_GATE_REJECTED"
EVIDENCE_GATE_DECISION_SCHEMA: Final[str] = "evidence-gate-decision/v1"

_SHA256_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")


class EvidenceGateOutcome(StrEnum):
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    INCONCLUSIVE = "inconclusive"
    CONFLICT = "conflict"


class EvidenceGateRejectionCode(StrEnum):
    INVALID_COMMAND = "INVALID_COMMAND"
    TARGET_STREAM_MISMATCH = "TARGET_STREAM_MISMATCH"
    BELIEF_NOT_FOUND = "BELIEF_NOT_FOUND"
    TERMINAL_BELIEF = "TERMINAL_BELIEF"
    REVISION_CONFLICT = "REVISION_CONFLICT"
    POLICY_NOT_APPROVED = "POLICY_NOT_APPROVED"
    CLAIM_TYPE_NOT_ALLOWED = "CLAIM_TYPE_NOT_ALLOWED"
    INVALID_EVIDENCE_SET = "INVALID_EVIDENCE_SET"
    INCONCLUSIVE = "INCONCLUSIVE"
    CONFLICT = "CONFLICT"
    OPEN_CONTRADICTIONS = "OPEN_CONTRADICTIONS"
    CONTRADICTION_REQUIRED = "CONTRADICTION_REQUIRED"


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    """One immutable assessed evidence record supplied to the gate.

    Provenance and quality fields remain assertions by the caller unless an
    outer authority layer independently validates them.
    """

    evidence_ref: str
    side: EvidenceSide
    source_group: str
    provenance_ref: str
    content_digest: str
    observed_at: str
    reliability_milli: int
    relevance_milli: int
    revoked: bool = False

    def __post_init__(self) -> None:
        for name in ("evidence_ref", "source_group", "provenance_ref"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.side, EvidenceSide):
            raise TypeError("side must be an EvidenceSide")
        if not isinstance(self.content_digest, str) or not _SHA256_RE.fullmatch(
            self.content_digest
        ):
            raise ValueError("content_digest must be a lowercase sha256 digest")
        try:
            observed_at = canonical_timestamp(self.observed_at)
        except (TypeError, ValueError) as exc:
            raise ValueError("observed_at must be a canonical timestamp") from exc
        object.__setattr__(self, "observed_at", observed_at)
        for name in ("reliability_milli", "relevance_milli"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")
            if not 0 <= value <= 1000:
                raise ValueError(f"{name} must be between 0 and 1000")
        if not isinstance(self.revoked, bool):
            raise TypeError("revoked must be boolean")

    def to_value(self) -> dict[str, object]:
        return {
            "evidence_ref": self.evidence_ref,
            "side": self.side.value,
            "source_group": self.source_group,
            "provenance_ref": self.provenance_ref,
            "content_digest": self.content_digest,
            "observed_at": self.observed_at,
            "reliability_milli": self.reliability_milli,
            "relevance_milli": self.relevance_milli,
            "revoked": self.revoked,
        }


@dataclass(frozen=True, slots=True)
class EvidenceGatePolicy:
    """Immutable reviewed policy profile, not a command-selected threshold bag."""

    policy_id: str
    allowed_claim_types: tuple[ClaimType, ...]
    minimum_source_groups_for: int
    minimum_source_groups_against: int
    minimum_reliability_milli: int
    minimum_relevance_milli: int
    maximum_age_seconds: int

    def __post_init__(self) -> None:
        if not isinstance(self.policy_id, str) or not self.policy_id.strip():
            raise ValueError("policy_id must be a non-empty string")
        claim_types = tuple(self.allowed_claim_types)
        if not claim_types or any(
            not isinstance(item, ClaimType) for item in claim_types
        ):
            raise TypeError("allowed_claim_types must contain ClaimType values")
        canonical_claim_types = tuple(sorted(set(claim_types), key=lambda item: item.value))
        if canonical_claim_types != claim_types:
            raise ValueError("allowed_claim_types must be sorted and unique")
        object.__setattr__(self, "allowed_claim_types", canonical_claim_types)
        for name in (
            "minimum_source_groups_for",
            "minimum_source_groups_against",
            "maximum_age_seconds",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        for name in ("minimum_reliability_milli", "minimum_relevance_milli"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")
            if not 0 <= value <= 1000:
                raise ValueError(f"{name} must be between 0 and 1000")

    def to_value(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "allowed_claim_types": [item.value for item in self.allowed_claim_types],
            "minimum_source_groups_for": self.minimum_source_groups_for,
            "minimum_source_groups_against": self.minimum_source_groups_against,
            "minimum_reliability_milli": self.minimum_reliability_milli,
            "minimum_relevance_milli": self.minimum_relevance_milli,
            "maximum_age_seconds": self.maximum_age_seconds,
        }


@dataclass(frozen=True, slots=True)
class EvidenceGatePolicyRegistry:
    """Closed set of exact policy profiles approved for one reducer profile."""

    policies: tuple[EvidenceGatePolicy, ...]

    def __post_init__(self) -> None:
        policies = tuple(self.policies)
        if not policies or any(
            not isinstance(policy, EvidenceGatePolicy) for policy in policies
        ):
            raise TypeError("policies must contain EvidenceGatePolicy values")
        identifiers = tuple(policy.policy_id for policy in policies)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("policy IDs must be unique")
        if tuple(sorted(identifiers)) != identifiers:
            raise ValueError("policies must be sorted by policy_id")
        object.__setattr__(self, "policies", policies)

    def get(self, policy_id: str) -> EvidenceGatePolicy | None:
        if not isinstance(policy_id, str) or not policy_id:
            return None
        return next(
            (policy for policy in self.policies if policy.policy_id == policy_id),
            None,
        )

    def require(self, policy_id: str) -> EvidenceGatePolicy:
        policy = self.get(policy_id)
        if policy is None:
            raise KeyError(f"unapproved evidence-gate policy: {policy_id}")
        return policy


P0_015_CONTEXTUAL_POLICY: Final[EvidenceGatePolicy] = EvidenceGatePolicy(
    policy_id="mentaury-evidence-contextual-v1",
    allowed_claim_types=(ClaimType.CONTEXTUAL,),
    minimum_source_groups_for=2,
    minimum_source_groups_against=2,
    minimum_reliability_milli=800,
    minimum_relevance_milli=800,
    maximum_age_seconds=86_400,
)
DEFAULT_EVIDENCE_GATE_POLICIES: Final[EvidenceGatePolicyRegistry] = (
    EvidenceGatePolicyRegistry((P0_015_CONTEXTUAL_POLICY,))
)


@dataclass(frozen=True, slots=True)
class EvidenceGateReceipt:
    profile: str
    belief_id: str
    belief_revision: int
    claim_type: ClaimType
    statement_digest: str
    evaluated_at: str
    policy_id: str
    policy_digest: str
    evidence_set_digest: str
    outcome: EvidenceGateOutcome
    qualifying_for_refs: tuple[str, ...]
    qualifying_against_refs: tuple[str, ...]
    source_groups_for: tuple[str, ...]
    source_groups_against: tuple[str, ...]
    rejected_refs: tuple[str, ...]
    receipt_digest: str

    def __post_init__(self) -> None:
        if self.profile != EVIDENCE_GATE_PROFILE:
            raise ValueError("unsupported evidence-gate profile")
        if not isinstance(self.belief_id, str) or not self.belief_id:
            raise ValueError("belief_id must be a non-empty string")
        if (
            isinstance(self.belief_revision, bool)
            or not isinstance(self.belief_revision, int)
            or self.belief_revision <= 0
        ):
            raise ValueError("belief_revision must be a positive integer")
        if not isinstance(self.claim_type, ClaimType):
            raise TypeError("claim_type must be a ClaimType")
        if not isinstance(self.policy_id, str) or not self.policy_id:
            raise ValueError("policy_id must be a non-empty string")
        for name in (
            "statement_digest",
            "policy_digest",
            "evidence_set_digest",
            "receipt_digest",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
                raise ValueError(f"{name} must be a lowercase sha256 digest")
        try:
            evaluated_at = canonical_timestamp(self.evaluated_at)
        except (TypeError, ValueError) as exc:
            raise ValueError("evaluated_at must be a canonical timestamp") from exc
        object.__setattr__(self, "evaluated_at", evaluated_at)
        if not isinstance(self.outcome, EvidenceGateOutcome):
            raise TypeError("outcome must be an EvidenceGateOutcome")
        for name in (
            "qualifying_for_refs",
            "qualifying_against_refs",
            "source_groups_for",
            "source_groups_against",
            "rejected_refs",
        ):
            value = getattr(self, name)
            if not isinstance(value, tuple) or any(
                not isinstance(item, str) or not item for item in value
            ):
                raise TypeError(f"{name} must be an immutable string sequence")
            if tuple(sorted(set(value))) != value:
                raise ValueError(f"{name} must be sorted and unique")

    def to_value(self) -> dict[str, object]:
        return {
            "profile": self.profile,
            "belief_id": self.belief_id,
            "belief_revision": self.belief_revision,
            "claim_type": self.claim_type.value,
            "statement_digest": self.statement_digest,
            "evaluated_at": self.evaluated_at,
            "policy_id": self.policy_id,
            "policy_digest": self.policy_digest,
            "evidence_set_digest": self.evidence_set_digest,
            "outcome": self.outcome.value,
            "qualifying_for_refs": list(self.qualifying_for_refs),
            "qualifying_against_refs": list(self.qualifying_against_refs),
            "source_groups_for": list(self.source_groups_for),
            "source_groups_against": list(self.source_groups_against),
            "rejected_refs": list(self.rejected_refs),
            "receipt_digest": self.receipt_digest,
        }


@dataclass(frozen=True, slots=True)
class EvidenceGateDecision:
    accepted: bool
    domain_events: tuple[PendingEvent, ...]
    receipt: EvidenceGateReceipt | None = None
    audit_event: PendingEvent | None = None
    rejection_code: EvidenceGateRejectionCode | None = None
    message: str | None = None

    def __post_init__(self) -> None:
        if self.accepted:
            if len(self.domain_events) != 1 or self.receipt is None:
                raise ValueError("accepted gate decision requires one event and receipt")
            if self.audit_event is not None or self.rejection_code is not None:
                raise ValueError("accepted decision cannot contain rejection evidence")
        else:
            if self.domain_events:
                raise ValueError("rejected gate decision cannot mutate domain state")
            if self.audit_event is None or self.rejection_code is None:
                raise ValueError("rejected gate decision requires audit evidence")
