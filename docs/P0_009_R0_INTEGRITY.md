# 🔗 P0-009 — Trusted Commit Boundary + Full R0 Verification

```text
Status:             DRAFT · OPEN PR #15 · NOT MERGED
Storage schema:     v3 candidate
Integrity profile:  trusted write allocation + R0 diagnostic verification
Failure mode:       fail closed / first actionable failure
Payload redaction:  NOT IMPLEMENTED
Replay:             NOT IMPLEMENTED
Domain truth:       NOT CLAIMED
Remote CI:          NOT PRESENT
```

## Purpose

P0-009 must prove two separate properties:

```text
WRITE PATH
→ only structurally admitted, canonically encoded, transactionally sealed events commit

R0 VERIFIER
→ persisted ledger, payload material, hash chain, batches and stream metadata remain consistent
```

Post-write diagnosis is not a substitute for a trusted commit boundary.

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

## 3. Fail-closed v2 → v3 migration

An empty v2 database can be upgraded without a registry. A populated v2 ledger
requires the appropriate `SchemaRegistry` and is verified under a write lock
before `stream_meta` is created or backfilled.

Migration verifies per stream:

1. contiguous versions;
2. complete ordered batches;
3. payload presence and UTF-8 JSON decoding;
4. exact canonical payload bytes;
5. registered event/schema identity;
6. structural payload validity;
7. payload digest recomputation;
8. previous-hash continuity;
9. event-hash recomputation.

Any failure rolls back the migration:

```text
corrupted v2 history
→ no stream_meta table accepted
→ schema version remains v2
→ explicit repair/review required
```

---

## 4. R0 verification

R0 independently verifies:

```text
1. reconstruct immutable envelope
2. verify stream_version sequence
3. verify batch completeness and order
4. verify registered event/schema pair
5. load and decode external payload
6. verify payload bytes are canonical
7. validate payload structure
8. recompute payload_digest
9. verify previous_hash continuity
10. recompute event_hash
11. compare stream_meta tail version/hash/count
12. return first actionable failure
```

Stable diagnostic codes include:

- stream version gaps;
- incomplete or out-of-order batches;
- schema defects;
- missing, undecodable, or non-canonical payloads;
- payload digest mismatch;
- previous-hash mismatch;
- event-hash mismatch;
- stream metadata version/hash/count mismatch.

---

## 5. Adversarial evidence required

The P0-009 test set must cover:

- caller-supplied fake hash fields are not persisted;
- schema rejection leaves payload, event, idempotency record, and `stream_meta` unchanged;
- incoherent single-event batch is rejected with zero writes;
- atomic/idempotent failures roll back all rows and metadata;
- stored non-canonical payload bytes are detected;
- corrupted populated v2 migration fails closed;
- valid populated v2 migration verifies history before backfill;
- populated migration without a registry is rejected.

---

## Validation status

```text
Structural validator → NOT YET RE-RUN AFTER TRUSTED-WRITE REFACTOR
pytest               → NOT YET RE-RUN AFTER TRUSTED-WRITE REFACTOR
compileall            → NOT YET RE-RUN AFTER TRUSTED-WRITE REFACTOR
GitHub Actions         → NOT PRESENT
```

No PASS is claimed until fresh execution evidence is produced against the
current PR head.

---

## Non-claims

```text
R0 consistency ≠ epistemic truth
Hash continuity ≠ authorization
Canonical encoding ≠ semantic correctness
Schema admission ≠ permission or authority approval
stream_meta ≠ source of truth
Local pass ≠ remote CI pass
R0 PASS ≠ R1 replay equivalence
Draft PR ≠ implemented milestone
```

## Next controlled step

```text
fresh validation
→ review of trusted write/migration boundaries
→ explicit merge decision for P0-009
→ only after merge: P0-010 Atomic Same-Stream Redaction
```
