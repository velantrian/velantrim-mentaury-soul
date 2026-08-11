# 🟢 Non-Projection Runtime Composition — Explicit Owner GO

```text
Status:                         OWNER_GO · GRANTED · DOCS_ONLY_AUTHORITY_MILESTONE
Decision date:                  2026-08-12
Baseline main:                  563e2c51c438d94f739fe434c63d00cbe78747ed
Owning contract:                NPG-COMP-v0.1 · FROZEN_DOCS
Owning classifier:              NPG-v0.1 · IMPLEMENTED_BOUNDED
Envelope:                       AIE-v0.1
Selected strategy:              SAME_ATTEMPT_SHADOW_COORDINATOR
Owner GO:                       GRANTED
Owner GO scope:                 NPG-COMP-v0.1_ONLY
Implementation authorization:   GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_2_IMPLEMENTATION
Phase 2 implementation:         NOT_STARTED
Non-Projection runtime:         NOT_AUTHORIZED
P1-004 assignment:              NOT_ASSIGNED
Action Gate:                    NOT_AUTHORIZED
Retrieval / Atlas:              NOT_AUTHORIZED
Tools / subprocess / plugins:   NOT_AUTHORIZED
Identity runtime:               NOT_AUTHORIZED
Relationship runtime:           NOT_AUTHORIZED
Direct or indirect M3 write:    FORBIDDEN
Persistence:                    NOT_AUTHORIZED
Deployment:                     NOT_AUTHORIZED
Governance mode:                SOLO_MAINTAINER
Independent human review:       NO
```

> **OWNER GO DECISION: GO — `NPG-COMP-v0.1_ONLY`.**
>
> The owner instruction in the active project conversation explicitly authorizes
> proceeding past the Phase 1 mandatory stop for the exact frozen
> `NPG-COMP-v0.1` contract. This record grants one bounded implementation
> authorization only. It does not itself implement, activate, deploy, persist,
> retrieve, execute tools, mutate identity/relationship/M3 state, or assign P1-004.

---

## 1. Live preflight basis

The fresh preflight immediately before this decision established:

```text
main = 563e2c51c438d94f739fe434c63d00cbe78747ed
open PRs = 0
ruleset = 20594300 · Mentaury main governance · ACTIVE
bypass list = empty
required approvals = 0 · SOLO_MAINTAINER
required check = Python 3.13 · validator · pytest · compileall
conversation resolution = required
force-push protection = enabled
deletion protection = enabled
Phase 1 PR #93 = MERGED
Phase 1 contract = FROZEN_DOCS · NPG-COMP-v0.1
Phase 2 = NOT_STARTED
```

Both permitted Notion pages were fetched before mutation and matched the Phase 1
checkpoint: contract frozen, Owner GO not granted, runtime not authorized and
P1-004 not assigned.

No open same-scope PR or competing runtime-composition authority record existed.

---

## 2. Exact authorized contract

Only this contract is authorized:

`docs/research/NON_PROJECTION_RUNTIME_COMPOSITION_CONTRACT_V0_1.md`

```text
CONTRACT = NPG-COMP-v0.1
STRATEGY = SAME_ATTEMPT_SHADOW_COORDINATOR
WHO = NON_PROJECTION_SHADOW_COORDINATOR_ONLY
WHAT = exact caller-supplied AIE-v0.1 + exact NonProjectionBudget + non-authority correlation refs
WHERE = same-attempt bound shadow observation only
PRIOR_RESULT_INPUT = FORBIDDEN
RESULT_REPLAY_AS_AUTHORITY = FORBIDDEN
```

The reserved implementation surface remains exactly:

```text
src/mentaury/composition/non_projection_shadow/__init__.py
src/mentaury/composition/non_projection_shadow/contracts.py
src/mentaury/composition/non_projection_shadow/coordinator.py
```

and the frozen public function remains:

```python
def evaluate_non_projection_shadow(
    *,
    context: NonProjectionShadowContext,
) -> NonProjectionShadowObservation:
    ...
```

No broader package, service, worker, scheduler or runtime root is authorized.

---

## 3. Required implementation properties

The next separate implementation PR must preserve all frozen Phase 1 properties:

- immutable typed context/output;
- exact `NPG-v0.1` / `AIE-v0.1` compatibility;
- exactly one `classify_non_projection(...)` call per evaluation attempt;
- no prior `NonProjectionResult` input;
- no fingerprint-as-bearer-token behavior;
- no semantic translation or second decision vocabulary;
- no retry/remediation loop;
- no network/filesystem/database/environment/clock/random/model/retrieval I/O;
- no identity, relationship, Character or M3 read/write;
- no Action Gate, tool, plugin or subprocess integration;
- no persistence and no deployment;
- executable `NRC-T01…NRC-T12` and `NRC-M01…NRC-M10` coverage;
- fail-closed compatibility behavior.

`PASS_ATTRIBUTED` remains:

```text
bounded NPG classification evidence only
≠ truth proof
≠ autobiography
≠ stable identity trait
≠ relationship / commitment / consent authority
≠ capability or Action Gate PASS
≠ retrieval permission
≠ tool / execution permission
≠ M3 authority
≠ deployment permission
```

---

## 4. One-time authorization semantics

```text
OWNER_GO_DECISION = GO
PHASE_2_OWNER_GO = GRANTED
OWNER_GO_SCOPE = NPG-COMP-v0.1_ONLY
IMPLEMENTATION_AUTHORIZATION = GRANTED_FOR_NEXT_SEPARATE_BOUNDED_PHASE_2_IMPLEMENTATION
```

This authorization is single-use. It becomes consumed only by a verified
implementation PR whose exact head matches the frozen contract and passes the
required review/CI gates.

```text
OWNER_GO_GRANTED
≠ IMPLEMENTATION_STARTED
≠ IMPLEMENTATION_COMPLETED
≠ RUNTIME_ACTIVATED
≠ P1_004_ASSIGNED
≠ ACTION_AUTHORITY
```

---

## 5. Explicitly not authorized

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
```

---

## 6. Next-step boundary

The next permitted work is one **separate** bounded implementation milestone:

```text
fresh exact-main compatibility check
→ clean implementation branch
→ exact reserved three-file package only
→ executable contract/adversarial/metamorphic tests
→ exact-head CI
→ Tier A correctness + adversarial review
→ guarded protected merge
→ resulting-main CI
→ completion receipt + status reconciliation
→ Notion sync
→ Owner GO consumed
→ STOP
```

If `NPG-COMP-v0.1`, `NPG-v0.1`, `AIE-v0.1`, API shape, ruleset, CI or writer state
changes before implementation begins:

```text
STOP_AND_RECONCILE
```
