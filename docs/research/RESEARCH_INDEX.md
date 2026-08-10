# 🔬 Mentaury Research Index

```text
Status:                       ADOPTED NAVIGATION · DOCS_ONLY · NON_CANONICAL
Updated:                      2026-08-10
Purpose:                      separate research from execution
Current governance:           SOLO_MAINTAINER
Completed execution milestone:P1-001 · IMPLEMENTED_BOUNDED
Completed execution milestone:P1-002 Privacy Reconciliation Classifier · IMPLEMENTED_BOUNDED
Completed readiness block:    CROSS_GATE_BINDING_AND_COMPOSITION_READINESS · READY
Next execution milestone:     NOT SELECTED · NOT AUTHORIZED
P1-003 assignment:            NONE
Runtime deployment authority: NONE
Mutation authority:           NONE
Retrieval authority:          NONE
Identity authority:           NONE
```

```text
Research presence ≠ roadmap priority
P1-002 completion ≠ remediation authority
ALLOW_REFERENCE ≠ retrieval permission
ELIGIBLE_FOR_NEXT_GATE ≠ execution permission
Readiness contract ≠ implementation GO
Notion explanation ≠ GitHub authority
Solo review ≠ independent human assurance
```

Authoritative governance: [`../GOVERNANCE.md`](../GOVERNANCE.md).

---

## 1. ✅ Completed execution checkpoints

### P1-001 Capability Lease Resolution

```text
P1_001_CAPABILITY_LEASE_RESOLUTION_IMPLEMENTED_BOUNDED
P1_001_PURE_RESOLVER_VALIDATED
P1_001_OWNER_GO_CONSUMED
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
```

- [Frozen contract](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md)
- [Authorization/completion receipt](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)

### P1-002 Privacy Reconciliation Classifier

```text
P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_IMPLEMENTED_BOUNDED
P1_002_PURE_CLASSIFIER_VALIDATED
P1_002_OWNER_GO_CONSUMED
P1_002_MUTATION_AUTHORITY_NONE
P1_002_RETRIEVAL_AUTHORITY_NONE
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
```

- [Frozen contract](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [Authorization/completion receipt](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [Roadmap](POST_P0_ROADMAP_V0.1.md)
- [Current status](../CURRENT_STATUS.md)

Verified P1-002 evidence:

```text
Contract PR #65
→ head 85bf0070e2f15b5ca752b82325337d6ef0190396
→ CI 31331396018 · success · 401 passed
→ merge 1dc7bcf97986f455f48beb121c2048dfc34bd11c
→ main CI 31331506606 · success

Authorization PR #66
→ head 670b10c7ea69e3c609453e979a8de6853b23c6bc
→ CI 31331910395 · success · 398 passed
→ merge 8f4c444e2144d1dffde20fc60d6d5250148d07e6
→ main CI 31331973557 · success

Implementation PR #67
→ reviewed head 74662fb626a545ed63b426e98aa03524449019db
→ CI 31332728486 · success · 461 passed
→ merge d64679fd745e859527a70746df5e69dc9aca0408
→ main CI 31332793742 · success · 461 passed
```

Implemented only:

```text
pure caller-supplied privacy classification
strict immutable contracts
exact linkage and policy revisions
canonical complete budgets
exact allowlists and first-match precedence
surface-specific fail-closed decisions
all PRIV-SC-001…PRIV-SC-015 scenarios
minimal result without permission material
```

Still forbidden:

```text
persistence or scanning
deletion/redaction/quarantine/rebuild execution
retrieval execution
event/replay integration
relationship, belief, identity or M3 mutation
P1-001 invocation from P1-002
Action Gate, Tool Receipt or tools
backend selection and deployment
```

---

## 2. ✅ Completed docs-only readiness checkpoint

### Cross-Gate Binding & Composition Readiness

- [Frozen readiness contract](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md)
- [Owning selection](POST_P1_002_MILESTONE_SELECTION.md)
- [Current status](../CURRENT_STATUS.md)
- [Roadmap](POST_P0_ROADMAP_V0.1.md)

```text
CROSS_GATE_BINDING_READINESS = READY
SELECTED_STRATEGY             = PURE_COORDINATOR_OVER_VERIFIED_SOURCE_INPUTS
BARE_RESULT_COMPOSITION       = REJECTED
EVIDENCE_ENVELOPE             = DERIVED_EVIDENCE_ONLY
CALLER_SUPPLIED_DIGEST        = NOT_AUTHORITY
POSITIVE_READINESS            = ELIGIBLE_FOR_NEXT_GATE
P1_003                        = NOT_ASSIGNED
IMPLEMENTATION_AUTHORIZATION  = NONE
```

The readiness contract binds the future architecture to one immutable canonical
evaluation context, same-attempt gate evaluation, revision/version freshness,
coordinator-computed fingerprints and fail-closed handling of mismatch, stale,
unknown, missing or contradictory evidence.

It does not modify the frozen P1 result shapes and does not authorize a runtime
composer, retrieval, Action Gate, tools, identity/relationship runtime, M3
writes, persistence, I/O or deployment.

---

## 3. 🧭 Document registry

| Document | Track | Disposition | Runtime |
|---|---|---|---|
| [`../GOVERNANCE.md`](../GOVERNANCE.md) | governance | ADOPTED | merge/review policy |
| [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md) | P1-001 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md) | P1-001 receipt | OWNER_GO_CONSUMED | complete |
| [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md) | P1-002 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md) | P1-002 receipt | OWNER_GO_CONSUMED | complete |
| [`POST_P1_002_MILESTONE_SELECTION.md`](POST_P1_002_MILESTONE_SELECTION.md) | post-P1 selection | COMPLETE | no runtime selected |
| [`CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md) | cross-gate readiness | FROZEN_DOCS · READY | NOT AUTHORIZED |
| [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md) | roadmap | readiness complete; stop active | no next authority |
| [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) | research | docs-only | NOT IMPLEMENTED |
| [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md) | research | docs-only | NOT IMPLEMENTED |
| [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) | external input | non-canonical | NOT AUTHORIZED |
| [`STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md`](STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md) | future profiles | not selected | NOT AUTHORIZED |

---

## 4. 🌱 Research backlog

| ID | Direction | Status | Promotion evidence required |
|---|---|---|---|
| `R-ELIDA-001` | Identity as Practice | CAPTURED HYPOTHESIS | longitudinal criteria + falsification |
| `R-NPG-001` | Non-Projection Gate | CAPTURED | taxonomy + provenance + threat model |
| `R-HPA-001` | Human Paths Atlas | PARTLY DOCUMENTED | bounded schema + source limits |
| `R-CO-001` | Controlled Origin | PARTLY DOCUMENTED | consent + provenance boundaries |
| `R-KDT-001` | Knowledge Density Transformer | CAPTURED | preservation tests |
| `R-VHE-001` | Volumetric Humor | CAPTURED | safety + factuality tests |
| `R-ECN-001` | Epistemic Conflict Navigator | CAPTURED | symmetric evidence protocol |
| `R-MM-001` | Memory Metabolism | CAPTURED | retention + replay + rollback |
| `R-CHAR-001` | Character runtime | DEFERRED | required Character validation discipline |
| `R-ID-001` | Identity / M2→M3 runtime | DEFERRED | evidence + authority + rollback |
| `R-REL-001` | Relationship continuity | DEFERRED | privacy + consent + scope contracts |
| `R-DEV-001` | Bounded self-development | DEFERRED | Action Gate + capability + reversibility |

These entries are not a ranked execution queue.

A possible future runtime candidate may be evaluated separately:

```text
Pure Governed Constraint Composer
```

It is **not** P1-003 until a separate owner decision assigns it, and it has no
implementation authority now.

---

## 5. 🚪 Promotion gate

```text
problem demonstrated
+ minimal bounded slice
+ explicit contracts and non-goals
+ threat model
+ Canon/P0 compatibility
+ explicit new Owner GO
+ clean Tier A implementation PR
+ correctness and adversarial review
+ green resulting main CI
```

Each Owner GO is consumed once. Both P1-001 and P1-002 Owner GO receipts are
consumed. Cross-gate readiness grants no reusable Owner GO. Issue #39 remains
the future transition trigger for genuine independent review.

---

## 6. 🔗 Boundaries

```text
Mentaury research ≠ Crystal Canon ≠ Titan runtime ≠ Native Kernel runtime
external research input ≠ integration ≠ shared runtime ≠ automatic M2/M3 promotion
```

No backend is selected. Notion remains a navigation/research workspace; GitHub
`main`, `docs/CURRENT_STATUS.md` and owning contracts remain engineering
authority.

---

## 7. 🏁 Rule

```text
Keep ideas.
Label their status.
Bind gate evidence before composition.
Promote one bounded milestone at a time.
Consume each Owner GO once.
Stop before any unreviewed authority expansion.
```
