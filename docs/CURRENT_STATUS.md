# 🚦 Mentaury Soul — Current Status

```text
Дата фиксации: 2026-08-05
Репозиторий: velantrian/velantrim-mentaury-soul

CANON_V0.1_FROZEN
P0-001…P0-008_IMPLEMENTED
P0-008_LOCAL_VALIDATION_PASS
P0-009_NEXT
P0_EVENT_SUBSTRATE_V3_IN_PROGRESS
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_NOT_VALIDATED
```

```text
P0-001 neutral skeleton             → implemented
P0-002 envelope contracts           → implemented
P0-003 canonical JSON               → implemented
P0-004 event/payload storage        → implemented
P0-005 structural schemas           → implemented
P0-006 atomic multi-event batch     → implemented
P0-007 event-aware idempotency      → implemented
P0-008 transactional concurrency    → implemented
Local structural validation         → PASS
Local pytest                         → 74 passed
Compileall                           → PASS
P0-009 R0 + stream metadata         → next controlled commit
```

# ⚙️ P0-008

Added bounded `BEGIN IMMEDIATE` and `COMMIT` retry handling, WAL file profile,
SQLite runtime gate, `StoreBusyError`, and controlled `VersionConflictError`.

```text
same key/same intent → APPLIED + ALREADY_APPLIED
same key/different intent → APPLIED + conflict
different keys/same version → APPLIED + VERSION_CONFLICT
held lock → STORE_BUSY + zero partial writes
```

```text
Concurrency control ≠ R0 integrity
WAL ≠ durability proof
SQLite lock ≠ authority approval
```

GitHub Actions remain scheduled for P0-012; remote CI is not claimed.

# 🗺️ Sequence

```text
P0-001…P0-008 ✅
→ P0-009 Full R0 + stream metadata verification
→ P0-010 Atomic same-stream redaction
→ P0-011 Adversarial integrity tests
→ P0-012 GitHub Actions CI
→ P0-013 R1 replay
→ P0-014 Minimal Belief Lifecycle
→ P0-015 Evidence Gate report
```

# 🏁 Next

```text
P0-009 FULL R0 + STREAM METADATA VERIFICATION
Status: NOT STARTED
```
