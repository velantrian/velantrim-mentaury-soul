# 🗺️ Post-P0 Roadmap

```text
Status:                       ADOPTED ROADMAP · DOCS_ONLY
Version:                      1.0
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
P1-003 assignment:             NONE
P1-003 contract:               NOT FROZEN
P1-003 Owner GO:               NOT GRANTED
Next bounded work:             P1_003_PURE_COMPOSER_CONTRACT_FREEZE · DOCS_ONLY
Next runtime milestone:       NOT SELECTED · NOT AUTHORIZED
Implementation authorization: NONE
Runtime deployment authority: NONE
Mutation authority:           NONE
Retrieval authority:          NONE
Direct or indirect M3 write:  FORBIDDEN
NO_POST_P1_001_RUNTIME_MILESTONE_AUTHORIZED
NO_POST_P1_002_RUNTIME_MILESTONE_AUTHORIZED
DOMAIN_RUNTIME_NOT_AUTHORIZED
```

```text
IMPLEMENTED_BOUNDED ≠ remediation execution
ALLOW_REFERENCE ≠ retrieval permission
positive classifier results ≠ common-bound authorization
ELIGIBLE_FOR_NEXT_GATE ≠ execution permission
readiness contract ≠ implementation GO
candidate selected ≠ P1-003 assigned
contract freeze ≠ Owner GO
P1-003 NOT_ASSIGNED ≠ missing work
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
```

Frozen contract: [`MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md`](MENTAURY_CAPABILITY_LEASE_RESOLUTION_NOTES.md).
Owning receipt: [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md).

P1-001 remains a pure capability classifier without registry persistence,
Action Gate, tool execution, identity/M3 mutation or deployment authority.
No registry service, Action Gate, P1-002 remediation execution or tool runtime
follows automatically from P1-001.

---

## 2. ✅ Completed P1-002 Privacy Reconciliation Classifier sequence

```text
P0-010 active-store redaction boundary
→ privacy copy-reconciliation gap identified
→ P1-002 contract frozen in PR #65
→ bounded Owner GO merged in PR #66
→ pure classifier implemented in PR #67
→ exact-head correctness and adversarial review passed
→ resulting main CI passed
→ P1-002 IMPLEMENTED_BOUNDED
```

### Contract freeze

```text
Reviewed head:   85bf0070e2f15b5ca752b82325337d6ef0190396
Exact-head CI:   31331396018 · success · 401 passed
Merge:           1dc7bcf97986f455f48beb121c2048dfc34bd11c
Post-merge CI:   31331506606 · success
```

### Authorization

```text
Reviewed head:   670b10c7ea69e3c609453e979a8de6853b23c6bc
Exact-head CI:   31331910395 · success · 398 passed
Merge:           8f4c444e2144d1dffde20fc60d6d5250148d07e6
Post-merge CI:   31331973557 · success
```

### Implementation

```text
Reviewed head:   74662fb626a545ed63b426e98aa03524449019db
Exact-head CI:   31332728486 · success · 461 passed
Merge:           d64679fd745e859527a70746df5e69dc9aca0408
Post-merge CI:   31332793742 · success · 461 passed
Correctness:     PASS
Adversarial:     PASS
Review threads:  0
```

Owning surfaces:

- [Frozen contract](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [Authorization and completion receipt](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [Current status](../CURRENT_STATUS.md)

---

## 3. 🧱 Implemented P1-002 boundary

The pure classifier accepts caller-supplied material, copy, access intent and
budget records. It returns exactly one classification:

```text
ALLOW_REFERENCE
DENY_RETRIEVAL
QUARANTINE_REQUIRED
REBUILD_REQUIRED
```

Implemented guarantees:

- strict typed-or-exact-mapping admission;
- immutable contracts and canonical sorted/unique collections;
- exact cross-record linkage;
- future-revision rejection;
- canonical byte-budget over all four inputs;
- fixed budget validation order;
- exact purpose and branch allowlists;
- empty allowlists grant nothing;
- normative first-match precedence;
- surface-specific fail-closed classification;
- minimal two-field result without permission material;
- all `PRIV-SC-001…PRIV-SC-015` frozen scenarios;
- no ambient I/O or clock access at import.

---

## 4. 🛡️ P1 adversarial corrections retained

Before P1-002 merge, review found and fixed:

1. an implicit-wildcard interpretation of empty allowlists;
2. manually constructible impossible decision/reason pairs;
3. raw canonical JSON exceptions crossing the contract boundary;
4. nondeterministic multi-budget validation order;
5. byte-budget accounting that initially excluded the budget record.

P1-001 retains its own exact-live-head, canonical-digest, lifecycle and immutable
snapshot checks from its bounded implementation review.

---

## 5. 🚫 Work not included

```text
privacy registry persistence
backup/fork discovery or scanning
content inspection
content deletion or P0 redaction execution
quarantine execution
index/embedding/graph/cache/summary rebuilding
retrieval execution
network, filesystem or database access
ambient clock or environment authority
event append or replay/projection integration
belief, relationship or identity mutation
M3 nomination or write
Capability Lease invocation from P1-002
Action Gate
Tool Receipt or tool execution
backend selection or migration
production deployment
```

---

## 6. ✅ Cross-gate binding/composition readiness

The post-P1-002 selection first demonstrated a structural composition gap:

- P1-001 `ResolutionResult` does not carry the evaluated `ActionIntent` binding;
- P1-002 `PrivacyReconciliationResult` contains only `decision` and `reason`;
- bare positive results therefore cannot prove common request, purpose, scope,
  branch or freshness.

The docs-only readiness contract now freezes the safe architecture:

[`CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md)

```text
one immutable canonical evaluation context
→ exact common purpose / operation / scope / side-effect / branch binding
→ original source inputs projected into existing pure P1 gates
→ same-attempt evaluation
→ verified lease revision/digest + privacy policy revisions
→ explicit gate/canonical/binding versions
→ coordinator-computed canonical fingerprints
→ at most ELIGIBLE_FOR_NEXT_GATE
```

Architectural decisions:

```text
CROSS_GATE_BINDING_READINESS = READY
STRATEGY_A_PURE_COORDINATOR  = SELECTED
STRATEGY_B_EVIDENCE_ENVELOPE = DERIVED_EVIDENCE_ONLY
STRATEGY_C_BARE_RESULTS       = REJECTED
CALLER_SUPPLIED_DIGEST        = NOT_AUTHORITY
FRESHNESS                     = SAME_ATTEMPT + REVISION_BOUND
```

The existing frozen P1-001/P1-002 contracts do not need modification to make
this architecture coherent. A future coordinator can retain and canonicalize
the original admitted source values while leaving both result shapes unchanged.

---

## 7. ✅ P1-003 candidate selection

The candidate-selection decision is frozen in:

[`P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md`](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md)

```text
P1_003_CANDIDATE_SELECTION = SELECTED
P1_003_CANDIDATE           = PURE_GOVERNED_CONSTRAINT_COMPOSER
P1_003_RUNTIME_ASSIGNMENT  = NOT_ASSIGNED
P1_003_CONTRACT            = NOT_FROZEN
P1_003_OWNER_GO            = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NONE
```

Why this candidate is selected:

- the cross-gate binding blocker is resolved at the architecture level;
- one immutable explicit-input coordinator can reuse the existing pure P1 gates;
- bare-result composition remains rejected;
- modifying the frozen P1 result shapes is unnecessary;
- an evidence envelope is useful only as derived evidence, not authority;
- Action Gate, retrieval, remediation and persistence are broader and are not
  the next bounded problem.

The candidate is not yet a runtime milestone. Candidate selection is only a
docs-level narrowing of the future design space.

---

## 8. ⛔ Authorization gate and next bounded work

The promotion sequence is:

```text
CANDIDATE_SELECTED_DOCS_ONLY
→ P1_003_CONTRACT_FROZEN_DOCS_ONLY
→ explicit separate P1_003_OWNER_GO_AUTHORIZED_BOUNDED
→ clean Tier A implementation PR
→ IMPLEMENTED_BOUNDED
```

Current state remains at the first line only.

The next bounded work is selected as:

```text
NEXT_BOUNDED_WORK = P1_003_PURE_COMPOSER_CONTRACT_FREEZE
MODE              = DOCS_ONLY
IMPLEMENTATION    = NOT_AUTHORIZED
OWNER_GO          = NOT_GRANTED
```

Before any code authorization, that later contract-freeze block must define the
exact runtime context schema, public API/package boundary, canonical projections,
fingerprint domains, source-provenance boundary, result/reason contract,
freshness/invalidation rules, T1–T12 executable adversarial mappings, M1–M10
executable metamorphic mappings, no-hidden-I/O proof strategy, malformed-input
semantics and exact implementation acceptance criteria.

The contract freeze itself still will not authorize code. A separate explicit
Owner GO is required after the contract is frozen and reviewed.

```text
Capability ALLOW
+ Privacy ALLOW_REFERENCE
+ cross-gate ELIGIBLE_FOR_NEXT_GATE
≠ Action Gate PASS
≠ retrieval permission
≠ tool/action permission
```

---

## 9. 🎭 Character / independent-review boundary

```text
CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION
```

P1-003 candidate selection adds no Character evidence and does not alter issue
#39. The repository remains in honest `SOLO_MAINTAINER` mode. Historical review
labels do not create current independent-human assurance.

---

## 10. 🔄 Status rules

| Event | Status result |
|---|---|
| Research captured | no runtime status change |
| Readiness/selection decision merged | may freeze docs-only architecture; no implementation authority |
| Candidate selected | design space narrowed; P1-003 remains unassigned |
| Contract frozen | `FROZEN_DOCS`; still no implementation authority |
| Bounded Owner GO merged | `AUTHORIZED_BOUNDED` |
| Code PR merged + green main CI | `IMPLEMENTED_BOUNDED` |
| Remediation/retrieval proposal | new independent authorization cycle required |

GitHub `main` and `docs/CURRENT_STATUS.md` remain authoritative. Notion is a
derived navigation/status surface synchronized only after verified evidence.

---

## 11. 🏁 Formula

```text
P0 complete
→ P1-001 implemented bounded
→ P1-002 implemented bounded
→ post-P1-002 selection demonstrated common-binding gap
→ cross-gate binding/readiness contract frozen docs-only
→ pure coordinator over verified source inputs selected architecturally
→ bare-result composition rejected
→ ELIGIBLE_FOR_NEXT_GATE limited to non-execution readiness
→ Pure Governed Constraint Composer selected as sole P1-003 candidate
→ next bounded work = docs-only P1-003 contract freeze
→ STOP before P1-003 assignment / Owner GO / implementation
```

### Related

- [`P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md`](P1_003_CANDIDATE_SELECTION_AND_AUTHORIZATION_BOUNDARY.md)
- [`CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md`](CROSS_GATE_BINDING_AND_COMPOSITION_READINESS.md)
- [`POST_P1_002_MILESTONE_SELECTION.md`](POST_P1_002_MILESTONE_SELECTION.md)
- [`P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md`](P1_002_PRIVACY_RECONCILIATION_CLASSIFIER_NOTES.md)
- [`../P1_002_IMPLEMENTATION_AUTHORIZATION.md`](../P1_002_IMPLEMENTATION_AUTHORIZATION.md)
- [`../P1_001_IMPLEMENTATION_AUTHORIZATION.md`](../P1_001_IMPLEMENTATION_AUTHORIZATION.md)
- [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md)
- [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md)
- [`../GOVERNANCE.md`](../GOVERNANCE.md)
