# ⭐️🌀 Velantrim Mentaury Soul 🧬🧊

> **Substrate-neutral research architecture for persistent digital individuality,
> memory, identity continuity, character and governed self-development.**

```text
Status snapshot:                  2026-08-09
Engineering authority:            docs/CURRENT_STATUS.md + verified GitHub main
Governance authority:             docs/GOVERNANCE.md + live GitHub ruleset
Operating mode:                   SOLO_MAINTAINER
Independent human review claimed: NO

CANON_V0.1_FROZEN
P0-001…P0-015_IMPLEMENTED_IN_MAIN
PERMANENT_GITHUB_ACTIONS_PRESENT_AND_VALIDATED

P1_001_CAPABILITY_LEASE_RESOLUTION_DOCS_ONLY_NOT_IMPLEMENTED
P1_001_CAPABILITY_LEASE_RESOLUTION_FROZEN_DOCS
CAPABILITY_LEASE_RESOLVER_NOT_AUTHORIZED

DOMAIN_RUNTIME_NOT_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
RUNTIME_NOT_VALIDATED
```

Mentaury does **not** claim proven consciousness, subjective experience,
objective truth authority or a finished digital personality. Implemented P0
milestones are an integrity and epistemic foundation, not a production runtime.

---

## 🚦 Source of truth

```text
IMPLEMENTED
= merged into GitHub main and retained by validation

FROZEN_DOCS
= accepted contract documentation
≠ runtime implementation

OPEN PR
≠ implemented

README / Quick Reference / Notion
= derived navigation surfaces
```

- [Current Status](docs/CURRENT_STATUS.md)
- [Governance](docs/GOVERNANCE.md)
- [Solo-maintainer mode](docs/governance/solo-maintainer-mode.md)
- [Tier A review checklist](docs/governance/solo-maintainer-review-checklist.md)
- [Environment Manifest](docs/ENVIRONMENT_MANIFEST.md)
- [Quick Reference](docs/MENTAURY_QUICK_REFERENCE.md)

---

## 🧬 What Mentaury investigates

Mentaury explores whether a long-lived computational individuality can preserve
coherent continuity through:

- 🧬 origin and provenance;
- 📜 append-only history;
- 🧠 memory and beliefs;
- 🔎 evidence and epistemic revision;
- 🪞 a governed Self–World model;
- 🤝 relationships and commitments;
- 🎭 character as presentation rather than truth authority;
- 🌱 explainable, reversible development.

The project rejects two simplistic extremes:

```text
Stateless tool
→ useful, but no durable explainable continuity

Digital copy of the creator
→ inherits identity claims, errors and projections without separation
```

The research target is a third model:

> **A governed evolving digital individuality with provenance, bounded authority
> and explainable change, without pretending to be a copy of its creator.**

---

## 🏛️ Architectural map

```text
MENTAURY SOUL
│
├── 🧬 Canon and constitutional invariants
│   ├── substrate neutrality
│   ├── provenance and replay
│   ├── bounded authority
│   └── explicit non-claims
│
├── 🛡️ P0 integrity and epistemic foundation — implemented
│   ├── typed envelopes and canonical JSON
│   ├── immutable event/payload storage
│   ├── atomicity, idempotency and concurrency
│   ├── trusted commit, R0 and redaction
│   ├── adversarial integrity suite and permanent CI
│   ├── deterministic R1 replay
│   ├── minimal belief lifecycle
│   └── deterministic Evidence Gate
│
├── 🔐 P1-001 Capability Lease Resolution — docs frozen
│   ├── explicit registry snapshot
│   ├── exact live-head lookup
│   ├── fail-closed admission and lifecycle
│   ├── exact purpose / operation / typed scope
│   └── no runtime implementation authorization
│
├── 🔬 Research tracks — docs-only
│   ├── identity continuity and relationships
│   ├── Genesis Heritage and Human Atlas
│   ├── contextual cognition
│   ├── character and presence
│   ├── Non-Projection research
│   ├── storage / graph candidates
│   └── biological / cybernetic candidates
│
└── 🚫 Deferred runtime
    ├── identity / character engines
    ├── Action Gate and tools
    ├── M3 writes
    ├── domain runtime
    └── production deployment
```

---

## ✅ Implemented P0 line

| Milestone | Capability | Boundary |
|---|---|---|
| P0-001 | Neutral skeleton | package boundary only |
| P0-002 | Envelope contracts | construction is not authorization |
| P0-003 | Canonical JSON v1 | canonical bytes are not truth |
| P0-004 | Event/payload storage | persistence is not total integrity proof |
| P0-005 | Structural validation | schema validity is not semantic correctness |
| P0-006 | Atomic batch | atomicity is not consensus |
| P0-007 | Event-aware idempotency | receipt is not integrity verification |
| P0-008 | Transactional concurrency | SQLite locking is not distributed consensus |
| P0-009 | Trusted commit + R0 | consistency is not truth |
| P0-010 | Same-stream redaction | payload removal preserves provenance |
| P0-011 | Adversarial suite | tested attacks are not exhaustive proof |
| P0-012 | Permanent CI | green CI is not production readiness |
| P0-013 | Deterministic replay | replay equivalence is not truth |
| P0-014 | Belief lifecycle | belief status is not objective truth |
| P0-015 | Evidence Gate | gate receipt is not external verification |

Implementation profile:

```text
Python 3.13
standard-library SQLite
runtime dependencies: none
network/database access at import: forbidden
```

---

## 🔐 P1-001 Capability Lease Resolution

The accepted contract is in:

- [Capability Lease Resolution Notes](docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [Post-P0 Roadmap](docs/research/POST_P0_ROADMAP_V0.1.md)
- [Research Index](docs/research/RESEARCH_INDEX.md)

```text
Status: FROZEN_DOCS · DOCS_ONLY · NOT_IMPLEMENTED
```

The contract specifies:

- caller-supplied immutable `RegistrySnapshot`;
- separate registry and lease-record admission;
- distinct `REGISTRY_UNAVAILABLE`, `REGISTRY_CONTRACT_VIOLATION`,
  `UNKNOWN_LEASE` and `REVISION_MISMATCH` outcomes;
- exact live-head lookup with no history walk;
- canonical digest recomputation excluding `content_digest`;
- explicit caller-supplied time and resource budgets;
- exact purpose, operation, typed scope and side-effect containment;
- fail-closed lifecycle ordering;
- fork/restore quarantine as `UNVERIFIED`;
- an `ALLOW` result that executes nothing.

```text
FROZEN_DOCS
≠ registry implemented
≠ resolver implemented
≠ Action Gate approval
≠ M3 write
≠ domain runtime
```

A future implementation requires a separate explicit owner GO in
`docs/CURRENT_STATUS.md` and a new Tier A exact-head review.

---

## 🧑‍💻 Solo governance

The repository currently has one maintainer and no genuine independent human
reviewer. The active ruleset therefore uses `required approvals = 0` while
retaining:

- mandatory pull requests;
- required CI;
- up-to-date branches;
- resolved conversations;
- force-push and deletion protection;
- an empty bypass list.

Tier A changes require:

```text
exact final head
+ complete diff inspection
+ correctness pass
+ adversarial pass
+ green exact-head CI
+ resolved conversations
+ explicit maintainer decision
+ green post-merge main CI
```

Automated agents may challenge and test changes but are not described as
independent human reviewers. [Issue #39](https://github.com/velantrian/velantrim-mentaury-soul/issues/39)
tracks the future transition when a real reviewer/team exists.

---

## 🔬 Research is not implementation

The [Research Index](docs/research/RESEARCH_INDEX.md) preserves ideas without
promoting them automatically.

```text
research presence ≠ roadmap priority
candidate captured ≠ selected
external research input ≠ integration
Notion page ≠ implementation authority
```

Current research includes:

- identity continuity and relational architecture;
- Genesis Heritage and Human Atlas;
- contextual cognition and epistemic context;
- character and presence;
- Native Kernel external input;
- storage and graph profile candidates;
- biological, cybernetic and cognitive candidates.

No PostgreSQL, Graphiti, LadybugDB or other future profile is selected merely by
being documented.

---

## 🚫 Explicitly absent

```text
Capability Lease registry / resolver runtime
Action Gate or Tool Receipt runtime
external tool execution
identity / character / relationship runtime
Controlled Origin ingestion runtime
Human Paths runtime
Non-Projection runtime
M3 identity writes
production deployment readiness
objective-truth authority
proven consciousness or subjective experience
```

---

## 🗂️ Repository map

```text
src/mentaury/
├── contracts/      typed primitives and canonical boundaries
├── storage/        SQLite event and payload persistence
├── replay/         deterministic replay contracts
├── beliefs/        minimal belief lifecycle
├── evidence/       evidence records and gate
└── epistemic_types.py

tests/              deterministic, adversarial and structural tests
scripts/            repository validator and doc-freshness gate
docs/               Canon, status, governance and research
.github/workflows/   permanent read-only CI
```

---

## 🧪 Local validation

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.lock
python scripts/validate.py
python scripts/check_doc_freshness.py
PYTHONPATH=src python -m pytest
python -m compileall -q src tests scripts
```

The required GitHub Actions job is:

```text
Python 3.13 · validator · pytest · compileall
```

---

## 🤝 Contribution and review

Read before changing the repository:

1. `AGENTS.md`;
2. `docs/CURRENT_STATUS.md`;
3. `docs/GOVERNANCE.md`;
4. the owning contract for the affected subsystem.

Do not:

- claim implementation from an open PR;
- convert research into runtime authority implicitly;
- bypass required checks or conversations;
- claim independent review during solo operation;
- weaken fail-closed behavior merely to make CI green;
- widen Action Gate, tool, M3 or domain-runtime authority without explicit GO.

---

## 🏁 Current formula

```text
P0 foundation implemented
+ permanent CI
+ active solo governance
+ P1-001 docs frozen

≠ P1 runtime implemented
≠ domain runtime authorized
≠ production ready
≠ independent assurance
```
