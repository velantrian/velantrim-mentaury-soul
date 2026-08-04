"""Explicit P0 storage adapters.

Importing this namespace opens no database and persists no state.
"""

from .sqlite_store import (
    SCHEMA_VERSION,
    SQLiteEventPayloadStore,
    StorageError,
    StoredPayload,
    StoreNotInitializedError,
)

__all__ = [
    "SCHEMA_VERSION",
    "SQLiteEventPayloadStore",
    "StorageError",
    "StoredPayload",
    "StoreNotInitializedError",
]
