# Claim -> Belief Provenance Binding Contract v0.1

```text
Contract: CBP-v0.1
Scope: bounded creation-time provenance binding
Implementation target: src/mentaury/claim_belief_binding/**
Runtime authority: NONE
Evidence Gate authority: UNCHANGED
Belief lifecycle authority: P0-014 remains owner
Identity / relationship / M3 authority: NONE
Retrieval / tools / network: NONE
```

## Purpose

CBP-v0.1 closes one specific gap: a belief created from a PCR claim must be able to retain an immutable reference to the exact PCR record identity used at genesis without turning that record into truth, evidence verdict, identity, or action permission.

## Selected bounded model

The v0.1 model uses a dedicated command path:

```text
CREATE_BELIEF_FROM_CLAIM
  + exact ProvenanceClaimRecord object
  -> delegate ordinary genesis to P0-014 CREATE_BELIEF
  -> emit BELIEF_CREATED
  -> emit BELIEF_CLAIM_BOUND
```

The two pending domain events are intended to be committed as one ordered atomic batch by the existing P0 atomic-batch infrastructure.

Legacy `CREATE_BELIEF` remains valid and unchanged. An unbound belief is therefore still representable, but it cannot claim a CBP-v0.1 PCR genesis binding.

## Binding fields

`BELIEF_CLAIM_BOUND` records only the minimum stable linkage:

```text
contract_version
belief_id
belief_revision = 1
claim_id
claim_record_fingerprint
claim_type
statement_ref
statement_equivalence = NOT_ESTABLISHED
binding_input_fingerprint
```

The event intentionally does not duplicate PCR source/scope objects. Exact PCR identity is referenced by `claim_id + claim_record_fingerprint`.

## Statement boundary

PCR stores an opaque `statement_ref`; P0-014 stores a concrete belief `statement` string. CBP-v0.1 does not have a source-resolution owner capable of proving byte-for-byte equality between them.

Therefore:

```text
statement_equivalence = NOT_ESTABLISHED
```

is mandatory and replay-enforced.

## Exact command binding

The external command must bind to the supplied exact `ProvenanceClaimRecord` through:

```text
claim_id == record.claim.claim_id
claim_record_fingerprint == record.input_fingerprint
claim_type == record.claim.claim_type
```

Any mismatch fails closed and emits no domain event.

## Authority semantics

```text
PCR record != belief
binding != truth
binding != evidence support
binding != EvidenceGateOutcome
binding != source authenticity proof
binding != statement equivalence proof
binding != identity fact
binding != relationship fact
binding != capability
binding != action permission
```

PCR `evidence_refs` are not copied into P0-014 evidence state and cannot promote the belief beyond `HYPOTHESIS`.

## Replay semantics

`ClaimBoundBeliefReducer` layers over the existing P0-015-capable belief reducer and adds one optional `claim_binding` projection field.

The binding event is accepted only when:

- the belief already exists;
- belief revision is exactly `1`;
- no prior claim binding exists;
- event stream/belief ID match;
- claim type matches the belief projection;
- contract and statement-equivalence literals match CBP-v0.1;
- fingerprints have exact lowercase SHA-256 shape;
- payload keys are exact.

Once present, the binding is preserved through later P0-014/P0-015 projection updates. CBP-v0.1 does not alter their transition or Evidence Gate rules.

## Required adversarial evidence

```text
CBP-T01 P0-014 remains genesis owner
CBP-T02 exact PCR identity preserved
CBP-T03 statement equality never inferred
CBP-T04 claim-id/fingerprint/type mismatch fails closed
CBP-T05 target status cannot be smuggled into binding command
CBP-T06 PCR evidence refs do not promote belief status
CBP-T07 binding cannot precede belief genesis
CBP-T08 duplicate/late binding fails closed
CBP-T09 binding survives later belief events without authority expansion
CBP-T10 no truth/evidence/identity/action vocabulary is produced
CBP-T11 deterministic input fingerprint
CBP-T12 local budgets fail without truncation/repair
CBP-T13 no hidden I/O/runtime imports
CBP-T14 unknown command schema fails closed
```

## Non-goals

- EPR-v0.1 implementation;
- terminal reconsideration/successor lineage;
- retrieval or source resolution;
- evidence collection;
- autonomous inquiry;
- identity/relationship/M3 mutation;
- Action Gate;
- deployment.
