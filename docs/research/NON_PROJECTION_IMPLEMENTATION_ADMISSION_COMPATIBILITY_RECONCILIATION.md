# 🧩 Non-Projection Implementation Admission Compatibility Reconciliation

```text
Status:                               RECONCILED · DOCS_ONLY
Date:                                 2026-08-10
Baseline main:                        4619225654d73e728a67d9b20185cf9214ae0bd2
Frozen contract:                      NPG-v0.1 · UNCHANGED
Envelope version:                     AIE-v0.1 · UNCHANGED
Candidate:                            PURE_NON_PROJECTION_CLASSIFIER · UNCHANGED
Owning contract PR:                   #86
Budget clarification PR:              #87
Explicit Owner GO PR:                 #88
Owner GO:                             GRANTED · NPG-v0.1_ONLY
Owner GO revalidation:                VALID_UNCHANGED
Implementation admission compatibility: READY
Implementation in this milestone:     NOT_STARTED
Runtime:                              NOT_AUTHORIZED
P1-004:                               NOT_ASSIGNED
Independent human review:             NO
Governance mode:                      SOLO_MAINTAINER
```

> **This reconciliation changes no NPG-v0.1 classifier semantics and grants no new authority.**
>
> It resolves one phase-bound structural-test contradiction discovered during the fresh preflight for the separately authorized bounded implementation milestone.

---

## 1. ⚠️ Reconciled contradiction

PR #88 was intentionally docs-only. Its structural proof included a repository-state assertion that the reserved implementation package did not yet exist:

```python
assert not (ROOT / "src" / "mentaury" / "non_projection").exists()
```

That assertion correctly proved the historical fact for PR #88:

```text
OWNER GO GRANTED
≠ IMPLEMENTATION STARTED IN PR #88
```

After #88 merged, however, the same executable assertion became an accidental perpetual invariant. The frozen NPG-v0.1 contract simultaneously reserves the future implementation package:

```text
src/mentaury/non_projection/__init__.py
src/mentaury/non_projection/contracts.py
src/mentaury/non_projection/classifier.py
```

Therefore an implementation conforming to the exact frozen contract would necessarily fail the historical #88 filesystem-absence assertion.

This is an acceptance-harness phase conflict, not a classifier-contract conflict.

---

## 2. ✅ Exact reconciliation decision

The #88 package-absence assertion is reclassified as **milestone-local evidence about PR #88**, not an enduring postcondition after a later separately authorized implementation begins.

The executable proof is changed to preserve the real invariant:

```text
PR #88 itself was docs-only
+ #88 did not start implementation
+ Owner GO remained bounded to NPG-v0.1
+ later creation of the exact reserved package is allowed only in a fresh separate bounded implementation milestone
```

The test must therefore verify the historical/authority record rather than require repository-wide non-existence of the package forever.

This reconciliation happens **before implementation**. Consequently, the later implementation milestone starts from a new authoritative baseline where this structural test is already reconciled. The frozen acceptance requirement that existing repository tests remain green and are not weakened merely to admit classifier behavior remains applicable to that later implementation baseline.

---

## 3. 🔒 Frozen semantics remain unchanged

No change is made to any of the following:

```text
NON_PROJECTION_CONTRACT_VERSION = NPG-v0.1
ATTRIBUTED_INTERPRETATION_ENVELOPE_VERSION = AIE-v0.1
NON_PROJECTION_CANDIDATE = PURE_NON_PROJECTION_CLASSIFIER

REJECT > DEFER > CONTESTED > REVISE_REQUIRED > PASS_ATTRIBUTED
VERIFIED_SELF → DEFER · SELF_BASIS_UNVERIFIED
hard-cap overflow → NonProjectionContractError
local-budget overflow while still inside hard caps → DEFER · BUDGET_EXHAUSTED

NPG-T01…NPG-T12 = unchanged
NPG-SC-001…NPG-SC-012 = unchanged
NPG-SC-CONTESTED-001 = unchanged
MT-NPG-001…MT-NPG-008 = unchanged
NPC-CTX-001…022 = unchanged
NPC-FP-001…008 = unchanged
NPC-DEC-001…016 = unchanged
NPC-T-001…012 = unchanged
NPC-SC-001…012 = unchanged
NPC-SC-CONTESTED-001 = unchanged
NPC-M-001…008 = unchanged
NPC-PURE-001…010 = unchanged
```

The exact future public API, package paths, dataclasses, enums, reason vocabulary, budget semantics, fingerprint algorithm, purity boundary and authority ceiling are unchanged.

---

## 4. 🧬 Owner GO revalidation

PR #88 remains valid without a new Owner GO because this reconciliation does not mutate the contract or widen authority:

```text
NON_PROJECTION_OWNER_GO = GRANTED
OWNER_GO_SCOPE = NPG-v0.1_ONLY
OWNER_GO_REVALIDATION = VALID_UNCHANGED
IMPLEMENTATION_AUTHORIZATION = GRANTED_FOR_NEXT_SEPARATE_BOUNDED_IMPLEMENTATION_MILESTONE
```

This reconciliation itself still does not start implementation.

---

## 5. 🚫 Explicit non-authorizations

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

No `src/**` file is created or changed by this reconciliation milestone.

---

## 6. 🛡️ Adversarial interpretation boundary

This decision cannot be used to claim that tests may be deleted, bypassed or weakened during implementation.

It authorizes exactly one phase correction:

```text
historical package absence in PR #88
→ historical/authority assertion
```

It does **not** authorize:

```text
classifier semantic changes
package-path changes
API changes
reason/threat changes
budget/fingerprint changes
purity weakening
runtime activation
Action Gate/retrieval/tool authority
identity/relationship authority
M3 write
P1-004 assignment
deployment
```

---

## 7. 🏁 Resulting authority state after this reconciliation

```text
NPG-v0.1 = FROZEN · UNCHANGED
OWNER GO = GRANTED · NPG-v0.1_ONLY · VALID_UNCHANGED
IMPLEMENTATION_ADMISSION_COMPATIBILITY = READY
NON_PROJECTION_IMPLEMENTATION = NOT_STARTED
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
P1_004 = NOT_ASSIGNED
```

Final formula:

```text
HISTORICAL #88 PACKAGE ABSENCE
≠ PERPETUAL PACKAGE PROHIBITION

RECONCILED IMPLEMENTATION ADMISSION
≠ IMPLEMENTATION STARTED

OWNER GO REMAINS VALID
≠ RUNTIME AUTHORITY
≠ ACTION AUTHORITY
```

After protected merge, resulting-main CI and Notion synchronization, the next possible work is a **fresh separate Pure Non-Projection Classifier bounded implementation milestone** starting from the reconciled resulting `main`.
