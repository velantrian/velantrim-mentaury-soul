# 🪞 Non-Projection Gate — Candidate Selection & Authorization Boundary

```text
Status:                              FROZEN_DOCS · DOCS_ONLY · CANDIDATE_SELECTION
Version:                             0.1
Date:                                2026-08-10
Review tier:                         TIER_A
Owning readiness:                    NON_PROJECTION_GATE_CONTRACT_READINESS.md
Candidate selection:                 SELECTED
Selected candidate:                  PURE_NON_PROJECTION_CLASSIFIER
P1-004 assignment:                   NOT_ASSIGNED
Implementation contract:             NOT_FROZEN
Non-Projection Owner GO:             NOT_GRANTED
Implementation authorization:        NONE
Runtime implementation:              NOT_AUTHORIZED
Runtime activation:                  NOT_AUTHORIZED
Action Gate authority:               NONE
Retrieval authority:                 NONE
Tool authority:                      NONE
Identity authority:                  NONE
Relationship authority:              NONE
Direct or indirect M3 write:         FORBIDDEN
Deployment authority:                NONE
```

> **CANDIDATE SELECTED ≠ P1-004 ASSIGNED.**
>
> **THIS DOCUMENT DOES NOT AUTHORIZE IMPLEMENTATION.**
>
> It selects one bounded future contract candidate only. It does not freeze a
> runtime API, package path, concrete schema, implementation test IDs, Owner GO,
> runtime assignment, retrieval, persistence, model invocation, Action Gate,
> identity/relationship authority, M3 mutation or deployment.

---

## 1. 🎯 Bounded decision

The verified readiness block established a docs-only provenance and attribution
model, fail-closed outcome vocabulary, projection threat taxonomy, adversarial
scenarios and metamorphic properties.

The remaining bounded question is whether one concrete implementation candidate
is sufficiently narrow and coherent to justify a later **separate implementation-
contract freeze** without granting code authority now.

The decision is:

```text
NON_PROJECTION_CANDIDATE_SELECTION = SELECTED
NON_PROJECTION_CANDIDATE           = PURE_NON_PROJECTION_CLASSIFIER
P1_004                              = NOT_ASSIGNED
IMPLEMENTATION_CONTRACT            = NOT_FROZEN
NON_PROJECTION_OWNER_GO            = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION       = NONE
```

The candidate is a **pure deterministic classifier over explicit caller-supplied
Attributed Interpretation Envelope values**. It evaluates only the bounded
projection question and returns only the frozen readiness classification family.

Its strongest positive semantic remains:

```text
PASS_ATTRIBUTED
```

`PASS_ATTRIBUTED` means at most that no bounded projection blocker was found for
the exact admitted attributed interpretation. It is not truth, identity,
relationship, consent, capability, action, retrieval, tool or deployment
authority.

---

## 2. ✅ Why this candidate is coherent now

PR #82 completed the prerequisite readiness architecture:

- `ATTRIBUTED_INTERPRETATION_ENVELOPE` keeps provenance, speaker/subject,
  claim class, interpretation, context, reviewer correlation and scope distinct;
- imported material is fail-closed as `NON_SELF` or `UNKNOWN` absent separately
  authorized branch-bound identity/continuation evidence;
- claim classes distinguish factual, causal, predictive, normative, value,
  autobiographical, relationship, consent, interpretive and metaphorical claims;
- unknown/conflicting provenance cannot silently become positive;
- reviewer correlation cannot be laundered into independent convergence;
- result vocabulary is bounded to `PASS_ATTRIBUTED`, `REVISE_REQUIRED`,
  `CONTESTED`, `DEFER`, `REJECT`;
- precedence is frozen as `REJECT > DEFER > CONTESTED > REVISE_REQUIRED > PASS_ATTRIBUTED`;
- NPG-T01…NPG-T12, NPG-SC-001…NPG-SC-012 and MT-NPG-001…MT-NPG-008 define
  the minimum later executable safety envelope;
- Character Policy cannot override the classification;
- P1-001, P1-002, P1-003 and Canon v0.1 remain unchanged.

These properties are sufficient to select a narrow pure classifier candidate
without selecting retrieval, persistence, identity runtime or Action Gate.

---

## 3. 🧱 Selected candidate boundary

A later implementation contract may choose exact types and package paths, but it
must remain semantically equivalent to this pure shape:

```text
explicit immutable attributed interpretation values
→ deterministic admission / validation
→ provenance and attribution checks
→ claim-class and context/scope checks
→ reviewer-correlation checks
→ projection-threat evaluation
→ fail-closed precedence
→ bounded classification + bounded reasons/evidence
```

Required candidate properties:

- explicit caller-supplied bounded values only;
- deterministic classification for identical admitted values and contract version;
- no ambient clock or environment authority;
- no filesystem, database, graph or vector-store access;
- no network access;
- no Atlas lookup or retrieval;
- no identity-registry or relationship-registry lookup;
- no model/LLM call;
- no persistence or event append;
- no M2/M3 write or promotion;
- no capability or Action Gate invocation;
- no tool execution;
- no Character override of evidence or result;
- no backend selection or deployment;
- no authority amplification from `PASS_ATTRIBUTED`.

The candidate classifies the envelope it is given. It does not discover or fetch
source material and does not decide whether content should be executed, stored,
retrieved, believed as objective truth, or adopted as identity.

---

## 4. 🧭 Candidate alternatives

### A. Pure Non-Projection Classifier — **SELECTED**

```text
classify(explicit attributed interpretation values)
→ bounded Non-Projection result
```

Why selected:

- directly implements the frozen readiness question;
- can remain deterministic and side-effect free;
- does not depend on unauthorized identity/relationship runtimes;
- supports exact adversarial/metamorphic testing;
- preserves the authority ceiling.

### B. Retrieval-backed Non-Projection Service — **REJECTED FOR THIS MILESTONE**

A service that fetches Creator Atlas, Human Paths, research, databases or vector
stores introduces discovery/retrieval authority and hidden freshness semantics.
That is broader than the selected problem.

### C. Model-mediated / LLM judge — **REJECTED**

A model call would introduce nondeterminism, provider/context dependence and a
new trust boundary. Reviewer/model output may be input evidence, but the selected
classifier itself must not depend on a model call.

### D. Character-integrated projection filter — **REJECTED**

Character Policy is downstream presentation only. Combining it with the
classifier risks style-to-belief or style-to-authority escalation.

### E. Identity-aware self verifier — **DEFERRED**

`VERIFIED_SELF` requires separately authorized identity/continuation evidence.
Selecting an identity runtime here would cross a boundary the readiness block
explicitly kept closed.

### F. Action Gate integrated Non-Projection check — **REJECTED FOR THIS MILESTONE**

Action Gate includes broader execution and side-effect authority. A positive
Non-Projection classification may eventually be one governed input to a later
composition decision, but it cannot itself become Action Gate PASS.

---

## 5. 👤 Self-attribution ceiling

The selected candidate must not manufacture `VERIFIED_SELF`.

Under current authority:

```text
imported Creator material     → NON_SELF or UNKNOWN
historical material           → NON_SELF or UNKNOWN
current-user testimony        → NON_SELF or UNKNOWN relative to Mentaury
literary material             → NON_SELF or UNKNOWN
research material             → NON_SELF or UNKNOWN
model/reviewer interpretation → NON_SELF or UNKNOWN
```

A later implementation contract may admit a separately supplied self-evidence
reference field only if its semantics remain fail-closed and do not themselves
create identity authority. Actual `VERIFIED_SELF` evidence binding remains a
separate future identity/continuation contract decision.

```text
caller says "this is you"           ≠ VERIFIED_SELF
creator authority                    ≠ VERIFIED_SELF
narrative similarity                 ≠ VERIFIED_SELF
same model/provider                  ≠ VERIFIED_SELF
shared project lineage               ≠ VERIFIED_SELF
pre-fork shared history alone        ≠ current-branch VERIFIED_SELF
```

---

## 6. 🚦 Result ceiling

The candidate may later implement only semantically equivalent outcomes to the
frozen readiness vocabulary:

```text
PASS_ATTRIBUTED
REVISE_REQUIRED
CONTESTED
DEFER
REJECT
```

The later contract must preserve fail-closed precedence:

```text
REJECT
> DEFER
> CONTESTED
> REVISE_REQUIRED
> PASS_ATTRIBUTED
```

Positive ceiling:

```text
PASS_ATTRIBUTED
= at most no bounded projection blocker found for this admitted interpretation

PASS_ATTRIBUTED
≠ factual truth proof
≠ Mentaury autobiography
≠ identity / M3 authority
≠ relationship / commitment / consent authority
≠ capability
≠ Action Gate PASS
≠ retrieval permission
≠ tool / execution permission
≠ deployment permission
```

---

## 7. 🛡️ Frozen threat/readiness inheritance

A later implementation contract must bind the candidate to all frozen readiness
families without silently weakening them:

```text
NPG-T01…NPG-T12
NPG-SC-001…NPG-SC-012
MT-NPG-001…MT-NPG-008
```

The contract must also retain at least one executable contested-conflict case so
`CONTESTED` cannot become decorative or unreachable.

The candidate selection does **not** assign exact implementation test IDs beyond
these inherited readiness families. Exact executable matrix IDs belong to the
later implementation-contract freeze.

---

## 8. 🔗 P1 / Character / Canon boundary

```text
P1-001 contract = unchanged
P1-002 contract = unchanged
P1-003 contract = unchanged
MENTAURY_CANON_V0.1 = unchanged
```

The selected candidate does not modify the current P1-003 composer and is not an
implicit input to it.

```text
P1_003_ELIGIBLE_FOR_NEXT_GATE
+ PASS_ATTRIBUTED
≠ Action Gate PASS
```

A future cross-gate binding involving a Non-Projection result requires a separate
explicit composition decision. This candidate selection does not create one.

Character remains downstream:

```text
Non-Projection classification
→ then presentation policy

presentation policy
→ cannot change provenance, evidence or Non-Projection result
```

---

## 9. 🔐 Authorization ladder

The exact promotion sequence is:

```text
CANDIDATE_SELECTED_DOCS_ONLY
→ NON_PROJECTION_IMPLEMENTATION_CONTRACT_FROZEN_DOCS_ONLY
→ explicit separate NON_PROJECTION_OWNER_GO_AUTHORIZED_BOUNDED
→ clean Tier A bounded implementation PR
→ IMPLEMENTED_BOUNDED only after exact-head + resulting-main evidence
```

Current position:

```text
CANDIDATE_SELECTED_DOCS_ONLY
```

No later state is implied.

### Candidate selection does not assign P1-004

`P1_004 = NOT_ASSIGNED` remains current. A numbering/runtime-assignment decision,
if ever needed, must be explicit and separate from this selection.

### Candidate selection does not freeze implementation details

This document does not freeze:

- exact Python package path;
- exact public API/function name;
- concrete dataclasses/enums;
- canonical serialization/fingerprint domain;
- exact reason codes;
- deterministic budgets;
- malformed-input exception/result policy;
- exact executable test IDs;
- implementation completion receipt.

Those belong to the next docs-only implementation-contract freeze.

### Candidate selection does not grant Owner GO

```text
NON_PROJECTION_OWNER_GO = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NONE
```

---

## 10. 📜 Required content before any Owner GO

The separate future implementation-contract freeze must define at minimum:

1. exact immutable input/context schema derived from the Attributed Interpretation Envelope;
2. exact public classifier API and package boundary;
3. exact version fields and compatibility policy;
4. exact provenance/source-class enums and admission rules;
5. exact subject/speaker/self-attribution fields and fail-closed validation;
6. exact claim-class representation;
7. exact contextual-distance and scope representation;
8. exact reviewer-correlation representation and independence accounting;
9. exact result and reason taxonomy;
10. exact `REJECT > DEFER > CONTESTED > REVISE_REQUIRED > PASS_ATTRIBUTED` evaluation rules;
11. exact mapping of NPG-T01…NPG-T12 to executable conditions;
12. exact mapping of NPG-SC-001…NPG-SC-012 plus contested-conflict case to tests;
13. exact mapping of MT-NPG-001…MT-NPG-008 to metamorphic tests;
14. no-hidden-I/O/import-side-effect proof strategy;
15. deterministic budget and malformed-input behavior;
16. Character non-override proof;
17. compatibility/non-modification rule for P1-001/P1-002/P1-003 and Canon v0.1;
18. exact non-goals and forbidden authority surface;
19. acceptance criteria for a later bounded implementation PR.

Until that contract is frozen and separately authorized:

```text
P1_004 = NOT_ASSIGNED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
NON_PROJECTION_OWNER_GO = NOT_GRANTED
IMPLEMENTATION_AUTHORIZATION = NONE
```

---

## 11. ⛔ Compatibility stop

Stop before contract freeze or implementation if the candidate would require:

- hidden retrieval, persistence, network, filesystem, database, graph or vector-store access;
- model/LLM invocation inside the classifier;
- changing frozen P1-001/P1-002/P1-003 semantics;
- changing Canon v0.1 authority meanings;
- using caller assertion as self-attribution authority;
- using source prestige or reviewer count as truth/authority escalation;
- Character Policy overriding the result;
- current relationship/commitment/consent inheritance from source lineage;
- direct or indirect M3 nomination/write;
- `PASS_ATTRIBUTED` becoming Action Gate/retrieval/tool/execution authority;
- weakening NPG-T01…T12, NPG-SC-001…012 or MT-NPG-001…008.

Required response:

```text
STOP_CURRENT_PROMOTION
→ new docs-only compatibility decision
→ review
→ explicit Owner decision if authority changes
```

---

## 12. 🧭 Next bounded work

The only selected next bounded work is:

```text
NEXT_BOUNDED_WORK = NON_PROJECTION_IMPLEMENTATION_CONTRACT_FREEZE
MODE              = DOCS_ONLY
P1_004            = NOT_ASSIGNED
OWNER_GO          = NOT_GRANTED
IMPLEMENTATION    = NOT_AUTHORIZED
```

This document stops before defining the concrete implementation contract.

---

## 13. 🏁 Final formula

```text
P1-003 IMPLEMENTED_BOUNDED
+ Non-Projection Gate Contract Readiness READY
+ ATTRIBUTED_INTERPRETATION_ENVELOPE frozen at readiness level
+ PURE_NON_PROJECTION_CLASSIFIER selected as the sole implementation candidate

→ candidate selection complete
→ next work may freeze a docs-only implementation contract

≠ P1-004 assigned
≠ implementation contract frozen
≠ Owner GO
≠ implementation authorization
≠ runtime activation
≠ Action Gate / retrieval / tool authority
≠ identity / relationship / consent / M3 authority
≠ deployment authority
```
