# 🧱 P0 Environment Manifest

```text
Status:             P0-003
Profile:            Python + standard-library SQLite (SQLite not used yet)
Python:             3.13.x
Runtime deps:       NONE
Network at import:  FORBIDDEN
Persistence import: FORBIDDEN
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
```

P0-003 provides deterministic UTF-8 serialization, strict numeric admission,
Unicode scalar validation, explicit decimal-string normalization, UTC timestamp
normalization, envelope projections, event hash-input bytes, and conformance
vectors.

```text
Canonical serialization ≠ schema correctness
Canonical serialization ≠ hash verification
Canonical serialization ≠ persisted immutability
Canonical serialization ≠ valid authority
```

## Numeric and text policy

```text
Float / NaN / Infinity → FORBIDDEN
Safe integer range     → ±(2^53-1)
Decimal object         → FORBIDDEN implicitly
Decimal helper output  → explicit schema-controlled string
Unicode normalization  → NONE
Lone surrogate         → FORBIDDEN
```

## Deferred milestones

- P0-004 implements immutable events and external payload storage.
- P0-005 adds event/schema registry and structural payload validators.
- Later commits add atomic batch, idempotency, concurrency, R0 and redaction.

## Runtime boundary

The package uses no third-party runtime dependencies. Python's standard library
is the only runtime base. SQLite integration begins only in a later sequential
P0 commit.

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
src/mentaury/storage     replaceable storage ports/adapters
src/mentaury/validation  fail-closed structural validation
scripts                  offline repository validation
tests                    deterministic offline tests + vectors
```

## Explicit exclusions

P0-003 contains no Event Store, SQLite persistence, schema registry, authority
resolver, hash engine, identity engine, relationship runtime, Character Engine,
Curiosity Controller, Exo-Cortex runtime, autonomous loop, background worker,
network connector, persistent self-state, or direct M3 interface.
