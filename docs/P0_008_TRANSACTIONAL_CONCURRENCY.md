# ⚙️ P0-008 — Transactional Concurrency and Busy Handling

```text
Status:             P0-008
Write boundary:     BEGIN IMMEDIATE
Journal profile:    WAL for file databases
Busy handling:      bounded application retries
SQLite minimum:     3.37.0
R0 integrity:       NOT IMPLEMENTED
Domain authority:   NONE
```

## Purpose

P0-008 serializes SQLite writers before they inspect idempotency or mutate event
state. One-event, atomic-batch and idempotent-batch writers now acquire the
reserved write lock through `BEGIN IMMEDIATE`.

```text
lock available → transaction proceeds
lock busy      → bounded retry/backoff
policy exhausted → STORE_BUSY
```

`COMMIT` also uses bounded busy retries; exhausted commit contention rolls back
and returns a controlled `StoreBusyError`.

## Contracts

```text
BusyRetryPolicy
StoreBusyError
VersionConflictError
begin_immediate
commit_with_retry
```

The connection profile exposes an explicit `busy_timeout_ms`; application retry
policy remains bounded and testable. Unsupported SQLite runtimes fail before
storage use. STRICT tables require SQLite ≥3.37.

## Controlled races

```text
same key + same semantic request
→ APPLIED + ALREADY_APPLIED

same key + changed semantic request
→ APPLIED + IDEMPOTENCY_CONFLICT

different keys + same stream/version
→ APPLIED + VERSION_CONFLICT

held write lock beyond policy
→ STORE_BUSY; no partial writes
```

`VersionConflictError` normalizes the unique `(stream_id, stream_version)`
constraint after rollback.

## Deliberate non-claims

```text
BEGIN IMMEDIATE ≠ distributed consensus
WAL ≠ durability proof
VERSION_CONFLICT ≠ stream-head integrity proof
bounded retry ≠ guaranteed eventual success
SQLite lock ≠ authority approval
concurrency safety ≠ event hash verification
```

P0-009 owns `stream_meta`, hash-chain recomputation and full R0 integrity.

## Validation evidence

```text
structural validator → PASS
pytest → 74 passed
compileall → PASS
race suite → repeated successfully
```

## Next milestone

```text
P0-009 FULL R0 + STREAM METADATA VERIFICATION
```
