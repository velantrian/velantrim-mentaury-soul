# 🧩 P1-003 Candidate Selection & Authorization Boundary

```text
Status:                         FROZEN_DOCS · DOCS_ONLY · CANDIDATE_SELECTION
Version:                        0.1
Date:                           2026-08-10
Review tier:                    TIER_A
P1-003 candidate selection:     SELECTED
Selected candidate:             PURE_GOVERNED_CONSTRAINT_COMPOSER
P1-003 runtime assignment:      NOT_ASSIGNED
P1-003 implementation contract: NOT_FROZEN
Owner GO:                       NOT_GRANTED
Implementation authorization:   NONE
Runtime implementation:         NOT_AUTHORIZED
Retrieval authority:            NONE
Action authority:               NONE
Tool authority:                 NONE
Identity authority:             NONE
Direct or indirect M3 write:    FORBIDDEN
Deployment authority:           NONE
```

> **CANDIDATE SELECTED ≠ P1-003 ASSIGNED.**
>
> **THIS DOCUMENT DOES NOT AUTHORIZE IMPLEMENTATION.**
>
> It does not authorize retrieval, persistence, filesystem/database/network I/O,
> Action Gate execution, tool execution, relationship or identity mutation,
> Character runtime, M3 writes, remediation or deployment.

---

## 1. 🎯 Bounded decision

Cross-gate binding readiness is already `READY`. The remaining bounded question
is whether one concrete next runtime-capable candidate is sufficiently coherent
to justify a later contract-freeze step without prematurely granting code
authority.

The decision is:

```text
P1_003_CANDIDATE_SELECTION = SELECTED
P1_003_CANDIDATE           = PURE_GOVERNED_CONSTRAINT_COMPOSER
P1_003_RUNTIME_ASSIGNMENT  = NOT_ASSIGNED
IMPLEMENTATION_AUTHORIZATION = NONE
```

The selected candidate is a **minimal pure coordinator** over the existing
bounded P1-001 Capability Lease resolver and P1-002 Privacy Reconciliation
classifier. It would own one immutable canonical evaluation context, project
that context into both gates, evaluate them in the same attempt, verify the
frozen cross-gate binding/freshness contract, and return only bounded readiness.

Its strongest positive semantic remains:

```text
ELIGIBLE_FOR_NEXT_GATE
```

That result is not executable authority.

---

## 2. ✅ Why this candidate is now coherent

The previous readiness block resolved the structural blocker that made a direct
composer premature:

- bare P1 results do not prove common request/context/freshness;
- a future coordinator can instead retain and verify original admitted source
  inputs in one immutable evaluation attempt;
- existing P1-001 and P1-002 result shapes do not need modification;
- caller-supplied digests are not authority;
- freshness is same-attempt and revision/version-bound;
- fail-closed outcomes are already frozen as `ELIGIBLE_FOR_NEXT_GATE`,
  `NOT_ELIGIBLE`, and `DEFER`;
- threat scenarios T1–T12 and metamorphic properties M1–M10 already define the
  minimum safety envelope for later executable tests.

Therefore one narrow coordinator candidate is architecturally justified without
selecting a broader runtime or Action Gate.

---

## 3. 🧱 Selected candidate boundary

A future `Pure Governed Constraint Composer` may only be considered valid if its
contract remains equivalent to this shape:

```text
explicit immutable inputs
→ canonical admission
→ derive common request / evaluation evidence binding
→ invoke existing pure P1-001 resolver
→ invoke existing pure P1-002 classifier
→ verify same-attempt binding and freshness
→ classify readiness
→ return bounded result/evidence
```

Required properties:

- deterministic and explicit-input only;
- no ambient clock, environment or hidden dependency lookup;
- no filesystem, database or network access;
- no persistence or durable permission token;
- no retrieval of protected content;
- no tool or action execution;
- no mutation of beliefs, relationships, identity or M3;
- no Character activation;
- no backend selection or deployment;
- no authority amplification beyond the checked P1 dimensions;
- `ELIGIBLE_FOR_NEXT_GATE` always requires a later separately authorized gate.

---

## 4. ❌ Alternatives not selected

### A. Bare-result composer

```text
compose(capability_result, privacy_result)
```

**REJECTED.** It cannot prove common request, purpose, scope, branch or freshness.

### B. Evidence-envelope service as authority

**NOT SELECTED AS THE MILESTONE.** A derived envelope may be useful audit evidence,
but an envelope or digest is not standalone permission and does not replace
source-input re-evaluation.

### C. Modify P1-001/P1-002 result contracts first

**NOT REQUIRED.** The frozen readiness architecture can retain the original
admitted source values in the coordinator without changing the existing result
shapes.

### D. Action Gate

**NOT SELECTED.** Action Gate is broader than capability + privacy composition and
may include constitutional, relationship/commitment, identity, side-effect and
other governed constraints.

### E. Retrieval / remediation / persistence runtime

**NOT SELECTED.** These introduce I/O and execution authority outside the bounded
composition problem.

---

## 5. 🔐 Authorization ladder

The exact promotion sequence is frozen as:

```text
CANDIDATE_SELECTED_DOCS_ONLY
→ P1_003_CONTRACT_FROZEN_DOCS_ONLY
→ explicit separate P1_003_OWNER_GO_AUTHORIZED_BOUNDED
→ clean Tier A implementation PR
→ IMPLEMENTED_BOUNDED only after exact-head + resulting-main evidence
```

Current position:

```text
CANDIDATE_SELECTED_DOCS_ONLY
```

No later state is implied.

### Candidate selection does not consume an Owner GO

No P1-003 Owner GO exists in this document. The prior P1-001 and P1-002 Owner GO
receipts remain consumed and cannot be reused.

### Contract freeze does not itself authorize code

A later contract document may freeze exact schemas and tests, but implementation
must still wait for a **separate explicit Owner GO**.

---

## 6. 📜 Required content before any P1-003 Owner GO

A separate future contract-freeze milestone must define, at minimum:

1. exact immutable `CrossGateEvaluationContext` schema;
2. exact public composer function/API and package boundary;
3. exact canonical projections into P1-001 and P1-002;
4. exact common-request and evaluation-evidence fingerprint domains;
5. canonicalization and binding contract version fields;
6. source-provenance trust boundary and caller-assertion rules;
7. exact readiness result contract and reason taxonomy;
8. exact `ELIGIBLE_FOR_NEXT_GATE` / `NOT_ELIGIBLE` / `DEFER` precedence;
9. explicit freshness and invalidation rules;
10. executable mappings for T1–T12 adversarial scenarios;
11. executable mappings for M1–M10 metamorphic properties;
12. no-hidden-I/O/import-side-effect proof strategy;
13. deterministic budget and malformed-input behavior;
14. compatibility/non-modification rule for frozen P1-001/P1-002 contracts;
15. exact non-goals and forbidden authority surface;
16. test matrix and acceptance criteria for a later implementation PR.

Until those items are frozen, `P1_003_RUNTIME_ASSIGNMENT` remains
`NOT_ASSIGNED`.

---

## 7. 🛑 Authority invariants

```text
Capability ALLOW
+ Privacy ALLOW_REFERENCE
+ verified cross-gate binding
= at most ELIGIBLE_FOR_NEXT_GATE

ELIGIBLE_FOR_NEXT_GATE ≠ ACTION_GATE_PASS
ELIGIBLE_FOR_NEXT_GATE ≠ RETRIEVAL_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ TOOL_PERMISSION
ELIGIBLE_FOR_NEXT_GATE ≠ EXECUTION_PERMISSION
```

The selected candidate may **coordinate classifications**. It may not silently
become the Action Gate or an execution layer.

---

## 8. 🎭 Character / identity / M3 boundary

```text
CHARACTER_RUNTIME_ACTIVATION_GATE = BLOCKED_PENDING_REQUIRED_VALIDATION
DIRECT_OR_INDIRECT_M3_WRITE       = FORBIDDEN
```

Selecting the composer candidate creates no Character evidence and no identity,
relationship, Genesis Heritage, Human Paths Atlas or M3 runtime authority.

Issue #39 remains the future transition trigger for genuine independent/team
review and is not a current solo-mode blocker.

---

## 9. 🛡️ Governance and later implementation evidence

Any future contract that changes roadmap/authority remains Tier A. Any later
implementation PR must use current solo-maintainer governance:

```text
exact current head
+ complete final diff
+ exact-head required CI
+ up-to-date branch
+ zero unresolved conversations
+ correctness pass
+ adversarial pass
+ explicit authorization-boundary check
+ explicit maintainer merge decision
+ green resulting-main CI
```

Independent human review is not claimed while the repository remains in
`SOLO_MAINTAINER` mode.

---

## 10. 🧭 Next bounded work

The only selected next bounded work is **docs-only contract freeze preparation**
for the candidate above.

```text
NEXT_BOUNDED_WORK = P1_003_PURE_COMPOSER_CONTRACT_FREEZE
MODE              = DOCS_ONLY
IMPLEMENTATION    = NOT_AUTHORIZED
OWNER_GO          = NOT_GRANTED
```

This document stops before defining or implementing runtime code.

---

## 11. 🏁 Final formula

```text
P1-001 IMPLEMENTED_BOUNDED
+ P1-002 IMPLEMENTED_BOUNDED
+ CROSS_GATE_BINDING_READINESS READY
+ PURE_GOVERNED_CONSTRAINT_COMPOSER selected as the sole P1-003 candidate

→ candidate selection complete
→ next work may freeze a docs-only implementation contract

≠ P1-003 assigned
≠ Owner GO
≠ implementation authorization
≠ retrieval or Action Gate authority
≠ identity/relationship/Character/M3 runtime
≠ deployment authority
```
