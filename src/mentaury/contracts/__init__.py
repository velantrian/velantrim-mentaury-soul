"""Typed P0 infrastructure contracts.

P0-002 provides immutable envelope shapes only. Canonical serialization,
schema-specific validation, hashing, persistence, and authority decisions are
owned by later sequential P0 commits.
"""

from .envelopes import (
    CommandEnvelope,
    EventEnvelope,
    PendingEvent,
    snapshot_pending_batch,
)
from .primitives import ActorRef, AuthorityRef, ProducerRef

__all__ = [
    "ActorRef",
    "AuthorityRef",
    "CommandEnvelope",
    "EventEnvelope",
    "PendingEvent",
    "ProducerRef",
    "snapshot_pending_batch",
]
