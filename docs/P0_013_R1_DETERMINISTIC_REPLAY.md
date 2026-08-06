# 🔁 P0-013 — R1 Deterministic Replay

```text
Status: IMPLEMENTATION PR
Base: main@dda1604253a49f0d88c77d01491a44cc3f09fe53
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
2. run bounded R0 verification on the complete stream;
3. verify snapshot reducer, stream, version and event-hash anchor;
4. recompute the snapshot state hash;
5. replay the complete stream from a canonical initial state;
6. compare the supplied snapshot state with the full-replay checkpoint state;
7. replay the tail from the supplied snapshot;
8. compare canonical final bytes and state hashes.

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

Full replay and snapshot-tail replay each operate under the declared bound.
P0-013 adds no unbounded scan, background worker or automatic startup replay.

## 🧪 Executable matrix

The P0-013 tests cover:

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
- explicit resource-budget failure.

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
