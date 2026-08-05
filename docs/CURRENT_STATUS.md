# 🚦 Mentaury Soul — Current Status

```text
Дата фиксации:       2026-08-05
Репозиторий:         velantrian/velantrim-mentaury-soul
Authoritative ref:   GitHub main
Current main head:   8d1fe4c4b2f274376383ab33ba5d04d787a3f244

CANON_V0.1_FROZEN
P0-001…P0-008_IMPLEMENTED_IN_MAIN
P0-008_LOCAL_VALIDATION_PASS
P0-009_OPEN_PR_15_NOT_MERGED
P0-010…P0-015_NOT_IMPLEMENTED
GITHUB_ACTIONS_NOT_PRESENT
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

## ⚖️ Правило текущей правды

```text
IMPLEMENTED
= merged into GitHub main

OPEN PR
≠ implemented in main

LOCAL PASS
≠ remote CI pass

Notion / README / Quick Reference
= derived navigation documents

Current maturity authority
= this file + verified GitHub main state
```

Любой статус в Notion, README, обсуждении или ответе ИИ считается производным и должен быть исправлен, если он расходится с фактическим `main`.

---

# ✅ Реализовано в `main`

| Milestone | Состояние | Проверенная граница |
|---|---|---|
| P0-001 Neutral Skeleton | ✅ Implemented | project/package boundary only |
| P0-002 Envelope Contracts | ✅ Implemented | construction ≠ authority approval |
| P0-003 Canonical JSON v1 | ✅ Implemented | canonical bytes ≠ valid schema or verified hash |
| P0-004 Event/Payload Storage | ✅ Implemented | persisted rows ≠ full integrity proof |
| P0-005 Structural Schema Validation | ✅ Implemented | schema validity ≠ truth or authorization |
| P0-006 Atomic Multi-Event Batch | ✅ Implemented | atomicity ≠ idempotency or concurrency control |
| P0-007 Event-Aware Idempotency | ✅ Implemented | replay receipt ≠ integrity verification |
| P0-008 Transactional Concurrency | ✅ Implemented | SQLite locking ≠ distributed consensus |

Последняя локальная валидация принятого `main` после P0-008:

```text
python3 scripts/validate.py  → PASS
pytest                       → 74 passed
compileall                   → PASS
GitHub Actions               → NOT PRESENT
```

---

# ⚙️ P0-008 — текущий принятый инженерный предел

Реализованы:

- bounded `BEGIN IMMEDIATE` retries;
- bounded `COMMIT` retries;
- WAL для file-backed SQLite;
- SQLite runtime gate;
- `StoreBusyError`;
- controlled `VersionConflictError`;
- реальные two-connection race tests.

```text
same key / same intent
→ APPLIED + ALREADY_APPLIED

same key / different intent
→ APPLIED + IDEMPOTENCY_CONFLICT

different keys / same stream version
→ APPLIED + VERSION_CONFLICT

held write lock
→ STORE_BUSY + zero partial writes
```

```text
Concurrency control ≠ R0 integrity
WAL ≠ durability proof
SQLite lock ≠ authority approval
```

---

# 🟡 P0-009 — код существует, но не принят

```text
PR:       #15
Title:    P0-009: add full R0 integrity verification
Branch:   agent/p0-r0-integrity
State:    OPEN
Merged:   NO
Main:     UNCHANGED
```

В ветке PR заявлены:

- storage schema v3 и transactional `stream_meta`;
- payload-digest recomputation;
- event-hash recomputation;
- `previous_hash` continuity;
- batch completeness and ordering checks;
- stream version and metadata checks;
- `R0IntegrityVerifier`;
- 88 локальных тестов.

Статус доказательства:

```text
CODE EXISTS IN OPEN PR
LOCAL VALIDATION CLAIMED
NOT PART OF MAIN
REMOTE CI ABSENT
REVIEW / FIX / MERGE REQUIRED
```

P0-009 не должен обозначаться как `IMPLEMENTED`, пока PR #15 не прошёл review и не был смержен.

---

# 🔴 Не реализовано

```text
P0-010 Atomic Same-Stream Redaction    → NOT IMPLEMENTED
P0-011 Adversarial Integrity Suite     → NOT IMPLEMENTED
P0-012 GitHub Actions CI               → NOT IMPLEMENTED
P0-013 R1 Deterministic Replay         → NOT IMPLEMENTED
P0-014 Minimal Belief Lifecycle        → NOT IMPLEMENTED
P0-015 Evidence Gate Report            → NOT IMPLEMENTED
```

На 2026-08-05 не существует принятых PR #16, #17 или #18 для этих milestones.

---

# 🚫 Domain runtime не авторизован

Пока отсутствуют:

- M0/M1/M2/M3 runtime;
- belief lifecycle runtime;
- Identity Continuity runtime;
- relationship and commitment runtime;
- Controlled Origin ingestion;
- Genesis Heritage runtime;
- Human Paths Atlas runtime;
- Governed Synthesis engine;
- Capability Lease resolver;
- Tool Receipt / Action Gate runtime;
- Character Engine;
- Curiosity controller;
- Titan, Crystal или Native Kernel runtime integration;
- LLM integration и autonomous goals.

Документация этих областей существует как `DOCS_ONLY`, `NON_CANONICAL` или `PRESENTATION_ONLY` research. Она не является работающим domain runtime.

---

# 🗺️ Контролируемая последовательность

```text
P0-001…P0-008 ✅ merged in main
→ review and correct P0-009 PR #15
→ merge P0-009 only after evidence is sufficient
→ P0-010 same-stream redaction
→ P0-011 adversarial integrity suite
→ P0-012 GitHub Actions CI
→ P0-013 R1 deterministic replay
→ P0-014 minimal belief lifecycle
→ P0-015 Evidence Gate report
```

# 🏁 Следующее действие

```text
P0-009 FULL R0 + STREAM METADATA VERIFICATION
Status: OPEN PR · NOT MERGED
Required: review → fixes → local validation → merge decision
```
