# 🧱 P0 Environment Manifest

```text
Status:             P0-001…P0-015 IMPLEMENTED IN MAIN
Main SHA:           1d3af6f0946e596529b9d40315a83cd3573918db
Profile:            Python 3.13 + standard-library SQLite 3.46.1
Minimum SQLite:     3.37.0
Journal mode:       WAL for file databases
Storage schema:     v4
Dev toolchain pin:  pytest==9.1.1 (requirements-dev.lock; PR #40)
Runtime deps:       NONE
Network at import:  FORBIDDEN
Database at import: FORBIDDEN
Domain runtime:     FORBIDDEN
Permanent CI:       PRESENT AND VALIDATED (.github/workflows/ci.yml)
```

This manifest historically documented only the P0-009 baseline. It is now
kept in sync with `docs/CURRENT_STATUS.md`, the authoritative source for
per-milestone PR numbers, merge SHAs and validation evidence; see that file
for P0-010…P0-015 detail.

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
P0-010 atomic same-stream redaction (storage schema v4)
P0-011 adversarial integrity suite
P0-012 permanent read-only GitHub Actions CI
P0-013 R1 deterministic replay
P0-014 minimal evidence-referenced belief lifecycle
P0-015 deterministic Evidence Gate
post-P0-015 audit hardening (PR #32; not a new P0 milestone)
Post-P0 Roadmap v0.1 adopted (docs-only; PR #34; not a P1 implementation)
P1-001 Capability Lease Resolution notes (docs-only; NOT IMPLEMENTED; PR #34)
security pin pytest 9.1.1 (PR #40; post-hoc review issue #42 still open)
Native Kernel external research input preserved (docs-only; PR #43; NOT PROMOTED)
storage/graph future profile candidates captured (docs-only; NOT SELECTED)
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
head `6f8ff1663e161e554c8d4610f1692187c2129b45` for P0-009.

That temporary workflow was not part of PR #15 or `main`. Permanent CI was
merged separately in P0-012 (PR #25, `.github/workflows/ci.yml`) and now runs
the same three checks on every pull request and push to `main`.

P0-010 added governed atomic same-stream redaction. P0-014/P0-015 added a
minimal, evidence-gated belief lifecycle. PR #32 closed a post-merge
lifecycle/reducer boundary gap, hardened digest schema admission, and added
a derived-doc freshness CI gate. No identity, relationship, Character,
Curiosity or Exo-Cortex runtime is present, and none of the P0 milestones
authorize one. PostgreSQL and graph engines (Graphiti, LadybugDB, etc.) remain
captured future profile candidates only; see
`docs/research/STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md`.
