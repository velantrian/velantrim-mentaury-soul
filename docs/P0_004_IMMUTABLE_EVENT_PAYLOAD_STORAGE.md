# 🗄️ P0-004 — Immutable Event Rows + External Payload Store

```text
Status:             P0-004
Profile:            SQLite 3.46.1 via Python standard library
Scope:              one-event storage primitive
Runtime deps:       NONE
Schema validation:  NOT IMPLEMENTED
Hash verification:  NOT IMPLEMENTED
Multi-event batch:  NOT IMPLEMENTED
Redaction workflow: NOT IMPLEMENTED
Domain authority:   NONE
```

## Purpose

P0-004 introduces the first explicit persistence adapter. Immutable event
metadata and erasable payload material are physically separated:

```text
events
→ immutable historical metadata

event_payloads
→ external canonical payload bytes
```

Importing `mentaury.storage` opens no database. A caller must explicitly connect
and initialize the schema.

## Storage model

The `events` table stores the complete `EventEnvelope` metadata as typed columns.
It does not contain payload bytes. The `event_payloads` table stores:

```text
payload_ref
payload_bytes
created_at
```

There is deliberately no foreign key from `events.payload_ref` to
`event_payloads.payload_ref`: future redaction must be able to remove payload
material while preserving the historical event row.

## Physical event-row immutability

SQLite triggers reject:

```text
UPDATE events
DELETE FROM events
```

Payload material also cannot be rewritten in place. P0-004 exposes no public
payload deletion or redaction API; the governed atomic redaction workflow belongs
to P0-010.

## Single-event transaction

`append_one(event, payload)` performs:

```text
canonicalize payload
BEGIN
├── INSERT external payload bytes
├── INSERT immutable event row
COMMIT
```

Any failure rolls back both inserts. This proves one-event/payload atomicity only.
Real ordered multi-event batch append remains P0-006.

## Reconstruction

`load_event(event_id)` reconstructs the complete immutable `EventEnvelope`.
`list_stream(stream_id)` returns reconstructed envelopes ordered by
`stream_version`. `load_payload(payload_ref)` returns external canonical bytes
without interpreting domain schema.

## Deliberate boundaries

```text
Stored digest field ≠ verified digest
Stored hash field ≠ verified hash
Unique stream version ≠ concurrency protocol
Single-event transaction ≠ real atomic batch
SQLite trigger ≠ tamper-proof database
External payload table ≠ governed redaction
Canonical payload bytes ≠ valid domain schema
```

The adapter records already-formed envelope fields. It does not allocate stream
versions, resolve authority, validate event/schema pairs, compute hashes, or
claim epistemic truth.

## Validation

```text
pytest → 30 passed
compileall → PASS
structural validator → PASS
```

Coverage includes:

- explicit initialization;
- separate event and payload tables;
- complete envelope reconstruction;
- normalized stored timestamps;
- direct event UPDATE/DELETE rejection;
- payload rewrite rejection;
- rollback when event insert fails;
- ordered stream reads;
- persistence across reopen;
- explicit proof that P0-004 records but does not verify hashes.

## Next milestone

```text
P0-005 STRUCTURAL EVENT / PAYLOAD SCHEMA VALIDATORS
```
