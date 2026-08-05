# 🧱 P0 Environment Manifest

```text
Status:             P0-009 DRAFT PR
Profile:            Python 3.13 + standard-library SQLite 3.46.1
Minimum SQLite:     3.37.0
Journal mode:       WAL for file databases
Storage schema:     v3 candidate
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
```

## P0-009 candidate boundary

PR #15 proposes:

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
Draft PR ≠ implemented milestone
```

Supported validation commands:

```bash
python3 scripts/validate.py
PYTHONPATH=src python3 -m pytest
python3 -m compileall -q src tests scripts
```

Validation-only run `31023632096` passed structural validation, full pytest and
compileall on Python 3.13 for code head
`1a4e4afd33d945875b567e2f65711d774eef7186`. The temporary workflow is not part
of PR #15 or `main` and is not P0-012. One final exact-head run is required after
recording this documentation evidence.

P0-010 owns governed atomic same-stream redaction. No identity, relationship,
Character, Curiosity or Exo-Cortex runtime is present.
