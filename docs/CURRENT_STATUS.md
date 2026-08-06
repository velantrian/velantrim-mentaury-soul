# 🚦 Mentaury Soul — Current Status

```text
Дата фиксации:                  2026-08-06
Репозиторий:                    velantrian/velantrim-mentaury-soul
Authoritative ref:              GitHub main
Verified implementation head:  7f78dd2c7db45206f293f0278a51033474db4918

CANON_V0.1_FROZEN
P0-001…P0-010_IMPLEMENTED_IN_MAIN
P0-010_FINAL_EXACT_HEAD_VALIDATION_PASS
P0-011…P0-015_NOT_IMPLEMENTED
PERMANENT_GITHUB_ACTIONS_NOT_PRESENT
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

## ⚖️ Правило текущей правды

```text
IMPLEMENTED
= merged into GitHub main

OPEN PR
≠ implemented in main

VALIDATION-ONLY WORKFLOW
≠ permanent project CI

Notion / README / Quick Reference
= derived navigation documents

Current maturity authority
= this file + verified GitHub main state
```

---

# ✅ Реализовано в `main`

| Milestone | Состояние | Проверенная граница |
|---|---|---|
| P0-001 Neutral Skeleton | ✅ Implemented | project/package boundary only |
| P0-002 Envelope Contracts | ✅ Implemented | construction ≠ authority approval |
| P0-003 Canonical JSON v1 | ✅ Implemented | canonical bytes ≠ truth or authorization |
| P0-004 Event/Payload Storage | ✅ Implemented | persisted rows ≠ complete integrity proof |
| P0-005 Structural Schema Validation | ✅ Implemented | schema validity ≠ semantic correctness |
| P0-006 Atomic Multi-Event Batch | ✅ Implemented | atomicity ≠ idempotency or concurrency |
| P0-007 Event-Aware Idempotency | ✅ Implemented | replay receipt ≠ integrity verification |
| P0-008 Transactional Concurrency | ✅ Implemented | SQLite locking ≠ distributed consensus |
| P0-009 Trusted Commit + Full R0 | ✅ Implemented | R0 consistency ≠ epistemic truth |
| P0-010 Atomic Same-Stream Redaction | ✅ Implemented | payload removal ≠ event-provenance deletion |

---

# 🔗 P0-009 — принятый инженерный предел

Merged PR:

```text
PR:       #15
Title:    P0-009: trusted commit boundary and full R0 integrity
Merged:   YES
Main SHA: 08c0e8b5b33aeaa283de4d9ece1f65669d09afd2
```

Реализовано:

- mandatory `SchemaRegistry` admission для production writes;
- canonical payload bytes shared by validation, hashing and persistence;
- payload digest, previous hash и event hash allocated in the trusted transaction boundary;
- transactional `stream_meta` schema v3;
- full R0 verification of canonical payload bytes, schema, digest, chain, versions, batches and metadata;
- explicit caller-supplied `VerificationBudget` for R0 and populated migration;
- fail-closed populated v2 → v3 migration;
- rollback on busy and unexpected `COMMIT` failures;
- exact-one `OneOfSpec` semantics;
- controlled cyclic-payload rejection.

Финальная validation-only проверка exact PR head:

```text
PR head             → 6f8ff1663e161e554c8d4610f1692187c2129b45
Run                  → 31023788916
Python 3.13          → PASS
Locked dependencies  → PASS
Structural validator → PASS
Full pytest          → PASS
Compileall            → PASS
```

Workflow существовал только на отдельной validation-ветке и не был добавлен в
PR #15 или `main`.

```text
R0 consistency ≠ epistemic truth
Schema admission ≠ authority approval
Hash continuity ≠ authorization
Resource budget ≠ Canonical threshold
Validation-only workflow ≠ P0-012
R0 PASS ≠ R1 replay equivalence
```

---

# ✅ P0-010 — Atomic Same-Stream Redaction

Merged PR:

```text
PR:                #19
Final tested head: e141e31f60f7a9aee78642fe3fe3b44570ced733
Merge SHA:         7f78dd2c7db45206f293f0278a51033474db4918
Validation run:    31074885346
Python:            CPython 3.13.14
Full pytest:       144 passed
Review:            Copilot 9/9 files, 0 new comments
```

Реализовано:

- immutable schema-v4 `redactions` evidence;
- one-transaction payload removal, audit append, `stream_meta` update and linkage write;
- preservation of the immutable target event row and original hash chain;
- complete R0 verification of redaction row → target event → audit event → canonical audit payload;
- fail-closed handling for forged, missing, cross-stream or inconsistent evidence;
- caller-supplied `VerificationBudget` applied before linked audit-payload decoding;
- authority-scoped semantic idempotency and deterministic rollback behavior;
- focused concurrency and adversarial regression coverage.

```text
Governed redaction ≠ epistemic truth
Payload removal ≠ event-provenance deletion
SQLite deletion ≠ backup-wide erasure proof
R0 PASS ≠ R1 replay equivalence
P0-010 merged ≠ domain consent/privacy runtime
```

---

# 🔴 Не реализовано

```text
P0-011 Adversarial Integrity Suite     → NOT IMPLEMENTED
P0-012 Permanent GitHub Actions CI     → NOT IMPLEMENTED
P0-013 R1 Deterministic Replay         → NOT IMPLEMENTED
P0-014 Minimal Belief Lifecycle        → NOT IMPLEMENTED
P0-015 Evidence Gate Report            → NOT IMPLEMENTED
```

---

# 🚫 Domain runtime не авторизован

Пока отсутствуют:

- M0/M1/M2/M3 domain runtime;
- belief lifecycle runtime;
- Identity Continuity runtime;
- relationship and commitment runtime;
- Controlled Origin ingestion;
- Genesis Heritage and Human Paths Atlas runtime;
- Governed Synthesis engine;
- Capability Lease resolver;
- Tool Receipt / Action Gate runtime;
- Character Engine;
- Curiosity controller;
- Titan, Crystal или Native Kernel runtime integration;
- LLM integration и autonomous goals.

Документация этих областей существует как `DOCS_ONLY`, `NON_CANONICAL` или
`PRESENTATION_ONLY` research. Она не является работающим domain runtime.

---

# 🗺️ Контролируемая последовательность

```text
P0-001…P0-010 ✅ merged in main
→ P0-011 adversarial integrity suite
→ P0-012 permanent GitHub Actions CI
→ P0-013 R1 deterministic replay
→ P0-014 minimal belief lifecycle
→ P0-015 Evidence Gate report
```

# 🏁 Следующее действие

```text
P0-011 ADVERSARIAL INTEGRITY SUITE
Status: NOT IMPLEMENTED
Precondition: combine tampering, migration, concurrency, redaction and resource-boundary proofs into one controlled matrix
```
