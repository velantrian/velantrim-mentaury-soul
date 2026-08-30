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
| CBP-v0.1 Claim→belief binding | IMPLEMENTED_BOUNDED | creation-time PCR identity binding; no truth/evidence promotion |
| EPR-v0.1 Epistemic Change Router | IMPLEMENTED_BOUNDED | pure next-owner routing; no mutation/execution authority |
| ATR-v0.1 Anchored Typed Relation | IMPLEMENTED_BOUNDED | relation representation; no truth/confidence authority |
| HDE-v0.1 Hypothesis Discrimination Evaluator | IMPLEMENTED_BOUNDED | structural discrimination only; no evidence verdict |
| V1 offline epistemic E2E | VERIFIED | PCR→CBP→EPR→P0-014→P0-015; terminal reopen refused |
| V1 Research/Core | 1.0.0 · FINAL_ACCEPTANCE | release closure only; no runtime/deployment authority |
| Terminal reconsideration lineage | NOT_IMPLEMENTED · V1.1/V2_BACKLOG | no predecessor rewrite/reopen authority |
| Runtime / retrieval / tools / Action Gate | NOT_AUTHORIZED | cognition primitives grant no execution authority |
| Identity / relationship / M3 mutation | NOT_AUTHORIZED | no current runtime mutation authority |
| Deployment | NOT_AUTHORIZED | research repository only |
| Governance | SOLO_MAINTAINER | independent human review not claimed |

## Current frontier

```text
PCR-v0.1  ✅ IMPLEMENTED_BOUNDED
   │
   ▼
CBP-v0.1  ✅ IMPLEMENTED_BOUNDED · PR #147
   │
   ▼
EPR-v0.1  ✅ IMPLEMENTED_BOUNDED · PR #148
   │
   ├── routes bounded next-owner responsibility only
   │
   └── does not own belief/evidence mutation
   │
   ▼
P0-014 / P0-015  ✅ EXISTING OWNERS
   │
   ▼
V1 offline epistemic E2E  ✅ VERIFIED · PR #150
   │
   ▼
V1 Research/Core 1.0.0  ✅ FINAL_ACCEPTANCE

terminal reconsideration / successor lineage
→ V1.1 / V2 BACKLOG
→ NOT IMPLEMENTED
→ NO OWNER GO / RUNTIME AUTHORITY IMPLIED
```

```text
PHASE_4_IMPLEMENTATION_IMPLEMENTED_BOUNDED
PHASE_4_OWNER_GO_CONSUMED_BY_PR_148
CLAIM_TO_BELIEF_BINDING_IMPLEMENTED_BOUNDED
CLAIM_TO_BELIEF_BINDING_MERGED_BY_PR_147
PHASE_6_IMPLEMENTATION_IMPLEMENTED_BOUNDED
PHASE_6_OWNER_GO_CONSUMED_BY_PR_127
V1_STAGE_5_FINAL_ACCEPTANCE_COMPLETE
RUNTIME_DEPLOYMENT_NOT_AUTHORIZED
```

Issue #129 is a closed/superseded historical research checkpoint. It no longer represents
current next work: the selected EPR route and claim→belief prerequisite were subsequently
implemented bounded. Terminal reconsideration / successor lineage remains the explicit
V1.1/V2 backlog item.

## Core separations

```text
SOURCE ≠ PROVENANCE ≠ CLAIM ≠ BELIEF ≠ TRUTH
CLAIM ≠ BELIEF
CLAIM BINDING ≠ EVIDENCE SUPPORT
EPR ROUTING ≠ BELIEF / EVIDENCE MUTATION
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

### 🧷 CBP-v0.1

Binds an exact PCR record identity to belief genesis while delegating belief ownership to
P0-014. Binding does not establish source authenticity, statement equivalence, evidence
support, truth, identity, action authority or runtime permission.

### ⚖️ EPR-v0.1

Routes a bounded epistemic-change request to the already-owned next semantic surface. EPR
does not execute the routed operation, mutate belief/evidence state, issue an Evidence Gate
verdict, reopen terminal beliefs or grant permission.

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

## Retained compatibility receipts

These literals are retained because existing historical conformance tests bind them to the
quick reference. They are **not** a second current-state ledger.

```text
P1-001 historical implementation evidence: 387 passed
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
```

## Navigation

- `docs/CURRENT_STATUS.md` — exact current engineering status
- `docs/GOVERNANCE.md` — risk tiers, merge/review and authority rules
- `docs/state/project_state.json` — derived machine snapshot
- `docs/research/RESEARCH_INDEX.md` — research navigation with explicit historical/currentness reconciliation
- `docs/research/POST_P0_ROADMAP_V0.1.md` — roadmap/milestone history; reconcile against Current Status before treating old checkpoint literals as current
- issue `#129` — closed/superseded historical post-HDE research checkpoint
