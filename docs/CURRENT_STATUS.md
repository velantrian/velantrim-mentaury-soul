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
P0-005_LOCAL_VALIDATION_PASS
P0-006_NEXT
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
Local structural validation         → PASS
Local pytest                         → 43 passed
Compileall                           → PASS
Third-party runtime dependencies    → none
P0-006 atomic multi-event batch     → next controlled commit
Domain runtime                      → not authorized
Full Mentaury runtime               → not validated
```

# 🧩 P0-005 — что добавлено

```text
src/mentaury/validation/issues.py
src/mentaury/validation/specs.py
src/mentaury/validation/validator.py
src/mentaury/validation/registry.py
src/mentaury/validation/__init__.py

StringSpec · IntegerSpec · BooleanSpec · NullSpec
ArraySpec · ObjectSpec · OneOfSpec
EventSchemaDefinition · SchemaRegistry
ValidationIssue · ValidationCode · SchemaValidationError

tests/test_schema_validation.py
docs/P0_005_STRUCTURAL_SCHEMA_VALIDATION.md
```

# 🔒 Fail-Closed Boundary

```text
unknown event type → rejected
payload schema mismatch → rejected
unsupported envelope version → rejected
affects_domain_state mismatch → rejected
missing required field → rejected
forbidden field → rejected
nested type mismatch → rejected
unsupported numeric / Unicode / container → rejected
```

Object schemas are strict by default. Registry and schema definitions snapshot
caller-owned mappings.

# 🔢 Portable Value Boundary

```text
float / Decimal → unsupported numeric
integer outside ±(2^53−1) → unsupported numeric
lone surrogate → invalid Unicode
non-string object key → rejected
cyclic container → rejected
```

Externally loaded raw payloads use `validate_event_payload()` without weakening
P0-002 envelope construction guards.

# ✅ P0-005 Validation

```text
python3 scripts/validate.py
→ P0-005 structural schema validation: PASS

PYTHONPATH=src python3 -m pytest
→ 43 passed

python3 -m compileall -q src tests scripts
→ PASS
```

GitHub Actions remain scheduled for `P0-012`; remote CI is not claimed.

# 🔒 Deliberate Non-Claims

```text
Schema validity ≠ epistemic truth
Structural match ≠ semantic correctness
Registry definition ≠ Canon
Registered event ≠ authorized event
Valid payload ≠ permitted mutation
Validation result ≠ persistence
Validation result ≠ hash verification
```

P0-005 is not silently wired into P0-004 storage. Later command/batch handling
must invoke validation explicitly.

# 🗺️ Следующая последовательность

```text
P0-001 Neutral Skeleton ✅
→ P0-002 Envelope Contracts ✅
→ P0-003 MENTAURY_CANONICAL_JSON_V1 ✅
→ P0-004 Immutable events + external Payload Store ✅
→ P0-005 Structural event/schema validators ✅
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

# 🚫 Non-Claims

```text
❌ production readiness
❌ validated security
❌ validated Event Substrate
❌ verified hashes
❌ authority-validated commands
❌ semantic truth validation
❌ multi-event atomic append
❌ governed redaction
❌ готовая цифровая индивидуальность
❌ runtime identity continuity
❌ autonomous cognition
```

# 🏁 Следующий milestone

```text
P0-006 REAL ATOMIC MULTI-EVENT BATCH
Status: NOT STARTED
Prerequisite: P0-005 merge and green review
```
