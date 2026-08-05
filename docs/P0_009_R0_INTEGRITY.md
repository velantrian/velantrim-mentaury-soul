# 🔗 P0-009 — Trusted Commit Boundary + Full R0 Verification

```text
Status:             DRAFT · OPEN PR #15 · NOT MERGED
Storage schema:     v3 candidate
Integrity profile:  trusted write allocation + bounded R0 verification
Failure mode:       fail closed / first actionable failure
Payload redaction:  NOT IMPLEMENTED
Replay:             NOT IMPLEMENTED
Domain truth:       NOT CLAIMED
Permanent CI:       NOT PRESENT
```

## Purpose

P0-009 must prove three separate properties:

```text
WRITE PATH
→ only structurally admitted, canonically encoded, transactionally sealed events commit

R0 VERIFIER
→ persisted ledger, payload material, hash chain, batches and stream metadata remain consistent

RESOURCE ENVELOPE
→ verification and populated migration stop at explicit caller-supplied limits
```

Post-write diagnosis is not a substitute for a trusted commit boundary. A valid
ledger is not permission to consume unbounded resources.

---

## 1. Trusted production writes

All production write paths require an explicit immutable `SchemaRegistry`:

```text
EventEnvelope proposal + payload
→ registered event/schema identity
→ structural payload validation
→ canonical payload bytes
→ BEGIN IMMEDIATE
→ locked stream tail / expected version
→ canonical payload digest allocation
→ previous_hash allocation from locked tail
→ canonical event_hash allocation
→ payload + immutable event + stream_meta
→ COMMIT
```

Caller-supplied `payload_digest`, `previous_hash` and `event_hash` are
non-authoritative inputs. The committed envelope returned by the store contains
the fields allocated by the trusted write path.

The same rule applies to:

- `SQLiteEventPayloadStore.append_one`;
- `SQLiteAtomicBatchAppender.append`;
- `SQLiteIdempotentBatchAppender.append`.

`append_one` additionally rejects any envelope that does not represent exactly
one complete event batch:

```text
batch_size == 1
batch_index == 0
```

Atomic batches are sealed sequentially under one write lock, so each event uses
the previous committed event hash from the same transaction.

---

## 2. Schema v3 and stream metadata

Schema v3 adds:

```text
stream_meta(
  stream_id,
  current_version,
  last_event_hash,
  event_count
)
```

Every accepted write updates metadata in the same transaction as payload and
immutable event rows. `stream_meta` remains a mutable acceleration/index record,
not the authoritative source of history.

---

## 3. Explicit resource budgets

R0 verification requires a caller-supplied `VerificationBudget`:

```text
max_events
max_payload_bytes
max_total_payload_bytes
```

Populated v2 → v3 migration requires the same explicit budget in addition to a
`SchemaRegistry`.

There is deliberately no global default:

```text
Test profile numbers       ≠ Canon
Deployment budget          ≠ Identity policy
Budget exhaustion          ≠ integrity corruption
No supplied budget         → operation not admitted
Exceeded supplied budget   → RESOURCE_BUDGET_EXCEEDED
```

The event-count limit is checked before the stream is materialized. Per-payload
and cumulative payload limits are checked before decoding and deeper validation.

---

## 4. Fail-closed v2 → v3 migration

An empty v2 database can be upgraded without a registry or budget. A populated
v2 ledger requires both and is verified under a write lock before `stream_meta`
is created or backfilled.

Migration verifies:

1. declared event-count budget;
2. contiguous versions;
3. complete ordered batches;
4. payload presence and declared byte budgets;
5. UTF-8 JSON decoding and exact canonical bytes;
6. registered event/schema identity;
7. structural payload validity;
8. payload digest recomputation;
9. previous-hash continuity;
10. event-hash recomputation.

Any failure rolls back the migration:

```text
corruption or budget exhaustion
→ no stream_meta table accepted
→ schema version remains v2
→ explicit repair, larger authorized profile, or review required
```

---

## 5. R0 verification

R0 independently verifies:

```text
1. check event-count budget before stream materialization
2. reconstruct immutable envelope
3. verify stream_version sequence
4. verify batch completeness and order
5. verify registered event/schema pair
6. load payload and check per-payload/cumulative budgets
7. decode payload and verify canonical bytes
8. validate payload structure
9. recompute payload_digest
10. verify previous_hash continuity
11. recompute event_hash
12. compare stream_meta tail version/hash/count
13. return first actionable failure
```

Stable diagnostic codes include:

- resource-budget exhaustion;
- stream version gaps;
- incomplete or out-of-order batches;
- schema defects;
- missing, undecodable, or non-canonical payloads;
- payload digest mismatch;
- previous-hash mismatch;
- event-hash mismatch;
- stream metadata version/hash/count mismatch.

---

## 6. Adversarial evidence required

The P0-009 test set covers or must cover:

- caller-supplied fake hash fields are not persisted;
- schema rejection leaves payload, event, idempotency record, and `stream_meta` unchanged;
- incoherent single-event batch is rejected with zero writes;
- atomic/idempotent failures roll back all rows and metadata;
- stored non-canonical payload bytes are detected;
- corrupted populated v2 migration fails closed;
- valid populated v2 migration verifies history before backfill;
- populated migration without registry or budget is rejected;
- event-count, per-payload and cumulative budget exhaustion is controlled;
- unexpected and exhausted busy `COMMIT` failures roll back;
- overlapping `OneOfSpec` matches are rejected;
- cyclic payload containers are rejected without uncontrolled recursion.

---

## Validation status

A temporary validation-only branch previously passed structural validation,
full pytest and compileall for the pre-budget head. Because budget contracts
changed the PR after that run, fresh exact-head evidence is required.

```text
Structural validator → PENDING ON CURRENT HEAD
Full pytest          → PENDING ON CURRENT HEAD
Compileall           → PENDING ON CURRENT HEAD
Permanent P0-012 CI  → NOT PRESENT
```

A validation-only workflow is not part of PR #15 or `main` and does not count as
P0-012.

---

## Non-claims

```text
R0 consistency ≠ epistemic truth
Hash continuity ≠ authorization
Canonical encoding ≠ semantic correctness
Schema admission ≠ permission or authority approval
Resource budget ≠ Canonical threshold
stream_meta ≠ source of truth
Validation-only run ≠ permanent CI
R0 PASS ≠ R1 replay equivalence
Draft PR ≠ implemented milestone
```

## Next controlled step

```text
fresh exact-head validation
→ review trusted write, migration and budget boundaries
→ explicit review-ready decision
→ explicit merge decision for P0-009
→ only after merge: P0-010 Atomic Same-Stream Redaction
```
