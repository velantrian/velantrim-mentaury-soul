# 🚦 Mentaury Soul — Current Status

```text
Status date:                       2026-08-10
Repository:                        velantrian/velantrim-mentaury-soul
Engineering authority:             this file + verified live GitHub state
Governance authority:              docs/GOVERNANCE.md + live GitHub ruleset
Current operating mode:            SOLO_MAINTAINER
Independent human review claimed:  NO
Live main tip:                      resolved from GitHub; not embedded here
```

```text
IMPLEMENTED_BOUNDED
= exact authorized subsystem merged and retained by validation
≠ broader runtime authority
≠ remediation or action authority
≠ deployment authority
```

---

## 1. 🧭 Current checkpoint

```text
CANON_V0.1_FROZEN
P0-001…P0-015_IMPLEMENTED_IN_MAIN
PERMANENT_GITHUB_ACTIONS_PRESENT_AND_VALIDATED
SOLO_MAINTAINER_GOVERNANCE_ACTIVE
TIER_A_TWO_PASS_MAINTAINER_REVIEW_REQUIRED
INDEPENDENT_HUMAN_REVIEW_NOT_CLAIMED

P1_001_CAPABILITY_LEASE_RESOLUTION_IMPLEMENTED_BOUNDED
P1_001_PURE_RESOLVER_VALIDATED
P1_001_OWNER_GO_CONSUMED
P1_001_REGISTRY_PERSISTENCE_NOT_IMPLEMENTED
P1_001_REGISTRY_SERVICE_NOT_IMPLEMENTED
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED

P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_IMPLEMENTED_BOUNDED
P1_002_PURE_CLASSIFIER_VALIDATED
P1_002_OWNER_GO_CONSUMED
P1_002_MUTATION_AUTHORITY_NONE
P1_002_RETRIEVAL_AUTHORITY_NONE
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED

POST_P1_002_SELECTION_COMPLETE
CROSS_GATE_BINDING_AND_COMPOSITION_READINESS_FROZEN_DOCS
CROSS_GATE_BINDING_READINESS_READY
SELECTED_BINDING_STRATEGY_PURE_COORDINATOR_OVER_VERIFIED_SOURCE_INPUTS
BARE_RESULT_COMPOSITION_REJECTED
POSITIVE_READINESS_ELIGIBLE_FOR_NEXT_GATE_ONLY

P1_003_CANDIDATE_SELECTION_COMPLETE
P1_003_CANDIDATE_PURE_GOVERNED_CONSTRAINT_COMPOSER
P1_003_CONTRACT_FROZEN_DOCS
P1_003_EXACT_CONTEXT_API_FINGERPRINT_RESULT_CONTRACT_FROZEN
P1_003_T1_T12_AND_M1_M10_EXECUTABLE_REQUIREMENTS_FROZEN
P1_003_NO_HIDDEN_IO_PROOF_REQUIREMENT_FROZEN
P1_003_OWNER_GO_NOT_GRANTED
P1_003_NOT_ASSIGNED
NEXT_REQUIRED_DECISION_EXPLICIT_P1_003_OWNER_GO
NO_RUNTIME_MILESTONE_SELECTED
IMPLEMENTATION_AUTHORIZATION_NONE

ACTION_GATE_NOT_AUTHORIZED
RETRIEVAL_EXECUTION_NOT_AUTHORIZED
TOOL_EXECUTION_NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE_FORBIDDEN
DOMAIN_RUNTIME_NOT_AUTHORIZED
RUNTIME_DEPLOYMENT_NOT_AUTHORIZED
```

---

## 2. ✅ Milestone table

| Milestone | State | Verified boundary |
|---|---|---|
| P0-001…P0-013 | ✅ Implemented | integrity, storage and deterministic replay foundation |
| P0-014 | ✅ Implemented | minimal evidence-referenced belief lifecycle |
| P0-015 | ✅ Implemented | deterministic Evidence Gate |
| P1-001 | ✅ Implemented bounded | pure Capability Lease classification only |
| P1-002 | ✅ Implemented bounded | pure Privacy Reconciliation classification only |
| Post-P1-002 selection | ✅ Docs-only decision | no runtime milestone selected; cross-gate binding/composition readiness selected |
| Cross-gate binding/composition readiness | ✅ Frozen docs-only | common binding/freshness contract ready; runtime still not authorized |
| P1-003 candidate selection | ✅ Frozen docs-only | Pure Governed Constraint Composer selected as candidate; P1-003 still not assigned; no Owner GO |
| P1-003 pure composer contract | ✅ Frozen docs-only | exact context/API/fingerprint/result/threat/metamorphic/purity contract frozen; Owner GO still absent |

---

## 3. 🔐 P1-001 retained evidence

```text
Authorization PR:       #62
Authorization merge:    d5e9e2fb11ea5a9c123c1cb1cc2b6f16dac53b98
Authorization main CI:  31322210843 · success
Implementation PR:      #63
Reviewed head:          e873e43331fa7273b92f896b371707e4779b17d4
Exact-head CI:          31323051934 · success · 387 passed
Implementation merge:   f21809d8f31a457bd7acfe1d766230973ba9ecf5
Post-merge CI:          31323138053 · success
```

P1-001 remains a pure caller-supplied resolver. `ALLOW` executes nothing and
contains no reusable capability material.

Implemented P1-001 slice:

```text
src/mentaury/capabilities/__init__.py
src/mentaury/capabilities/lease/__init__.py
src/mentaury/capabilities/lease/contracts.py
src/mentaury/capabilities/lease/resolver.py
tests/test_capability_lease_resolution.py
```

---

## 4. 🔐 P1-002 Privacy Reconciliation Classifier — verified evidence

### Contract freeze

```text
Contract PR:            #65
Reviewed head:          85bf0070e2f15b5ca752b82325337d6ef0190396
Exact-head CI:          31331396018 · success · 401 passed
Contract merge:         1dc7bcf97986f455f48beb121c2048dfc34bd11c
Post-merge CI:          31331506606 · success
```

### Bounded authorization

```text
Authorization PR:       #66
Reviewed head:          670b10c7ea69e3c609453e979a8de6853b23c6bc
Exact-head CI:          31331910395 · success · 398 passed
Authorization merge:    8f4c444e2144d1dffde20fc60d6d5250148d07e6
Post-merge CI:          31331973557 · success
```

### Implementation

```text
Implementation PR:      #67
Reviewed head:          74662fb626a545ed63b426e98aa03524449019db
Exact-head CI:          31332728486 · success · 461 passed
Implementation merge:   d64679fd745e859527a70746df5e69dc9aca0408
Post-merge CI:          31332793742 · success · 461 passed
Correctness pass:       PASS
Adversarial pass:       PASS
Review threads:         0
Independent assurance:  NOT CLAIMED
```

Historical checkpoint preserved as provenance only; it is superseded by the
implemented-bounded evidence above and is not current authority:

```text
P1_002_OWNER_GO_AUTHORIZED_BOUNDED
P1_002_IMPLEMENTATION_NOT_STARTED
```

---

## 5. ✅ Implemented P1-002 slice

```text
src/mentaury/privacy/__init__.py
src/mentaury/privacy/reconciliation/__init__.py
src/mentaury/privacy/reconciliation/contracts.py
src/mentaury/privacy/reconciliation/classifier.py
tests/test_privacy_reconciliation_classifier.py
```

Inputs are caller supplied:

```text
PrivacyMaterial
PrivacyCopy
PrivacyAccessIntent
PrivacyReconciliationBudget
```

Output is one minimal two-field `PrivacyReconciliationResult`:

```text
ALLOW_REFERENCE
DENY_RETRIEVAL
QUARANTINE_REQUIRED
REBUILD_REQUIRED
```

Implemented behavior:

- immutable typed contracts and strict exact-field mapping admission;
- canonical sorted and unique purpose/branch collections;
- deterministic linkage and future-revision validation;
- canonical byte-budget over material, copy, intent and budget;
- deterministic purpose and branch collection budgets;
- exact first-match precedence;
- surface-specific fail-closed classification;
- all frozen `PRIV-SC-001…PRIV-SC-015` scenarios;
- typed/mapping equivalence and repeatability;
- fresh-process import with ambient I/O and clock calls blocked.

`ALLOW_REFERENCE` is observation/classification data. It is not permission to
retrieve and contains no token, credential, capability or mutation instruction.

---

## 6. 🛡️ Adversarial findings resolved before P1-002 merge

The implementation review found and fixed:

1. empty purpose/branch allowlists initially risked being interpreted as
   wildcard authority for public material; final behavior grants nothing unless
   purpose and branch are explicitly listed;
2. the result type initially allowed impossible decision/reason pairs; final
   contracts reject fixed-reason mismatches and prevent
   `INPUT_CONTRACT_VIOLATION` from becoming a result;
3. canonical JSON failures are normalized to `PrivacyContractError`;
4. budget-field validation order is fixed and canonical byte-budget includes
   all four caller-supplied inputs.

---

## 7. 🚫 Explicitly not implemented or authorized

```text
privacy registry persistence
backup or fork discovery/scanning
content inspection
content deletion or P0 redaction execution
quarantine execution
index, embedding, graph, cache or summary rebuilding
retrieval execution
network, filesystem or database access
ambient clock or environment authority
event append or replay/projection integration
belief, relationship or identity mutation
M3 nomination or write
Capability Lease invocation from P1-002
Action Gate
Tool Receipt runtime
tool execution
backend selection or migration
production deployment
objective-truth authority
consciousness or subjective-experience claims
```

---

## 8. 🔗 Cross-gate binding/composition readiness

The docs-only readiness contract is frozen in:

`docs/research/CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`

The confirmed source-level problem remains:

```text
P1-001 ResolutionResult
→ does not retain the evaluated ActionIntent binding

P1-002 PrivacyReconciliationResult
→ contains only decision + reason

bare positive result A + bare positive result B
→ cannot prove common request/context/freshness
```

The selected safe architecture is:

```text
one immutable canonical evaluation context
→ project original source inputs into P1-001 and P1-002
→ invoke both existing pure classifiers in the same evaluation attempt
→ verify common request/purpose/operation/scope/side-effect/branch binding
→ bind lease and privacy revisions + contract versions + canonical profile
→ emit at most ELIGIBLE_FOR_NEXT_GATE
```

A caller-supplied digest is not authority evidence. Any future fingerprint must
be recomputed from versioned admitted canonical values. A derived evidence
envelope may support audit, but a caller-asserted wrapper around bare results is
not a valid composition input.

Freshness is same-attempt and revision-bound. No durable authorization token or
arbitrary TTL is created. Any authority/freshness mutation requires a new full
evaluation attempt.

```text
CROSS_GATE_BINDING_READINESS = READY
RUNTIME_IMPLEMENTATION       = NOT_AUTHORIZED
P1_003                       = NOT_ASSIGNED
IMPLEMENTATION_AUTHORIZATION = NONE
```

---

## 9. 🧩 P1-003 candidate and frozen contract

Candidate selection remains frozen in:

`docs/research/P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md`

The exact implementation contract is now frozen in:

`docs/research/P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`

```text
P1_003_CANDIDATE_SELECTION = SELECTED
P1_003_CANDIDATE           = PURE_GOVERNED_CONSTRAINT_COMPOSER
P1_003_RUNTIME_ASSIGNMENT  = NOT_ASSIGNED
P1_003_CONTRACT            = FROZEN_DOCS
P1_003_OWNER_GO            = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NONE
```

The frozen contract defines:

- exact `CrossGateEvaluationContext` and `CompositionBudget` schemas;
- the only public API `compose_governed_constraints(*, context=...)`;
- exact projections into the existing P1-001/P1-002 gates;
- fixed version/domain constants and `MENTAURY_CANONICAL_JSON_V1` reuse;
- common-request and targeted evaluation-evidence SHA-256 fingerprints;
- exact three-state result contract and primary reason taxonomy;
- exact P1 outcome → positive/blocker/defer mapping and precedence;
- same-attempt freshness/invalidation;
- executable T1–T12 and M1–M10 requirements;
- mandatory `CGC-*` implementation test matrix;
- no-hidden-I/O/import/call proof strategy;
- explicit non-goals and implementation acceptance criteria.

The API explicitly forbids bare-result composition and caller-supplied digests.
The source-provenance scope remains `CALLER_SUPPLIED_VALUE_EVIDENCE_ONLY`; a pure
composer does not claim external source authenticity.

The promotion ladder is now:

```text
CANDIDATE_SELECTED_DOCS_ONLY
→ P1_003_CONTRACT_FROZEN_DOCS_ONLY   ← current
→ explicit separate P1_003_OWNER_GO_AUTHORIZED_BOUNDED
→ clean Tier A implementation PR
→ IMPLEMENTED_BOUNDED only after exact-head + resulting-main evidence
```

The next possible step is not implementation. It is a separate Owner GO
decision against the frozen contract:

```text
NEXT_REQUIRED_DECISION = EXPLICIT_P1_003_OWNER_GO
IMPLEMENTATION         = NOT_AUTHORIZED
OWNER_GO               = NOT_GRANTED
```

---

## 10. 🧱 Action Gate / retrieval boundary

```text
Capability ALLOW
+ Privacy ALLOW_REFERENCE
+ ELIGIBLE_FOR_NEXT_GATE
≠ Action Gate PASS
```

A complete Action Gate may include constitutional,
relationship/commitment, side-effect and other authority layers. The P1-003
contract does not implement or collapse them.

Likewise:

```text
ALLOW_REFERENCE ≠ retrieval permission
ELIGIBLE_FOR_NEXT_GATE ≠ retrieval permission
```

No deletion, quarantine, rebuild, retrieval, relationship, identity, Action
Gate, tool or deployment work follows automatically.

---

## 11. 🎭 Character / identity boundary

```text
CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION
```

No Character validation, identity/relationship runtime, Genesis Heritage runtime,
Human Paths Atlas runtime or direct/indirect M3 write is created by cross-gate
readiness, P1-003 candidate selection or the P1-003 contract freeze.

Issue #39 remains the future transition trigger for genuine independent/team
review and is not a current solo-mode blocker.

---

## 12. 🛡️ Governance state

The live solo ruleset retains mandatory PRs, exact required CI, up-to-date
branches, resolved conversations, deletion/force-push protection and empty
bypass. Required approvals remain `0` while no genuine independent reviewer
exists.

Tier A docs that affect authority/readiness require the same exact-head,
correctness, adversarial and resulting-main evidence discipline as other Tier A
work.

---

## 13. 🔗 Authoritative navigation

- Canon: `docs/MENTAURY_CANON_V0.1.md`
- Governance: `docs/GOVERNANCE.md`
- P1-001 receipt: `docs/P1_001_IMPLEMENTATION_AUTHORIZATION.md`
- P1-002 receipt: `docs/P1_002_IMPLEMENTATION_AUTHORIZATION.md`
- P1-002 contract: `docs/research/P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`
- Post-P1-002 selection: `docs/research/POST_P1_002_MILESTONE_SELECTION.md`
- Cross-gate readiness: `docs/research/CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`
- P1-003 candidate selection: `docs/research/P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md`
- P1-003 frozen composer contract: `docs/research/P1_003_PURE_GOVERNED_CONSTRAINT_COMPOSER_CONTRACT.md`
- Roadmap: `docs/research/POST_P0_ROADMAP_V0.1.md`
- Research Index: `docs/research/RESEARCH_INDEX.md`
- Environment: `docs/ENVIRONMENT_MANIFEST.md`

---

## 14. 🏁 Current formula

```text
P0 foundation implemented
+ P1-001 pure capability resolver implemented bounded
+ P1-002 pure privacy classifier implemented bounded
+ post-P1-002 selection completed
+ cross-gate binding/composition readiness frozen docs-only
+ pure coordinator strategy selected architecturally
+ bare-result composition rejected
+ ELIGIBLE_FOR_NEXT_GATE limited to next-gate readiness
+ Pure Governed Constraint Composer selected as P1-003 candidate docs-only
+ exact P1-003 composer contract frozen docs-only
+ P1-003 remains unassigned; Owner GO not granted
+ permanent CI
+ active solo governance

≠ runtime composition authorization
≠ P1-003 runtime assignment
≠ Owner GO
≠ remediation or retrieval runtime
≠ Action Gate or tools
≠ identity or M3 mutation
≠ domain runtime or deployment
≠ independent human assurance
```
