"""P0-014 neutral contracts for the minimal M2 belief lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from mentaury.contracts import PendingEvent


CREATE_BELIEF = "CREATE_BELIEF"
ATTACH_EVIDENCE = "ATTACH_EVIDENCE"
REGISTER_CONTRADICTION = "REGISTER_CONTRADICTION"
REVISE_BELIEF = "REVISE_BELIEF"

BELIEF_CREATED = "BELIEF_CREATED"
EVIDENCE_ATTACHED = "EVIDENCE_ATTACHED"
CONTRADICTION_REGISTERED = "CONTRADICTION_REGISTERED"
BELIEF_REVISED = "BELIEF_REVISED"

COMMAND_REJECTED = "COMMAND_REJECTED"
BELIEF_REVISION_REJECTED = "BELIEF_REVISION_REJECTED"
AUTHORITY_CHECK_FAILED = "AUTHORITY_CHECK_FAILED"
INVARIANT_CHECK_FAILED = "INVARIANT_CHECK_FAILED"

BELIEF_CREATED_SCHEMA = "belief-created/v1"
EVIDENCE_ATTACHED_SCHEMA = "evidence-attached/v1"
CONTRADICTION_REGISTERED_SCHEMA = "contradiction-registered/v1"
BELIEF_REVISED_SCHEMA = "belief-revised/v1"
BELIEF_DECISION_SCHEMA = "belief-decision/v1"


class ClaimType(StrEnum):
    UNIVERSAL = "universal"
    STATISTICAL = "statistical"
    CAUSAL = "causal"
    CONTEXTUAL = "contextual"
    EXISTENTIAL = "existential"
    UNSPECIFIED = "unspecified"


class BeliefStatus(StrEnum):
    HYPOTHESIS = "hypothesis"
    PROVISIONAL = "provisional"
    SUPPORTED = "supported"
    CONTESTED = "contested"
    CONTRADICTED = "contradicted"
    SUPERSEDED = "superseded"
    UNRESOLVED = "unresolved"


class EvidenceSide(StrEnum):
    FOR = "for"
    AGAINST = "against"


class BeliefRejectionCode(StrEnum):
    INVALID_COMMAND = "INVALID_COMMAND"
    TARGET_STREAM_MISMATCH = "TARGET_STREAM_MISMATCH"
    BELIEF_ALREADY_EXISTS = "BELIEF_ALREADY_EXISTS"
    BELIEF_NOT_FOUND = "BELIEF_NOT_FOUND"
    TERMINAL_BELIEF = "TERMINAL_BELIEF"
    DUPLICATE_EVIDENCE = "DUPLICATE_EVIDENCE"
    DUPLICATE_CONTRADICTION = "DUPLICATE_CONTRADICTION"
    UNKNOWN_EVIDENCE_REF = "UNKNOWN_EVIDENCE_REF"
    UNKNOWN_CONTRADICTION = "UNKNOWN_CONTRADICTION"
    REVISION_CONFLICT = "REVISION_CONFLICT"
    INVALID_STATUS_TRANSITION = "INVALID_STATUS_TRANSITION"
    NO_EFFECT = "NO_EFFECT"


@dataclass(frozen=True, slots=True)
class BeliefDecision:
    """Pure decision result; persistence remains an explicit caller action."""

    accepted: bool
    domain_events: tuple[PendingEvent, ...]
    audit_event: PendingEvent | None = None
    rejection_code: BeliefRejectionCode | None = None
    message: str | None = None

    def __post_init__(self) -> None:
        if self.accepted:
            if not self.domain_events:
                raise ValueError("accepted decision requires a domain event")
            if self.audit_event is not None or self.rejection_code is not None:
                raise ValueError("accepted decision cannot contain rejection evidence")
        else:
            if self.domain_events:
                raise ValueError("rejected decision cannot mutate domain state")
            if self.audit_event is None or self.rejection_code is None:
                raise ValueError("rejected decision requires an audit event and code")


def belief_stream_id(belief_id: str) -> str:
    if not isinstance(belief_id, str) or not belief_id.strip():
        raise ValueError("belief_id must be a non-empty string")
    return f"belief:{belief_id}"
