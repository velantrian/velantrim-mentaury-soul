"""Typed P0 infrastructure contracts.

P0-003 adds deterministic canonical serialization while schema-specific
validation, hashing, persistence, and authority decisions remain owned by later
sequential P0 commits.
"""

from .canonical_json import (
    PROFILE_NAME,
    SAFE_INTEGER_MAX,
    SAFE_INTEGER_MIN,
    CanonicalJSONError,
    canonical_command_bytes,
    canonical_decimal_string,
    canonical_event_bytes,
    canonical_event_hash_input_bytes,
    canonical_json_bytes,
    canonical_json_text,
    canonical_pending_batch_bytes,
    canonical_timestamp,
    command_envelope_value,
    event_envelope_value,
    event_hash_input_value,
    pending_batch_value,
    pending_event_value,
)
from .envelopes import (
    CommandEnvelope,
    EventEnvelope,
    PendingEvent,
    snapshot_pending_batch,
)
from .primitives import ActorRef, AuthorityRef, ProducerRef

__all__ = [
    "PROFILE_NAME",
    "SAFE_INTEGER_MAX",
    "SAFE_INTEGER_MIN",
    "ActorRef",
    "AuthorityRef",
    "CanonicalJSONError",
    "CommandEnvelope",
    "EventEnvelope",
    "PendingEvent",
    "ProducerRef",
    "canonical_command_bytes",
    "canonical_decimal_string",
    "canonical_event_bytes",
    "canonical_event_hash_input_bytes",
    "canonical_json_bytes",
    "canonical_json_text",
    "canonical_pending_batch_bytes",
    "canonical_timestamp",
    "command_envelope_value",
    "event_envelope_value",
    "event_hash_input_value",
    "pending_batch_value",
    "pending_event_value",
    "snapshot_pending_batch",
]
