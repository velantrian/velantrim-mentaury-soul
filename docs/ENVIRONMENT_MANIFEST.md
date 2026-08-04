# 🧱 P0 Environment Manifest

```text
Status:             P0-002
Profile:            Python + standard-library SQLite (SQLite not used yet)
Python:             3.13.x
Runtime deps:       NONE
Network at import:  FORBIDDEN
Persistence import: FORBIDDEN
Domain runtime:     FORBIDDEN
```

## Purpose

This manifest records the first replaceable implementation profile for the neutral Mentaury P0 infrastructure. It is not part of the substrate-neutral Canon.

## P0-002 contract boundary

P0-002 adds immutable typed contracts for:

```text
CommandEnvelope
PendingEvent
EventEnvelope
ActorRef
AuthorityRef
ProducerRef
```

Caller-provided payload trees are copied into recursively read-only snapshots. This protects envelope-local immutability but does not claim canonical serialization, cryptographic integrity, schema correctness, persisted immutability, or valid authority.

```text
Envelope construction ≠ authority approval
Frozen payload snapshot ≠ canonical JSON
EventEnvelope value ≠ committed storage row
Payload digest field ≠ verified digest
```

## Deferred milestones

- P0-003 defines `MENTAURY_CANONICAL_JSON_V1` and conformance vectors.
- P0-004 implements immutable events and external payload storage.
- P0-005 adds event/schema registry and structural payload validators.
- Later commits add atomic batch, idempotency, concurrency, R0 and redaction.

## Runtime boundary

The package uses no third-party runtime dependencies. Python's standard library is the only runtime base. SQLite integration begins only in a later sequential P0 commit.

## Supported local commands

```bash
python3 scripts/validate.py
PYTHONPATH=src python3 -m pytest
python3 -m compileall -q src tests scripts
```

## Directory ownership

```text
src/mentaury/core        substrate-level primitives only
src/mentaury/contracts   typed infrastructure contracts
src/mentaury/storage     replaceable storage ports/adapters
src/mentaury/validation  fail-closed structural validation
scripts                  offline repository validation
tests                    deterministic offline tests
```

## Explicit exclusions

P0-002 contains no Event Store, SQLite persistence, canonical serializer, schema registry, authority resolver, identity engine, relationship runtime, Character Engine, Curiosity Controller, Exo-Cortex runtime, autonomous loop, background worker, network connector, persistent self-state, or direct M3 interface.
