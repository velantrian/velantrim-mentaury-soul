# INIT-01 — Return of `UNRESOLVED` beliefs to active work (research spec)

```text
Status: RESEARCH NOTE · NON-CANONICAL · DOCS_ONLY · Tier C (GOVERNANCE §3.4)
Authority: NONE — grants no runtime, backend, roadmap, Canon, truth or action authority
Implementation: NOT SELECTED · NOT AUTHORIZED (any code here is Tier A and needs an Owner GO)
Source: Mentaury-Kernel docs/consciousness-architecture/05-init-01-unresolved-initiative.md
Date: 2026-10-14
```

## 1. Question

A belief in status `unresolved` is currently inert: nothing in the lifecycle brings it
back. INIT-01 describes, as rules only, **when and how such a belief may be proposed for
re-examination** ("initiative") without creating any new authority.

## 2. Grounding in the existing lifecycle (read-only reference)

From `src/mentaury/beliefs/contracts.py` (`_P0_014_ALLOWED_TRANSITIONS`) and
`reducer.py` / `lifecycle.py`:

| From | Allowed by P0-014 reducer |
|---|---|
| `unresolved` | `hypothesis`, `provisional`, `contested`, `superseded` (or same status) |
| `hypothesis` / `provisional` / `contested` | → `unresolved` allowed (return path) |
| any | → `supported` / `contradicted` only via a future Evidence Gate receipt (`belief_status_requires_evidence_gate`) |
| `supported`, `contradicted`, `superseded` | terminal for P0-014 — no INIT-01 re-entry |

Further constraints INIT-01 must respect unchanged:

- every revision cites evidence **already attached** (`evidence_refs ⊆ evidence_for ∪ evidence_against`);
- `previous_revision` / `previous_status` must match the projection; `new_revision = revision + 1`;
- leaving `contested` (except to `contested`/`unresolved`) requires addressing every open contradiction;
- a contradiction always yields `contested`;
- a revision with no effect is rejected.

INIT-01 adds **no new status, event type or transition**.

## 3. Re-activation triggers (candidate)

A belief in `unresolved` becomes a *candidate for review* (not a revision) when:

1. **New evidence** — an `evidence_attached` event lands on the belief.
2. **Contradiction** — a `contradiction_registered` event references it (reducer moves it to `contested`; INIT-01 only notes it).
3. **Decision relevance** — an external, explicitly recorded decision context cites the belief (reference only; INIT-01 never initiates the decision).
4. **Time / review** — a review interval elapses since the last revision (deterministic, from event time; no wall-clock side effects).

No trigger fires on its own reasoning output alone (no self-feeding loop).

## 4. Priority ordering (candidate)

Deterministic ordering of candidates, highest first:

1. open contradiction present;
2. decision relevance;
3. count of new evidence refs since last revision;
4. age since last revision (older first);
5. tie-break: `belief_id` lexical.

Weights are research parameters, not Canon.

## 5. Budget

- fixed max candidates per review cycle (e.g. N = 3);
- each belief at most once per cycle; cool-down after a review that ends `unresolved`;
- budget exhaustion is recorded, never silently dropped.

## 6. Outcomes of a review

A review produces at most one ordinary `belief_revised` proposal going through the
existing `BeliefLifecycle.decide` → reducer path, with outcome one of:

- `unresolved` → `hypothesis` / `provisional` / `contested` (with attached evidence);
- `unresolved` → `superseded`;
- **return to `unresolved`**: no change is proposed; the belief stays `unresolved` and a cool-down applies;
- `supported` / `contradicted`: not reachable via INIT-01; only via Evidence Gate.

Rejections (`INVALID_STATUS_TRANSITION`, `REVISION_CONFLICT`, `UNKNOWN_EVIDENCE_REF`, …) are kept as-is.

## 7. Trace / receipt

Each review cycle records (as research artifact, not a new event type):
trigger(s), ordering inputs, budget used, chosen candidate, proposed command or
"no proposal", and the lifecycle decision / rejection code. Replaying the same event
log must reproduce the same candidates and ordering.

## 8. Non-goals

- no runtime, scheduler, daemon or background loop;
- no action, tool execution or external effect;
- no authority, lease or Canon promotion; no new statuses/events;
- no bypass of Evidence Gate; no identity/"mine" semantics;
- no change to `src/`, tests, schemas or CI.

## 9. Open questions

- who records "decision relevance" without granting it authority?
- review interval and budget values; cool-down length;
- does a review-ending-`unresolved` need its own receipt type (would be Tier A)?
