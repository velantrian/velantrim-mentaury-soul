# 🗑️ P0-010 — Atomic Same-Stream Redaction

```text
Status:             CODE + TESTS ON BRANCH · NOT YET MERGED
Storage schema:      v4
Redaction profile:   governed same-stream payload removal
Failure mode:        fail closed / whole-transaction rollback
R1 replay:           NOT IMPLEMENTED · P0-013
Permanent CI:        NOT PRESENT · P0-012
Domain truth:        NOT CLAIMED
```

## Purpose

P0-010 lets one governed actor remove external payload material for one
already-committed event without rewriting or deleting history:

```text
IMMUTABLE EVENT ROW
→ stays forever, byte-for-byte, hash still verifiable

EXTERNAL PAYLOAD MATERIAL
→ may be removed, once, under authority and evidence

SAME-STREAM AUDIT EVENT
→ records why, by whom, and which payload was removed
```

`events` rows are never `UPDATE`d or `DELETE`d by redaction — the same
immutability triggers from P0-004/P0-009 still forbid that at the SQL layer.
Only the detached `event_payloads` row for the target event is removed, and
only inside the same transaction that appends the audit evidence.

---

## 1. Schema v4: the `redactions` table

```text
redactions(
  target_event_id     PRIMARY KEY,
  idempotency_key      UNIQUE,
  fingerprint,
  target_stream_id,
  target_payload_ref,
  audit_event_id,
  reason,
  capability_lease_id,
  capability_revision,
  redacted_at
)
```

`target_event_id` is the primary key: a given event can be governed-redacted
at most once, ever. `idempotency_key` is separately unique: a semantic retry
of the *same* request replays the same outcome; a different key against an
already-redacted target is rejected, not silently accepted. The table is
insert-only — `UPDATE`/`DELETE` triggers raise `ABORT`, mirroring
`idempotency_records`.

An empty v3 database upgrades to v4 by creating this table; no registry or
budget is required, because the migration adds no data to verify.

---

## 2. Redaction transaction

```text
BEGIN IMMEDIATE
├── replay by idempotency_key           → ALREADY_REDACTED (early return)
├── reject if idempotency_key reused for a different target/reason/authority
├── reject if target already redacted under a different key
├── load target event; reject if absent
├── reject if target event's stream_id != requested target_stream
├── check expected_stream_version for the audit append   (before any mutation)
├── validate audit event/schema identity and payload      (before any mutation)
├── reject if target payload material is already absent  (before any mutation)
├── delete target payload row
├── seal and insert REDACTION_RECORDED audit event + its own payload
├── update stream_meta
├── insert redactions evidence row
COMMIT
```

Version and schema validation run before the payload `DELETE`, so a stale
caller-observed tail or an invalid audit payload leaves the target payload
untouched. Everything after `BEGIN IMMEDIATE` is one transaction: any later
failure — including the audit event insert or the evidence-row insert —
rolls back the payload deletion too. A redaction is never observed
half-applied.

`REDACTION_RECORDED` / `redaction-recorded/v1` are ordinary event-type and
payload-schema identifiers: callers must register them in their
`SchemaRegistry` like any other event, and choose the structural shape
of the payload their own registry accepts. `SQLiteRedactionExecutor` always
builds that payload from `redaction_payload_value(...)` — target event id,
target stream id, target payload ref, reason, and authority reference — so
verification of the audit content does not depend on parsing free-form text.

---

## 3. R0 becomes redaction-aware

R0 must distinguish a governed redaction from missing-payload corruption. For
each event in a stream, R0 now checks the `redactions` table first:

```text
event_id in redactions for this stream
├── stored target_payload_ref must equal event.payload_ref
│     otherwise → REDACTION_PAYLOAD_REF_MISMATCH
├── payload material must be ABSENT
│     if present  → REDACTED_PAYLOAD_STILL_PRESENT   (reappearance is tamper evidence)
├── previous_hash and event_hash are still recomputed and compared
│     (unaffected: both are derived from the immutable row, not payload bytes)
└── payload-dependent checks (digest recompute, decode, canonical bytes,
    structural payload validation) are skipped — there is no payload to check

event_id not in redactions
└── full existing P0-009 checks apply unchanged, including PAYLOAD_MISSING
    as a corruption signal
```

Because `event_hash` is computed from the immutable row's own fields
(including the `payload_digest` value allocated at the original commit, not
recomputed from live bytes), a redacted event's hash remains verifiable
forever — redaction removes material, not evidence.

---

## 4. Adversarial evidence

`tests/test_redaction.py` covers:

- cross-stream redaction is rejected;
- redaction against a missing target event is rejected;
- a stale `expected_stream_version` leaves the target payload untouched;
- a repeated request under the same idempotency key replays `ALREADY_REDACTED`;
- a conflicting request under the same key is rejected before any new write;
- a duplicate redaction attempt under a different key against an
  already-redacted target is rejected;
- failure at the audit-event insert rolls back the payload deletion;
- failure at the evidence-row insert rolls back the payload deletion, the
  audit event, and the `stream_meta` update together;
- target payload already absent (outside the redaction path) is rejected
  defensively instead of silently treated as already-redacted;
- `redactions` rows are immutable (`UPDATE`/`DELETE` both raise);
- R0 passes both before and after a governed redaction;
- R0 detects a reappeared payload for a redacted event;
- R0 detects a tampered `target_payload_ref` in the evidence row;
- redaction state and R0 both survive an explicit store close/reopen;
- two concurrent redaction attempts against the same target (different
  idempotency keys, two SQLite connections) produce exactly one `REDACTED`
  winner and one controlled `TargetAlreadyRedactedError`.

---

## Non-claims

```text
Governed redaction ≠ erases event provenance (the immutable row and its hash remain)
Redaction evidence ≠ epistemic justification for the reason given
Authority reference ≠ verified permission (still a reference, as in P0-002)
R0 PASS after redaction ≠ R1 replay equivalence
Redaction implemented ≠ domain-level consent or privacy policy
```

## Next controlled step

```text
P0-011 Adversarial Integrity Suite
→ broaden coverage across tampering, migration, and concurrency layers
→ exercise redaction alongside the rest of the P0 substrate under one matrix
```
