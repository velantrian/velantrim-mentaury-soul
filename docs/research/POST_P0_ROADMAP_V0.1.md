# 🗺️ Post-P0 Roadmap

```text
Status:                       ADOPTED ROADMAP · DOCS_ONLY
Version:                      1.5
Updated:                      2026-08-12
Current review mode:          SOLO_MAINTAINER · TIER_A
P1-001 implementation:        IMPLEMENTED_BOUNDED
P1-002 implementation:        IMPLEMENTED_BOUNDED
P1-002 Owner GO:              CONSUMED
Post-P1-002 selection:         COMPLETE
Cross-gate readiness:         READY · FROZEN_DOCS · DOCS_ONLY
Selected binding strategy:    PURE_COORDINATOR_OVER_VERIFIED_SOURCE_INPUTS
Bare-result composition:      REJECTED
Positive readiness meaning:   ELIGIBLE_FOR_NEXT_GATE only
P1-003 candidate selection:    SELECTED
P1-003 candidate:              PURE_GOVERNED_CONSTRAINT_COMPOSER
P1-003 contract:               FROZEN_DOCS
P1-003 Owner GO:               CONSUMED
P1-003 implementation:         IMPLEMENTED_BOUNDED
P1-003 validation:             EXACT_HEAD_AND_MAIN_CI_PASS
P1-003 runtime assignment:     NOT_ASSIGNED
Post-P1-003 selection:         COMPLETE
Non-Projection readiness:     READY · FROZEN_DOCS · DOCS_ONLY
Selected Non-Projection model: ATTRIBUTED_INTERPRETATION_ENVELOPE
Readiness positive meaning:   PASS_ATTRIBUTED only
Non-Projection candidate:     PURE_NON_PROJECTION_CLASSIFIER · SELECTED
Implementation contract:      FROZEN_DOCS · NPG-v0.1
Envelope version:             AIE-v0.1
Non-Projection Owner GO:      CONSUMED_BY_PR_90
Implementation authorization: CONSUMED · NPG-v0.1_ONLY
Non-Projection implementation:IMPLEMENTED_BOUNDED
Phase 1 composition readiness: READY
Phase 1 composition contract: FROZEN_DOCS · NPG-COMP-v0.1
Phase 2 Owner GO:             GRANTED_BY_PR_94
Phase 2 Owner GO scope:       NPG-COMP-v0.1_ONLY · SINGLE_USE
Phase 2 implementation:       NOT_STARTED
Next bounded implementation:  NPG-COMP-v0.1_SHADOW · AUTHORIZED_NOT_STARTED
Non-Projection runtime:       NOT_AUTHORIZED
P1-004 assignment:            NOT_ASSIGNED
Runtime activation milestone: NOT_SELECTED · NOT_AUTHORIZED
Runtime deployment authority: NONE
Action Gate authority:         NONE
Mutation authority:           NONE
Retrieval authority:          NONE
Tool authority:               NONE
Identity authority:           NONE
Relationship authority:       NONE
Direct or indirect M3 write:  FORBIDDEN
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
DOMAIN_RUNTIME_NOT_AUTHORIZED
```

```text
IMPLEMENTED_BOUNDED ≠ runtime activation
READINESS_READY ≠ implementation authority
ALLOW_REFERENCE ≠ retrieval permission
ELIGIBLE_FOR_NEXT_GATE ≠ execution permission
PASS_ATTRIBUTED ≠ truth / identity / action authority
P1-003 completion ≠ Action Gate authority
P1-003 completion ≠ retrieval/tool authority
P1-003 completion ≠ runtime assignment
NPG-v0.1 implementation ≠ NPG runtime activation
NPG-v0.1 implementation ≠ P1-004 assignment
NPG-v0.1 Owner GO consumed ≠ reusable authority
NPG-COMP-v0.1 Owner GO = one bounded implementation authorization only
NPG-COMP-v0.1 Owner GO ≠ runtime activation / Action Gate / retrieval / tools / identity / M3
Solo review ≠ independent certification
```

The filename retains `V0.1` for stable historical links. Document metadata is
the current version authority. Historical readiness/selection sections below
retain the state that was true at those milestones; current authority is the
header, current next-authority section, current formula and owning receipts.

---

## 1. ✅ P1-001 retained checkpoint

```text
Authorization PR:       #62
Implementation PR:      #63
Reviewed head:          e873e43331fa7273b92f896b371707e4779b17d4
Exact-head CI:          31323051934 · success · 387 passed
Implementation merge:   f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI:          31323138053 · success
P1-001 Owner GO:        CONSUMED
```

Frozen contract: [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md).
Owning receipt: [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md).

P1-001 remains a pure capability classifier without registry persistence,
Action Gate, tool execution, identity/M3 mutation or deployment authority.
The consumed P1-001 authorization rolls forward to **no registry service, Action Gate, P1-002** or later runtime milestone.

---

## 2. ✅ P1-002 Privacy Reconciliation Classifier retained checkpoint

```text
Contract PR:            #65
Authorization PR:       #66
Implementation PR:      #67
Reviewed head:          74662fb626a545ed63b426e98aa03524449019db
Exact-head CI:          31332728486 · success · 461 passed
Implementation merge:   d64679fd745e859527a70746df5e69dc9aca0408
Post-merge CI:          31332793742 · success · 461 passed
Correctness:            PASS
Adversarial:            PASS
P1-002 Owner GO:        CONSUMED
```

Owning surfaces:

- [Frozen contract](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [Authorization and completion receipt](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [Current status](../CURRENT_STATUS.md)

`ALLOW_REFERENCE` remains classification data only and performs no retrieval or
remediation.

---

## 3. ✅ Cross-gate binding/composition readiness

The post-P1-002 work demonstrated that bare P1 results cannot prove a common
request/context/freshness binding. The frozen docs-only architecture is:

[`CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md)

```text
one immutable canonical evaluation context
→ original source inputs projected into existing pure P1 gates
→ same-attempt evaluation
→ request + authority + privacy revision/version binding
→ coordinator-computed canonical fingerprints
→ at most ELIGIBLE_FOR_NEXT_GATE
```

```text
CROSS_GATE_BINDING_READINESS = READY
STRATEGY_A_PURE_COORDINATOR  = SELECTED
STRATEGY_B_EVIDENCE_ENVELOPE = DERIVED_EVIDENCE_ONLY
STRATEGY_C_BARE_RESULTS       = REJECTED
CALLER_SUPPLIED_DIGEST        = NOT_AUTHORITY
FRESHNESS                     = SAME_ATTEMPT + REVISION_BOUND
```

---

## 4. ✅ P1-003 candidate and contract checkpoints

Candidate selection:

[`P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md`](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md)

Frozen implementation contract:

[`P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`](P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md)

```text
P1_003_CANDIDATE_SELECTION = SELECTED
P1_003_CANDIDATE           = PURE_GOVERNED_CONSTRAINT_COMPOSER
P1_003_CONTRACT            = FROZEN_DOCS
P1_003_RUNTIME_ASSIGNMENT  = NOT_ASSIGNED
```

The frozen contract retains exact context/API/result/fingerprint semantics,
P1-001 `v0.2`, P1-002 `v0.1`, `MENTAURY_CANONICAL_JSON_V1`, T1–T12, M1–M10,
all `CGC-*` families, no-hidden-I/O proof and the compatibility stop.

---

## 5. ✅ P1-003 Owner GO and reconciliation sequence

Owning receipt:

[`../P1_003_IMPLEMENTATION_AUTHORIZATION.md`](../P1_003_IMPLEMENTATION_AUTHORIZATION.md)

### Owner GO — PR #77

```text
Reviewed head:   79fcedc8fe7dee64acad8dfffd8c8a17122ae97c
Exact-head CI:   31389769422 · success · 482 passed
Merge/main:      20a2073ef70eaa0e18ad7e8cf87b728d28617598
Post-merge CI:   31390149526 · success · 482 passed
Tier A review:   4896914677
```

### Receipt reconciliation — PR #78

```text
Reviewed head:   0f52e683a03fe9fe27428e7effe0349fd496bd26
Exact-head CI:   31393515732 · success · 482 passed
Merge/main:      813944b8083406da2ce95948bfb722158493fdb4
Post-merge CI:   31393836549 · success
Tier A review:   4897295575
```

PR #78 changed no P1-003 semantics. It only aligned the authorization receipt's
explicit shorthand with the already frozen complete matrix:

```text
CGC-CTX-001…014
CGC-FP-001…010
CGC-DEC-001…014
CGC-T-001…012
CGC-M-001…010
CGC-PURE-001…008
```

---

## 6. ✅ P1-003 bounded implementation complete

Implementation PR #79 consumed the one-time Owner GO and implemented only the
frozen pure composer slice.

```text
Implementation PR:         #79
Reviewed head:             9855f766f2bf801c8297c4f870b21d3ed37911fb
Exact-head CI:             31394829487 · success · 552 passed
Implementation merge/main: 59f2caa4deacd06aee0bbfc8dae1221edcb666eb
Post-merge CI:             31395291622 · success · 552 passed
Tier A review:             4897445251
Correctness:               PASS
Adversarial:               PASS
Authorization boundary:    PRESERVED
Review threads:            0
Independent human review:  NO
```

Exact completed source package:

```text
src/mentaury/composition/__init__.py
src/mentaury/composition/governed_constraints/__init__.py
src/mentaury/composition/governed_constraints/contracts.py
src/mentaury/composition/governed_constraints/composer.py
```

Current state:

```text
P1_003_OWNER_GO              = CONSUMED
P1_003_IMPLEMENTATION        = IMPLEMENTED_BOUNDED
P1_003_RUNTIME_ASSIGNMENT    = NOT_ASSIGNED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```

`IMPLEMENTED_BOUNDED` means the pure package exists and is retained by exact-head
and resulting-main validation. It does not mean runtime activation or broader
authority.

---

## 7. 🧱 P1-003 retained result boundary

```text
Capability ALLOW
+ Privacy ALLOW_REFERENCE
+ verified same-attempt binding
= at most ELIGIBLE_FOR_NEXT_GATE
```

Still explicitly:

```text
ELIGIBLE_FOR_NEXT_GATE ≠ ACTION_GATE_PASS
ELIGIBLE_FOR_NEXT_GATE ≠ RETRIEVAL_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ TOOL_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ EXECUTION_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ IDENTITY_AUTHORITY
ELIGIBLE_FOR_NEXT_GATE ≠ RELATIONSHIP_AUTHORITY
ELIGIBLE_FOR_NEXT_GATE ≠ M3_AUTHORITY
ELIGIBLE_FOR_NEXT_GATE ≠ DEPLOYMENT_AUTHORITY
```

---

## 8. 🪞 Historical Post-P1-003 Non-Projection selection

Owning historical selection:

[`POST_P1_003_MILESTONE_SELECTION.md`](POST_P1_003_MILESTONE_SELECTION.md)

At that milestone, the selected bounded work was docs-only:

```text
POST_P1_003_SELECTION = COMPLETE
SELECTED_BOUNDED_WORK = NON_PROJECTION_GATE_CONTRACT_READINESS
P1_004                 = NOT_ASSIGNED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
OWNER_GO               = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NONE
```

Those `NOT_GRANTED/NONE` values are historical selection-time provenance only;
they are not the current NPG authority state after PRs #86–#91.

---

## 9. ✅ Non-Projection readiness, contract and bounded implementation

Owning historical readiness document:

[`NON_PROJECTION_GATE_CONTRACT_READINESS.md`](NON_PROJECTION_GATE_CONTRACT_READINESS.md)

Owning candidate, frozen contract and completion receipt:

- [`NON_PROJECTION_GATE_CANDIDATE_SELECTION.md`](NON_PROJECTION_GATE_CANDIDATE_SELECTION.md)
- [`NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md`](NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md)
- [`../NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md`](../NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md)

The readiness model remains `ATTRIBUTED_INTERPRETATION_ENVELOPE` with
`PASS_ATTRIBUTED` as the bounded positive result. Subsequent bounded milestones
selected the pure classifier, froze `NPG-v0.1`, granted one exact Owner GO, and
consumed that GO through PR #90 implementation plus PR #91 completion receipt.

Current state:

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

Verified implementation checkpoint:

```text
Implementation PR:             #90
Reviewed exact head:           a61427f85c70531b329894d5dc310e43bcc9d7de
Exact-head CI:                 31438692348 · success · 762 passed
Implementation merge/main:    cfb59fb7a49166d55360c6a8843269ab8f18b9e0
Resulting-main CI:             31438898049 · success · 762 passed
Completion PR:                 #91
Pre-Phase-0 main:              a8891793532a47ed682a0b713a587d08f16a23bc
Pre-Phase-0 main CI:           31439211018 · success · 768 passed
```

The frozen fail-closed source/self attribution, claim classes, reviewer
correlation semantics, contextual/scope requirements, NPG-T01…T12,
NPG-SC-001…012 and MT-NPG-001…008 remain unchanged.

```text
PASS_ATTRIBUTED
= no bounded projection blocker found for the exact attributed interpretation
≠ factual truth proof
≠ autobiography or identity authority
≠ relationship / commitment / consent authority
≠ M3 authority
≠ capability / Action Gate PASS
≠ retrieval / tool / execution authority
```

Character presentation cannot override this result. Frozen P1 contracts and
Canon v0.1 remain unchanged.

---

## 10. 🚫 Work not included

```text
registry persistence or services
backup/fork discovery or scanning
content remediation execution
retrieval execution
network/filesystem/database authority
ambient clock/environment authority
event append or replay/projection integration
belief/relationship/identity mutation
M3 nomination or write
Action Gate
Tool Receipt or tool execution
P1-003 runtime assignment
P1-003 runtime activation
Phase 2 NPG-COMP-v0.1 implementation (authorized, not yet started)
Non-Projection runtime activation
P1-004 assignment
backend/plugin discovery
backend selection or migration
production deployment
```

---

## 11. 🎭 Character / independent-review boundary

```text
CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
```

Issue #39 remains open as the future genuine independent/team-review transition
trigger and is not a current solo-maintainer blocker.

---

## 12. 🔄 Status rules

| Event | Status result |
|---|---|
| Research captured | no runtime status change |
| Readiness model frozen | `READINESS_READY · FROZEN_DOCS` only |
| Candidate selected | docs-only candidate status; no code authority |
| Implementation contract frozen | `FROZEN_DOCS`; still no Owner GO |
| Bounded Owner GO merged | `AUTHORIZED_BOUNDED` |
| Code PR merged + green main CI | `IMPLEMENTED_BOUNDED` |
| Owner GO used by verified implementation | `OWNER_GO_CONSUMED` |
| Runtime assignment/activation proposal | new independent authorization cycle required |
| Action/retrieval/tool/deployment proposal | new independent authorization cycle required |

GitHub `main` and `docs/CURRENT_STATUS.md` remain authoritative. Notion is a
derived status/navigation surface synchronized only from verified evidence.

---

## 13. 🚪 Required next authority ladder

The NPG-v0.1 classifier cycle is complete. Phase 1 runtime-composition readiness
and `NPG-COMP-v0.1` contract freeze are complete, and PR #94 granted the one-time
`NPG-COMP-v0.1_ONLY` Phase 2 implementation authorization.

```text
CURRENT = NPG-COMP-v0.1 FROZEN_DOCS · OWNER_GO GRANTED · IMPLEMENTATION NOT_STARTED
→ fresh exact-main compatibility check
→ separate clean bounded implementation branch
→ exact reserved three-file shadow package only
→ executable NRC-T01…T12 + NRC-M01…M10 validation
→ exact-head review and CI
→ protected merge
→ green resulting-main CI
→ completion/status reconciliation
→ Notion sync
→ Owner GO consumed
→ STOP
```

No runtime activation, retrieval, Action Gate, tool, identity/relationship, M3,
persistence or deployment step is authorized by completing this ladder.

---

## 14. 🏁 Formula

```text
P0 complete
→ P1-001 implemented bounded
→ P1-002 implemented bounded
→ cross-gate binding/readiness frozen
→ P1-003 candidate selected
→ P1-003 contract frozen
→ P1-003 Owner GO authorized and reconciled
→ P1-003 Pure Governed Constraint Composer implemented bounded
→ P1-003 Owner GO consumed
→ post-P1-003 Non-Projection readiness selected
→ Non-Projection Gate Contract Readiness READY · FROZEN_DOCS
→ PURE_NON_PROJECTION_CLASSIFIER selected
→ NPG-v0.1 implementation contract FROZEN_DOCS
→ NPG-v0.1 Owner GO consumed by PR #90
→ NPG-v0.1 Pure Classifier IMPLEMENTED_BOUNDED
→ Phase 0 NPG status reconciliation COMPLETE
→ Phase 1 NPG runtime-composition readiness READY
→ NPG-COMP-v0.1 contract FROZEN_DOCS
→ Phase 2 NPG-COMP-v0.1 Owner GO GRANTED by PR #94
→ NEXT: separate bounded NPG-COMP-v0.1 shadow implementation

PHASE_2_IMPLEMENTATION = NOT_STARTED
PHASE_2_OWNER_GO = GRANTED · NPG-COMP-v0.1_ONLY · SINGLE_USE
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
P1_004 = NOT_ASSIGNED
ACTION_GATE = NOT_AUTHORIZED
RETRIEVAL_EXECUTION = NOT_AUTHORIZED
TOOL_EXECUTION = NOT_AUTHORIZED
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
RUNTIME_DEPLOYMENT = NOT_AUTHORIZED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```

### Related

- [`NON_PROJECTION_GATE_CONTRACT_READINESS.md`](NON_PROJECTION_GATE_CONTRACT_READINESS.md)
- [`NON_PROJECTION_GATE_CANDIDATE_SELECTION.md`](NON_PROJECTION_GATE_CANDIDATE_SELECTION.md)
- [`NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md`](NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md)
- [`../NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md`](../NON_PROJECTION_IMPLEMENTATION_AUTHORIZATION.md)
- [`NON_PROJECTION_RUNTIME_COMPOSITION_READINESS.md`](NON_PROJECTION_RUNTIME_COMPOSITION_READINESS.md)
- [`NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT_V0_1.md`](NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT_V0_1.md)
- [`NON_PROJECTION_RUNTIME_COMPOSITION_OWNER_GO_DECISION.md`](NON_PROJECTION_RUNTIME_COMPOSITION_OWNER_GO_DECISION.md)
- [`POST_P1_003_MILESTONE_SELECTION.md`](POST_P1_003_MILESTONE_SELECTION.md)
- [`../P1_003_IMPLEMENTATION_AUTHORIZATION.md`](../P1_003_IMPLEMENTATION_AUTHORIZATION.md)
- [`P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`](P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md)
- [`P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md`](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md)
- [`CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md)
- [`POST_P1_002_MILESTONE_SELECTION.md`](POST_P1_002_MILESTONE_SELECTION.md)
- [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)
