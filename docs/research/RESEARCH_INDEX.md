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
Completed execution milestone:NPG-COMP-v0.1 Shadow Composition · IMPLEMENTED_BOUNDED
Completed readiness block:    CROSS_GATE_BINDING_AND_COMPOSITION_READINESS · READY
Completed readiness block:    NON_PROJECTION_GATE_CONTRACT_READINESS · READY
Completed readiness block:    NPG-COMP-v0.1 RUNTIME_COMPOSITION_READINESS · READY
Completed readiness block:    PHASE_3_PROVENANCE_CLAIM_REPRESENTATION · READY
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
NPG-COMP contract:             FROZEN_DOCS · NPG-COMP-v0.1
NPG-COMP strategy:             SAME_ATTEMPT_SHADOW_COORDINATOR
Phase 2 Owner GO:             CONSUMED_BY_PR_96
Phase 2 Owner GO scope:       NPG-COMP-v0.1_ONLY · CONSUMED
Phase 2 implementation:       IMPLEMENTED_BOUNDED
Phase 3 readiness:            READY · DOCS_ONLY
Phase 3 candidate:            PURE_PROVENANCE_CLAIM_RECORD · SELECTED
Phase 3 contract:             FROZEN_DOCS · PCR-v0.1
Phase 3 implementation:       NOT_STARTED
Phase 3 Owner GO:             NOT_GRANTED
Phase 3 runtime:              NOT_AUTHORIZED
Next execution milestone:     PCR-v0.1 · OWNER_GO_REQUIRED
Phase 4:                      NOT_STARTED · OWNER_GO_NOT_GRANTED
Non-Projection runtime:       NOT_AUTHORIZED
P1-004 assignment:            NOT_ASSIGNED
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
P1-003 Owner GO consumed ≠ reusable authority
NPG-v0.1 implemented bounded ≠ runtime activation
NPG-v0.1 Owner GO consumed ≠ reusable authority
NPG-COMP-v0.1 implemented bounded ≠ runtime activation
NPG-COMP-v0.1 Owner GO consumed ≠ reusable authority
PCR-v0.1 frozen representation ≠ source admission / evidence support / belief promotion
ClaimClass ≠ ClaimType ≠ EpistemicRole
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

The P1-001 Owner GO is consumed and does not authorize any later registry
service, Action Gate, P1-002 or subsequent runtime milestone.

### P1-002 Privacy Reconciliation Classifier

```text
P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_IMPLEMENTED_BOUNDED
P1_002_PURE_CLASSIFIER_VALIDATED
P1_002_OWNER_GO_CONSUMED
P1_002_OWNER_GO_AUTHORIZED_BOUNDED   # historical provenance
P1_002_IMPLEMENTATION_NOT_STARTED    # historical provenance
P1_002_MUTATION_AUTHORITY_NONE
P1_002_RETRIEVAL_AUTHORITY_NONE
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
```

- [Frozen contract](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [Authorization/completion receipt](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [Roadmap](POST_P0_ROADMAP_V0.1.md)
- [Current status](../CURRENT_STATUS.md)

```text
PR #67
→ reviewed head 74662fb626a545ed63b426e98aa03524449019db
→ CI 31332728486 · success · 461 passed
→ merge/main d64679fd745e859527a70746df5e69dc9aca0408
→ main CI 31332793742 · success · 461 passed
```

---

## 2. ✅ Cross-Gate Binding & Composition Readiness

- [Frozen readiness contract](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md)
- [Owning selection](POST_P1_002_MILESTONE_SELECTION.md)

```text
CROSS_GATE_BINDING_READINESS = READY
SELECTED_STRATEGY             = PURE_COORDINATOR_OVER_VERIFIED_SOURCE_INPUTS
BARE_RESULT_COMPOSITION       = REJECTED
EVIDENCE_ENVELOPE             = DERIVED_EVIDENCE_ONLY
CALLER_SUPPLIED_DIGEST        = NOT_AUTHORITY
POSITIVE_READINESS            = ELIGIBLE_FOR_NEXT_GATE
```

---

## 3. ✅ P1-003 checkpoints

- [Candidate selection](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md)
- [Frozen contract](P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md)
- [Authorization/completion receipt](../P1_003_IMPLEMENTATION_AUTHORIZATION.md)

```text
P1_003_CANDIDATE_SELECTION = SELECTED
P1_003_CANDIDATE           = PURE_GOVERNED_CONSTRAINT_COMPOSER
P1_003_CONTRACT            = FROZEN_DOCS
P1_003_OWNER_GO            = CONSUMED
P1_003_IMPLEMENTATION      = IMPLEMENTED_BOUNDED
P1_003_RUNTIME_ASSIGNMENT  = NOT_ASSIGNED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```

```text
Implementation PR:         #79
Reviewed head:             9855f766f2bf801c8297c4f870b21d3ed37911fb
Exact-head CI:             31394829487 · success · 552 passed
Implementation merge/main: 59f2caa4deacd06aee0bbfc8dae1221edcb666eb
Resulting-main CI:         31395291622 · success · 552 passed
Tier A review:             4897445251
```

The P1-003 Owner GO is consumed. The pure composer remains bounded and does not
activate a runtime or Action Gate.

---

## 4. ✅ Non-Projection Gate — pure classifier

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

```text
PASS_ATTRIBUTED
≠ factual truth proof
≠ Mentaury autobiography
≠ identity / M3 authority
≠ relationship / commitment / consent authority
≠ capability or Action Gate PASS
≠ retrieval / tool / execution authority
```

---

## 5. ✅ Phase 1 NPG-COMP readiness and contract

- [Runtime-composition readiness](NON_PROJECTION_RUNTIME_COMPOSITION_READINESS.md)
- [Frozen contract](NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT_V0_1.md)

```text
NON_PROJECTION_RUNTIME_COMPOSITION_READINESS = READY
NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT = FROZEN_DOCS · NPG-COMP-v0.1
STRATEGY = SAME_ATTEMPT_SHADOW_COORDINATOR
WHO = NON_PROJECTION_SHADOW_COORDINATOR_ONLY
WHAT = exact caller-supplied AIE-v0.1 + exact NonProjectionBudget
WHERE = same-attempt bound shadow observation only
PRIOR_RESULT_INPUT = FORBIDDEN
RESULT_REPLAY_AS_AUTHORITY = FORBIDDEN
```

Historical Phase-1 `PHASE_2_OWNER_GO = NOT_GRANTED` remains freeze-time
provenance, not current authority.

---

## 6. 🟢 Phase 2 Owner GO and reconciliation — historical authority chain

- [Owner GO decision](NON_PROJECTION_RUNTIME_COMPOSITION_OWNER_GO_DECISION.md)
- [Post-GO reconciliation](NON_PROJECTION_RUNTIME_COMPOSITION_GO_STATUS_RECONCILIATION_2026_08_12.md)

```text
Owner GO PR:             #94
Owner GO exact head:     25a8cbf58fbdbee9fafc9ca41aa9575d47cd9450
Owner GO CI:             31547098692 · success · 783 passed
Owner GO review:         4911669134
Owner GO merge/main:     d0be41a0712d076101d508812a7eb491558b4f57
Owner GO main CI:        31547170338 · success · 783 passed
Reconciliation PR:       #95
Reconciliation head:     88b68a363981ff3c3b8f66259e06def49208af1b
Reconciliation CI:       31548130967 · success · 788 passed
Reconciliation review:   4911758911
Reconciliation main:     8c2be99b03e0dc5eee614b757060d8569bb88596
Reconciliation main CI:  31548204752 · success · 788 passed
```

The #94 authorization was single-use and is now consumed by the verified #96
implementation.

---

## 7. ✅ Phase 2 NPG-COMP-v0.1 shadow composition

Owning completion receipt:

[Phase 2 implementation authorization/completion receipt](../NON_PROJECTION_RUNTIME_COMPOSITION_IMPLEMENTATION_AUTHORIZATION.md)

```text
PHASE_2_OWNER_GO = CONSUMED_BY_PR_96
OWNER_GO_SCOPE = NPG-COMP-v0.1_ONLY
IMPLEMENTATION_AUTHORIZATION = CONSUMED · NPG-COMP-v0.1_ONLY
PHASE_2_IMPLEMENTATION = IMPLEMENTED_BOUNDED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
P1_004 = NOT_ASSIGNED
```

Verified implementation:

```text
Implementation PR:         #96
Reviewed exact head:       8a7b524de46c042e0479186ea4564f363248a366
Exact-head CI:             31548525699 · success · 842 passed
Tier A review:             4911798445
Correctness:               PASS
Adversarial:               PASS
Authorization boundary:    PRESERVED
Review threads:            0
Implementation merge/main: 153d64d142e5b5555bc3a942cb0beedce89b91e0
Resulting-main CI:         31548659423 · success · 842 passed
Independent human review:  NO
```

Exact source package:

```text
src/mentaury/composition/non_projection_shadow/__init__.py
src/mentaury/composition/non_projection_shadow/contracts.py
src/mentaury/composition/non_projection_shadow/coordinator.py
```

Executable frozen validation:

```text
NRC-T01…NRC-T12
NRC-M01…NRC-M10
```

This implementation is a pure same-attempt wrapper only. It does not persist,
self-schedule, retrieve, execute tools, mutate identity/relationship/M3 state,
pass Action Gate or activate deployment/runtime authority.

---

## 7.1 🧬 Phase 3 Provenance + Claim Representation — frozen docs-only

- [Readiness](PROVENANCE_CLAIM_REPRESENTATION_READINESS.md)
- [Candidate selection](PROVENANCE_CLAIM_REPRESENTATION_CANDIDATE_SELECTION.md)
- [Frozen `PCR-v0.1` contract](PROVENANCE_CLAIM_REPRESENTATION_CONTRACT_V0_1.md)
- [Tracking issue #98](https://github.com/velantrian/velantrim-mentaury-soul/issues/98)

```text
PHASE_3_PROVENANCE_CLAIM_REPRESENTATION_READINESS = READY
PHASE_3_CANDIDATE_SELECTION = SELECTED
PHASE_3_CANDIDATE = PURE_PROVENANCE_CLAIM_RECORD
PHASE_3_IMPLEMENTATION_CONTRACT = FROZEN_DOCS
PHASE_3_CONTRACT_VERSION = PCR-v0.1
PHASE_3_IMPLEMENTATION = NOT_STARTED
PHASE_3_OWNER_GO = NOT_GRANTED
PHASE_3_RUNTIME = NOT_AUTHORIZED
PHASE_4_EPISTEMIC_PROMOTION_REVISION = NOT_STARTED
PHASE_4_OWNER_GO = NOT_GRANTED
```

PCR-v0.1 owns representation only. It keeps `ClaimClass`, `ClaimType` and
`EpistemicRole` separate; reuses current class identities where they already
exist; introduces no second Evidence Gate or source admission gate; and treats
`evidence_refs` as references only, never as support status. Reserved
`src/mentaury/claims/**` implementation remains absent and unauthorized until a
later separate explicit Owner GO.

---

## 8. 🧭 Document registry

| Document | Track | Disposition | Runtime |
|---|---|---|---|
| [`../GOVERNANCE.md`](../GOVERNANCE.md) | governance | ADOPTED | merge/review policy |
| [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md) | P1-001 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md) | P1-001 receipt | OWNER_GO_CONSUMED | complete |
| [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md) | P1-002 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md) | P1-002 receipt | OWNER_GO_CONSUMED | complete |
| [`CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md) | cross-gate readiness | FROZEN_DOCS · READY | architecture only |
| [`P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`](P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md) | P1-003 contract | FROZEN_DOCS | implemented bounded |
| [`../P1_003_IMPLEMENTATION_AUTHORIZATION.md`](../P1_003_IMPLEMENTATION_AUTHORIZATION.md) | P1-003 receipt | OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED | runtime NOT_ASSIGNED |
| [`POST_P1_003_MILESTONE_SELECTION.md`](POST_P1_003_MILESTONE_SELECTION.md) | historical selection | COMPLETE | P1-004 not assigned |
| [`NON_PROJECTION_GATE_CONTRACT_READINESS.md`](NON_PROJECTION_GATE_CONTRACT_READINESS.md) | NPG readiness | FROZEN_DOCS · READY | historical readiness checkpoint |
| [`NON_PROJECTION_GATE_CANDIDATE_SELECTION.md`](NON_PROJECTION_GATE_CANDIDATE_SELECTION.md) | NPG candidate | SELECTED | historical design checkpoint |
| [`NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md`](NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md) | NPG contract | FROZEN_DOCS · NPG-v0.1 | implemented bounded |
| [`../NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md`](../NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md) | NPG receipt | OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED | runtime NOT_AUTHORIZED |
| [`NON_PROJECTION_RUNTIME_COMPOSITION_READINESS.md`](NON_PROJECTION_RUNTIME_COMPOSITION_READINESS.md) | Phase 1 composition readiness | READY · DOCS_ONLY | no runtime authority |
| [`NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT_V0_1.md`](NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT_V0_1.md) | Phase 1 composition contract | FROZEN_DOCS · NPG-COMP-v0.1 | implemented bounded by later authority |
| [`NON_PROJECTION_RUNTIME_COMPOSITION_OWNER_GO_DECISION.md`](NON_PROJECTION_RUNTIME_COMPOSITION_OWNER_GO_DECISION.md) | Phase 2 authority | OWNER_GO_CONSUMED | historical grant record |
| [`../NON_PROJECTION_RUNTIME_COMPOSITION_IMPLEMENTATION_AUTHORIZATION.md`](../NON_PROJECTION_RUNTIME_COMPOSITION_IMPLEMENTATION_AUTHORIZATION.md) | Phase 2 receipt | IMPLEMENTED_BOUNDED · OWNER_GO_CONSUMED | runtime NOT_AUTHORIZED |
| [`PROVENANCE_CLAIM_REPRESENTATION_READINESS.md`](PROVENANCE_CLAIM_REPRESENTATION_READINESS.md) | Phase 3 readiness | READY · DOCS_ONLY | no runtime authority |
| [`PROVENANCE_CLAIM_REPRESENTATION_CANDIDATE_SELECTION.md`](PROVENANCE_CLAIM_REPRESENTATION_CANDIDATE_SELECTION.md) | Phase 3 candidate | SELECTED · PURE_PROVENANCE_CLAIM_RECORD | no implementation authority |
| [`PROVENANCE_CLAIM_REPRESENTATION_CONTRACT_V0_1.md`](PROVENANCE_CLAIM_REPRESENTATION_CONTRACT_V0_1.md) | Phase 3 contract | FROZEN_DOCS · PCR-v0.1 | implementation NOT_STARTED |
| [`POST_P0_ROADMAP_V0.1.md`](POST_P0_ROADMAP_V0.1.md) | roadmap | Phase 3 contract frozen; Owner GO required | runtime NOT_AUTHORIZED |
| [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) | research | docs-only | NOT IMPLEMENTED |
| [`GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md`](GENESIS_HERITAGE_INTERPRETATION_AND_HUMAN_ATLAS_NOTES.md) | research | docs-only | NOT IMPLEMENTED |
| [`NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md`](NATIVE_KERNEL_RESEARCH_INPUT_NOTES_V0.1.md) | external input | non-canonical | NOT AUTHORIZED |
| [`STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md`](STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md) | future profiles | not selected | NOT AUTHORIZED |

---

## 9. 🌱 Research backlog

| ID | Direction | Status | Promotion evidence required |
|---|---|---|---|
| `R-ELIDA-001` | Identity as Practice | CAPTURED HYPOTHESIS | longitudinal criteria + falsification |
| `R-NPG-001` | Non-Projection Gate | **PHASE_2_IMPLEMENTED_BOUNDED** | runtime activation remains a separate authority cycle |
| `R-PCR-001` | Provenance + Claim Representation | **CONTRACT_FROZEN · PCR-v0.1** | separate explicit Owner GO before implementation |
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

These entries are not a ranked execution queue. PCR-v0.1 contract freeze creates
no runtime activation, promotion, retrieval, action, identity, relationship, M3
or deployment authority.

---

## 10. 🚪 Promotion gate

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

P1-001, P1-002, P1-003, NPG-v0.1 and NPG-COMP-v0.1 bounded Owner GO receipts
are consumed. No Owner GO rolls forward. PCR-v0.1 currently has **no Owner GO**.
Issue #39 remains the future transition trigger for genuine independent review.

---

## 11. 🔗 Boundaries

```text
Mentaury research ≠ external project authority
bounded implementation ≠ runtime activation
READINESS_READY ≠ implementation authorization
ELIGIBLE_FOR_NEXT_GATE ≠ Action Gate PASS
ALLOW_REFERENCE ≠ retrieval authority
PASS_ATTRIBUTED ≠ identity, relationship, consent or execution authority
NPG-COMP bounded completion ≠ runtime activation / retrieval / tools / identity / M3
PCR-v0.1 valid representation ≠ source admission / evidence support / belief promotion
PCR-v0.1 contract frozen ≠ Owner GO
ClaimClass ≠ ClaimType ≠ EpistemicRole
```

No backend is selected. Notion remains a navigation/research workspace; GitHub
`main`, `docs/CURRENT_STATUS.md` and owning contracts/receipts remain engineering
authority.

---

## 12. 🏁 Rule

```text
Keep ideas.
Label their status.
Bind gate evidence before composition.
Preserve source/self attribution before learning from human experience.
Separate ClaimClass, ClaimType and EpistemicRole.
Treat evidence references as references, never support status.
Freeze readiness before candidate promotion.
Freeze implementation contracts before implementation authority.
Consume each Owner GO once.
Treat IMPLEMENTED_BOUNDED as narrower than runtime activation.
Stop before any unreviewed authority expansion.

P1_004 = NOT_ASSIGNED
NON_PROJECTION_IMPLEMENTATION_CONTRACT = FROZEN_DOCS · NPG-v0.1
NON_PROJECTION_OWNER_GO = CONSUMED_BY_PR_90
NON_PROJECTION_IMPLEMENTATION = IMPLEMENTED_BOUNDED
NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT = FROZEN_DOCS · NPG-COMP-v0.1
PHASE_2_OWNER_GO = CONSUMED_BY_PR_96
PHASE_2_IMPLEMENTATION = IMPLEMENTED_BOUNDED
PHASE_3_PROVENANCE_CLAIM_REPRESENTATION_READINESS = READY
PHASE_3_CANDIDATE = PURE_PROVENANCE_CLAIM_RECORD
PHASE_3_IMPLEMENTATION_CONTRACT = FROZEN_DOCS · PCR-v0.1
PHASE_3_IMPLEMENTATION = NOT_STARTED
PHASE_3_OWNER_GO = NOT_GRANTED
PHASE_3_RUNTIME = NOT_AUTHORIZED
PHASE_4_EPISTEMIC_PROMOTION_REVISION = NOT_STARTED
PHASE_4_OWNER_GO = NOT_GRANTED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```
