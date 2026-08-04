# 🧱 P0 Environment Manifest

```text
Status:             P0-004
Profile:            Python 3.13 + standard-library SQLite 3.46.1
Runtime deps:       NONE
Network at import:  FORBIDDEN
Database at import: FORBIDDEN
Domain runtime:     FORBIDDEN
```

## Purpose

This manifest records the first replaceable implementation profile for the
neutral Mentaury P0 infrastructure. It is not part of the substrate-neutral
Canon.

## Implemented boundary

```text
P0-001 → neutral package skeleton
P0-002 → immutable typed envelope contracts
P0-003 → MENTAURY_CANONICAL_JSON_V1
P0-004 → immutable SQLite event rows + external payload bytes
```

## Explicit initialization

Importing the package creates no connection and writes no state. Storage use
requires:

```text
SQLiteEventPayloadStore.connect(path)
→ initialize_schema()
→ explicit operations
```

## P0-004 persistence boundary

```text
events          → immutable metadata rows
event_payloads  → separately stored canonical payload bytes
```

SQLite triggers reject event UPDATE/DELETE and payload-byte rewrites. The public
adapter exposes no redaction/delete method yet.

```text
SQLite trigger ≠ tamper-proof security boundary
Single-event transaction ≠ multi-event batch
Stored hash ≠ verified hash
External payload table ≠ governed redaction
```

## Runtime boundary

The package has no third-party runtime dependencies. SQLite is accessed only
through Python's standard library. The tested SQLite runtime is `3.46.1`.

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
src/mentaury/validation  fail-closed structural validation
scripts                  offline repository validation
tests                    deterministic offline tests + vectors
```

## Deferred milestones

- P0-005 adds event/schema registry and structural validators.
- P0-006 implements real ordered atomic multi-event batch append.
- P0-007 adds event-aware idempotency.
- P0-008 adds controlled concurrency and busy handling.
- P0-009 adds full R0 and stream metadata verification.
- P0-010 adds governed atomic same-stream redaction.

## Explicit exclusions

P0-004 contains no authority resolver, schema registry, hash verifier,
multi-event command handler, idempotency engine, concurrency controller,
redaction workflow, identity engine, relationship runtime, Character Engine,
Curiosity Controller, Exo-Cortex runtime, autonomous loop, background worker,
network connector, persistent self-state, or direct M3 interface.
