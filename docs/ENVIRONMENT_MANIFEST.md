# 🧱 P0 Environment Manifest

```text
Status:             P0-005
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
```

## P0-005 boundary

```text
EventSchemaDefinition
→ event type / payload schema identity
→ envelope version + state-effect expectation
→ strict recursive payload shape
→ stable ValidationIssue collection
```

Unknown event types fail closed. Object schemas reject undeclared fields by
default. Numeric and Unicode admission aligns with P0-003.

```text
Schema validity ≠ truth
Structural match ≠ semantic correctness
Registered event ≠ authorized event
Validation ≠ persistence
Registry definition ≠ Canon
```

Validation is not automatically embedded in storage. Later command and batch
orchestration must invoke it explicitly.

## Explicit initialization

Importing the package creates no connection and writes no state. Storage still
requires explicit `connect()` and `initialize_schema()` calls.

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
src/mentaury/storage     explicit replaceable storage adapters
src/mentaury/validation  fail-closed registry and structural validators
scripts                  offline repository validation
tests                    deterministic offline tests + vectors
```

## Deferred milestones

- P0-006: real ordered atomic multi-event append.
- P0-007: event-aware idempotency.
- P0-008: controlled concurrency and busy handling.
- P0-009: full R0 and stream metadata verification.
- P0-010: governed atomic same-stream redaction.

## Explicit exclusions

P0-005 contains no authority resolver, semantic belief validator, hash verifier,
multi-event command handler, idempotency engine, concurrency controller,
redaction workflow, identity engine, relationship runtime, Character Engine,
Curiosity Controller, Exo-Cortex runtime, autonomous loop, background worker,
network connector, persistent self-state, or direct M3 interface.
