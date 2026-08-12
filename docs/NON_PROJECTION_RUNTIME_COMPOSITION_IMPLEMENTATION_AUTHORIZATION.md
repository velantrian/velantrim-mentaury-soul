# ✅ NPG-COMP-v0.1 — Implementation Authorization & Completion Receipt

```text
Status:                         OWNER_GO_CONSUMED · IMPLEMENTED_BOUNDED
Date:                           2026-08-12
Contract:                       NPG-COMP-v0.1 · FROZEN_DOCS · UNCHANGED
Underlying classifier:          NPG-v0.1 · IMPLEMENTED_BOUNDED · UNCHANGED
Envelope:                       AIE-v0.1 · UNCHANGED
Strategy:                       SAME_ATTEMPT_SHADOW_COORDINATOR
Phase 2 Owner GO:               CONSUMED_BY_PR_96
Owner GO scope:                 NPG-COMP-v0.1_ONLY
Implementation authorization:   CONSUMED · NPG-COMP-v0.1_ONLY
Phase 2 implementation:         IMPLEMENTED_BOUNDED
Non-Projection runtime:         NOT_AUTHORIZED
P1-004 assignment:              NOT_ASSIGNED
Action Gate:                    NOT_AUTHORIZED
Retrieval / Atlas:              NOT_AUTHORIZED
Tools / plugins / subprocess:   NOT_AUTHORIZED
Identity runtime:               NOT_AUTHORIZED
Relationship runtime:           NOT_AUTHORIZED
Character runtime:              NOT_AUTHORIZED
Direct or indirect M3 write:    FORBIDDEN
Persistence:                    NOT_AUTHORIZED
Deployment:                     NOT_AUTHORIZED
Autonomous background loop:     NOT_AUTHORIZED
Independent human review:       NO
```

> `IMPLEMENTED_BOUNDED` means only the exact frozen shadow-composition package
> exists and passed exact-head plus resulting-main validation. It does not mean
> runtime activation, scheduling, persistence, retrieval, action or deployment.

---

## 1. Authority chain

### Phase 1 contract freeze — PR #93

```text
Contract:               NPG-COMP-v0.1 · FROZEN_DOCS
Strategy:               SAME_ATTEMPT_SHADOW_COORDINATOR
WHO:                    NON_PROJECTION_SHADOW_COORDINATOR_ONLY
WHAT:                   exact caller-supplied AIE-v0.1 + NonProjectionBudget
WHERE:                  same-attempt bound shadow observation only
Phase 2 Owner GO:       NOT_GRANTED at freeze time
Runtime:                NOT_AUTHORIZED
```

### Explicit Owner GO — PR #94

```text
Owner GO:               GRANTED
Owner GO scope:         NPG-COMP-v0.1_ONLY · SINGLE_USE
Reviewed exact head:    25a8cbf58fbdbee9fafc9ca41aa9575d47cd9450
Exact-head CI:          31547098692 · SUCCESS · 783 passed
Tier A review:          4911669134
Authorization merge:    d0be41a0712d076101d508812a7eb491558b4f57
Resulting-main CI:      31547170338 · SUCCESS · 783 passed
Implementation:         NOT_STARTED at decision time
```

### Post-GO status reconciliation — PR #95

```text
Reviewed exact head:    88b68a363981ff3c3b8f66259e06def49208af1b
Exact-head CI:          31548130967 · SUCCESS · 788 passed
Tier A review:          4911758911
Reconciliation merge:   8c2be99b03e0dc5eee614b757060d8569bb88596
Resulting-main CI:      31548204752 · SUCCESS · 788 passed
Source/runtime change:  NONE
New authority:          NONE
```

PR #95 preserved Phase-1 `NOT_GRANTED` as historical freeze-time provenance and
made the already-authoritative #94 grant explicit in current/navigation status.

---

## 2. Verified bounded implementation — PR #96

```text
Implementation PR:         #96
Baseline main:              8c2be99b03e0dc5eee614b757060d8569bb88596
Reviewed exact head:        8a7b524de46c042e0479186ea4564f363248a366
Exact-head CI:              31548525699 · SUCCESS · 842 passed
Tier A review:              4911798445
Correctness pass:           PASS
Adversarial pass:           PASS
Authorization boundary:     PRESERVED
Review threads:             0
Independent human review:   NO
Implementation merge/main:  153d64d142e5b5555bc3a942cb0beedce89b91e0
Merge signature:            VERIFIED · VALID
Resulting-main CI:          31548659423 · SUCCESS · 842 passed
```

The first PR #96 validation run `31548459726` was not accepted: it exposed one
stale historical P1-003 structural assertion that incorrectly treated the whole
`composition` namespace as permanently exclusive. The assertion was narrowed to
the exact historical P1-003 package. Final review and merge used only the later
green exact head `8a7b524d…`.

---

## 3. Exact implemented source surface

```text
src/mentaury/composition/non_projection_shadow/__init__.py
src/mentaury/composition/non_projection_shadow/contracts.py
src/mentaury/composition/non_projection_shadow/coordinator.py
```

No service, runtime root, worker, scheduler, persistence adapter, retriever,
Atlas adapter, model/LLM client, Action Gate, tool adapter, plugin, subprocess,
identity/relationship store or deployment switch was added.

---

## 4. Frozen API and semantics retained

```python
def evaluate_non_projection_shadow(
    *,
    context: NonProjectionShadowContext,
) -> NonProjectionShadowObservation:
    ...
```

```text
context = evaluation_id + proposal_ref + exact AIE-v0.1 + exact NonProjectionBudget
→ strict admission
→ local NPG-COMP/NPG/AIE compatibility check
→ classify_non_projection(...) exactly once
→ exact NonProjectionResult preserved
→ bind result to evaluation_id + proposal_ref
→ immutable NonProjectionShadowObservation
```

A prior `NonProjectionResult`, caller-supplied fingerprint, destination,
retriever, Atlas/model/tool handle, identity/relationship/M3 state, callback,
retry/remediation policy or persistence handle is not part of the API.

---

## 5. Executable validation retained

PR #96 executes the frozen families:

```text
NRC-T01…NRC-T12
NRC-M01…NRC-M10
```

The tests additionally verify:

- exact contract constants and keyword-only API;
- frozen/immutable input and output;
- exact type admission and fail-closed contract errors;
- exactly one NPG classifier call per attempt;
- preservation of all 12 projection-threat results;
- preservation of DEFER / REJECT / PASS_ATTRIBUTED semantics;
- deterministic repeat behavior;
- fresh NPG classification when envelope or budget changes;
- wrapper-only rebinding when evaluation/proposal references change;
- `STOP_AND_RECONCILE` on NPG/AIE version drift;
- exact three-file package surface;
- no forbidden I/O/runtime imports;
- no persistence/destination/authority fields.

---

## 6. Authority ceiling remains unchanged

```text
PASS_ATTRIBUTED
= no bounded Non-Projection blocker found for the exact admitted proposal
≠ truth proof
≠ Mentaury autobiography
≠ stable identity trait
≠ relationship / commitment / consent authority
≠ capability or Action Gate PASS
≠ retrieval permission
≠ tool permission
≠ execution permission
≠ M3 authority
≠ deployment permission
```

The `NonProjectionShadowObservation` is same-attempt evidence/provenance only. It
is not a bearer token and is not reusable authority.

---

## 7. Owner GO consumption

The single-use PR #94 authorization is now consumed by the verified #96
implementation:

```text
PHASE_2_OWNER_GO = CONSUMED_BY_PR_96
OWNER_GO_SCOPE = NPG-COMP-v0.1_ONLY
IMPLEMENTATION_AUTHORIZATION = CONSUMED · NPG-COMP-v0.1_ONLY
PHASE_2_IMPLEMENTATION = IMPLEMENTED_BOUNDED
```

It cannot authorize any later runtime wiring, activation, retrieval, Action Gate,
tool, identity/relationship, M3, persistence, deployment or Phase 3 work.

---

## 8. Mandatory post-completion boundary

```text
NON_PROJECTION_RUNTIME = NOT_AUTHORIZED
P1_004 = NOT_ASSIGNED
ACTION_GATE = NOT_AUTHORIZED
RETRIEVAL_EXECUTION = NOT_AUTHORIZED
ATLAS_ACCESS = NOT_AUTHORIZED
TOOL_EXECUTION = NOT_AUTHORIZED
PLUGIN_EXECUTION = NOT_AUTHORIZED
SUBPROCESS_EXECUTION = NOT_AUTHORIZED
IDENTITY_RUNTIME = NOT_AUTHORIZED
RELATIONSHIP_RUNTIME = NOT_AUTHORIZED
CHARACTER_RUNTIME = NOT_AUTHORIZED
DIRECT_OR_INDIRECT_M3_WRITE = FORBIDDEN
PERSISTENCE = NOT_AUTHORIZED
RUNTIME_DEPLOYMENT = NOT_AUTHORIZED
AUTONOMOUS_BACKGROUND_LOOP = NOT_AUTHORIZED
PHASE_3_PROVENANCE_CLAIM_REPRESENTATION = NOT_STARTED
PHASE_3_OWNER_GO = NOT_GRANTED
```

> **STOP.** Completion of Phase 2 creates no automatic authority for Phase 3 or
> any runtime activation. A later milestone requires a fresh live preflight and
> its own bounded contract/Owner-GO cycle.
