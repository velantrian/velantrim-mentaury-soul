# 🔬 Mentaury Research Index

```text
Status:                       ADOPTED NAVIGATION · DOCS_ONLY · NON_CANONICAL
Updated:                      2026-08-10
Purpose:                      separate research from execution
Current governance:           SOLO_MAINTAINER
Completed execution milestone:P1-001 · IMPLEMENTED_BOUNDED
Completed execution milestone:P1-002 Privacy Reconciliation Classifier · IMPLEMENTED_BOUNDED
Completed readiness block:    CROSS_GATE_BINDING_AND_COMPOSITION_READINESS · READY
P1-003 candidate selection:    SELECTED
P1-003 candidate:              PURE_GOVERNED_CONSTRAINT_COMPOSER
P1-003 contract:               FROZEN_DOCS
P1-003 assignment:            NONE
P1-003 Owner GO:              AUTHORIZED_BOUNDED
P1-003 implementation:         NOT_STARTED
Next bounded milestone:        P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_BOUNDED_IMPLEMENTATION
Implementation authorization: AUTHORIZED_BOUNDED · P1-003-v0.1 ONLY
Runtime deployment authority: NONE
Action Gate authority:         NONE
Mutation authority:           NONE
Retrieval authority:          NONE
Tool authority:               NONE
Identity authority:           NONE
Relationship authority:       NONE
Direct or indirect M3 write:  FORBIDDEN
```

```text
Research presence ≠ roadmap priority
P1-002 completion ≠ remediation authority
ALLOW_REFERENCE ≠ retrieval permission
ELIGIBLE_FOR_NEXT_GATE ≠ execution permission
Readiness contract ≠ implementation GO
candidate selected ≠ P1-003 assigned
contract freeze ≠ Owner GO
Owner GO ≠ implementation complete
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
```

The readiness contract binds the future architecture to one immutable canonical
evaluation context, same-attempt gate evaluation, revision/version freshness,
coordinator-computed fingerprints and fail-closed handling of mismatch, stale,
unknown, missing or contradictory evidence.

It does not modify the frozen P1 result shapes and does not authorize a runtime
composer, retrieval, Action Gate, tools, identity/relationship runtime, M3
writes, persistence, I/O or deployment.

---

## 3. ✅ P1-003 candidate selection checkpoint

- [Candidate selection & authorization boundary](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md)
- [Current status](../CURRENT_STATUS.md)
- [Roadmap](POST_P0_ROADMAP_V0.1.md)

```text
P1_003_CANDIDATE_SELECTION = SELECTED
P1_003_CANDIDATE           = PURE_GOVERNED_CONSTRAINT_COMPOSER
P1_003_RUNTIME_ASSIGNMENT  = NOT_ASSIGNED
```

The selected candidate is a minimal pure same-attempt coordinator over the
existing bounded P1-001 and P1-002 gates. It may eventually produce only bounded
readiness and derived evidence. It is not an Action Gate, retrieval service,
persistence service, execution layer or identity/relationship runtime.

---

## 4. ✅ P1-003 frozen contract checkpoint

- [Frozen Pure Composer contract](P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md)
- [Candidate selection boundary](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md)
- [Current status](../CURRENT_STATUS.md)
- [Roadmap](POST_P0_ROADMAP_V0.1.md)

The contract-freeze document remains historical evidence of the no-GO state at
freeze time and is intentionally not rewritten by the later Owner GO receipt.
Its contract semantics remain frozen.

```text
P1_003_CONTRACT              = FROZEN_DOCS
P1_003_RUNTIME_ASSIGNMENT    = NOT_ASSIGNED
CONTRACT_FROZEN              ≠ OWNER_GO
```

Frozen implementation surface:

```text
CrossGateEvaluationContext exact immutable schema
CompositionBudget exact bounded schema
compose_governed_constraints(*, context=...) exact public API
no bare P1 result input
no caller digest/fingerprint input
P1-001-v0.2 + P1-002-v0.1 exact version expectations
MENTAURY_CANONICAL_JSON_V1
common-request SHA-256 fingerprint
targeted evaluation-evidence SHA-256 fingerprint
CALLER_SUPPLIED_VALUE_EVIDENCE_ONLY provenance scope
ELIGIBLE_FOR_NEXT_GATE / NOT_ELIGIBLE / DEFER exact result vocabulary
exact gate outcome disposition mapping and precedence
same-attempt freshness / no replay
T1–T12 executable adversarial requirements
M1–M10 executable metamorphic requirements
CGC-* mandatory test matrix
import-time + call-time no-hidden-I/O proof
compatibility stop if frozen P1 semantics would need changes
```

---

## 5. ✅ P1-003 bounded Owner GO checkpoint

- [Bounded Owner GO receipt](../P1_003_IMPLEMENTATION_AUTHORIZATION.md)
- [Frozen Pure Composer contract](P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md)
- [Current status](../CURRENT_STATUS.md)
- [Roadmap](POST_P0_ROADMAP_V0.1.md)

```text
P1_003_CONTRACT              = FROZEN_DOCS
P1_003_OWNER_GO              = AUTHORIZED_BOUNDED
P1_003_OWNER_GO_AUTHORIZED_BOUNDED
P1_003_IMPLEMENTATION_NOT_STARTED
P1_003_RUNTIME_ASSIGNMENT    = NOT_ASSIGNED
IMPLEMENTATION_AUTHORIZATION = AUTHORIZED_BOUNDED · P1-003-v0.1 ONLY
```

The authorization is exact-contract-bound, scope-bound, one-time/consumable and
non-transferable. It authorizes only a future separate bounded implementation
milestone for the frozen P1-003 v0.1 package and API. It does not create runtime
code or grant runtime activation, Action Gate, retrieval, tools, identity,
relationship, M3, Character or deployment authority.

The next implementation milestone must start with a fresh live-state preflight,
consume this exact receipt, and stop for a new docs-only contract revision plus
new Owner decision if implementation would require changing frozen P1-001,
P1-002, canonical JSON or P1-003 semantics.

---

## 6. 🧭 Document registry

| Document | Track | Disposition | Runtime |
|---|---|---|---|
| [`../GOVERNANCE.md`](../GOVERNANCE.md) | governance | ADOPTED | merge/review policy |
| [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md) | P1-001 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md) | P1-001 receipt | OWNER_GO_CONSUMED | complete |
| [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md) | P1-002 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md) | P1-002 receipt | OWNER_GO_CONSUMED | complete |
| [`POST_P1_002_MILESTONE_SELECTION.md`](POST_P1_002_MILESTONE_SELECTION.md) | post-P1 selection | COMPLETE | no runtime selected |
| [`CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md) | cross-gate readiness | FROZEN_DOCS · READY | NOT AUTHORIZED |
| [`P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md`](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md) | P1-003 candidate | FROZEN_DOCS · SELECTED_CANDIDATE | NOT ASSIGNED |
| [`P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`](P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md) | P1-003 contract | FROZEN_DOCS | contract unchanged; no self-authorization |
| [`../P1_003_IMPLEMENTATION_AUTHORIZATION.md`](../P1_003_IMPLEMENTATION_AUTHORIZATION.md) | P1-003 receipt | OWNER_GO · AUTHORIZED_BOUNDED · NOT_STARTED | exact P1-003-v0.1 implementation only; no activation |
| [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md) | roadmap | Owner GO authorized; implementation next separate block | NOT_STARTED |
| [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) | research | docs-only | NOT IMPLEMENTED |
| [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md) | research | docs-only | NOT IMPLEMENTED |
| [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) | external input | non-canonical | NOT AUTHORIZED |
| [`STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md`](STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md) | future profiles | not selected | NOT AUTHORIZED |

---

## 7. 🌱 Research backlog

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

`Pure Governed Constraint Composer` is no longer an unfrozen research candidate:
its contract is frozen and one bounded Owner GO is now recorded, while the
implementation remains `NOT_STARTED` and runtime assignment remains absent.

---

## 8. 🚪 Promotion gate

```text
problem demonstrated
+ minimal bounded slice
+ explicit contracts and non-goals
+ threat model
+ Canon/P0 compatibility
+ explicit new Owner GO
+ clean Tier A implementation PR in a separate bounded milestone
+ correctness and adversarial review
+ green resulting main CI
```

Each Owner GO is consumed once. P1-001 and P1-002 Owner GO receipts are consumed.
The P1-003 v0.1 Owner GO is now authorized but unconsumed because implementation
has not started. Cross-gate readiness, candidate selection and contract freeze do
not themselves grant reusable authority. Issue #39 remains the future transition
trigger for genuine independent review.

---

## 9. 🔗 Boundaries

```text
Mentaury research ≠ Crystal Canon ≠ Titan runtime ≠ Native Kernel runtime
external research input ≠ integration ≠ shared runtime ≠ automatic M2/M3 promotion
```

No backend is selected. Notion remains a navigation/research workspace; GitHub
`main`, `docs/CURRENT_STATUS.md` and owning contracts/receipts remain engineering
authority.

---

## 10. 🏁 Rule

```text
Keep ideas.
Label their status.
Bind gate evidence before composition.
Select one bounded candidate at a time.
Freeze its contract before any Owner GO.
Require a separate explicit Owner GO before implementation.
Consume each Owner GO once.
Run implementation only as a new bounded milestone after fresh live preflight.
Stop before any unreviewed authority expansion.
```
