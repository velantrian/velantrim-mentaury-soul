# 🧱 P0 Environment Manifest

```text
Status:             P0-006
Profile:            Python 3.13 + standard-library SQLite 3.46.1
Runtime deps:       NONE
Network at import:  FORBIDDEN
Database at import: FORBIDDEN
Domain runtime:     FORBIDDEN
```

## Implemented boundary

```text
P0-001 → neutral package skeleton
P0-002 → immutable typed envelope contracts
P0-003 → MENTAURY_CANONICAL_JSON_V1
P0-004 → immutable SQLite event rows + external payload bytes
P0-005 → fail-closed structural event/payload validation
P0-006 → real ordered atomic multi-event batch append
```

## P0-006 transaction boundary

```text
batch preflight + canonicalization
→ BEGIN
→ ordered payload/event inserts
→ COMMIT or full ROLLBACK
```

The first profile permits one target stream per batch and requires coherent
batch metadata, contiguous versions, common causation/correlation context, and
unique event/payload identifiers.

```text
Atomic batch ≠ idempotency
Atomic batch ≠ concurrency control
Contiguous versions ≠ verified stream head
Shared authority ref ≠ authority approval
```

## Runtime boundary

The package has no third-party runtime dependencies. SQLite is accessed through
Python's standard library; the tested runtime is `3.46.1`.

## Supported local commands

```bash
python3 scripts/validate.py
PYTHONPATH=src python3 -m pytest
python3 -m compileall -q src tests scripts
```

## Directory ownership

```text
src/mentaury/core        substrate-level primitives only
src/mentaury/contracts   typed contracts + canonical serialization
src/mentaury/storage     immutable storage + atomic batch primitives
src/mentaury/validation  fail-closed registry and structural validators
scripts                  offline repository validation
tests                    deterministic offline tests + vectors
```

## Deferred milestones

- P0-007: event-aware idempotency fingerprint and result replay.
- P0-008: transactional concurrency and controlled busy handling.
- P0-009: full R0 and stream metadata verification.
- P0-010: governed atomic same-stream redaction.

## Explicit exclusions

P0-006 contains no idempotency engine, concurrency controller, authority
resolver, semantic belief validator, hash verifier, stream-head verifier,
redaction workflow, identity engine, relationship runtime, Character Engine,
Curiosity Controller, Exo-Cortex runtime, autonomous loop, background worker,
network connector, persistent self-state, or direct M3 interface.
