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
P1-001…P1-001_IMPLEMENTED_IN_MAIN
P1_001_CAPABILITY_LEASE_RESOLUTION_IMPLEMENTED_BOUNDED
P1_001_PURE_RESOLVER_VALIDATED

NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
ACTION_GATE_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
DOMAIN_RUNTIME_NOT_AUTHORIZED
```

Mentaury does **not** claim proven consciousness, objective truth authority, a
finished digital personality or production readiness. Implemented milestones
are bounded architectural capabilities, not unrestricted runtime authority.

---

## 🚦 Source of truth

```text
IMPLEMENTED_BOUNDED
= exact authorized subsystem merged and retained by validation
≠ registry service
≠ Action Gate
≠ external action authority
≠ deployment
```

- [Current Status](docs/CURRENT_STATUS.md)
- [Governance](docs/GOVERNANCE.md)
- [P1-001 authorization and completion receipt](docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [P1-001 frozen contract](docs/research/MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [Post-P0 Roadmap](docs/research/POST_P0_ROADMAP_V0.1.md)
- [Research Index](docs/research/RESEARCH_INDEX.md)
- [Environment Manifest](docs/ENVIRONMENT_MANIFEST.md)
- [Quick Reference](docs/MENTAURY_QUICK_REFERENCE.md)

---

## 🧬 Architecture map

```text
MENTAURY SOUL
│
├── 🛡️ P0 integrity and epistemic foundation — implemented
│   ├── typed envelopes and canonical JSON
│   ├── immutable event/payload storage
│   ├── atomicity, idempotency and concurrency
│   ├── R0 integrity and deterministic R1 replay
│   ├── minimal belief lifecycle
│   └── deterministic Evidence Gate
│
├── 🔐 P1-001 Capability Lease Resolution — implemented bounded
│   ├── immutable typed contracts
│   ├── caller-supplied registry, intent, time and budgets
│   ├── exact live-head lookup; no history walk
│   ├── canonical digest and fail-closed invariants
│   ├── exact purpose / operation / typed scope / effects
│   ├── deterministic first-match denial
│   └── ALLOW executes nothing
│
├── 🔬 Research tracks — docs-only
│   ├── identity continuity and relationships
│   ├── Genesis Heritage and Human Atlas
│   ├── contextual cognition
│   ├── character and presence
│   └── biological / storage / graph candidates
│
└── 🚫 Not authorized
    ├── registry persistence or service
    ├── Action Gate and Tool Receipt
    ├── external tool execution
    ├── identity / relationship / M3 mutation
    ├── domain runtime
    └── production deployment
```

---

## ✅ P1-001 evidence

```text
Authorization PR #62
  exact-head CI 31322108100 · 327 passed
  merge d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
  post-merge CI 31322210843 · success

Implementation PR #63
  reviewed head e873e43331fa7273b92f896b371707e4779b17d4
  exact-head CI 31323051934 · 387 passed
  merge f21809d8f31a457bd7acfe1d766230973ba9ecf5
  post-merge CI 31323138053 · success
```

The final implementation covers all frozen `CAP-SC-001…CAP-SC-025` scenarios.
During adversarial review, nested snapshot mutability was found and corrected
before merge by recursively freezing stored records and adding a regression.

Implemented package:

```text
src/mentaury/capabilities/
└── lease/
    ├── contracts.py
    └── resolver.py
```

`ResolutionResult(ALLOW)` contains observations only, grants no reusable token
and performs no action.

---

## 🧑‍💻 Solo governance

The active ruleset retains mandatory PRs, required CI, up-to-date branches,
resolved conversations, force-push/deletion protection and an empty bypass
list. Approvals remain `0` while no genuine independent reviewer exists.

Tier A changes require exact-head CI, complete diff inspection, distinct
correctness and adversarial passes, resolved conversations, explicit maintainer
decision and green post-merge `main` CI.

[Issue #39](https://github.com/velantrian/velantrim-mentaury-soul/issues/39)
tracks only the future team transition.

---

## 🔬 Research is not implementation

```text
research presence ≠ roadmap priority
candidate captured ≠ selected
external research input ≠ integration
Notion page ≠ implementation authority
```

No backend or next runtime milestone is currently selected or authorized.

---

## 🚫 Explicitly absent

```text
Capability Lease registry persistence/service
network registry lookup or ambient clock authority
Action Gate / Tool Receipt runtime
external tool execution
P1 integration with event append or replay
identity / character / relationship runtime
M3 identity writes
backend selection or migration
production deployment readiness
objective-truth authority
consciousness claims
```

---

## 🧪 Local validation

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.lock
python scripts/validate.py
python scripts/check_doc_freshness.py
PYTHONPATH=src python -m pytest
python -m compileall -q src tests scripts
```

Required GitHub Actions job:

```text
Python 3.13 · validator · pytest · compileall
```

---

## 🏁 Current formula

```text
P0 foundation implemented
+ permanent CI
+ active solo governance
+ P1-001 pure resolver implemented bounded

≠ registry service
≠ Action Gate or tools
≠ domain runtime
≠ production ready
≠ independent assurance
```
