# 🧱 P0 Environment Manifest

```text
Status:             P0-008
Profile:            Python 3.13 + standard-library SQLite 3.46.1
Minimum SQLite:     3.37.0
Journal mode:       WAL for file databases
Storage schema:     v2
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
```

All write paths use `BEGIN IMMEDIATE`; busy lock acquisition and commit use a
bounded `BusyRetryPolicy`. File databases use WAL. Same-version uniqueness is
normalized to `VersionConflictError` after rollback.

```text
SQLite concurrency ≠ distributed consensus
WAL ≠ R0 integrity
VERSION_CONFLICT ≠ verified stream head
```

Supported local commands:

```bash
python3 scripts/validate.py
PYTHONPATH=src python3 -m pytest
python3 -m compileall -q src tests scripts
```

P0-009 adds stream metadata and full integrity verification. No authority,
identity, relationship, Character, Curiosity or Exo-Cortex runtime is present.
