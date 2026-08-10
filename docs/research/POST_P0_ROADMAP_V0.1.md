# 🗺️ Post-P0 Roadmap

```text
Status:                       ADOPTED ROADMAP · DOCS_ONLY
Version:                      1.2
Updated:                      2026-08-10
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
Next runtime milestone:        NOT_SELECTED · NOT_AUTHORIZED
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
ALLOW_REFERENCE ≠ retrieval permission
ELIGIBLE_FOR_NEXT_GATE ≠ execution permission
P1-003 completion ≠ Action Gate authority
P1-003 completion ≠ retrieval/tool authority
P1-003 completion ≠ runtime assignment
P1-003 completion ≠ deployment authority
Solo review ≠ independent certification
```

The filename retains `V0.1` for stable historical links. Document metadata is
the current version authority.

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

## 8. 🚫 Work not included

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
backend/plugin discovery
backend selection or migration
production deployment
```

---

## 9. 🎭 Character / independent-review boundary

```text
CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
```

Issue #39 remains open as the future genuine independent/team-review transition
trigger and is not a current solo-maintainer blocker.

---

## 10. 🔄 Status rules

| Event | Status result |
|---|---|
| Research captured | no runtime status change |
| Contract frozen | `FROZEN_DOCS` |
| Bounded Owner GO merged | `AUTHORIZED_BOUNDED` |
| Code PR merged + green main CI | `IMPLEMENTED_BOUNDED` |
| Owner GO used by verified implementation | `OWNER_GO_CONSUMED` |
| Runtime assignment/activation proposal | new independent authorization cycle required |
| Action/retrieval/tool/deployment proposal | new independent authorization cycle required |

GitHub `main` and `docs/CURRENT_STATUS.md` remain authoritative. Notion is a
derived status/navigation surface synchronized only from verified evidence.

---

## 11. 🏁 Formula

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
→ STOP

P1_003_RUNTIME_ASSIGNMENT = NOT_ASSIGNED
NO_POST_P1_003_RUNTIME_MILESTONE_AUTHORIZED
```

### Related

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
