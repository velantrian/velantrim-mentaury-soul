# 📨 P0-002 Envelope Contracts

```text
Status:               IMPLEMENTED
Milestone:            P0-002
Implementation:       Python 3.13 profile
Runtime dependencies: NONE
Persistence:          NONE
Canonical JSON:       DEFERRED TO P0-003
Schema registry:      DEFERRED TO P0-005
```

## Purpose

P0-002 separates submitted intent, proposed facts, and committed event metadata through three immutable infrastructure contracts.

```text
CommandEnvelope
→ submitted intent

PendingEvent
→ proposed fact before commit

EventEnvelope
→ metadata of one committed event with external payload reference
```

Constructing any envelope does not prove authority, truth, persistence, cryptographic integrity, or successful commit.

## Shared references

```text
ActorRef
→ actor type + attributable actor id

AuthorityRef
→ capability lease id + revision

ProducerRef
→ component id + implementation version
```

`AuthorityRef` is a reference to an external authority record. It is never treated as an embedded trusted permission copy.

## CommandEnvelope

```text
command_id
command_type
command_schema
target_stream
expected_stream_version
issued_at
issuer
authority
correlation_id
idempotency_key
payload
```

The command remains intent. No event exists merely because the command object was constructed.

## PendingEvent

```text
event_type
payload_schema
affects_domain_state
payload
```

A pending event has no assigned event id, stream version, batch position, payload digest, previous hash, or event hash.

## EventEnvelope

```text
event_id
event_type
envelope_schema_version
payload_schema
stream_id
stream_version
batch_id
batch_index
batch_size
occurred_at
recorded_at
producer
initiator
authority
causation_id
correlation_id
affects_domain_state
payload_digest
payload_ref
previous_hash
event_hash
```

The envelope contains a payload reference and digest, not payload bytes. Actual committed-row immutability and digest verification begin in later P0 milestones.

## Local immutability

Caller-provided payload mappings and sequences are copied recursively into read-only mappings and tuples.

```text
Caller mutation after construction
≠ envelope payload mutation
```

This is a local object-safety property only:

```text
Frozen Python object
≠ canonical serialization
≠ persisted immutable row
≠ verified cryptographic hash
```

## Basic invariants

P0-002 enforces only contract-local conditions:

- required identifiers are non-empty;
- stream versions and revisions are non-negative or positive as applicable;
- event batch size is positive;
- `0 <= batch_index < batch_size`;
- actor, authority and producer fields use typed references;
- pending batches are non-empty and ordered;
- payload object keys are strings;
- payload values exclude non-portable binary objects.

Timestamp format, identifier grammar, safe integer limits, float policy, event/schema compatibility, strict payload fields and hash format are deliberately deferred.

## Scope exclusions

```text
No Event Store
No SQLite persistence
No canonical JSON
No event/schema registry
No command handler
No authority resolver
No hashing implementation
No atomic append
No identity or relationship runtime
No Exo-Cortex or Character runtime
```

## Validation evidence

```text
python3 scripts/validate.py
→ PASS

PYTHONPATH=src python3 -m pytest
→ 12 passed

python3 -m compileall -q src tests scripts
→ PASS

editable package build/import
→ PASS
```
