# 📦 P0-006 — Real Atomic Multi-Event Batch

```text
Status:            P0-006
Scope:             one coherent ordered batch / one SQLite transaction
Target streams:    exactly one stream per batch
Schema authority:  external, not hidden in storage
Idempotency:       NOT IMPLEMENTED
Concurrency:       NOT IMPLEMENTED
Hash verification: NOT IMPLEMENTED
```

## Purpose

P0-006 upgrades the P0-004 one-event primitive into a real ordered batch where
all external payloads and immutable event rows are committed together or not at
all.

```text
prepare complete batch
→ validate batch coherence
→ canonicalize every payload
→ BEGIN
   for each ordered entry:
     insert payload
     insert immutable event row
→ COMMIT
```

Any SQL failure triggers `ROLLBACK` for the complete new batch.

## Batch contracts

```text
BatchEntry
BatchAppendReceipt
BatchInvariantError
SQLiteAtomicBatchAppender
```

A valid batch requires at least one entry, one batch ID, one target stream,
ordered indexes `0…N−1`, `batch_size == N`, contiguous stream versions, common
causation/correlation context, identical initiator/authority references, and
unique event/payload identifiers.

These are coherence rules, not authority approval.

## Preflight before transaction

All payloads are canonicalized before `BEGIN`. Invalid JSON values therefore
cannot open or partially mutate a transaction.

```text
serialization failure
→ no transaction
→ zero rows
```

## Atomicity evidence

```text
successful 3-event batch → all events + all payloads
middle event conflict     → zero new events + zero new payloads
late payload conflict     → prior new rows rolled back
pre-existing history      → preserved
```

## Receipt semantics

`BatchAppendReceipt` reports batch ID, stream ID, ordered event IDs, and the
first/last stream versions. It is an operation result, not authority, truth,
integrity, or idempotency proof.

## Deliberate non-claims

```text
Atomic batch ≠ idempotent retry
Atomic batch ≠ concurrency control
Contiguous versions ≠ verified stream head
Stored hash ≠ verified hash chain
Shared authority ref ≠ authority approval
Batch receipt ≠ governance receipt
```

A repeated identical batch currently reaches SQLite uniqueness constraints and
fails. P0-007 owns event-aware idempotency and controlled result replay.

## Validation evidence

```text
structural validator → PASS
pytest → 55 passed
compileall → PASS
```

## Next milestone

```text
P0-007 EVENT-AWARE IDEMPOTENCY FINGERPRINT
```
