<!-- Source: [Russian original](../EXPERIMENT_LOG.md). This English mirror is not independent authority. -->

# 🔬 Mentaury P0 — Experiment & Audit Ledger

**Status:** `RESEARCH RECORD · NON-CANONICAL IMPLEMENTATIONS`  
**Purpose:** preserve a reproducible history of experimental prototypes, audits, fixes, and Evidence Gate decisions.

---

## 🧭 Ledger Rule

Experimental code does not become a canonical implementation merely because its tests pass.

```text
code exists
≠ invariant proven

tests pass
≠ complete adversarial coverage

replay works
≠ knowledge is true
```

For each experiment, the following are recorded:

- artifact identifier;
- environment manifest;
- code hash;
- test command;
- observed result;
- independently reproduced result;
- known gaps;
- gate decision.

---

# EXP-P0-v1

## 📦 Artifact

```text
mentaury-soul-P0.zip
```

## 🧪 Reproduced Result

```text
13 tests passed
```

## ✅ What Worked

- basic canonical subset;
- basic SQLite append;
- ordinary version conflict;
- simple idempotent retry;
- WAL + synchronous FULL configuration.

## 🚨 Independently Reproduced Defects

```text
payload tampering
→ verify_chain returned ok

event_hash tampering
→ verify_chain returned ok

stale redaction
→ VERSION_CONFLICT
→ payload already deleted
→ REDACTION_RECORDED absent
```

Additional problems:

- version read before the write transaction;
- the single-event API was called atomic batch;
- incomplete envelope persistence;
- short identifiers;
- payload/schema validation only nominal.

## 🧊 Gate Decision

```text
REJECT_AS_CANONICAL
RETAIN_AS_EXPERIMENT
```

---

# EXP-P0-v2

## 📦 Artifact

```text
mentaury-soul-P0-v2.zip
```

## 🧪 Reproduced Result

```text
21 tests passed
```

## ✅ Confirmed Fixes

- R0 recomputes event hash;
- payload tampering detected;
- event hash tampering detected;
- redaction rollback fixed;
- `BEGIN IMMEDIATE` before version read;
- two-connection conflict controlled;
- full UUID identifiers;
- `MENTAURY_CANONICAL_JSON_V1` naming;
- float and unsafe integer rejection;
- event/schema pair registry;
- basic idempotency conflict;
- richer environment manifest.

## 🚨 New Independently Reproduced Defects

### Event-aware idempotency gap

The same command fingerprint and key could be accompanied by a different actual event payload/type and return `ALREADY_APPLIED` instead of conflict.

### Cross-stream redaction

A command could delete the payload of an event in stream A and record the audit event in stream B.

### Physical immutability violation

Redaction continued to modify a committed row in `events`.

### Stream metadata gap

R0 did not verify the consistency of `stream_meta` with the tail event.

### Incomplete batch semantics

The Append API still accepted a single event.

### Nominal schema validation

The schema name was checked, but not the entire payload structure.

## 🧊 Gate Decision

```text
RETAIN_AS_EXP-P0-v2
USE_AS_PATCH SOURCE
DO_NOT MERGE DIRECTLY
```

---

# 🧩 What Is Carried Over to P0-v3

```text
✅ hash recomputation
✅ payload_digest model
✅ BEGIN IMMEDIATE
✅ rollback discipline
✅ full UUID
✅ canonical profile
✅ adversarial tampering tests
✅ environment manifest
✅ controlled concurrency result
```

To be rewritten:

```text
🔧 immutable event/payload split
🔧 command + pending batch fingerprint
🔧 same-stream redaction
🔧 stream_meta verification
🔧 real list[PendingEvent] batch
🔧 structural schema validation
🔧 full EventEnvelope storage boundary
```

---

# 🧪 Required P0-v3 Regression Cases

```text
same key + changed event payload
same key + changed event type
same key + changed event count/order
cross-stream redaction
stream_meta version tampering
stream_meta hash tampering
historical row byte-for-byte immutability
schema structural violation
partial multi-event batch failure
payload-store failure rollback
```

---

# 🏁 Decision at the Time of EXP-P0-v1/v2 (Superseded)

> ⚠️ **Outdated.** The block below records the decision at the time of the EXP-P0-v1/v2 experiments, when `main` was indeed documentation-only. Since then, `agent/p0-event-substrate-v3` was implemented and merged (PR #6, P0-001), and the entire P0-001…P0-015 line was implemented and validated in `main`. This block is preserved as a historical protocol, rather than rewritten, in accordance with the project's own principle of "Continuity with Correctability" (errors and outdated records are corrected with new versions, not by hidden overwriting of the past). For the current status, always refer to [`CURRENT_STATUS.md`](../CURRENT_STATUS.md).

```text
NEXT IMPLEMENTATION (as of EXP-P0-v1/v2):
agent/p0-event-substrate-v3

CURRENT MAIN (as of EXP-P0-v1/v2):
documentation-only

R1 ALLOWED:
only after adversarial R0 Gate
```
