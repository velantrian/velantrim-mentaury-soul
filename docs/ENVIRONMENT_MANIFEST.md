# 🧱 Mentaury Environment Manifest

```text
Status:             P0 + P1-001 IMPLEMENTED IN MAIN
Updated:            2026-08-09
Authority:          docs/CURRENT_STATUS.md + verified GitHub main
Profile:            Python 3.13 + standard library
Minimum SQLite:     3.37.0
P0 journal mode:    WAL for file databases
P0 storage schema:  v4
Dev toolchain pin:  pytest==9.1.1
Runtime deps:       NONE
Network at import:  FORBIDDEN
Database at import: FORBIDDEN
Filesystem mutation at import: FORBIDDEN
Domain runtime:     FORBIDDEN
Governance mode:    SOLO_MAINTAINER

P0-001…P0-015_IMPLEMENTED_IN_MAIN
P1-001…P1-001_IMPLEMENTED_IN_MAIN
```

This manifest records stable environment and implementation boundaries. It does
not embed a mutable current `main` tip or open-PR head.

---

## 1. ✅ Accepted implementation line

```text
P0-001…P0-013 integrity, storage and replay foundation
P0-014 minimal evidence-referenced belief lifecycle
P0-015 deterministic Evidence Gate
P1-001 pure Capability Lease resolver · IMPLEMENTED_BOUNDED
```

P1-001 evidence:

```text
Authorization merge:   d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
Authorization main CI: 31322210843 · success
Implementation head:   e873e43331fa7273b92f896b371707e4779b17d4
Exact-head CI:         31323051934 · success · 387 passed
Implementation merge: f21809d8f31a457bd7acfe1d766230973ba9ecf5
Implementation main CI:31323138053 · success
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

Green CI proves repository conformance for the checked revision. It does not
prove production readiness, independent assurance or external authorization.

---

## 3. 🗄️ Storage boundary

P0 uses standard-library SQLite as its accepted storage profile. P1-001 is
storage-free and makes no schema, journal, persistence or replay change.

```text
P1-001 registry persistence: NOT IMPLEMENTED
P1-001 registry service:     NOT IMPLEMENTED
network registry lookup:     FORBIDDEN
backend selection/migration: NOT AUTHORIZED
```

---

## 4. 🔒 Import and dependency boundaries

At module import:

```text
network access    → forbidden
database opening  → forbidden
filesystem write  → forbidden
ambient clock     → forbidden
ambient authority → forbidden
```

Runtime dependencies remain empty.

P1-001 package:

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
```

Its fresh-process import test blocks `open`, `socket.socket`, `sqlite3.connect`
and `time.time`; import still succeeds.

---

## 5. 🔐 P1-001 execution environment

Inputs are entirely caller supplied:

```text
RegistrySnapshot
AuthorityRef(capability_lease_id, capability_revision)
ActionIntent
canonical UTC-Z evaluated_at
ResolutionBudget
```

Output:

```text
ResolutionResult
```

The resolver performs strict admission, exact live-head lookup, canonical digest
verification, deterministic invariant/lifecycle checks and exact intent matching.
Stored registry records are recursively immutable.

`ALLOW` executes nothing and contains no reusable permission token, operations,
scope, side effects or tool credentials.

---

## 6. 🧠 Epistemic and state boundary

P1-001 does not import or mutate storage, replay, beliefs or evidence packages.
It does not append events, alter projections, change belief status, write
identity/relationship state or authorize M3 mutation.

```text
capability resolution ≠ objective truth
capability resolution ≠ action execution
capability resolution ≠ identity authority
```

---

## 7. 🧑‍💻 Governance environment

The active ruleset requires PRs, current branches, required CI, resolved
conversations, deletion protection and force-push protection.

```text
required approvals: 0
reason: explicit solo-maintainer phase
independent human review claimed: no
Tier A review: correctness + adversarial passes on exact head
```

`src/mentaury/capabilities/lease/**` is an active Tier A path in Governance and
CODEOWNERS. Issue #39 governs only the future team transition.

---

## 8. ⛔ Next milestone boundary

```text
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
```

No registry service, Action Gate, Tool Receipt, external action adapter, P1-002,
identity runtime or deployment follows automatically. Each requires a separate
contract, threat model and Owner GO.

---

## 9. 🚫 Explicit non-environment claims

This manifest does not claim:

```text
production deployment readiness
registry service availability
Action Gate or external tools
identity or relationship runtime
M3 authority
backend portability beyond validated profiles
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
