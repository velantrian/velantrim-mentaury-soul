# 🚦 Mentaury Soul — Current Status

```text
Дата фиксации: 2026-08-05
Репозиторий: velantrian/velantrim-mentaury-soul

CANON_V0.1_FROZEN
ARCHITECTURE_RECONCILIATION_V0.1_COMPLETED
ARCHITECTURE_READINESS_REVIEW_V0.1_COMPLETED
READY_FOR_NEUTRAL_SKELETON
P0-001_NEUTRAL_SKELETON_IMPLEMENTED
P0-002_ENVELOPE_CONTRACTS_IMPLEMENTED
P0-003_CANONICAL_JSON_V1_IMPLEMENTED
P0-003_LOCAL_VALIDATION_PASS
P0-004_NEXT
P0_EVENT_SUBSTRATE_V3_IN_PROGRESS
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

---

## 🧭 Текущая точка

`P0-003` реализует только однозначную сериализацию portable value trees и
P0-002 envelope projections. Он не создаёт Event Store и не вычисляет hash.

```text
P0-001 neutral skeleton             → implemented
P0-002 envelope contracts           → implemented
P0-003 canonical JSON               → implemented
Local structural validation         → PASS
Local pytest                         → 20 passed
Compileall                           → PASS
Third-party runtime dependencies    → none
P0-004 event + payload storage      → next controlled commit
Domain runtime                      → not authorized
Full Mentaury runtime               → not validated
```

---

# 🔤 P0-003 — что добавлено

```text
src/mentaury/contracts/canonical_json.py

typed deterministic helpers:
canonical_json_text
canonical_json_bytes
canonical_timestamp
canonical_decimal_string

P0 envelope projections:
command_envelope_value
pending_event_value
pending_batch_value
event_envelope_value
event_hash_input_value

byte helpers:
canonical_command_bytes
canonical_pending_batch_bytes
canonical_event_bytes
canonical_event_hash_input_bytes

tests/test_canonical_json.py
tests/fixtures/canonical_json_v1_vectors.json
docs/P0_003_CANONICAL_JSON.md
```

---

# 🔒 Canonical Profile Boundary

```text
UTF-8
sorted object keys
no insignificant whitespace
exact Unicode scalar sequence
lone surrogates forbidden
float forbidden
safe integers only
explicit decimal strings
UTC timestamps
millisecond maximum precision
cycles forbidden
```

Event hash input:

```text
previous_hash → included
event_hash    → excluded
```

Защитные различия:

```text
Canonical bytes ≠ valid schema
Canonical bytes ≠ verified hash
Canonical bytes ≠ persisted immutable row
Canonical bytes ≠ authorized fact
Canonical bytes ≠ truth
```

---

# ✅ P0-003 Validation

```text
python3 scripts/validate.py
→ P0-003 canonical JSON validation: PASS

PYTHONPATH=src python3 -m pytest
→ 20 passed

python3 -m compileall -q src tests scripts
→ PASS
```

GitHub Actions ещё не добавлены; они запланированы на `P0-012`. Поэтому remote
CI не заявляется.

---

# 🔒 Scope Protection

P0-003 не реализует:

```text
Event Store
SQLite persistence
payload blob storage
schema registry
strict payload schema validation
hash computation / verification
atomic append
idempotency
concurrency
R0 / R1
redaction
Identity Continuity Engine
Relationship / Commitment Runtime
Governed Synthesis Engine
automatic M2 → M3
Human Paths Atlas Runtime
Character Engine
Exo-Cortex Runtime
Curiosity Controller
background cognition
network actions
```

---

# 🗺️ Следующая последовательность

```text
P0-001 Neutral Skeleton ✅
→ P0-002 Envelope Contracts ✅
→ P0-003 MENTAURY_CANONICAL_JSON_V1 ✅
→ P0-004 Immutable events + external Payload Store
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
❌ persisted immutable history
❌ verified authority
❌ verified event hashes
❌ готовая цифровая индивидуальность
❌ runtime identity continuity
❌ autonomous cognition
❌ direct integration into Titan / Crystal / Native Kernel
```

---

# 🏁 Следующий milestone

```text
P0-004 IMMUTABLE EVENTS + EXTERNAL PAYLOAD STORE
Status: NOT STARTED
Prerequisite: P0-003 merge and green review
```
