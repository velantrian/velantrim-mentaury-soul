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

`events` rows are never `UPDATE`d or `DELETE`d by redaction. Only the detached
`event_payloads` row for the target event is removed, and only inside the same
transaction that appends the audit event and immutable redaction linkage.

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
at most once. `idempotency_key` is separately unique: a semantic retry of the
same request replays the original result; a different key against an already
redacted target is rejected. The table is insert-only and immutable under SQL
`UPDATE`/`DELETE` triggers.

An empty v3 database upgrades to v4 by creating this table; no registry or
verification budget is required because the migration creates no evidence.

### Authority-scoped idempotency

The redaction fingerprint identifies:

- target event;
- target stream;
- reason;
- `AuthorityRef` capability lease and revision.

`issuer` is deliberately excluded. A retry may be reissued by a different
operational actor under the same authority without becoming a different
redaction intent. The original audit event and its original initiator remain
immutable and are returned for the replay. Changing the authority reference
changes the fingerprint and produces an idempotency conflict.

This rule is pinned by regression coverage; it is not an implicit side effect
of omitted fields.

---

## 2. Redaction transaction

```text
BEGIN IMMEDIATE
├── replay by idempotency_key           → ALREADY_REDACTED
├── reject key reuse for different target/reason/authority
├── reject target already redacted under another key
├── load target event; reject if absent
├── enforce target event stream
├── check expected stream version       (before mutation)
├── validate audit identity and payload (before mutation)
├── reject unexplained missing payload  (before mutation)
├── delete target payload material
├── seal and insert REDACTION_RECORDED audit event + payload
├── update stream_meta
├── insert immutable redaction evidence
COMMIT
```

Everything after `BEGIN IMMEDIATE` is one transaction. Audit insertion,
`stream_meta` update, evidence insertion, or commit failure rolls back the
target payload deletion. A half-applied redaction is never committed.

`SQLiteRedactionExecutor` builds the audit payload from the target event ID,
target stream ID, target payload reference, reason, and authority reference;
verification never depends on parsing free-form log text.

---

## 3. R0 redaction evidence linkage

A `redactions` row alone is not sufficient proof of governed absence. R0 now
verifies the complete immutable relation:

```text
redaction row
├── target event exists in declared stream
├── target payload_ref equals immutable event payload_ref
├── target payload material is absent
├── linked audit event exists
├── audit event type = REDACTION_RECORDED
├── audit payload schema = redaction-recorded/v1
├── audit event is in the same stream and follows the target
├── audit envelope authority matches the redaction row
├── audit payload exists, decodes and is canonical
├── audit payload target ID / stream / payload ref match the row
├── audit payload reason and authority match the row
├── registry validates audit envelope and payload
└── audit payload digest matches the immutable audit event
```

Any absent or inconsistent link fails closed with a specific integrity code.
A forged redaction row plus direct payload deletion is therefore classified as
corruption, not governed redaction.

For the target event itself, `previous_hash` and `event_hash` remain
recomputable because they derive from the immutable event row. Payload-byte
checks are skipped only after the complete audit linkage above succeeds.

---

## 4. Adversarial evidence

`tests/test_redaction.py` covers transaction, idempotency, rollback, reopen,
payload reappearance, migration, and concurrency behavior.

`tests/test_redaction_evidence_linkage.py` additionally covers:

- forged redaction row without an audit event;
- redaction row naming a missing target event;
- wrong audit event type;
- wrong audit payload schema;
- audit event in another stream;
- missing audit payload;
- mismatched target event ID, stream ID, or payload reference;
- mismatched reason;
- mismatched authority in either row or payload;
- authority-scoped idempotency and issuer-independent retries.

---

## Non-claims

```text
Governed redaction ≠ erased event provenance
Redaction evidence ≠ epistemic justification for the reason
Authority reference ≠ verified permission
Payload deletion ≠ backup-wide deletion proof
R0 PASS after redaction ≠ R1 replay equivalence
Redaction primitive ≠ domain consent/privacy runtime
```

## Next controlled step

```text
P0-011 Adversarial Integrity Suite
→ broaden tampering, migration, and concurrency coverage
→ exercise the complete P0 substrate under one permanent matrix
```
