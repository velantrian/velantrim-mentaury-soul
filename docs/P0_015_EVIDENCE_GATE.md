# ⚖️ P0-015 — Deterministic Evidence Gate

```text
Status: IMPLEMENTATION PR
Base: main@3ff90816b8d095987a8adcdc2cb633c128877212
Scope: governed M2 belief status gate
M3 identity writes: NOT AUTHORIZED
Domain runtime wiring: NOT AUTHORIZED
Epistemic truth claim: NOT AUTHORIZED
```

## 🎯 Goal

P0-015 adds the smallest deterministic gate that can move a P0-014 belief into
`SUPPORTED` or `CONTRADICTED` without allowing a command or a forged domain event
to select arbitrary thresholds or manufacture a self-consistent receipt.

```text
complete attached evidence set
→ exact approved policy lookup
→ structural and independence checks
→ bounded quality/freshness evaluation
→ deterministic receipt
→ accepted gated event or non-state rejection audit
→ reducer recomputation during R1 replay
```

The gate governs a status transition. It does not prove objective truth,
authenticate an external source, validate a capability lease, start a worker, or
write identity state.

## 🔒 Approved policy registry

A command supplies only `policy_id`. It cannot supply thresholds.

The lifecycle and reducer share an immutable `EvidenceGatePolicyRegistry`. The
event preserves the full selected policy, but replay succeeds only when that
policy is byte-equivalent to the policy currently approved by the reducer
profile.

P0-015 ships one deliberately narrow profile:

```text
mentaury-evidence-contextual-v1
allowed claim types: contextual, unspecified
minimum independent source groups: 2 per side
minimum reliability: 800 / 1000
minimum relevance: 800 / 1000
maximum age: 86400 seconds
```

Causal, statistical, universal and existential claims remain ungated until a
separate reviewed policy defines the necessary method-specific requirements.
This prevents a generic source-count rule from pretending to validate every
claim type.

## 📦 Evidence record

Each attached evidence reference must have exactly one record:

```text
evidence_ref
side: for | against
source_group
provenance_ref
content_digest
observed_at
reliability_milli
relevance_milli
revoked
```

The record set must exactly equal the belief projection's complete
`evidence_for ∪ evidence_against` set. Missing and extra records fail closed.

Anti-duplication boundaries:

- evidence references are unique;
- one content digest cannot appear under multiple references;
- one provenance reference cannot appear under multiple references;
- one source group cannot be counted on both sides;
- multiple records from one source group count as one independent group.

These checks prevent simple duplication from manufacturing confirmation. They
do not externally authenticate `source_group`, provenance, quality scores or the
underlying content.

## ⏱️ Deterministic freshness anchor

The lifecycle uses canonical `CommandEnvelope.issued_at` as `evaluated_at`.
The committed gated event must use the same value as immutable
`EventEnvelope.occurred_at`. The reducer rejects time rebinding during replay.

This preserves deterministic freshness semantics. It does not prove that the
issuer's clock was honest; trusted-clock validation remains an outer authority
concern.

## 🧾 Outcomes

```text
for side passes, against does not  → supported
against side passes, for does not  → contradicted
both sides pass                     → conflict, no state mutation
neither side passes                 → inconclusive, no state mutation
```

Additional belief constraints:

- `supported` requires no open registered contradiction;
- `contradicted` requires at least one open registered contradiction;
- `supported`, `contradicted` and `superseded` remain terminal in this profile;
- a successful gate increments belief revision exactly once;
- statement and claim type are unchanged by the gate.

A valid but rejected evaluation preserves its deterministic receipt inside the
non-state `EVIDENCE_GATE_REJECTED` audit event.

## 🔁 Replay-verifiable receipt

`EvidenceGateReceipt` binds:

```text
profile
belief ID and revision
claim type
statement digest
evaluation time
approved policy ID and digest
complete evidence-set digest
outcome
qualifying references
independent source groups
rejected references
receipt digest
```

`EvidenceGatedBeliefReducer` v2 does not trust the stored receipt. During replay
it independently:

1. checks belief, revision, statement, claim type and prior status;
2. binds `evaluated_at` to the event's `occurred_at`;
3. requires the exact approved policy profile;
4. requires canonical sorted records with exact fields;
5. recomputes the gate from the current projection and embedded records;
6. compares the full canonical receipt;
7. checks the resulting status and contradiction boundary;
8. applies the terminal status and preserves receipt digests in history.

A forged receipt, modified threshold, incomplete record set, reordered event
record list, time rebinding or mismatched status fails closed as a reducer error.

## 🧪 Required adversarial matrix

```text
exact complete evidence set
order-independent receipt
low-quality / stale / revoked exclusion
future evidence rejection
source-group deduplication
duplicate content/provenance rejection
cross-side source-group rejection
conflict and inconclusive audits
unapproved policy rejection
unsupported claim-type rejection
hidden command-field rejection
open-contradiction boundaries
receipt tampering
policy tampering
record omission and reordering
time rebinding
direct-event status mismatch
strict schemas
R1 full replay
```

## ⚖️ Preserved boundaries

```text
supported status ≠ objective truth
contradicted status ≠ universal falsity
receipt ≠ externally authenticated evidence
source_group string ≠ proven independent organization
quality score ≠ independently calibrated quality
provenance_ref ≠ verified provenance chain
AuthorityRef ≠ validated capability lease
P0-015 ≠ M3 identity update
P0-015 ≠ autonomous learning
P0-015 ≠ runtime authorization
```

## 🏁 Completion gate

P0-015 is complete only after:

```text
retained Mentaury CI passes exact PR head
full adversarial test suite passes
compileall passes
exact diff audit passes
unresolved review threads = 0
squash merge uses expected head SHA
retained CI passes resulting main SHA
README + CURRENT_STATUS + Notion are synchronized
```
