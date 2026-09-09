# Cognitive Orientation View v0.1

**Status:** `RESEARCH_SPECIFICATION_V0_1 · PROPOSED_FREEZE`  
**Scope:** `RESEARCH_ONLY · BOUNDED · NO_RUNTIME_AUTHORITY`  
**Baseline:** `main@501f745a748ac81e839522ee3b22b6311519db07`  
**Frozen C1 blob:** `48ae11f8956cbde85cd270858876c85b8c0d38ba`  
**Evidence:** Issues #183–#191

## 1. Purpose

This document freezes the minimum research-level **Cognitive Orientation View** justified by the bounded O3–O11 semantic sequence.

The view represents what is happening now, what objective is actually active, what materially constrains the situation, what alternatives remain live, which unknowns matter, and what class of bounded next step is justified.

It is not a goal system, planner, scheduler, memory owner, truth owner, or action authority.

## 2. Authority boundary

```text
COGNITIVE_ORIENTATION_VIEW != truth owner
COGNITIVE_ORIENTATION_VIEW != Evidence Gate
COGNITIVE_ORIENTATION_VIEW != Action Gate
COGNITIVE_ORIENTATION_VIEW != runtime authority
COGNITIVE_ORIENTATION_VIEW != persistence owner
COGNITIVE_ORIENTATION_VIEW != Goal Engine
```

Nothing here authorizes tools, retrieval, actions, deployment, persistence, scheduler activity, autonomous retry, belief/identity/relationship mutation, or runtime execution.

`AUTHORIZED_ACTION` remains orthogonal and must never be inferred from orientation state alone.

## 3. Relationship to frozen C1

The view is **additive to** frozen C1. It does not claim that the literal frozen `c1_profile.txt` already contains the new research vocabulary.

Frozen C1 already requires:

```text
1. current task/objective
2. material active constraints
3. meaningful alternatives that remain live
4. decision-relevant consequences
5. critical unknowns
6. whether further discrimination is justified or stop/defer is better
```

O6, O7, and O9 justified additional research-level semantics:

```text
OBJECTIVE_REF
OBJECTIVE_STATUS
```

Therefore:

```text
RESEARCH_VIEW_ADDITIVE_TO_C1 = YES
C1_PROFILE_BYTES_CHANGED_BY_THIS_FREEZE = NO
```

## 4. Minimum representation

```text
OBJECTIVE_REF
  = transient / local / derived

For each OBJECTIVE_REF O:
OBJECTIVE_STATUS(O) ∈ {
  CURRENT_PRIMARY,
  DEFERRED,
  SUPERSEDED,
  COMPLETED
}

Cardinality:
  0..n objectives may occupy each label

+ frozen C1 construction checklist
+ materially relevant referable bounded history
+ coreference from supplied grounding

AUTHORIZED_ACTION
  = separate / orthogonal
```

The cardinality clarification does not imply total ordering, scheduler semantics, concurrent execution, or automatic priority resolution.

If several `CURRENT_PRIMARY` objectives are supplied and their ordering matters but is not supplied, use C1 alternatives/constraints/critical-unknown handling rather than inventing a priority.

## 5. OBJECTIVE_REF

`OBJECTIVE_REF` is a local semantic handle for bounded orientation.

It is:

- transient;
- local to supplied/bounded context;
- derived from supplied grounding;
- able to distinguish two explicitly separate objectives with identical text;
- able to map paraphrases/coreferential mentions to the same objective when context supports that mapping.

It is not:

- a durable UUID;
- a persistent cross-session identity;
- a scheduler key;
- a task-database key;
- an authority token.

If coreference is ambiguous:

```text
COREFERENCE = UNKNOWN
CRITICAL_UNKNOWN = which objective is intended
NEXT_STEP = minimal clarification / discrimination
```

Do not guess.

## 6. Objective statuses

### CURRENT_PRIMARY

The objective is currently primary in bounded orientation.

```text
CURRENT_PRIMARY != EXECUTE_NOW
CURRENT_PRIMARY != AUTHORIZED_ACTION
```

A current-primary objective may still be unable to progress because of a material constraint.

### DEFERRED

The objective is retained but not currently primary.

```text
DEFERRED != CANCELLED
DEFERRED != SCHEDULED_TASK
DEFERRED != PERSISTED
DEFERRED != AUTOMATIC_RESUME
```

Soft and hard defer conditions remain C1 constraints, not separate statuses.

### SUPERSEDED

The objective is no longer current, while its history/provenance remains.

```text
SUPERSEDED != ERASED_HISTORY
SUPERSEDED != FALSE
SUPERSEDED != COMPLETED
```

Replacement by another objective and cancellation-without-successor may both be represented as `SUPERSEDED`; bounded history preserves whether a successor was supplied.

A separate `CANCELLED` status is not justified unless a future counterexample proves that `SUPERSEDED + bounded history` collapses materially different next-step orientation.

### COMPLETED

According to supplied semantic input, the bounded objective is represented as satisfied.

```text
COMPLETED != VERIFIED
COMPLETED != TRUE_IN_THE_WORLD
COMPLETED != Evidence Gate SUPPORTED
COMPLETED != AUTHORIZED_ACTION
COMPLETED != PERSISTED
COMPLETED != RUNTIME_EXECUTION_PROOF
```

If completion is uncertain, preserve the critical unknown and do not assign `COMPLETED`.

Partial component completion does not justify `PARTIALLY_COMPLETED`.

A later reassessment/update request does not erase historical completion; it creates/selects a new current reassessment objective.

## 7. Objective revision

Explicit user revision may change the current objective while the prior objective remains historical context.

```text
PRIOR_OBJECTIVE != CURRENT_OBJECTIVE
HISTORICAL_INTENT != ACTIVE_INTENT
OLD_PLAN_TECHNICALLY_POSSIBLE != OLD_PLAN_CURRENTLY_RELEVANT
REVISION != ERASURE_OF_HISTORY
```

No Goal Revision Engine or persistent objective lifecycle is justified.

## 8. Objective vs proposed means

```text
OBJECTIVE != PROPOSED_MEANS
```

A literal requested method may be only one proposed way to satisfy the actual bounded objective.

Existing C1 alternatives, consequences, constraints, and critical unknowns are used to identify whether the proposed method is actually relevant or whether minimal discrimination is required first.

Orientation never authorizes the method.

## 9. Ambiguity

```text
AMBIGUOUS_INTENT != LICENSE_TO_GUESS
```

Materially different interpretations remain live until minimally discriminated.

Use:

```text
meaningful alternatives
+ critical unknown
+ minimal clarification when needed
```

## 10. Long-gap and cross-session boundary

```text
TIME_GAP != CONTEXT_LOSS
SESSION_BOUNDARY != PERSISTENCE_REQUIREMENT
```

If sufficient grounding is supplied later, a new local ref may be reconstructed.

If identifying grounding is absent:

```text
OBJECTIVE_REF = UNRESOLVED
COREFERENCE = UNKNOWN
```

Do not infer persistent identity.

If a future product requirement demands seamless cross-session resume, reference-bearing information must be available from somewhere. That does not establish that Mentaury owns persistence, retrieval, or stable objective IDs.

## 11. Blocking and constraints

A blocker is situation information, not an objective status.

```text
BLOCKING_CONDITION != OBJECTIVE_STATUS
BLOCKED_PROGRESS != DEFERRED_INTENT
BLOCKER_CLEARED != AUTHORIZED_ACTION
```

An objective may be:

```text
CURRENT_PRIMARY + material blocker
```

or:

```text
DEFERRED + material blocker
```

Existing C1 material constraints, alternatives, consequences, and critical unknowns are sufficient for the tested O11 cases.

No `BLOCKED`, `WAITING`, `PAUSED`, `PENDING`, dependency engine, watcher, or polling contract is justified.

## 12. Attempts, failure, and bounded history

```text
UNSUCCESSFUL_ATTEMPT != OBJECTIVE_STATUS
FAILED_ATTEMPT != SUPERSEDED
FAILED_ATTEMPT != AUTHORIZED_RETRY
SUCCESSFUL_ATTEMPT != COMPLETED_OBJECTIVE
```

Materially relevant attempt outcomes remain **referable bounded history / decision-relevant facts**.

The current evidence does not justify freezing:

```text
FAILED as OBJECTIVE_STATUS
ATTEMPT_RESULT enum
ATTEMPT_REF
ATTEMPT_ID
retry count
retry policy
backoff
retry engine
```

Multiple attempts with different outcomes demonstrate why a singular `ATTEMPT_RESULT(O)` would itself be underspecified.

If a future case proves that ordinary bounded history cannot distinguish a specific prior occurrence that changes the correct next step, test the smallest semantic repair separately.

## 13. Next-step classes

The view may yield a bounded orientation class such as:

```text
DIRECT / ХВАТИТ
DEEPEN / УГЛУБИТЬСЯ
VERIFY
REOPEN
STOP
UNKNOWN
```

These are orientation outcomes only.

They do not mean:

```text
ALLOW ACTION
DENY ACTION
SUPPORTED
CONTRADICTED
```

and do not execute anything.

## 14. Stable distinctions

```text
LITERAL_REQUEST != OBJECTIVE
OBJECTIVE != PROPOSED_MEANS
OBSERVATION != INSTRUCTION
PRIOR_OBJECTIVE != CURRENT_OBJECTIVE
SUPERSEDED != ERASED_HISTORY
CURRENT_INTENT != AUTHORIZATION
OBJECTIVE_STATUS != ACTION_AUTHORITY
CURRENT_PRIMARY != EXECUTE_NOW
DEFERRED != SCHEDULED_TASK
COMPLETED != VERIFIED
COMPLETED != SUPERSEDED
FAILED_ATTEMPT != FAILED_OBJECTIVE
BLOCKING_CONDITION != OBJECTIVE_STATUS
UNKNOWN != FALSE
NOT_AVAILABLE_IN_INPUT != ABSENT_FROM_HISTORY
LOCAL_REF != PERSISTENT_ID
COREFERENCE != MEMORY_WRITE
ORIENTATION != ACTION_GATE
ORIENTATION != EVIDENCE_GATE
RESEARCH_VIEW != RUNTIME_OWNER
```

## 15. Explicitly not justified

Current evidence does not justify:

```text
FAILED as OBJECTIVE_STATUS
BLOCKED as OBJECTIVE_STATUS
CANCELLED as OBJECTIVE_STATUS
SOFT_DEFERRED / HARD_DEFERRED
PARTIALLY_COMPLETED
UNKNOWN as OBJECTIVE_STATUS
frozen ATTEMPT_RESULT contract
ATTEMPT_REF / durable attempt IDs
persistent OBJECTIVE_ID
Goal Engine
Goal Manager
objective lifecycle state machine
retry engine
scheduler
watcher / polling
dependency engine
persistence owner
retrieval owner
new runtime owner
new authority owner
```

Natural-language shorthand may be used descriptively but must not be promoted into a frozen semantic contract without a concrete collapse.

## 16. Evidence chain

```text
#183  O3/O4  objective vs proposed means; intent ambiguity
#184  O5     explicit objective revision
#185  O6     DEFERRED vs SUPERSEDED; Level-2 status freeze; soft/hard residual
#186  O7     local OBJECTIVE_REF / coreference
#187  O8     long-gap / cross-session grounding boundary
#188  O9     COMPLETED status
#189  O10    failed-attempt semantics; corrected to ordinary bounded history
#190  O11    blocked-progress semantics; existing C1 constraints sufficient
#191          consolidation + independent adversarial clarifications
```

Where a first-pass result was later corrected, the later corrective conclusion governs this freeze while earlier comments remain provenance.

## 17. Stop rule

Do not create O12 or extend the vocabulary merely to continue the sequence.

A new fixture is justified only if a concrete pair of states/histories:

1. collapses under this representation;
2. requires materially different bounded next-step orientation;
3. cannot be preserved by frozen C1 + local `OBJECTIVE_REF` + four statuses + materially relevant bounded history;
4. can be repaired by a smaller semantic distinction than a new engine.

Until such a counterexample exists:

```text
JUSTIFIED_STOP = YES
NO_NEW_COGNITIVE_CONTRACT_BY_DEFAULT
O12_JUSTIFIED_NOW = NO
```

## 18. Freeze conclusion

The smallest Cognitive Orientation View justified by O3–O11 is:

```text
OBJECTIVE_REF
  = transient / local / derived

For each OBJECTIVE_REF O:
OBJECTIVE_STATUS(O) ∈ {
  CURRENT_PRIMARY,
  DEFERRED,
  SUPERSEDED,
  COMPLETED
}

Cardinality:
  0..n per label

+ frozen C1 construction checklist
+ materially relevant referable bounded history
+ coreference from supplied grounding

AUTHORIZED_ACTION
  = separate / orthogonal
```

This is a **research specification**, not a runtime component.

No new engine, persistence layer, scheduler, retrieval owner, runtime owner, or authority owner is justified by this freeze.