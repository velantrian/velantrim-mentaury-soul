# 🧱 P0 Environment Manifest

```text
Status:             P0-009
Profile:            Python 3.13 + standard-library SQLite 3.46.1
Minimum SQLite:     3.37.0
Journal mode:       WAL for file databases
Storage schema:     v3
Runtime deps:       NONE
Network at import:  FORBIDDEN
Database at import: FORBIDDEN
Domain runtime:     FORBIDDEN
```

## Implemented boundary

```text
P0-001 neutral skeleton
P0-002 typed envelopes
P0-003 canonical JSON
P0-004 immutable event/external payload storage
P0-005 fail-closed structural validation
P0-006 atomic multi-event batch
P0-007 semantic idempotency
P0-008 controlled SQLite concurrency
P0-009 full R0 + stream metadata verification
```

Schema v3 adds `stream_meta(current_version, last_event_hash, event_count)` and
backfills it during explicit migration. Every write updates metadata in the same
transaction. R0 independently recomputes payload digests, event hashes, chain,
versions, batches and the ledger tail.

```text
R0 consistency ≠ truth
Hash chain ≠ authority
stream_meta ≠ source of truth
```

Supported commands:

```bash
python3 scripts/validate.py
PYTHONPATH=src python3 -m pytest
python3 -m compileall -q src tests scripts
```

P0-010 owns governed atomic same-stream redaction. No identity, relationship,
Character, Curiosity or Exo-Cortex runtime is present.
