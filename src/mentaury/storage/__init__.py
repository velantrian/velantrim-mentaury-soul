"""Explicit P0 storage, batch, and idempotency primitives."""

from .atomic_batch import (
    BatchAppendReceipt,
    BatchEntry,
    BatchInvariantError,
    SQLiteAtomicBatchAppender,
)
from .concurrency import (
    DEFAULT_BUSY_RETRY_POLICY,
    BusyRetryPolicy,
    StoreBusyError,
    VersionConflictError,
)
from .integrity import (
    IntegrityCode,
    IntegrityFailure,
    R0IntegrityReport,
    R0IntegrityVerifier,
    compute_event_hash,
    compute_payload_digest,
    seal_event,
)
from .stream_meta import GENESIS_HASH, StreamMeta
from .idempotency import (
    IDEMPOTENCY_PROFILE,
    IdempotencyConflictError,
    IdempotencyInvariantError,
    IdempotencyStatus,
    IdempotentAppendResult,
    IdempotentBatchRequest,
    SQLiteIdempotentBatchAppender,
    idempotency_fingerprint,
)
from .sqlite_store import (
    MINIMUM_SQLITE_VERSION,
    SCHEMA_VERSION,
    SQLiteEventPayloadStore,
    StorageError,
    StoredPayload,
    StoreNotInitializedError,
    ensure_supported_sqlite_runtime,
)

__all__ = [
    "DEFAULT_BUSY_RETRY_POLICY",
    "GENESIS_HASH",
    "IntegrityCode",
    "IntegrityFailure",
    "R0IntegrityReport",
    "R0IntegrityVerifier",
    "StreamMeta",
    "IDEMPOTENCY_PROFILE",
    "BusyRetryPolicy",
    "BatchAppendReceipt",
    "BatchEntry",
    "BatchInvariantError",
    "IdempotencyConflictError",
    "IdempotencyInvariantError",
    "IdempotencyStatus",
    "IdempotentAppendResult",
    "IdempotentBatchRequest",
    "MINIMUM_SQLITE_VERSION",
    "SCHEMA_VERSION",
    "SQLiteAtomicBatchAppender",
    "SQLiteEventPayloadStore",
    "SQLiteIdempotentBatchAppender",
    "StorageError",
    "StoredPayload",
    "StoreBusyError",
    "StoreNotInitializedError",
    "VersionConflictError",
    "compute_event_hash",
    "compute_payload_digest",
    "seal_event",
    "ensure_supported_sqlite_runtime",
    "idempotency_fingerprint",
]
