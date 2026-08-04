# 🔑 P0-007 — Event-Aware Idempotency Fingerprint

```text
Status:             P0-007
Profile:            MENTAURY_IDEMPOTENCY_V1
Scope:              semantic command + ordered pending batch
Storage schema:     v2
Concurrency races:  NOT CONTROLLED
Hash-chain proof:   NOT IMPLEMENTED
Domain authority:   NONE
```

## Purpose

P0-007 distinguishes a legitimate retry from reuse of the same idempotency key for a different mutation.

```text
same key + same semantic command + same ordered pending batch
→ ALREADY_APPLIED + original receipt

same key + changed semantics
→ IDEMPOTENCY_CONFLICT
```

No payload or event row is appended during `ALREADY_APPLIED` replay.

## Fingerprint input

The SHA-256 fingerprint covers profile, command type/schema, target stream, expected version, issuer/authority, command payload, and the ordered PendingEvent batch.

Volatile commit metadata is excluded:

```text
command_id · issued_at · correlation_id
batch_id · event_id · payload_ref
timestamps · producer · payload_digest
event_hash · previous_hash
```

```text
idempotency key ≠ command ID
fingerprint ≠ event hash
semantic retry ≠ duplicate append
```

## Alignment contract

`IdempotentBatchRequest` requires command, pending events, and committed entries to agree on stream/version, issuer/initiator, authority, causation/correlation links, event type/schema/state-effect, payload bytes, count, and order.

`BatchEntry` takes a recursive detached payload snapshot so nested caller mutation cannot alter persisted bytes after alignment.

## Atomic storage

Schema v2 adds immutable `idempotency_records` and migrates explicitly from v1.

```text
BEGIN
├── look up idempotency key
├── append payloads + immutable events
├── insert immutable idempotency record + receipt
COMMIT
```

If the idempotency-record insert fails, the complete new batch is rolled back. Idempotency records cannot be updated or deleted directly.

## Deliberate non-claims

```text
Idempotency fingerprint ≠ authorization
ALREADY_APPLIED ≠ integrity verification
Stored receipt ≠ governance receipt
SHA-256 fingerprint ≠ event hash chain
Single-writer correctness ≠ concurrent-writer correctness
Immutable record trigger ≠ tamper-proof database
```

P0-008 owns concurrent writers and busy handling. P0-009 owns full R0 integrity.

## Validation evidence

```text
structural validator → PASS
pytest → 68 passed
compileall → PASS
```

Changed command payload, pending payload, event type, schema, event count, and event order all produce controlled conflicts.

## Next milestone

```text
P0-008 TRANSACTIONAL CONCURRENCY AND BUSY HANDLING
```
