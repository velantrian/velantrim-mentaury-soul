<!-- Source: [../MENTAURY_P0_IMPLEMENTATION_PLAN.md](../MENTAURY_P0_IMPLEMENTATION_PLAN.md). This mirror is not independent authority. -->

# 🛠️ Mentaury P0 Implementation Plan v0.3

**Status:** `READY_FOR_EVENT_SUBSTRATE_V3 IMPLEMENTATION`  
**Canon:** `SUBSTRATE-NEUTRAL`  
**First profile:** `Python + SQLite`  
**Working branch:** `agent/p0-event-substrate-v3`

---

# 1. 🎯 P0 Goal

P0 does not implement a complete digital identity. It builds a minimum verifiable continuity foundation.

P0 must prove that the system can:

- distinguish the intention from the fact that occurred;
- verify authority, schema, and domain invariants;
- atomically record a complete event batch;
- preserve committed events as physically immutable;
- remove protected content without rewriting historical fact;
- detect corruption of an event, payload digest, chain, and stream metadata;
- safely handle retry and concurrent writers;
- restore state through deterministic replay;
- preserve old belief versions and contradictions;
- audit significant rejected decisions;
- reproduce the result in an independent environment.

```text
Command
→ Authority + Schema + Invariant Validation
→ Decision
   ├── Reject → Decision Audit · state unchanged
   └── Accept → Fingerprinted Pending Event Batch
                     ↓
                BEGIN IMMEDIATE
                     ↓
                Atomic Append
                     ↓
                R0 Integrity
                     ↓
                R1 Replay
```

---

# 2. 🧪 Experimental Basis

## EXP-P0-v1

```text
13 tests reproduced
```

Identified:

- stored hash was not recomputed;
- payload/hash tampering was not detected;
- redaction could complete halfway;
- the version check occurred before the write transaction.

## EXP-P0-v2

```text
21 tests reproduced
```

Fixed:

- hash recomputation;
- payload/hash tampering detection;
- redaction rollback;
- `BEGIN IMMEDIATE` concurrency boundary;
- full UUID;
- canonical JSON profile;
- basic event/schema and idempotency conflict checks.

Remaining:

- physical event immutability;
- event-aware idempotency;
- same-stream redaction;
- `stream_meta` integrity;
- real atomic batch;
- structural payload validation;
- full Event Envelope storage boundary.

EXP-P0-v2 is used as a **patch source**, but is not transferred directly to `main`.

---

# 3. ⚖️ P0 invariants

## P0-INV-1 — Command ≠ Event

A Command expresses an intention. An Event records a confirmed fact.

## P0-INV-2 — Rejection ≠ Disappearance

A rejection does not change domain state, but a high-risk or identity-relevant decision remains in the audit.

## P0-INV-3 — Immutable History

A committed event row is not changed. Redaction acts only on external payload material.

## P0-INV-4 — Atomicity

Either the entire event batch and associated metadata updates are recorded, or nothing is recorded.

## P0-INV-5 — Replay Consistency ≠ Truth

Replay proves the technical reproducibility of state transitions, but not the truth of belief.

## P0-INV-6 — Implementation Profile ≠ Canon

Python and SQLite are replaceable as the first profile.

## P0-INV-7 — Style ≠ Epistemic State

Character/voice do not change claim status, evidence weight, uncertainty class, or the authority decision.

## P0-INV-8 — Identity Change Requires Governance

The M3 Identity Profile is not updated directly from M0, a single episode, or a single response.

---

# 4. 📐 Execution Contract

## 4.1 Command Envelope

```yaml
command:
  command_id: "0192..."
  command_type: "CREATE_BELIEF"
  command_schema: "create-belief/v1"
  target_stream: "belief:B-204"
  expected_stream_version: 0
  issued_at: "2026-08-04T06:00:00Z"
  issuer:
    type: "operator"
    id: "operator:primary"
  authority:
    capability_lease_id: "CAP-81"
    capability_revision: 2
  correlation_id: "CORR-12"
  idempotency_key: "create-belief:B-204:request-1"
  payload:
    statement: "..."
    claim_type: "unspecified"
```

The command stores a link to the authority record, not a trusted copy of permissions.

## 4.2 Pending Event

```yaml
pending_event:
  event_type: "BELIEF_CREATED"
  payload_schema: "belief-created/v1"
  affects_domain_state: true
  payload:
    belief_id: "B-204"
    statement: "..."
    claim_type: "unspecified"
```

## 4.3 Idempotency Fingerprint

The fingerprint is calculated from:

```text
canonical command identity
+ target stream
+ expected version
+ ordered pending event batch
+ each event type
+ each payload schema
+ each payload digest
+ affects_domain_state flags
```

Behavior:

```text
same key + same fingerprint
→ ALREADY_APPLIED

same key + changed payload/type/schema/count/order
→ IDEMPOTENCY_CONFLICT
```

---

# 5. 🛡️ Immutable Event Substrate

## 5.1 Event Envelope

```yaml
event:
  event_id: "0192..."
  event_type: "BELIEF_CREATED"
  envelope_schema_version: 1
  payload_schema: "belief-created/v1"
  stream_id: "belief:B-204"
  stream_version: 1
  batch_id: "BATCH-0192..."
  batch_index: 0
  batch_size: 1
  occurred_at: "2026-08-04T06:00:00Z"
  recorded_at: "2026-08-04T06:00:00.120Z"
  producer:
    component: "belief-command-handler"
    version: "0.1.0"
  initiator:
    type: "operator"
    id: "operator:primary"
  authority:
    capability_lease_id: "CAP-81"
    capability_revision: 2
  causation_id: "CMD-0192..."
  correlation_id: "CORR-12"
  affects_domain_state: true
  payload_digest: "sha256:..."
  payload_ref: "PAYLOAD-0192..."
  previous_hash: "sha256:..."
  event_hash: "sha256:..."
```

All hash fields must be stored, recoverable, immutable, and unambiguously serializable.

## 5.2 Storage Model

```text
events
├── immutable envelope
├── payload_digest
├── payload_ref
├── previous_hash
└── event_hash

event_payloads
├── payload_ref
├── payload_bytes / encrypted_blob
├── created_at
└── redacted_at

stream_meta
├── current_version
└── last_event_hash

idempotency_records
├── producer
├── idempotency_key
├── fingerprint
└── resulting_event_ids
```

`events` is never changed by redaction.

---

# 6. 🔤 MENTAURY_CANONICAL_JSON_V1

```text
Encoding       = UTF-8
Object keys    = deterministic order
Whitespace     = absent
Timestamp      = RFC 3339 UTC
Float          = forbidden
NaN/Infinity   = forbidden
Large integers = restricted or encoded as strings
event_hash     = excluded from hash input
previous_hash  = included
```

The following are additionally fixed:

- Unicode policy;
- safe integer range;
- lone surrogate rejection;
- Decimal encoding rules;
- timestamp precision;
- conformance vectors.

This is a proprietary restricted profile, not a claim of full RFC 8785 implementation.

---

# 7. 📋 Event and Payload Schema Registry

```python
SUPPORTED_EVENT_SCHEMAS = {
    "BELIEF_CREATED": {"belief-created/v1"},
    "EVIDENCE_ATTACHED": {"evidence-attached/v1"},
    "CONTRADICTION_REGISTERED": {"contradiction-registered/v1"},
    "BELIEF_REVISED": {"belief-revised/v1"},
    "REDACTION_RECORDED": {"redaction-recorded/v1"},
}
```

Each payload schema has a structural validator.

Fail-closed requirements:

- unknown event type;
- unsupported pair;
- missing required field;
- forbidden extra field, if the schema is strict;
- invalid identifier;
- invalid timestamp;
- unsupported numeric representation.

---

# 8. ⚙️ Real Atomic Batch and Concurrency

```text
BEGIN IMMEDIATE
├── lookup idempotency record
├── compare full fingerprint
├── read stream_meta
├── compare expected version
├── validate complete ordered event batch
├── allocate versions and hashes
├── insert all immutable events
├── insert all payload records
├── update stream_meta
├── store idempotency result
COMMIT
```

On any error:

```text
ROLLBACK
```

Controlled results:

```text
APPENDED
ALREADY_APPLIED
IDEMPOTENCY_CONFLICT
VERSION_CONFLICT
SCHEMA_REJECTED
AUTHORITY_REJECTED
TARGET_STREAM_MISMATCH
INTEGRITY_ERROR
BUSY_RETRY_EXHAUSTED
```

Required:

- `busy_timeout`;
- controlled `SQLITE_BUSY` handling;
- no partial payload writes;
- no partial event batch;
- no metadata-only commit;
- supported SQLite runtime gate.

---

# 9. 🗑️ Atomic Same-Stream Redaction

```text
BEGIN IMMEDIATE
├── validate authority
├── load target event
├── verify command.target_stream == target_event.stream_id
├── verify audit stream == target_event.stream_id
├── check expected version
├── check event-aware idempotency
├── delete payload blob or destroy encryption key
├── append REDACTION_RECORDED to same stream
├── update stream_meta
COMMIT
```

Prohibited:

- `UPDATE events SET payload = NULL`;
- recalculating the original event hash;
- recording the audit event in another stream;
- deleting the payload before version/authority checks;
- completing redaction without an audit event.

---

# 10. 🔐 R0 Integrity Verification

R0 performs:

```text
1. reconstruct full immutable envelope
2. validate event/schema pair
3. validate structural payload when present
4. recompute payload digest when payload exists
5. recompute event_hash
6. compare stored and recomputed hash
7. verify previous_hash
8. verify stream_version sequence
9. verify batch completeness and order
10. verify stream_meta tail consistency
11. detect missing event or version gap
12. report first actionable integrity failure
```

R0 checks:

```text
stream_meta.current_version == tail.stream_version
stream_meta.last_event_hash == tail.event_hash
```

For an empty stream:

```text
current_version = 0
last_event_hash = GENESIS_HASH
```

R0 integrity is not proof of the epistemic truth of payload.

---

# 11. 🔁 R1 Reducer and State Replay

Transition to R1 is permitted only after passing the complete adversarial R0 Gate.

```python
new_state = reduce_belief(old_state, event)
```

The reducer must be:

- pure;
- deterministic;
- versioned;
- network-free;
- clock-free;
- randomness-free or seed-recorded;
- fail-closed for unknown event/schema;
- safe with immutable inputs;

R1 check:

```text
state_hash(full replay)
==
state_hash(snapshot + tail replay)
```

Snapshot is an accelerator, not a source of truth.

---

# 12. 🔎 Minimal Belief Lifecycle

## Commands

```text
CREATE_BELIEF
ATTACH_EVIDENCE
REGISTER_CONTRADICTION
REVISE_BELIEF
```

## Domain Events

```text
BELIEF_CREATED
EVIDENCE_ATTACHED
CONTRADICTION_REGISTERED
BELIEF_REVISED
```

## Audit Decisions

```text
COMMAND_REJECTED
BELIEF_REVISION_REJECTED
AUTHORITY_CHECK_FAILED
INVARIANT_CHECK_FAILED
```

Flow:

```text
CREATE_BELIEF
→ BELIEF_CREATED
→ EVIDENCE_ATTACHED
→ CONTRADICTION_REGISTERED
→ REVISE_BELIEF
   ├── BELIEF_REVISION_REJECTED
   └── BELIEF_REVISED
→ R0
→ R1
```

After revision, the old version, evidence, and contradiction remain available.

---

# 13. 🧬 M3 Identity Update Experiment

M3 is not part of the first belief vertical slice, but its governance contract is fixed before future implementation.

```text
M1/M2 pattern
→ M3_CHANGE_CANDIDATE
→ longitudinal evidence
→ drift analysis
→ CR2 review
→ IDENTITY_PROFILE_UPDATED
   or IDENTITY_UPDATE_REJECTED
```

One episode or one response cannot directly change M3.

---

# 14. 🎭 Scenario Evaluation

The Scenario Checker remains an experiment.

```yaml
experimental: true
advisory_only: true
merge_blocking: false
```

Three axes:

1. **Policy tests** — mandatory invariants.
2. **Robustness tests** — paraphrase, negation, multilingual, and adversarial forms.
3. **State tests** — actual ledger/state mutation.

## MT-STYLE-001

```text
same meaning + different style
→ same claim status
→ same confidence
→ same evidence requirements
→ same contradiction set
→ same authority decision
```

Transition to merge-blocking is possible only after:

```text
benchmark corpus
→ blinded independent labels
→ baseline comparison
→ FP/FN report
→ governance review
```

---

# 15. 🔍 Open Question Scheduler

Contradiction does not always create an open question.

```text
CONTRADICTION_REGISTERED
→ unresolved analysis
   ├── claim resolved → no question
   └── uncertainty remains → OPEN_QUESTION_CREATED
```

Compared policies:

```text
random
FIFO
depth-only
novelty-only
combined
```

Metrics:

- starvation;
- resolved questions;
- closed inconclusive;
- barren cycles;
- CPU/wall time;
- memory;
- emitted events;
- capability calls.

---

# 16. 🚧 External Quarantine Gate

Before any transfer of results to Titan, Crystal, or Native Kernel:

```text
Research Export Package
→ Quarantine
→ Human Review
→ RFC
→ Independent Reimplementation
→ Target-System Tests
```

Algorithms, fixtures, aggregate metrics, failure modes, reproducible code, manifest, and hashes are permitted.

Self-state, autobiography, character state, internal goals, private relationships, capability state, and identity mutation history are prohibited.

---

# 17. 🧪 Acceptance Test Matrix

## Integrity

1. Payload tampering causes R0 failure.
2. Payload digest tampering is detected.
3. Event hash tampering is detected even for a single event.
4. Previous hash corruption is detected.
5. Immutable metadata tampering is detected.
6. A stream version gap is detected.
7. A missing event is detected.
8. `stream_meta.current_version` tampering is detected.
9. `stream_meta.last_event_hash` tampering is detected.
10. The full immutable envelope is recoverable.

## Schema

11. Event/schema mismatch is rejected.
12. Missing required payload field is rejected.
13. Forbidden payload field is rejected in strict schema.
14. Unsupported numeric value is rejected.

## Atomicity

15. Multi-event batch commit preserves all events.
16. Failure inside batch leaves zero events.
17. Payload write failure rolls back event rows.
18. Metadata update failure rolls back the entire batch.

## Idempotency

19. Same key + same command + same batch → `ALREADY_APPLIED`.
20. Same key + changed payload → `IDEMPOTENCY_CONFLICT`.
21. Same key + changed event type → `IDEMPOTENCY_CONFLICT`.
22. Same key + changed schema → `IDEMPOTENCY_CONFLICT`.
23. Same key + changed event count/order → `IDEMPOTENCY_CONFLICT`.

## Concurrency

24. Two writers produce one `APPENDED` and one controlled `VERSION_CONFLICT`.
25. `SQLITE_BUSY` exhaustion returns a controlled result.
26. No duplicate stream version appears.

## Redaction

27. The historical event row remains byte-for-byte unchanged.
28. The payload is removed only from the Payload Store.
29. `REDACTION_RECORDED` is appended to the same stream.
30. Cross-stream redaction is rejected.
31. A stale version leaves the payload untouched.
32. Audit append failure rolls back payload deletion.
33. The original event hash remains verifiable after redaction.

## Replay and Belief

34. The reducer is deterministic.
35. Full replay equals snapshot + tail replay.
36. A rejected revision does not change state.
37. The previous belief version is reconstructable.
38. The contradiction survives revision.

## Character and Identity Contracts

39. Style variation does not change epistemic status.
40. Style variation does not change the authority decision.
41. A single episode cannot update M3.
42. An M3 update requires a CR2 receipt and preservation of the previous version.

---

# 18. 🧊 Evidence Gate

```text
FREEZE             → mechanism confirmed
ITERATE            → promising, but requires fixes
RETAIN_EXPERIMENTAL → retain without canonization
REJECT             → mechanism violates invariants or has not shown benefit
```

Until the Gate is passed, it is prohibited to declare the Event Substrate validated.

---

# 19. 🔨 Commit Sequence

| Commit | Content |
|---|---|
| `P0-001` | Project skeleton, typing, dependency lock, environment manifest |
| `P0-002` | CommandEnvelope, EventEnvelope, PendingEvent |
| `P0-003` | Canonical JSON and conformance vectors |
| `P0-004` | Immutable events and external Payload Store |
| `P0-005` | Structural event/schema validators |
| `P0-006` | Real atomic multi-event batch |
| `P0-007` | Event-aware idempotency fingerprint |
| `P0-008` | Transactional concurrency and busy handling |
| `P0-009` | Full R0 and stream metadata verification |
| `P0-010` | Atomic same-stream redaction |
| `P0-011` | Adversarial integrity test suite |
| `P0-012` | GitHub Actions CI |
| `P0-013` | Pure reducer and R1 replay |
| `P0-014` | Minimal Belief Lifecycle |
| `P0-015` | Evidence Gate report |

Each commit must leave the branch green.

---

# 20. 🏁 P0 Completion Criterion

P0 is complete when an independent executor can perform:

```text
CREATE_BELIEF
→ validate authority and schema
→ produce ordered pending event batch
→ fingerprint command + batch
→ atomic append
→ independently recompute R0
→ attach evidence
→ register contradiction
→ revise or reject
→ preserve decision audit
→ rebuild through R1
→ compare state hashes
→ redact payload without changing event
→ verify same-stream audit
→ detect intentional corruption
→ reproduce the same result
```

Final formula:

```text
Intention is separated from fact.
The fact is recorded atomically.
The historical row is immutable.
Content can be deleted without rewriting the fact.
Retry does not mask another mutation.
Cross-stream change is prohibited.
Hash, chain, and stream metadata are verified.
State is reproducible.
Identity change is governed.
Style does not substitute for truth.
```