# 🧭 Mentaury Quick Reference

> **Role:** compact derived navigation only. For exact current engineering truth, use
> `docs/CURRENT_STATUS.md` plus live GitHub code/tests/CI. Historical milestone receipts
> remain in their owning documents and `docs/history/`.

```text
P0-001…P0-015_IMPLEMENTED_IN_MAIN
P1-001…P1-001_IMPLEMENTED_IN_MAIN
P1-002…P1-002_IMPLEMENTED_IN_MAIN
P1-003…P1-003_IMPLEMENTED_IN_MAIN
```

## Current state

| Area | State | Boundary |
|---|---|---|
| Canon v0.1 | FROZEN | architecture invariant source, not runtime authority |
| P0 foundation | IMPLEMENTED | deterministic storage/replay/belief/evidence substrate |
| P1-001 Capability Lease | IMPLEMENTED_BOUNDED | pure resolver; no registry/runtime service |
| P1-002 Privacy Reconciliation | IMPLEMENTED_BOUNDED | pure classifier; no mutation/retrieval authority |
| P1-003 Governed Constraint Composer | IMPLEMENTED_BOUNDED | pure composition; positive result ≠ action permission |
| NPG-v0.1 Non-Projection | IMPLEMENTED_BOUNDED | attribution protection only |
| NPG-COMP-v0.1 shadow composition | IMPLEMENTED_BOUNDED | same-attempt shadow observation only |
| PCR-v0.1 Provenance Claim Record | IMPLEMENTED_BOUNDED | claim/provenance representation only |
| EPR-v0.1 Epistemic Change Router | FROZEN_DOCS · NOT_IMPLEMENTED | routing contract only; Owner GO not granted |
| ATR-v0.1 Anchored Typed Relation | IMPLEMENTED_BOUNDED | relation representation; no truth/confidence authority |
| HDE-v0.1 Hypothesis Discrimination Evaluator | IMPLEMENTED_BOUNDED | structural discrimination only; no evidence verdict |
| Claim→belief binding | NOT_IMPLEMENTED | remains a separate research boundary |
| Terminal reconsideration lineage | NOT_IMPLEMENTED | remains a separate research boundary |
| Runtime / retrieval / tools / Action Gate | NOT_AUTHORIZED | cognition primitives grant no execution authority |
| Identity / relationship / M3 mutation | NOT_AUTHORIZED | no current runtime mutation authority |
| Deployment | NOT_AUTHORIZED | research repository only |
| Governance | SOLO_MAINTAINER | independent human review not claimed |

## Current frontier

```text
PCR-v0.1  ✅ IMPLEMENTED_BOUNDED
   │
   ├── EPR-v0.1  🧊 FROZEN_DOCS · NOT_IMPLEMENTED
   │
   └── ATR-v0.1  ✅ IMPLEMENTED_BOUNDED
                    │
                    ▼
              HDE-v0.1  ✅ IMPLEMENTED_BOUNDED
                    │
                    ▼
        next cognitive gap = RESEARCH ONLY
                  issue #129
```

```text
PHASE_6_IMPLEMENTATION_IMPLEMENTED_BOUNDED
PHASE_6_OWNER_GO_CONSUMED_BY_PR_127
PHASE_6_RUNTIME_NOT_AUTHORIZED
```

Issue #129 is a research/navigation question only. It does not select EPR, grant a new
Owner GO, authorize Phase 7, or authorize runtime.

## Core separations

```text
SOURCE ≠ PROVENANCE ≠ CLAIM ≠ BELIEF ≠ TRUTH
CLAIM ≠ BELIEF
RELATION ≠ TRUTH
RELATION TYPE ≠ CONFIDENCE
HYPOTHESIS ≠ FACT
PROPOSED OBSERVATION ≠ EVIDENCE
DISCRIMINATION ≠ EVIDENCE GATE VERDICT
IMPLEMENTED_BOUNDED ≠ RUNTIME AUTHORITY
THINK ≠ LEARN ≠ REMEMBER ≠ CHANGE SELF ≠ ACT
```

## Current implemented semantic primitives

### 🔐 Capability / privacy / composition

```text
caller-supplied context
        │
        ├─ capability lease resolution
        ├─ privacy reconciliation
        └─ governed constraint composition
        │
        ▼
classification / next-gate readiness only
```

No result performs retrieval, mutation, tool execution or deployment.

### 🪞 Non-Projection

```text
attributed interpretation
        │
        ▼
pure Non-Projection classifier
        │
        └── PASS_ATTRIBUTED / bounded alternatives
```

`PASS_ATTRIBUTED` is not truth, SELF, autobiography or runtime activation.

### 🌱 PCR-v0.1

Represents exact caller-supplied claims with provenance/basis while preserving distinct
claim class, type and epistemic role. PCR does not promote a claim into a belief or truth.

### 🔗 ATR-v0.1

Represents exact PCR-anchored typed relation candidates. ATR carries no confidence,
Evidence Gate verdict, graph-truth authority or belief mutation authority.

### 🔬 HDE-v0.1

Evaluates caller-supplied H1/H2 outcome partitions structurally and returns only bounded
`DISCRIMINATING`, `NON_DISCRIMINATING` or `INCONCLUSIVE_STRUCTURE` outcomes. HDE does
not execute observations, collect evidence or issue `SUPPORTED` / `CONTRADICTED`.

## Not authorized

```text
observation execution or evidence collection
retrieval execution
network / model / tool execution
scheduler or autonomous inquiry
new Evidence Gate / belief owner
graph truth or confidence propagation
Action Gate
identity, relationship or M3 mutation
runtime activation
deployment / production authority
```

## Navigation

- `docs/CURRENT_STATUS.md` — exact current engineering status
- `docs/GOVERNANCE.md` — risk tiers, merge/review and authority rules
- `docs/state/project_state.json` — derived machine snapshot
- `docs/research/RESEARCH_INDEX.md` — current research navigation
- `docs/research/POST_P0_ROADMAP_V0.1.md` — roadmap and milestone history
- issue `#129` — post-HDE cognitive-gap discrimination, research only
