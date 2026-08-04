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
P0-005_STRUCTURAL_SCHEMA_VALIDATION_IMPLEMENTED
P0-006_ATOMIC_MULTI_EVENT_BATCH_IMPLEMENTED
P0-007_EVENT_AWARE_IDEMPOTENCY_IMPLEMENTED
P0-007_LOCAL_VALIDATION_PASS
P0-008_NEXT
P0_EVENT_SUBSTRATE_V3_IN_PROGRESS
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

## 🧭 Текущая точка

```text
P0-001 neutral skeleton             → implemented
P0-002 envelope contracts           → implemented
P0-003 canonical JSON               → implemented
P0-004 event/payload storage        → implemented
P0-005 structural schemas           → implemented
P0-006 atomic multi-event batch     → implemented
P0-007 event-aware idempotency      → implemented
Local structural validation         → PASS
Local pytest                         → 68 passed
Compileall                           → PASS
Third-party runtime dependencies    → none
P0-008 transactional concurrency    → next controlled commit
Domain runtime                      → not authorized
Full Mentaury runtime               → not validated
```

# 🔑 P0-007 — что добавлено

```text
src/mentaury/storage/idempotency.py
storage schema migration v1 → v2
immutable idempotency_records table

MENTAURY_IDEMPOTENCY_V1
IdempotentBatchRequest
IdempotentAppendResult
IdempotencyStatus
IdempotencyConflictError
SQLiteIdempotentBatchAppender
idempotency_fingerprint

tests/test_idempotency.py
docs/P0_007_EVENT_AWARE_IDEMPOTENCY.md
```

Fingerprint covers semantic command intent and the ordered pending batch. It excludes generated IDs, timestamps, batch IDs, payload refs and event hash fields.

```text
same semantic retry with regenerated technical metadata
→ ALREADY_APPLIED + original receipt

same key + changed payload/type/schema/count/order
→ IDEMPOTENCY_CONFLICT
```

```text
BEGIN
├── lookup key + fingerprint
├── append complete payload/event batch
├── store immutable idempotency record + receipt
COMMIT
```

A failed idempotency-record insert rolls back the complete new batch.

# ✅ P0-007 Validation

```text
python3 scripts/validate.py
→ P0-007 event-aware idempotency validation: PASS

PYTHONPATH=src python3 -m pytest
→ 68 passed

python3 -m compileall -q src tests scripts
→ PASS
```

GitHub Actions remain scheduled for `P0-012`; remote CI is not claimed.

# 🔒 Deliberate Non-Claims

```text
Idempotency fingerprint ≠ authorization
ALREADY_APPLIED ≠ integrity verification
Stored receipt ≠ governance receipt
SHA-256 fingerprint ≠ event hash chain
Single-writer idempotency ≠ concurrent-writer correctness
Immutable SQLite trigger ≠ tamper-proof database
```

# 🗺️ Следующая последовательность

```text
P0-001 Neutral Skeleton ✅
→ P0-002 Envelope Contracts ✅
→ P0-003 MENTAURY_CANONICAL_JSON_V1 ✅
→ P0-004 Immutable events + external Payload Store ✅
→ P0-005 Structural event/schema validators ✅
→ P0-006 Real atomic multi-event batch ✅
→ P0-007 Event-aware idempotency ✅
→ P0-008 Transactional concurrency
→ P0-009 Full R0 + stream metadata verification
→ P0-010 Atomic same-stream redaction
→ P0-011 Adversarial integrity tests
→ P0-012 GitHub Actions CI
→ P0-013 R1 replay
→ P0-014 Minimal Belief Lifecycle
→ P0-015 Evidence Gate report
```

# 🚫 Non-Claims

```text
❌ production readiness
❌ validated security
❌ validated Event Substrate
❌ controlled concurrent writers
❌ verified event hash chain / stream head
❌ governed redaction
❌ ready domain runtime
❌ autonomous cognition
```

# 🏁 Следующий milestone

```text
P0-008 TRANSACTIONAL CONCURRENCY AND BUSY HANDLING
Status: NOT STARTED
Prerequisite: P0-007 merge and green review
```
