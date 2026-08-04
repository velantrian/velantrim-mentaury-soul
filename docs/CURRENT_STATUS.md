# 🚦 Mentaury Soul — Current Status

```text
Дата фиксации: 2026-08-04
Репозиторий: velantrian/velantrim-mentaury-soul

CANON_V0.1_FROZEN
CONTROLLED_ORIGIN_RESEARCH_V0.2_DOCS_ONLY
IDENTITY_CONTINUITY_RESEARCH_V0.1_DOCS_ONLY
CHARACTER_AND_PRESENCE_V0.1_PRESENTATION_ONLY
ARCHITECTURE_RECONCILIATION_V0.1_COMPLETED
ARCHITECTURE_READINESS_REVIEW_V0.1_COMPLETED
READY_FOR_NEUTRAL_SKELETON
P0-001_AUTHORIZED
P0_EVENT_SUBSTRATE_V3_PLANNED
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

---

## 🧭 Текущая точка

Архитектурный цикл до технического skeleton завершён на уровне research и документационных контрактов.

```text
Architecture                         → advanced and reconciled
Architecture Readiness Review        → completed
Readiness result                     → READY_FOR_NEUTRAL_SKELETON
Neutral technical skeleton           → authorized
P0-001                               → next controlled commit
P0-002…P0-015                        → sequential plan only
Identity / Relationship runtime      → not authorized
Exo-Cortex runtime                   → not authorized
Full Mentaury runtime                → not validated
```

Основное решение review:

> Архитектура достаточно определена для создания заменяемого инфраструктурного каркаса, но не для реализации личности как runtime.

---

# ✅ Что сформировано

## Нормативная база

- [Mentaury Canon v0.1](MENTAURY_CANON_V0.1.md) — frozen;
- шесть корневых инвариантов;
- Memory M0–M3;
- Identity Zones Z0–Z6;
- Change Risk Classes;
- External Research Boundary.

## Инженерная база

- [P0 Implementation Plan v0.3](MENTAURY_P0_IMPLEMENTATION_PLAN.md);
- Event Substrate v3 commit sequence;
- integrity, atomicity, idempotency, concurrency, redaction и replay requirements;
- minimal belief vertical slice;
- Evidence Gate.

## Research-база

- [Controlled Origin Research v0.2](research/GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md);
- [Identity Continuity & Relational Architecture v0.1](research/MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md);
- [Character & Presence Spec v0.1](MENTAURY_CHARACTER_AND_PRESENCE_SPEC_V0.1.md);
- [Architecture Reconciliation v0.1](research/ARCHITECTURE_RECONCILIATION_V0.1.md);
- [Architecture Readiness Review v0.1](research/ARCHITECTURE_READINESS_REVIEW_V0.1.md).

---

# 🧬 Зафиксированные границы

```text
Origin ≠ Identity Control
Testimony ≠ Identity
Pain ≠ Drive
Story ≠ Law
Interpretation ≠ Truth
Method ≠ Conclusion
Method ≠ Neutrality
Memory Tier ≠ Identity Zone
Character ≠ Evidence
Character Policy ≠ Reasoning Authority
Tool Output ≠ Belief
Capability ≠ Identity
Effectiveness ≠ Authorization
Continuity ≠ Exclusive Identity Claim
Record Merge ≠ Identity Merge
Replay Consistency ≠ Truth
```

---

# 🧱 Разрешённый следующий шаг — P0-001

P0-001 может включать только:

```text
project structure
Python package boundary
strict typing conventions
dependency lock
environment manifest
minimal offline smoke tests
local validation commands
```

P0-001 не может включать:

```text
Identity Continuity Engine
Relationship Runtime
Commitment Runtime
Governed Synthesis Engine
automatic M2 → M3
Human Paths Atlas Runtime
Genesis Heritage Engine
Character Engine
Exo-Cortex Runtime
Curiosity Controller
autonomous goals or missions
network actions
background cognition workers
```

---

# 🔒 P0 Scope Protection

P0 остаётся инфраструктурным:

```text
append-only event substrate
causal linking
replay
projection rebuilding
idempotency
recovery
schema evolution
receipts
minimal belief lifecycle
fail-closed behavior
```

Research scenarios не создают semantic event types автоматически.

---

# ⚠️ Что остаётся блокером до domain runtime

1. P0 Event Substrate не реализован и не прошёл Evidence Gate.
2. Scenario contracts не превращены в executable fixtures.
3. Capability Lease не проверен adversarial implementation tests.
4. Privacy deletion не проверена через backups, projections и forks.
5. Relationship/commitment reconciliation не реализованы.
6. M2 → M3 nomination не имеет executable governance workflow.
7. Governed Synthesis остаётся research contract.
8. Character остаётся presentation-only.

---

# 🧪 Экспериментальная история

```text
EXP-P0-v1 → 13 tests reproduced → retained as experiment
EXP-P0-v2 → 21 tests reproduced → patch source only
```

EXP-P0-v2 не переносится напрямую. P0-v3 строится последовательно по плану.

---

# 🗺️ Текущая последовательность

```text
Architecture Readiness Review ✅
→ P0-001 neutral skeleton
→ P0-002 envelopes
→ P0-003 canonical serialization
→ immutable substrate
→ validation / batch / idempotency / concurrency
→ R0 integrity
→ redaction
→ adversarial tests and CI
→ R1 replay
→ minimal belief lifecycle
→ P0 Evidence Gate
→ bounded post-P0 research prototypes
```

---

# 🚫 Non-Claims

```text
❌ production readiness
❌ validated security
❌ доказанное сознание
❌ subjective experience
❌ готовая цифровая личность
❌ готовый autonomous cognition runtime
❌ automatic M2 → M3
❌ direct integration into Titan / Crystal / Native Kernel
```

---

# 🏁 Следующий milestone

```text
P0-001 PROJECT SKELETON
Status: AUTHORIZED · NOT YET MERGED
```

После P0-001 каждый следующий commit обязан оставлять branch зелёной и сохранять все architecture guardrails.