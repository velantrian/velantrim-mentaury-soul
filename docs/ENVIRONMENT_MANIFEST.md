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

Post-P0 status:

```text
P1-001 contract         → FROZEN_DOCS
P1-001 owner GO         → AUTHORIZED_BOUNDED
P1-001 implementation   → NOT_STARTED
P1-001 completion       → NOT_CLAIMED
Action Gate / tools / M3 / domain runtime → NOT AUTHORIZED
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

Required workflow job:

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

Current implementation uses SQLite as the first P0 profile. P1-001 pure resolver
implementation is explicitly storage-free and does not select, modify or add a
backend.

---

## 4. 🔒 Import and dependency boundaries

At module import:

```text
network access    → forbidden
database opening  → forbidden
filesystem write  → forbidden
ambient authority → forbidden
```

Runtime dependencies remain empty. Development dependencies are locked
separately and are not product runtime requirements.

The future authorized P1-001 package must preserve the same import boundary:

```text
src/mentaury/capabilities/lease/**
→ standard library only
→ no network
→ no database
→ no filesystem mutation
→ no clock or environment read
```

---

## 5. 🛡️ Integrity boundary

Implemented storage and replay capabilities include canonical payload bytes,
payload digests and event hashes, atomic batches, semantic idempotency, bounded
R0 verification, same-stream redaction and deterministic R1 replay.

```text
hash chain ≠ truth
successful replay ≠ authorization
budget exhaustion ≠ ledger corruption
redaction ≠ deletion of event provenance
```

P1-001 must not change storage schema, historical hashes, P0 envelope contracts
or replay behavior.

---

## 6. 🧠 Belief and evidence boundary

Implemented P0 contracts include a minimal belief lifecycle and deterministic
Evidence Gate. They do not authorize objective truth, identity runtime, M3
writes or external actions.

P1-001 must remain independent from belief mutation and Evidence Gate status
changes. Capability resolution classifies an explicit intent against an
explicit lease record; it does not alter epistemic state.

---

## 7. 🔐 P1-001 authorized environment

Authorization authority:

- `docs/CURRENT_STATUS.md`;
- `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`.

Authorized implementation paths:

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

Required execution environment:

```text
caller-supplied RegistrySnapshot
caller-supplied AuthorityRef
caller-supplied ActionIntent
caller-supplied evaluated_at
caller-supplied ResolutionBudget
pure deterministic ResolutionResult
```

Forbidden environment dependencies:

```text
network registry lookup
system clock
process environment authority
filesystem registry
SQLite registry
external service
background worker
Action Gate
Tool Receipt
execution adapter
```

`ALLOW` executes nothing and carries no reusable permission material.

---

## 8. 🧑‍💻 Governance environment

The active ruleset requires PRs, current branches, required CI, resolved
conversations, deletion protection and force-push protection.

```text
required approvals: 0
reason: explicit solo-maintainer phase
independent human review claimed: no
Tier A review: correctness + adversarial passes on exact head
```

The created `src/mentaury/**/lease/**` path is a reserved Tier A path and must be
made active in governance/CODEOWNERS when implementation files are added.

Issue #39 defines the future transition when a genuine independent reviewer or
team exists. Until then, technical work proceeds under documented solo review.

---

## 9. 🚫 Explicit non-environment claims

This manifest does not claim:

```text
P1-001 implementation completion
production deployment readiness
registry service availability
distributed-database equivalence
cloud or mobile runtime readiness
LLM integration
identity or relationship runtime
Action Gate or external tools
independent certification
```

---

## 10. 🔗 References

- `docs/CURRENT_STATUS.md`
- `docs/GOVERNANCE.md`
- `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`
- `docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`
- `docs/research/POST_P0_ROADMAP_V0.1.md`
- `.github/workflows/ci.yml`
- `requirements-dev.lock`
- `pyproject.toml`
