# 🚦 Mentaury Soul — Current Status

```text
Дата фиксации: 2026-08-05
Репозиторий: velantrian/velantrim-mentaury-soul

CANON_V0.1_FROZEN
P0-001…P0-009_IMPLEMENTED
P0-009_LOCAL_VALIDATION_PASS
P0-010_NEXT
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
P0-009 full R0 integrity            → implemented
Local structural validation         → PASS
Local pytest                         → 88 passed
Compileall                           → PASS
P0-010 same-stream redaction        → next controlled commit
```

# 🔗 P0-009

Storage schema v3 adds transactional `stream_meta`. R0 independently verifies:

```text
contiguous stream versions
complete ordered batches
event/schema + payload structure
payload digest recomputation
previous_hash continuity
event_hash recomputation
stream_meta version/hash/count
```

Adversarial tests mutate payloads, event fields, batch order and metadata after
bypassing normal SQLite guards; R0 reports the first actionable failure.

```text
R0 consistency ≠ epistemic truth
Hash continuity ≠ authorization
R0 PASS ≠ deterministic replay proof
```

GitHub Actions remain scheduled for P0-012; remote CI is not claimed.

# 🗺️ Sequence

```text
P0-001…P0-009 ✅
→ P0-010 Atomic same-stream redaction
→ P0-011 Adversarial integrity tests
→ P0-012 GitHub Actions CI
→ P0-013 R1 replay
→ P0-014 Minimal Belief Lifecycle
→ P0-015 Evidence Gate report
```

# 🏁 Next

```text
P0-010 ATOMIC SAME-STREAM REDACTION
Status: NOT STARTED
```
