# 🧱 Mentaury Environment Manifest

```text
Status:             P0-001…P0-015 IMPLEMENTED IN MAIN
Updated:            2026-08-09
Authority:          docs/CURRENT_STATUS.md + verified GitHub main
Profile:            Python 3.13 + standard-library SQLite
Minimum SQLite:     3.37.0
Journal mode:       WAL for file databases
Storage schema:     v4
Dev toolchain pin:  pytest==9.1.1
Runtime deps:       NONE
Network at import:  FORBIDDEN
Database at import: FORBIDDEN
Domain runtime:     FORBIDDEN
Permanent CI:       PRESENT AND VALIDATED
Governance mode:    SOLO_MAINTAINER
```

This manifest records stable environment and implementation boundaries. It does
not embed a mutable current `main` tip or open-PR head.

---

## 1. ✅ Accepted implementation line

```text
P0-001 neutral skeleton
P0-002 typed envelopes
P0-003 canonical JSON
P0-004 immutable event and external-payload storage
P0-005 fail-closed structural validation
P0-006 atomic multi-event batch
P0-007 semantic idempotency
P0-008 controlled SQLite concurrency
P0-009 trusted commit + bounded R0 integrity
P0-010 atomic same-stream redaction
P0-011 adversarial integrity suite
P0-012 permanent read-only GitHub Actions CI
P0-013 R1 deterministic replay
P0-014 minimal evidence-referenced belief lifecycle
P0-015 deterministic Evidence Gate
```

Post-P0 accepted documentation:

```text
Post-P0 Roadmap → adopted docs-only
P1-001 Capability Lease Resolution → FROZEN_DOCS · NOT IMPLEMENTED
Research Index → navigation-only · non-canonical
Native Kernel input → preserved · not integrated
Storage/graph profiles → candidates captured · none selected
```

---

## 2. 🐍 Python environment

```text
Interpreter target: Python 3.13
Package layout:     src/mentaury
Runtime packages:   standard library only
Development tool:   pytest==9.1.1
```

Supported validation commands:

```bash
python3 scripts/validate.py
python3 scripts/check_doc_freshness.py
PYTHONPATH=src python3 -m pytest
python3 -m compileall -q src tests scripts
```

The permanent workflow runs the required job:

```text
Python 3.13 · validator · pytest · compileall
```

Green CI proves only that the checked revision passed the repository's current
structural, test and compilation gates. It does not prove semantic completeness,
production readiness or independent assurance.

---

## 3. 🗄️ SQLite profile

```text
Backend:             sqlite3 from the Python standard library
Minimum version:     3.37.0
Accepted profile:    SQLite
File journal mode:   WAL
Foreign keys:        enabled where required by store setup
Storage schema:      v4
```

Current implementation uses SQLite as the first profile. Research mentions of
PostgreSQL, Graphiti, LadybugDB or other systems are not backend selection and
do not authorize runtime wiring.

---

## 4. 🔒 Import and dependency boundaries

At module import:

```text
network access   → forbidden
database opening → forbidden
filesystem write → forbidden unless an explicit operation requests it
ambient authority → forbidden
```

Runtime dependencies remain empty. Development dependencies are locked
separately and must not be interpreted as product runtime requirements.

---

## 5. 🛡️ Integrity boundary

Implemented storage and replay capabilities include:

- canonical payload bytes;
- payload digests and event hashes;
- previous-hash allocation from the locked stream tail;
- stream version and event-count tracking;
- atomic multi-event batches;
- event-aware idempotency;
- same-stream redaction events;
- R0 bounded integrity verification;
- R1 deterministic full replay and verified snapshot-tail equivalence;
- explicit caller-supplied verification and replay budgets.

```text
hash chain ≠ truth
stream metadata ≠ independent source of truth
successful replay ≠ authorization
budget exhaustion ≠ ledger corruption
redaction ≠ deletion of event provenance
```

---

## 6. 🧠 Belief and evidence boundary

Implemented P0 contracts include:

- minimal belief lifecycle;
- evidence references;
- deterministic Evidence Gate;
- policy-bound receipts;
- fail-closed conflict handling.

They do not authorize:

```text
objective truth claims
identity runtime
Character runtime
M3 writes
external actions
```

Legacy PR #48 / issue #47 track an import-order and contradiction-path cleanup.
That work requires a current-main successor and Tier A review before merge.

---

## 7. 🔐 P1-001 environment boundary

The P1-001 Capability Lease contract is frozen as documentation only.

```text
registry implementation: NOT PRESENT
resolver implementation: NOT PRESENT
network registry lookup: FORBIDDEN BY CONTRACT
ambient wall clock: FORBIDDEN BY CONTRACT
Action Gate: NOT AUTHORIZED
Tool execution: NOT AUTHORIZED
M3 write: FORBIDDEN
```

A future implementation requires separate owner authorization in
`docs/CURRENT_STATUS.md`; this manifest does not grant it.

---

## 8. 🧑‍💻 Governance environment

The active ruleset requires PRs, current branches, the required CI check,
resolved conversations, deletion protection and force-push protection.

```text
required approvals: 0
reason: explicit solo-maintainer phase
independent human review claimed: no
Tier A review: correctness + adversarial passes on exact head
```

When a genuine independent reviewer/team exists, issue #39 defines the future
transition. Until then, technical work proceeds under documented solo review
without fabricated approval.

---

## 9. 🚫 Explicit non-environment claims

This manifest does not claim:

```text
production deployment readiness
distributed-database equivalence
cloud service availability
mobile runtime readiness
LLM integration
identity or relationship runtime
Action Gate or external tools
independent certification
```

---

## 10. 🔗 References

- `docs/CURRENT_STATUS.md`
- `docs/GOVERNANCE.md`
- `docs/governance/solo-maintainer-mode.md`
- `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`
- `.github/workflows/ci.yml`
- `requirements-dev.lock`
- `pyproject.toml`
