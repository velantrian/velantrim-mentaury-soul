# 🧱 P0 Environment Manifest

```text
Status:             P0-007
Profile:            Python 3.13 + standard-library SQLite 3.46.1
Storage schema:     v2
Runtime deps:       NONE
Network at import:  FORBIDDEN
Database at import: FORBIDDEN
Domain runtime:     FORBIDDEN
```

## Implemented boundary

```text
P0-001 → neutral package skeleton
P0-002 → immutable typed envelope contracts
P0-003 → MENTAURY_CANONICAL_JSON_V1
P0-004 → immutable SQLite event rows + external payload bytes
P0-005 → fail-closed structural event/payload validation
P0-006 → real ordered atomic multi-event batch append
P0-007 → event-aware idempotency fingerprint + result replay
```

P0-007 computes `MENTAURY_IDEMPOTENCY_V1` over semantic command intent and the ordered pending batch. Schema v2 adds immutable idempotency records and migrates explicitly from v1.

```text
idempotency record + payloads + event rows
→ one transaction
```

```text
Fingerprint ≠ authorization
Fingerprint ≠ event hash
ALREADY_APPLIED ≠ R0 verification
Single writer ≠ concurrency proof
```

The package has no third-party runtime dependencies. SQLite is accessed through Python's standard library.

## Supported local commands

```bash
python3 scripts/validate.py
PYTHONPATH=src python3 -m pytest
python3 -m compileall -q src tests scripts
```

## Deferred milestones

- P0-008: transactional concurrency and controlled busy handling.
- P0-009: full R0 and stream metadata verification.
- P0-010: governed atomic same-stream redaction.
- P0-011: adversarial integrity suite.
- P0-012: GitHub Actions CI.

## Explicit exclusions

No concurrency controller, authority resolver, semantic belief validator, event hash-chain verifier, stream-head verifier, redaction workflow, identity engine, relationship runtime, Character Engine, Curiosity Controller, Exo-Cortex runtime, autonomous loop, background worker, network connector, persistent self-state, or direct M3 interface.
