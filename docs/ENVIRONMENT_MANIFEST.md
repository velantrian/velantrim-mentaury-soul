# 🧱 P0 Environment Manifest

```text
Status:             P0-009 IMPLEMENTED IN MAIN
Main SHA:           08c0e8b5b33aeaa283de4d9ece1f65669d09afd2
Profile:            Python 3.13 + standard-library SQLite 3.46.1
Minimum SQLite:     3.37.0
Journal mode:       WAL for file databases
Storage schema:     v3
Runtime deps:       NONE
Network at import:  FORBIDDEN
Database at import: FORBIDDEN
Domain runtime:     FORBIDDEN
Permanent CI:       NOT PRESENT
```

## Accepted baseline in `main`

```text
P0-001 neutral skeleton
P0-002 typed envelopes
P0-003 canonical JSON
P0-004 immutable event/external payload storage
P0-005 fail-closed structural validation
P0-006 atomic multi-event batch
P0-007 semantic idempotency
P0-008 controlled SQLite concurrency
P0-009 trusted commit boundary + bounded R0 integrity
```

## P0-009 implementation boundary

Merged PR #15 provides:

- storage schema v3 with `stream_meta(current_version, last_event_hash, event_count)`;
- mandatory `SchemaRegistry` admission for production writes;
- canonical payload bytes shared by validation, hashing, and persistence;
- payload digest and event hash allocation inside the transactional write boundary;
- previous-hash allocation from the locked stream tail rather than caller input;
- single-event batch invariants for `append_one`;
- sequential sealing of atomic and idempotent batches under one write lock;
- fail-closed verification before populated v2 → v3 migration;
- explicit caller-supplied `VerificationBudget` for populated migration and R0;
- event-count, per-payload and cumulative payload byte limits;
- R0 verification of canonical payload bytes, schema, digest, chain, batches, versions, budgets and stream metadata.

```text
Caller hash fields ≠ committed hash fields
Post-write verification ≠ trusted commit validation
No supplied budget ≠ permission to scan without limits
Test/deployment budget ≠ Canon
Budget exhaustion ≠ ledger corruption
R0 consistency ≠ truth
Hash chain ≠ authority
stream_meta ≠ source of truth
Implemented P0-009 ≠ domain runtime
```

Supported validation commands:

```bash
python3 scripts/validate.py
PYTHONPATH=src python3 -m pytest
python3 -m compileall -q src tests scripts
```

Final validation-only run `31023788916` passed Python setup, locked dependency
installation, structural validation, full pytest and compileall against exact PR
head `6f8ff1663e161e554c8d4610f1692187c2129b45`.

The temporary workflow was not part of PR #15 or `main` and is not P0-012.

P0-010 owns governed atomic same-stream redaction. No identity, relationship,
Character, Curiosity or Exo-Cortex runtime is present.
