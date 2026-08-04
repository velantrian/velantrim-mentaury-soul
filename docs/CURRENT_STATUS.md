# 🚦 Mentaury Soul — Current Status

```text
Дата фиксации: 2026-08-04
Репозиторий: velantrian/velantrim-mentaury-soul

CANON_V0.1_FROZEN
ARCHITECTURE_RECONCILIATION_V0.1_COMPLETED
ARCHITECTURE_READINESS_REVIEW_V0.1_COMPLETED
READY_FOR_NEUTRAL_SKELETON
P0-001_NEUTRAL_SKELETON_IMPLEMENTED
P0-002_ENVELOPE_CONTRACTS_IMPLEMENTED
P0-002_LOCAL_VALIDATION_PASS
P0-003_NEXT
P0_EVENT_SUBSTRATE_V3_IN_PROGRESS
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

---

## 🧭 Текущая точка

`P0-002` реализует только immutable typed envelope contracts. Он не создаёт Event Store и не утверждает, что событие было сохранено, авторизовано или криптографически проверено.

```text
P0-001 neutral skeleton             → implemented
P0-002 envelope contracts           → implemented
Local structural validation         → PASS
Local pytest                         → 12 passed
Compileall                           → PASS
Editable package build/import       → PASS
Third-party runtime dependencies    → none
P0-003 canonical JSON               → next controlled commit
Domain runtime                      → not authorized
Full Mentaury runtime               → not validated
```

---

# 📨 P0-002 — что добавлено

```text
src/mentaury/contracts/primitives.py
src/mentaury/contracts/envelopes.py

typed references:
ActorRef
AuthorityRef
ProducerRef

immutable contracts:
CommandEnvelope
PendingEvent
EventEnvelope

ordered helper:
snapshot_pending_batch

tests/test_envelopes.py
docs/P0_002_ENVELOPE_CONTRACTS.md
```

Обновлены:

```text
src/mentaury/contracts/__init__.py
src/mentaury/__init__.py
scripts/validate.py
docs/ENVIRONMENT_MANIFEST.md
docs/CURRENT_STATUS.md
```

---

# 🔒 P0-002 Contract Boundary

```text
CommandEnvelope
→ submitted intent

PendingEvent
→ proposed fact before commit

EventEnvelope
→ committed-event metadata shape with external payload reference
```

Защитные различия:

```text
Envelope construction ≠ authority approval
Command ≠ Event
PendingEvent ≠ committed event
EventEnvelope object ≠ persisted immutable row
Payload digest field ≠ verified digest
Frozen payload snapshot ≠ canonical JSON
```

Payload containers defensively копируются в read-only mappings и tuples. Это защищает локальный snapshot от последующей мутации caller-owned объектов, но не заменяет P0-003 canonical serialization или P0-004 storage immutability.

---

# ✅ P0-002 Validation

```text
python3 scripts/validate.py
→ P0-002 envelope contract validation: PASS

PYTHONPATH=src python3 -m pytest
→ 12 passed

python3 -m compileall -q src tests scripts
→ PASS

editable package build/import
→ PASS
```

GitHub Actions ещё не добавлены; они запланированы на `P0-012`. Поэтому remote CI не заявляется.

---

# 🔒 Scope Protection

P0-002 не реализует:

```text
canonical JSON
conformance vectors
Event Store
SQLite persistence
payload digest computation
hash chain
schema registry
strict payload schema validation
authority resolver
command handler
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
→ P0-003 MENTAURY_CANONICAL_JSON_V1
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
P0-003 MENTAURY_CANONICAL_JSON_V1
Status: NOT STARTED
Prerequisite: P0-002 merge and green review
```
