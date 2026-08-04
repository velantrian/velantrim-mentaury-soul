# 🚦 Mentaury Soul — Current Status

```text
Дата фиксации: 2026-08-05
Репозиторий: velantrian/velantrim-mentaury-soul

CANON_V0.1_FROZEN
ARCHITECTURE_RECONCILIATION_V0.1_COMPLETED
ARCHITECTURE_READINESS_REVIEW_V0.1_COMPLETED
P0-001_NEUTRAL_SKELETON_IMPLEMENTED
P0-002_ENVELOPE_CONTRACTS_IMPLEMENTED
P0-003_CANONICAL_JSON_V1_IMPLEMENTED
P0-004_IMMUTABLE_EVENT_PAYLOAD_STORAGE_IMPLEMENTED
P0-004_LOCAL_VALIDATION_PASS
P0-005_NEXT
P0_EVENT_SUBSTRATE_V3_IN_PROGRESS
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

---

## 🧭 Текущая точка

`P0-004` добавляет первый explicit SQLite persistence adapter: immutable event
rows и отдельно хранимые canonical payload bytes.

```text
P0-001 neutral skeleton             → implemented
P0-002 envelope contracts           → implemented
P0-003 canonical JSON               → implemented
P0-004 event/payload storage        → implemented
Local structural validation         → PASS
Local pytest                         → 30 passed
Compileall                           → PASS
Third-party runtime dependencies    → none
P0-005 structural schemas           → next controlled commit
Domain runtime                      → not authorized
Full Mentaury runtime               → not validated
```

---

# 🗄️ P0-004 — что добавлено

```text
src/mentaury/storage/sqlite_store.py
src/mentaury/storage/__init__.py

SQLiteEventPayloadStore
StoredPayload
StorageError
StoreNotInitializedError

explicit schema initialization
separate events / event_payloads tables
immutable event UPDATE/DELETE triggers
payload rewrite trigger
single-event + payload transaction
full EventEnvelope reconstruction
ordered stream reads
persistent reopen test

tests/test_sqlite_store.py
docs/P0_004_IMMUTABLE_EVENT_PAYLOAD_STORAGE.md
```

---

# 🔒 Storage Boundary

```text
events
→ complete immutable EventEnvelope metadata

event_payloads
→ canonical payload bytes stored outside event row
```

The event table contains no payload blob. There is no foreign key that would
prevent future payload erasure while retaining event history.

```text
Direct UPDATE events → denied by SQLite trigger
Direct DELETE events → denied by SQLite trigger
Payload rewrite      → denied by SQLite trigger
Public payload delete/redact API → absent until P0-010
```

---

# ⚙️ Single-Event Transaction

```text
canonicalize payload
BEGIN
├── insert external payload
├── insert immutable event row
COMMIT
```

A failed event insert rolls back the newly inserted payload. This is not the
real ordered multi-event batch required by P0-006.

---

# ✅ P0-004 Validation

```text
python3 scripts/validate.py
→ P0-004 immutable event/payload storage validation: PASS

PYTHONPATH=src python3 -m pytest
→ 30 passed

python3 -m compileall -q src tests scripts
→ PASS
```

GitHub Actions remain scheduled for `P0-012`; remote CI is not claimed.

---

# 🔒 Deliberate Non-Claims

```text
Stored digest field ≠ verified digest
Stored hash field ≠ verified hash
Unique stream version ≠ concurrency protocol
Single-event transaction ≠ real atomic batch
SQLite trigger ≠ tamper-proof database
External payload table ≠ governed redaction
Canonical payload bytes ≠ valid domain schema
```

P0-004 does not allocate versions, compute hashes, resolve authority, validate
schema pairs, implement redaction, or interpret domain meaning.

---

# 🗺️ Следующая последовательность

```text
P0-001 Neutral Skeleton ✅
→ P0-002 Envelope Contracts ✅
→ P0-003 MENTAURY_CANONICAL_JSON_V1 ✅
→ P0-004 Immutable events + external Payload Store ✅
→ P0-005 Structural event/schema validators
→ P0-006 Real atomic multi-event batch
→ P0-007 Event-aware idempotency
→ P0-008 Transactional concurrency
→ P0-009 Full R0 + stream metadata verification
→ P0-010 Atomic same-stream redaction
→ P0-011 Adversarial integrity tests
→ P0-012 GitHub Actions CI
→ P0-013 R1 replay
→ P0-014 Minimal Belief Lifecycle
→ P0-015 Evidence Gate report
```

---

# 🚫 Non-Claims

```text
❌ production readiness
❌ validated security
❌ validated Event Substrate
❌ verified hashes
❌ schema-validated payloads
❌ multi-event atomic append
❌ governed redaction
❌ готовая цифровая индивидуальность
❌ runtime identity continuity
❌ autonomous cognition
❌ direct integration into Titan / Crystal / Native Kernel
```

---

# 🏁 Следующий milestone

```text
P0-005 STRUCTURAL EVENT / PAYLOAD SCHEMA VALIDATORS
Status: NOT STARTED
Prerequisite: P0-004 merge and green review
```
