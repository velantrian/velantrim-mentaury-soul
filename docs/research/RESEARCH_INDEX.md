# 🔬 Mentaury Research Index

```text
Status:                       ADOPTED NAVIGATION · DOCS_ONLY · NON_CANONICAL
Updated:                      2026-08-09
Purpose:                      separate research from execution
Current governance:           SOLO_MAINTAINER
Completed execution milestone:P1-001 · IMPLEMENTED_BOUNDED
Next execution milestone:     NOT SELECTED · NOT AUTHORIZED
Runtime deployment authority: NONE
Truth authority:              NONE
Identity authority:           NONE
Capability grant authority:   NONE
```

```text
Research presence ≠ roadmap priority
Research adoption ≠ implementation authorization
P1-001 completion ≠ authority for the next milestone
Candidate captured ≠ candidate selected
Notion explanation ≠ GitHub authority
Solo review ≠ independent human assurance
```

---

## 1. ✅ Completed execution checkpoint

Authoritative navigation:

- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md) — maturity and authorization;
- [`../GOVERNANCE.md`](../GOVERNANCE.md) — risk tiers and review policy;
- [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md) — authorization and completion receipt;
- [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md) — ordering and stop gate;
- [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md) — frozen P1-001 contract.

```text
P1_001_CAPABILITY_LEASE_RESOLUTION_IMPLEMENTED_BOUNDED
P1_001_PURE_RESOLVER_VALIDATED
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
```

Verified implementation evidence:

```text
Authorization PR #62
→ merge d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
→ post-merge CI 31322210843 · success

Implementation PR #63
→ reviewed head e873e43331fa7273b92f896b371707e4779b17d4
→ exact-head CI 31323051934 · success · 387 passed
→ merge f21809d8f31a457bd7acfe1d766230973ba9ecf5
→ post-merge CI 31323138053 · success
```

Implemented only:

```text
pure caller-supplied resolver
strict immutable contracts
exact admitted live-head lookup
canonical digest verification
exact denial precedence
all CAP-SC-001…CAP-SC-025 scenarios
recursive registry snapshot immutability
ALLOW executes nothing
```

Still forbidden:

```text
registry persistence or service
network or ambient-clock resolution
Action Gate
Tool Receipt or tool execution
event/replay integration
belief, identity, relationship or M3 mutation
domain runtime
backend selection
production deployment
```

---

## 2. 🧭 Document registry

| Document | Track | Disposition | Runtime |
|---|---|---|---|
| [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md) | execution contract | FROZEN_DOCS | implemented by bounded pure resolver |
| [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md) | authorization/evidence | OWNER_GO_CONSUMED | exact P1-001 slice complete |
| [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md) | roadmap | P1-001 complete; stop gate active | no next runtime authority |
| [`MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md`](MENTAURY_CONTEXTUAL_COGNITION_AND_EPISTEMIC_CONTEXT_NOTES.md) | research side-track | adopted docs-only | NOT IMPLEMENTED |
| [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md) | active research | adopted docs-only | NOT IMPLEMENTED |
| [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) | active research | adopted docs-only | NOT IMPLEMENTED |
| [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) | external research input | preserved · non-canonical | NOT AUTHORIZED |
| [`STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md`](STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md) | future profiles | captured · not selected | NOT AUTHORIZED |
| [`BIOLOGICAL_CYBERNETIC_AND_COGNITIVE_CANDIDATES_V0.1.md`](BIOLOGICAL_CYBERNETIC_AND_COGNITIVE_CANDIDATES_V0.1.md) | candidates | captured · none selected | NOT AUTHORIZED |

---

## 3. 🌱 Backlog

| ID | Direction | Status | Promotion evidence required |
|---|---|---|---|
| `R-ELIDA-001` | Identity as Practice | CAPTURED HYPOTHESIS | longitudinal criteria + falsification |
| `R-NPG-001` | Non-Projection Gate | CAPTURED | claim taxonomy + provenance + threat model |
| `R-HPA-001` | Human Paths Atlas | PARTLY DOCUMENTED | bounded schema + analogy/source limits |
| `R-CO-001` | Controlled Origin | PARTLY DOCUMENTED | consent + provenance + promotion boundaries |
| `R-KDT-001` | Knowledge Density Transformer | CAPTURED | conceptual-core preservation tests |
| `R-VHE-001` | Volumetric Humor | CAPTURED | safety suppression + factuality tests |
| `R-ECN-001` | Epistemic Conflict Navigator | CAPTURED | symmetric evidence + motive guardrails |
| `R-MM-001` | Memory Metabolism | CAPTURED | retention + replay + rollback semantics |
| `R-CHAR-001` | Character runtime | DEFERRED | Non-Projection and belief boundaries |
| `R-ID-001` | Identity / M2→M3 runtime | DEFERRED | longitudinal evidence + authority + rollback |
| `R-REL-001` | Relationship continuity | DEFERRED | privacy + consent + scope contracts |
| `R-DEV-001` | Bounded self-development | DEFERRED | Action Gate + capability authority + reversibility |

These entries are not a ranked execution queue.

---

## 4. 🚪 Promotion gate

Research becomes eligible for execution planning only after:

```text
problem demonstrated
+ existing mechanisms insufficient
+ minimal bounded slice
+ inputs / outputs / invariants
+ explicit non-goals
+ threat model
+ Canon and P0 compatibility
+ current-governance correctness review
+ current-governance adversarial review
+ explicit new owner authorization
```

The P1-001 Owner GO is consumed and cannot be reused for another milestone.
During solo operation, review remains attributable maintainer review. Issue #39
governs the future transition when a genuine independent reviewer/team exists.

---

## 5. 🔗 External and ecosystem boundary

```text
Mentaury research
≠ Crystal Canon
≠ Titan runtime
≠ Native Kernel runtime
≠ automatic ecosystem authority

Native Kernel input
≠ Native Kernel integration
≠ shared runtime
≠ automatic M2/M3 promotion
```

No backend is selected. PostgreSQL, Graphiti, LadybugDB and other candidates
remain research-only and provide no implementation authority.

---

## 6. 🗺️ Notion boundary

Notion is navigation and research workspace. GitHub `main`,
`docs/CURRENT_STATUS.md` and owning contracts remain engineering authority. A
Notion page cannot authorize implementation or select the next milestone.

---

## 7. 🏁 Rule

```text
Keep ideas.
Label their epistemic and implementation status.
Do not let research impersonate runtime truth.
Promote one bounded milestone at a time.
Stop after completion until a new bounded Owner GO exists.
```
