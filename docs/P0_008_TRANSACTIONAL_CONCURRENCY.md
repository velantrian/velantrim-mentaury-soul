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

## Transaction ownership (Stage 01 remediation)

```text
Public writers + initialize_schema REQUIRE AN IDLE CONNECTION.
OPERATION MAY COMMIT OR ROLLBACK ONLY ITS OWN TRANSACTION.
```

`TransactionOwnershipError` (also exported from `mentaury.storage`) is raised
when `connection.in_transaction` is already true: in `begin_immediate` before
any BEGIN or retry, and in `initialize_schema` before the first `executescript`,
DDL or PRAGMA. The refusal neither commits nor rolls back the caller's work.
Writers call `begin_immediate` *before* their rollback-guarded `try` block, so
their handlers only ever undo a transaction they opened themselves. This
includes idempotent replay (`ALREADY_APPLIED` / `ALREADY_REDACTED`) paths, which
are refused rather than answered inside a foreign transaction.

```text
isolation_level=None / autocommit=True   → idle connection supported
isolation_level="" / "IMMEDIATE" (legacy) → supported while idle; a driver-opened
                                            implicit BEGIN is a foreign transaction
autocommit=False                         → always in a transaction → always refused
```

`commit_with_retry` and every writer's failure handler end the operation's *own*
transaction through `rollback_after_failure`. Non-busy COMMIT failures
(`IntegrityError` from deferred foreign keys, authorizer denials, any other
`sqlite3.Error`) are rolled back and re-raised unchanged; a failing ROLLBACK is
attached to the original error as a note and never replaces it, and success is
claimed only once `in_transaction` is verifiably false. A failed BEGIN opened
nothing and is never followed by a rollback.

No savepoint-based composition is provided, and sharing one connection between
concurrent threads is not a supported contract. Ownership is not authority:
this guard grants no runtime, action or deployment authority.

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
