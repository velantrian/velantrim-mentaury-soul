# 🔬 Mentaury Research Index

```text
Status:                       ADOPTED NAVIGATION · DOCS_ONLY · NON_CANONICAL
Updated:                      2026-08-12
Purpose:                      separate research from execution
Current governance:           SOLO_MAINTAINER
Completed execution milestone:P1-001 · IMPLEMENTED_BOUNDED
Completed execution milestone:P1-002 Privacy Reconciliation Classifier · IMPLEMENTED_BOUNDED
Completed execution milestone:P1-003 Pure Governed Constraint Composer · IMPLEMENTED_BOUNDED
Completed execution milestone:NPG-v0.1 Pure Non-Projection Classifier · IMPLEMENTED_BOUNDED
Completed readiness block:    CROSS_GATE_BINDING_AND_COMPOSITION_READINESS · READY
Completed readiness block:    NON_PROJECTION_GATE_CONTRACT_READINESS · READY
P1-003 candidate:              PURE_GOVERNED_CONSTRAINT_COMPOSER
P1-003 contract:               FROZEN_DOCS
P1-003 Owner GO:              CONSUMED
P1-003 implementation:         IMPLEMENTED_BOUNDED
P1-003 runtime assignment:     NOT_ASSIGNED
Post-P1-003 selection:         COMPLETE
Selected Non-Projection model: ATTRIBUTED_INTERPRETATION_ENVELOPE
Non-Projection readiness:     READY · FROZEN_DOCS · DOCS_ONLY
Readiness positive meaning:   PASS_ATTRIBUTED only
Non-Projection candidate:     PURE_NON_PROJECTION_CLASSIFIER · SELECTED
Implementation contract:      FROZEN_DOCS · NPG-v0.1
Envelope version:             AIE-v0.1
Non-Projection Owner GO:      CONSUMED_BY_PR_90
Implementation authorization: CONSUMED · NPG-v0.1_ONLY
Non-Projection implementation:IMPLEMENTED_BOUNDED
Non-Projection runtime:       NOT_AUTHORIZED
P1-004 assignment:            NOT_ASSIGNED
Next execution milestone:      NOT_SELECTED · NOT_AUTHORIZED
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
READINESS_READY ≠ implementation authority
P1-002 completion ≠ remediation authority
ALLOW_REFERENCE ≠ retrieval permission
ELIGIBLE_FOR_NEXT_GATE ≠ execution permission
PASS_ATTRIBUTED ≠ truth / identity / relationship / action authority
P1-003 implemented bounded ≠ runtime activation
P1-003 implemented bounded ≠ Action Gate
P1-003 implemented bounded ≠ retrieval/tool authority
P1-003 Owner GO consumed ≠ reusable authority
NPG-v0.1 implemented bounded ≠ runtime activation
NPG-v0.1 Owner GO consumed ≠ reusable authority
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

The P1-001 Owner GO is consumed and does not authorize any later registry service,
Action Gate, P1-002 or subsequent runtime milestone.

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

Verified P1-002 implementation:

```text
PR #67
→ reviewed head 74662fb626a545ed63b426e98aa03524449019db
→ CI 31332728486 · success · 461 passed
→ merge/main d64679fd745e859527a70746df5e69dc9aca0408
→ main CI 31332793742 · success · 461 passed
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
```

The architecture retains original source inputs in one immutable canonical
context, evaluates both existing bounded gates in one attempt, binds relevant
revisions/versions and computes its own fingerprints.

---

## 3. ✅ P1-003 design checkpoints

### Candidate selection

- [Candidate selection & authorization boundary](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md)

```text
P1_003_CANDIDATE_SELECTION = SELECTED
P1_003_CANDIDATE           = PURE_GOVERNED_CONSTRAINT_COMPOSER
```

### Frozen contract

- [Frozen Pure Composer contract](P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md)

```text
P1_003_CONTRACT           = FROZEN_DOCS
P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED
```

The frozen implementation surface includes the exact immutable context/budget,
one public API, P1-001 `v0.2`, P1-002 `v0.1`, canonical JSON v1, two targeted
SHA-256 fingerprints, exact three-state result semantics, T1–T12, M1–M10, full
`CGC-*` matrix, no-hidden-I/O proof and the compatibility stop.

---

## 4. ✅ P1-003 Owner GO sequence

- [Authorization/completion receipt](../P1_003_IMPLEMENTATION_AUTHORIZATION.md)
- [Current status](../CURRENT_STATUS.md)
- [Roadmap](POST_P0_ROADMAP_V0.1.md)

### Owner GO — PR #77

```text
Reviewed head:   79fcedc8fe7dee64acad8dfffd8c8a17122ae97c
Exact-head CI:   31389769422 · success · 482 passed
Merge/main:      20a2073ef70eaa0e18ad7e8cf87b728d28617598
Main CI:         31390149526 · success · 482 passed
Review:          4896914677
```

### Receipt reconciliation — PR #78

```text
Reviewed head:   0f52e683a03fe9fe27428e7effe0349fd496bd26
Exact-head CI:   31393515732 · success · 482 passed
Merge/main:      813944b8083406da2ce95948bfb722158493fdb4
Main CI:         31393836549 · success
Review:          4897295575
```

The reconciled full frozen matrix is:

```text
CGC-CTX-001…014
CGC-FP-001…010
CGC-DEC-001…014
CGC-T-001…012
CGC-M-001…010
CGC-PURE-001…008
```

---

## 5. ✅ P1-003 bounded implementation checkpoint

PR #79 consumed the one-time bounded Owner GO.

```text
P1_003_OWNER_GO           = CONSUMED
P1_003_IMPLEMENTATION     = IMPLEMENTED_BOUNDED
P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```

Verified evidence:

```text
Implementation PR:         #79
Reviewed head:             9855f766f2bf801c8297c4f870b21d3ed37911fb
Exact-head CI:             31394829487 · success · 552 passed
Implementation merge/main: 59f2caa4deacd06aee0bbfc8dae1221edcb666eb
Resulting-main CI:         31395291622 · success · 552 passed
Tier A review:             4897445251
Correctness:               PASS
Adversarial:               PASS
Authorization boundary:    PRESERVED
Review threads:            0
Independent human review:  NO
```

Exact source package:

```text
src/mentaury/composition/__init__.py
src/mentaury/composition/governed_constraints/__init__.py
src/mentaury/composition/governed_constraints/contracts.py
src/mentaury/composition/governed_constraints/composer.py
```

The implementation performs pure same-attempt composition only. It does not
activate a runtime, retrieve data, execute tools, pass an Action Gate, mutate
identity/relationship/M3 state or deploy anything.

---

## 6. ✅ Non-Projection Gate — readiness through bounded implementation

Historical owning records:

- [Post-P1-003 selection](POST_P1_003_MILESTONE_SELECTION.md)
- [Frozen readiness contract](NON_PROJECTION_GATE_CONTRACT_READINESS.md)
- [Candidate selection](NON_PROJECTION_GATE_CANDIDATE_SELECTION.md)

Current owning contract/receipt:

- [Frozen NPG-v0.1 implementation contract](NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md)
- [NPG-v0.1 authorization/completion receipt](../NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md)
- [Current status](../CURRENT_STATUS.md)
- [Roadmap](POST_P0_ROADMAP_V0.1.md)

```text
NON_PROJECTION_GATE_CONTRACT_READINESS = READY
READINESS_STATUS                        = FROZEN_DOCS · DOCS_ONLY
SELECTED_MODEL                          = ATTRIBUTED_INTERPRETATION_ENVELOPE
READINESS_POSITIVE                      = PASS_ATTRIBUTED_ONLY
NON_PROJECTION_CANDIDATE_SELECTION      = SELECTED
NON_PROJECTION_CANDIDATE                = PURE_NON_PROJECTION_CLASSIFIER
NON_PROJECTION_IMPLEMENTATION_CONTRACT  = FROZEN_DOCS
NON_PROJECTION_CONTRACT_VERSION         = NPG-v0.1
ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION = AIE-v0.1
NON_PROJECTION_OWNER_GO                 = CONSUMED_BY_PR_90
IMPLEMENTATION_AUTHORIZATION            = CONSUMED · NPG-v0.1_ONLY
NON_PROJECTION_IMPLEMENTATION           = IMPLEMENTED_BOUNDED
NON_PROJECTION_RUNTIME                  = NOT_AUTHORIZED
P1_004                                  = NOT_ASSIGNED
```

Verified NPG implementation evidence:

```text
Implementation PR:             #90
Reviewed exact head:           a61427f85c70531b329894d5dc310e43bcc9d7de
Exact-head CI:                 31438692348 · success · 762 passed
Implementation merge/main:    cfb59fb7a49166d55360c6a8843269ab8f18b9e0
Resulting-main CI:             31438898049 · success · 762 passed
Completion PR:                 #91
Pre-Phase-0 main:              a8891793532a47ed682a0b713a587d08f16a23bc
Pre-Phase-0 main CI:           31439211018 · success · 768 passed
Independent human review:      NO
```

The readiness model still freezes provenance state/source classes,
speaker/subject attribution, claim classes, reviewer-correlation semantics,
scope/contextual-distance boundaries, fail-closed vocabulary and the complete
`NPG-T01…NPG-T12`, `NPG-SC-001…NPG-SC-012`, `MT-NPG-001…MT-NPG-008` families.

```text
PASS_ATTRIBUTED
≠ factual truth proof
≠ Mentaury autobiography
≠ identity / M3 authority
≠ relationship / commitment / consent authority
≠ capability or Action Gate PASS
≠ retrieval / tool / execution authority
```

Imported human/source material cannot become `VERIFIED_SELF` through prestige,
operator instruction, narrative similarity, model identity or shared project
lineage. NPG-v0.1 creates no identity runtime or self-attribution authority.

---

## 7. 🧭 Document registry

| Document | Track | Disposition | Runtime |
|---|---|---|---|
| [`../GOVERNANCE.md`](../GOVERNANCE.md) | governance | ADOPTED | merge/review policy |
| [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md) | P1-001 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md) | P1-001 receipt | OWNER_GO_CONSUMED | complete |
| [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md) | P1-002 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md) | P1-002 receipt | OWNER_GO_CONSUMED | complete |
| [`POST_P1_002_MILESTONE_SELECTION.md`](POST_P1_002_MILESTONE_SELECTION.md) | post-P1 selection | COMPLETE | no runtime selected |
| [`CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md) | cross-gate readiness | FROZEN_DOCS · READY | architecture only |
| [`P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md`](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md) | P1-003 candidate | FROZEN_DOCS · SELECTED_CANDIDATE | historical design checkpoint |
| [`P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`](P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md) | P1-003 contract | FROZEN_DOCS | implemented bounded against exact contract |
| [`../P1_003_IMPLEMENTATION_AUTHORIZATION.md`](../P1_003_IMPLEMENTATION_AUTHORIZATION.md) | P1-003 receipt | OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED | source implemented; runtime NOT_ASSIGNED |
| [`POST_P1_003_MILESTONE_SELECTION.md`](POST_P1_003_MILESTONE_SELECTION.md) | post-P1-003 selection | COMPLETE | historical Non-Projection readiness selection; P1-004 not assigned |
| [`NON_PROJECTION_GATE_CONTRACT_READINESS.md`](NON_PROJECTION_GATE_CONTRACT_READINESS.md) | Non-Projection readiness | FROZEN_DOCS · READY | historical readiness checkpoint |
| [`NON_PROJECTION_GATE_CANDIDATE_SELECTION.md`](NON_PROJECTION_GATE_CANDIDATE_SELECTION.md) | Non-Projection candidate | SELECTED | pure classifier selected; historical pre-contract checkpoint |
| [`NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md`](NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md) | Non-Projection contract | FROZEN_DOCS · NPG-v0.1 | implemented bounded; runtime NOT_AUTHORIZED |
| [`../NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md`](../NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md) | Non-Projection receipt | OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED | pure classifier complete; runtime NOT_AUTHORIZED |
| [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md) | roadmap | NPG-v0.1 bounded implementation complete; stop active | no next runtime authority |
| [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) | research | docs-only | NOT IMPLEMENTED |
| [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md) | research | docs-only | NOT IMPLEMENTED |
| [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) | external input | non-canonical | NOT AUTHORIZED |
| [`STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md`](STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md) | future profiles | not selected | NOT AUTHORIZED |

---

## 8. 🌱 Research backlog

| ID | Direction | Status | Promotion evidence required |
|---|---|---|---|
| `R-ELIDA-001` | Identity as Practice | CAPTURED HYPOTHESIS | longitudinal criteria + falsification |
| `R-NPG-001` | Non-Projection Gate | **IMPLEMENTED_BOUNDED** | any runtime composition/activation requires a new separate readiness/contract/Owner-GO cycle |
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

These entries are not a ranked execution queue. `IMPLEMENTED_BOUNDED` for
R-NPG-001 means only that the exact pure `NPG-v0.1` classifier is present and
validated. It creates no runtime, retrieval, action, identity, relationship, M3
or deployment authority.

---

## 9. 🚪 Promotion gate

```text
problem demonstrated
+ minimal bounded slice
+ explicit contracts and non-goals
+ threat model
+ Canon/P0 compatibility
+ docs-only readiness where required
+ separate candidate selection
+ separate implementation-contract freeze
+ explicit new Owner GO when authority is required
+ clean Tier A implementation PR
+ correctness and adversarial review
+ green resulting main CI
```

P1-001, P1-002, P1-003 and NPG-v0.1 bounded Owner GO receipts are consumed. A
consumed receipt cannot authorize a later runtime-capable milestone. Issue #39
remains the future transition trigger for genuine independent review.

---

## 10. 🔗 Boundaries

```text
Mentaury research ≠ external project authority
bounded implementation ≠ runtime activation
READINESS_READY ≠ implementation authorization
ELIGIBLE_FOR_NEXT_GATE ≠ Action Gate PASS
ALLOW_REFERENCE ≠ retrieval authority
PASS_ATTRIBUTED ≠ identity, relationship, consent or execution authority
```

No backend is selected. Notion remains a navigation/research workspace; GitHub
`main`, `docs/CURRENT_STATUS.md` and owning contracts/receipts remain engineering
authority.

---

## 11. 🏁 Rule

```text
Keep ideas.
Label their status.
Bind gate evidence before composition.
Preserve source/self attribution before learning from human experience.
Freeze readiness before candidate promotion.
Freeze implementation contracts before implementation authority.
Consume each Owner GO once.
Treat IMPLEMENTED_BOUNDED as narrower than runtime activation.
Stop before any unreviewed authority expansion.

P1_004 = NOT_ASSIGNED
NON_PROJECTION_IMPLEMENTATION_CONTRACT = FROZEN_DOCS · NPG-v0.1
NON_PROJECTION_OWNER_GO = CONSUMED_BY_PR_90
NON_PROJECTION_IMPLEMENTATION = IMPLEMENTED_BOUNDED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```
