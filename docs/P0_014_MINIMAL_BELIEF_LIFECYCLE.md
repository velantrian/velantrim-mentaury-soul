# 🧠 P0-014 — Minimal Belief Lifecycle

```text
Status: MERGED IN MAIN · PR AND MAIN CI PASS
Implementation base: main@024deeec456549584273c79ccfc5e1442d480add
Merge SHA: 3ff90816b8d095987a8adcdc2cb633c128877212
Scope: minimal M2 belief lifecycle only
P0-015 Evidence Gate: NOT INCLUDED
M3 identity writes: NOT AUTHORIZED
Domain runtime wiring: NOT AUTHORIZED
```

## 🎯 Goal

P0-014 adds the smallest evidence-referenced belief lifecycle that can be
replayed deterministically by P0-013 without treating stored belief state as
truth.

```text
CommandEnvelope + current immutable belief projection
→ pure lifecycle decision
   ├── accepted domain PendingEvent
   └── rejected non-state audit PendingEvent
→ explicit caller persistence
→ BeliefReducer v1
→ R1 deterministic replay
```

The lifecycle is a decision and projection layer. It does not start a worker,
register an HTTP route, write Canon, mutate identity or automatically persist a
decision.

## 🧩 Commands

```text
CREATE_BELIEF
ATTACH_EVIDENCE
REGISTER_CONTRADICTION
REVISE_BELIEF
```

Every command targets exactly one stream:

```text
belief:<belief_id>
```

`CommandEnvelope.authority` is preserved as provenance only. P0-014 does not
prove that the referenced capability lease exists or grants the operation.

## 📜 Domain events

| Event | State effect |
|---|---|
| `BELIEF_CREATED` | creates revision 1 in `hypothesis` status |
| `EVIDENCE_ATTACHED` | adds one unique reference on the `for` or `against` side |
| `CONTRADICTION_REGISTERED` | preserves contradiction details and marks the belief `contested` |
| `BELIEF_REVISED` | appends a new immutable revision and may address known contradictions |

The projection preserves:

```text
belief_id
statement
claim_type
status
revision
origin_event_id
evidence_for[]
evidence_against[]
contradictions[]
history[]
```

Revisions never erase earlier statement/status history. Addressed
contradictions remain visible with the revision that addressed them. Leaving
`contested` for a non-contested/non-unresolved status requires every open
contradiction to be explicitly addressed by that revision.

## 🧾 Audit decisions

Rejected commands produce a proposed non-state audit event and no domain event:

```text
COMMAND_REJECTED
BELIEF_REVISION_REJECTED
```

The shared strict audit schema is also available for explicit outer-boundary
failures:

```text
AUTHORITY_CHECK_FAILED
INVARIANT_CHECK_FAILED
```

The pure lifecycle does not persist audit events automatically. The caller must
make a separate explicit append decision. Therefore a rejected command cannot
silently mutate domain state.

Audit payloads distinguish three concurrency concepts rather than conflating
them: `expected_stream_version` from the storage CAS envelope,
`current_belief_revision` from the projection and
`requested_belief_revision` from a revision command payload.

## 🧠 Status model

```text
hypothesis
provisional
supported
contested
contradicted
unresolved
superseded
```

`supported` and `contradicted` exist in the shared status vocabulary but are
deliberately unreachable in P0-014. Both the lifecycle decision and reducer reject
a direct transition to either status until P0-015 defines a governed Evidence
Gate receipt and event contract.

`superseded` is terminal for this minimal lifecycle. A later lifecycle may add a
separate reactivation event only through a new reviewed specification.

`REGISTER_CONTRADICTION` moves a non-contradicted belief to `contested` but does
not increment the belief revision. Statement/status revisions occur only through
`BELIEF_REVISED` and increment the revision exactly by one.

## 🔗 Evidence-reference boundary

P0-014 verifies only structural reference integrity:

- an evidence reference is a non-empty unique string;
- the reference is attached to the same belief before contradiction/revision;
- a revision contains at least one attached evidence reference;
- addressed contradiction IDs must already exist.

It does **not** verify:

- that evidence material exists;
- source authenticity or provenance chain;
- evidence quality, relevance or freshness;
- contradiction strength;
- minimum evidence thresholds;
- whether a belief deserves `supported` status.

P0-014 therefore rejects `supported` and `contradicted` through
`EVIDENCE_GATE_REQUIRED`; a caller cannot bypass this by appending a direct
`BELIEF_REVISED` event because the v1 reducer enforces the same status, terminal,
open-contradiction and no-effect policy.

Those controls belong to **P0-015 Evidence Gate**. Therefore:

```text
status = supported ≠ truth
attached evidence_ref ≠ verified evidence
lifecycle acceptance ≠ epistemic approval
```

## 🔁 R1 compatibility

`BeliefReducer` is a versioned neutral reducer profile:

```text
reducer_id      mentaury-belief-projection
reducer_version 1
```

It supports only the four state-affecting belief event/schema pairs. Audit
events are non-state and are skipped by R1 while remaining in immutable stream
history.

The integration test commits:

```text
BELIEF_CREATED
→ rejected duplicate command audit
→ EVIDENCE_ATTACHED
```

and proves full replay equals a verified creation snapshot plus the tail.

## 🛡️ Rejection model

Controlled rejection codes include:

- invalid command or stream target;
- duplicate creation/evidence/contradiction;
- missing belief, terminal superseded belief, or terminal Evidence
  Gate-owned belief (`supported`/`contradicted`);
- unknown evidence/contradiction references;
- revision conflict;
- invalid status transition;
- no-effect revision.

`ATTACH_EVIDENCE`, `REGISTER_CONTRADICTION` and `REVISE_BELIEF` all reject with
`EVIDENCE_GATE_OWNED_BELIEF` once a belief has reached `supported` or
`contradicted`, mirroring the P0-015 reducer boundary so a `decide()`
acceptance can never produce an event that the reducer later refuses to
project.

A rejection is not an exception from ordinary lifecycle policy. Malformed
projection state or reducer history remains an invariant error and fails closed.

## ⚖️ Preserved boundaries

```text
Belief projection ≠ truth
Belief status ≠ calibrated confidence
Evidence reference ≠ verified evidence
Command authority reference ≠ authorized capability
Rejected audit proposal ≠ automatically persisted audit
P0-014 ≠ P0-015 Evidence Gate
P0-014 ≠ M3 identity update
P0-014 ≠ autonomous learning
P0-014 ≠ domain runtime authorization
```

## ✅ Validation evidence

```text
PR:                  #29
Final tested head:   fe3ae74d4ef92fc06ab1bee4def88066ded402a5
Merge SHA:           3ff90816b8d095987a8adcdc2cb633c128877212
PR workflow run:     31090898077
Main push run:       31091006506
Python:              CPython 3.13.14
Full pytest:         208 passed on PR and main
Compileall:          PASS
Changed files:       7 intended files
Review threads:      0
Review:              4873291547
```

P0-015 was subsequently implemented as a separate reviewed milestone. P0-014
history and reducer-v1 boundaries remain unchanged; the gated reducer is a new
versioned profile rather than a rewrite of prior events.
