# 🔁 P0-013 — R1 Deterministic Replay

```text
Status: FINAL CANDIDATE · EXACT-HEAD CI REQUIRED
Base: main@dda1604253a49f0d88c77d01491a44cc3f09fe53
Hardened lineage through: e26d2045cd383e0e865a7e82e60566b63d8d6c92
Scope: neutral replay framework only
P0-014 belief lifecycle: NOT INCLUDED
Snapshot persistence: NOT INCLUDED
Domain runtime: NOT AUTHORIZED
```

## 🎯 Goal

R1 proves that a versioned pure reducer reaches the same canonical projection
state through two paths:

```text
R0-verified complete stream
→ initial state
→ full replay
→ final state hash

independently supplied snapshot
→ verify reducer identity/version
→ verify stream and event-hash anchor
→ compare snapshot state with full replay at checkpoint
→ replay verified tail
→ final state hash
```

The required invariant is:

```text
state_hash(full replay)
==
state_hash(verified snapshot + tail replay)
```

A snapshot is an accelerator candidate and portability artifact. It is never a
source of truth and cannot replace unavailable state-affecting history.

## 🧱 Neutral contracts

### Reducer

A reducer declares:

```text
reducer_id
reducer_version
supported_event_schemas: frozenset[(event_type, payload_schema)]
initial_state()
apply(immutable_state, event, immutable_payload)
```

The reducer contract is deliberately neutral. P0-013 does not introduce
belief, identity, relationship, character or world-model event types.

### Snapshot

A snapshot records:

```text
reducer identity and version
stream_id
through_stream_version
through_event_hash
canonical projection state
state_hash
```

The state hash is domain-separated:

```text
SHA-256("MENTAURY_R1_STATE_V1\0" || canonical_state_bytes)
```

## 🛡️ Verification order

R1 performs:

1. validate reducer identity, version and supported schema declarations;
2. open one SQLite read snapshot for all verification reads;
3. run bounded R0 verification on the complete stream inside that snapshot;
4. capture the same verified event count/tail metadata before replay;
5. verify snapshot reducer, stream, version and event-hash anchor;
6. recompute the snapshot state hash and apply state-size bounds;
7. replay the complete stream from a canonical bounded initial state;
8. recheck each replayed payload digest against its immutable envelope;
9. compare the supplied snapshot state with the full-replay checkpoint state;
10. replay the tail from the supplied snapshot;
11. compare canonical final bytes and state hashes.

R0 failure stops R1. R1 does not reinterpret an R0 failure.

## 🔬 Reducer determinism checks

For every state-affecting event, the engine:

```text
clone immutable state and payload twice
→ call reducer twice with identical logical inputs
→ canonicalize both returned states
→ compare canonical bytes and hashes
```

The engine rejects:

- unknown state-affecting event/schema pairs;
- reducers that reuse the input state object;
- reducer exceptions;
- noncanonical reducer states;
- different outputs for identical inputs;
- invalid initial state;
- undeclared or malformed reducer contracts.

Dual execution detects observable nondeterminism. It does not prove the absence
of hidden side effects and is not a process sandbox.

## 🗑️ Redaction boundary

Governed redaction may pass R0 because immutable event provenance and same-stream
audit evidence remain valid. R1 has a different requirement: it needs payload
material for every state-affecting transition in the full replay path.

```text
state-affecting payload unavailable
→ PAYLOAD_UNAVAILABLE
→ R1 FAIL
```

A later snapshot cannot hide the missing transition. Recovery from intentionally
removed state material requires a separately governed portable-state or
cryptographic-erasure design; P0-013 does not invent one.

Non-state-affecting events may be skipped by the reducer while remaining valid
snapshot anchors.

## 📦 Resource boundary

The caller supplies `VerificationBudget` limits for:

- event count;
- one payload size;
- total payload material per replay path.

The caller also supplies `ReplayStateBudget` limits for:

- one canonical projection state;
- cumulative canonical state material produced per replay path.

Full replay and snapshot-tail replay each operate under the declared bounds.
P0-013 adds no unbounded scan, background worker or automatic startup replay.

## 🧪 Executable matrix

The P0-013 suite contains **22 replay tests** covering:

- full replay equals snapshot + tail;
- genesis and empty-stream snapshots;
- non-state event checkpoint anchors;
- reducer identity/version mismatch;
- stream, checkpoint and anchor mismatch;
- tampered snapshot hash;
- self-consistent but false snapshot state;
- unknown state-affecting schema;
- observable reducer nondeterminism;
- input-state reuse and mutation attempts;
- invalid initial state and malformed reducer contract;
- R0 prerequisite failure;
- governed redaction with unavailable state payload;
- explicit event/payload and reducer-state resource-budget failure;
- one SQLite read snapshot across R0, event capture and payload replay;
- concurrent append semantics with an explicitly reported verified prefix;
- stream-stability capture after R0;
- replay-time payload digest verification.

## ✅ Hardened validation checkpoint

Temporary self-cleaning run `31086784452` validated the production, test and
specification tree through `e26d2045cd383e0e865a7e82e60566b63d8d6c92`:

```text
CPython 3.13.14            → PASS
locked install + pip check → PASS
structural validator       → PASS
full pytest                → 184 passed
compileall                 → PASS
temporary files            → removed from final diff
```

The final owner-authored documentation checkpoint must pass retained
`Mentaury CI` on its exact immutable head before merge.

## ⚖️ Preserved boundaries

```text
R1 PASS ≠ epistemic truth
R1 PASS ≠ reducer correctness for real-world meaning
R1 PASS ≠ hidden-side-effect proof
R1 PASS ≠ snapshot persistence authorization
R1 PASS ≠ authority validation
R1 PASS ≠ P0-014 belief lifecycle
R1 PASS ≠ domain runtime authorization
```

All R0, event, metadata and payload reads occur under one SQLite read snapshot.
A concurrent append after that snapshot may complete in WAL mode, but it is not
silently included. A successful report records the exact captured stream version
and tail event hash so callers do not confuse a verified immutable prefix with an
open-ended claim about future appends.

R1 verifies deterministic state reconstruction for one declared reducer and one
R0-verified stream. It does not establish cross-stream transaction semantics,
snapshot signing, distributed consensus, deployment compatibility or user-data
retention policy.

## ➡️ Next controlled milestone

After P0-013 is merged, validated by retained CI and synchronized:

```text
P0-014 → Minimal Belief Lifecycle
```

P0-014 may define belief commands/events and use the neutral R1 framework, but
must not weaken reducer versioning, snapshot verification or R0 prerequisites.
