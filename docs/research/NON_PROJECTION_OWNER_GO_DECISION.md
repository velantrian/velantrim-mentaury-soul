# 🪞 Non-Projection Explicit Owner GO Decision — NPG-v0.1

```text
Status:                              OWNER_GO · GRANTED · DOCS_ONLY_AUTHORITY_MILESTONE
Decision date:                       2026-08-10
Review tier:                         TIER_A
Baseline main SHA:                   1c8016b32e9b0ddc641af4a4410a5bdae05fd625
Owning contract PR:                  #86
Budget clarification PR:             #87
Owner GO PR:                         #88
Candidate:                           PURE_NON_PROJECTION_CLASSIFIER
Contract version:                    NPG-v0.1
Envelope version:                    AIE-v0.1
Non-Projection Owner GO:             GRANTED
Owner GO scope:                      NPG-v0.1_ONLY
Implementation authorization:        GRANTED_FOR_NEXT_SEPARATE_BOUNDED_IMPLEMENTATION_MILESTONE
Non-Projection implementation:       NOT_STARTED
Non-Projection runtime:              NOT_AUTHORIZED
P1-004 assignment:                   NOT_ASSIGNED
Action Gate:                         NOT_AUTHORIZED
Retrieval execution:                 NOT_AUTHORIZED
Tool execution:                      NOT_AUTHORIZED
Identity runtime:                    NOT_AUTHORIZED
Relationship runtime:                NOT_AUTHORIZED
Direct or indirect M3 write:         FORBIDDEN
Runtime deployment:                  NOT_AUTHORIZED
Governance mode:                     SOLO_MAINTAINER = ACTIVE
Independent human review:            NO
Issue #39:                           OPEN · FUTURE INDEPENDENT/TEAM REVIEW TRIGGER
Codex review:                        NOT PERFORMED · QUOTA EXHAUSTED · PR #88 comment 5246225861
```

> **OWNER GO DECISION: GO.**
>
> This record grants one bounded owner authorization for the exact frozen
> `NPG-v0.1` contract only. It does not implement the classifier, assign P1-004,
> activate a runtime, grant Action Gate/retrieval/tool authority, authorize
> identity/relationship state, permit M3 writes, or authorize deployment.

---

## 1. Decision basis

The owner explicitly authorized this separate decision milestone after the
reconciled implementation contract reached merged `main` through PR #86 and the
budget-admission clarification reached merged `main` through PR #87.

The live preflight for this decision established:

```text
main = 1c8016b32e9b0ddc641af4a4410a5bdae05fd625
open PRs = 0
open issues = #39 only
ruleset = 20594300 · Mentaury main governance · ACTIVE
bypass list = empty
required approvals = 0 · SOLO_MAINTAINER
required check = Python 3.13 · validator · pytest · compileall
conversation resolution = required
force-push protection = enabled
deletion protection = enabled
resulting-main CI = 31431741694 · SUCCESS · exact main SHA · 599 passed
```

Both existing Notion authority surfaces were fetched before repository mutation
and matched the merged #86/#87 checkpoint: contract frozen, Owner GO not yet
granted, P1-004 not assigned, implementation not started and runtime not
authorized.

Historical branches/closed PRs #84/#85 provide no acceptance authority. No open
same-scope PR, second Owner GO document, implementation PR or runtime PR existed
at first-write preflight. The old `agent/non-projection-implementation-contract-freeze`
branch is historical closed/unmerged work and is not an active writer path.

---

## 2. Authoritative contract identity

The exact contract authorized by this GO is only:

`docs/research/NON_PROJECTION_PURE_CLASSIFIER_CONTRACT_V0_1.md`

```text
NON_PROJECTION_GATE_CONTRACT_READINESS = READY
NON_PROJECTION_CANDIDATE_SELECTION = SELECTED
NON_PROJECTION_CANDIDATE = PURE_NON_PROJECTION_CLASSIFIER
NON_PROJECTION_IMPLEMENTATION_CONTRACT = FROZEN_DOCS
NON_PROJECTION_CONTRACT_VERSION = NPG-v0.1
ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION = AIE-v0.1
```

No second competing authoritative contract exists on the live baseline. PR #84
and PR #85 are closed without merge and do not contribute acceptance evidence.

The exact future public API remains:

```python
def classify_non_projection(
    *,
    envelope: AttributedInterpretationEnvelope,
    budget: NonProjectionBudget,
) -> NonProjectionResult:
    ...
```

This GO does not alter that API, any enum, schema, reason vocabulary, fingerprint,
budget, hard cap, threat mapping, scenario mapping or metamorphic obligation.

---

## 3. Owner GO precondition audit

### A. Contract identity — PASS

`PURE_NON_PROJECTION_CLASSIFIER`, `NPG-v0.1` and `AIE-v0.1` are exact and unique.

### B. API freeze — PASS

The one public classifier API above is frozen by the authoritative contract.

### C. Purity boundary — PASS

The frozen future implementation is limited to explicit caller-supplied bounded
values. It may not depend on network, filesystem, database, vector/graph stores,
Creator Atlas or Human Paths Atlas persistence, identity/relationship registries,
ambient clock, environment variables, model/LLM calls, retrieval, tools,
subprocesses or plugins.

### D. Self/non-self safety — PASS

NPG-v0.1 owns no authoritative identity binder:

```text
NON_SELF      → eligible for bounded evaluation
UNKNOWN       → DEFER · SUBJECT_RELATION_UNKNOWN
VERIFIED_SELF → DEFER · SELF_BASIS_UNVERIFIED
```

Creator/user assertion, narrative voice, provider/model identity, project lineage,
pre-fork history, prestige or repetition cannot create `VERIFIED_SELF` authority.

### E. Positive result ceiling — PASS

```text
PASS_ATTRIBUTED
= at most no bounded projection blocker found for this exact admitted proposal
≠ factual truth proof
≠ Mentaury autobiography
≠ identity claim or stable M3 trait
≠ relationship / commitment / consent authority
≠ capability
≠ Action Gate PASS
≠ retrieval permission
≠ tool / execution permission
≠ deployment permission
```

### F. Decision precedence — PASS

```text
REJECT > DEFER > CONTESTED > REVISE_REQUIRED > PASS_ATTRIBUTED
```

### G. Budget semantics — PASS

PR #87 removed the only wording ambiguity without changing contract scope:

```text
hard-cap overflow → NonProjectionContractError
local-budget overflow while still inside hard caps → DEFER · BUDGET_EXHAUSTED
```

Silent truncation, sampling, reordering, auto-upgrade and permissive fallback
remain forbidden.

### H. Threat coverage — PASS

The full frozen family `NPG-T01…NPG-T12` remains mandatory: autobiography
laundering, authority inheritance, truth escalation, emotion-to-drive projection,
style-to-belief projection, historical-law projection, correlated-consensus
laundering, context collapse, relationship projection, identity-trait projection,
interpretation laundering and consent inheritance.

### I. Scenario coverage — PASS

`NPG-SC-001…NPG-SC-012` remain exact and the separate credible-vs-credible
unresolved conflict fixture remains `NPG-SC-CONTESTED-001 → CONTESTED`.

### J. Metamorphic coverage — PASS

`MT-NPG-001…MT-NPG-008` remain frozen: attribution preservation, prestige
non-escalation, repetition non-escalation, context monotonicity, self/non-self
invalidation, no M3 amplification, no relationship amplification and determinism.

### K. Executable implementation obligations — PASS

The later implementation remains bound to the exact frozen families:

```text
NPC-CTX-001…022
NPC-FP-001…008
NPC-DEC-001…016
NPC-T-001…012
NPC-SC-001…012
NPC-SC-CONTESTED-001
NPC-M-001…008
NPC-PURE-001…010
```

The existing structural proof for the frozen contract remains
`tests/test_non_projection_implementation_contract_docs.py`.

---

## 4. Compatibility and authority reconciliation

P1-001, P1-002, P1-003 and Canon v0.1 are unchanged by this decision.

```text
P1-001 contract = unchanged
P1-002 contract = unchanged
P1-003 contract = unchanged
MENTAURY_CANON_V0.1 = unchanged
P1_004 = NOT_ASSIGNED
```

`docs/CURRENT_STATUS.md`, `docs/research/POST_P0_ROADMAP_V0.1.md` and
`docs/research/RESEARCH_INDEX.md` still contain pre-#86 summary wording such as
`IMPLEMENTATION_CONTRACT = NOT_FROZEN`. Those lines are stale summary/navigation
state, not a competing contract. They are superseded for this exact
Non-Projection authority transition by the later merged authoritative chain:

```text
PR #86 frozen NPG-v0.1 contract
→ PR #87 budget clarification
→ this explicit Owner GO decision
```

This reconciliation does not edit or reinterpret the frozen contract and does not
convert those older summary lines into implementation authority.

---

## 5. Explicit Owner authorization

The decision is exactly:

```text
OWNER_GO_DECISION = GO
NON_PROJECTION_OWNER_GO = GRANTED
OWNER_GO_SCOPE = NPG-v0.1_ONLY
IMPLEMENTATION_AUTHORIZATION = GRANTED_FOR_NEXT_SEPARATE_BOUNDED_IMPLEMENTATION_MILESTONE
```

The grant authorizes only the possibility of starting a **future separate**
bounded implementation milestone after its own fresh live preflight. It does not
start that milestone now.

```text
OWNER_GO_GRANTED
≠ IMPLEMENTATION_STARTED
≠ IMPLEMENTATION_COMPLETED
≠ RUNTIME_ENABLED
≠ ACTION_AUTHORITY
```

---

## 6. Explicit non-authorizations and stop boundary

After this GO, the required state is still:

```text
NON_PROJECTION_IMPLEMENTATION = NOT_STARTED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
P1_004 = NOT_ASSIGNED
ACTION_GATE = NOT_AUTHORIZED
RETRIEVAL_EXECUTION = NOT_AUTHORIZED
TOOL_EXECUTION = NOT_AUTHORIZED
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
RUNTIME_DEPLOYMENT = NOT_AUTHORIZED
```

No retrieval, Atlas access, model call, identity binder, relationship binder,
M2/M3 write, Action Gate integration, tool execution or deployment may be inferred
from this record.

The mandatory stop is:

```text
CONTRACT FROZEN
+ EXPLICIT OWNER GO
≠ IMPLEMENTATION

OWNER GO
≠ RUNTIME ENABLEMENT

OWNER GO
≠ ACTION AUTHORITY

→ STOP
→ next possible work: separate Pure Non-Projection Classifier bounded implementation milestone
→ fresh live preflight required before any code
```

---

## 7. Governance and review provenance

```text
Review mode = SOLO_MAINTAINER
SOLO_MAINTAINER = ACTIVE
INDEPENDENT_HUMAN_REVIEW = NO
MULTI_AGENT_EXECUTION_MODE = SERIALIZED_BY_BOUNDED_MILESTONE
ONE_BOUNDED_MILESTONE = ONE_ACTIVE_WRITER
AUTHORITY_MILESTONES = STRICTLY_SERIALIZED
```

Automated analysis may support the review but is not independent human assurance.
Issue #39 remains open as the future transition trigger for genuine independent or
team review.

The exact PR head, exact-head CI, final Tier A correctness/adversarial review,
pre-merge drift gate, protected merge and resulting-main CI must all be recorded
on the owning PR before this milestone is complete. Notion synchronization is
permitted only after resulting-main CI succeeds.
