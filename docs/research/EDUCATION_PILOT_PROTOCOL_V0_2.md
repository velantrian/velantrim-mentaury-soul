# Mentaury Education Pilot Protocol v0.2

**Status:** `PROPOSED · RESEARCH_ONLY · OFFLINE · HUMAN_LED · NO_RUNTIME_AUTHORITY`  
**Owner direction:** foundation fixes authorized on 2026-08-19. This document does **not** authorize provider/model calls, retrieval, tools, scheduler activity, Evidence Gate verdicts, belief/identity/relationship mutation, Action Gate, or deployment.

## 1. Purpose

The pilot uses Mentaury Soul as a discipline for provenance, claim/evidence separation, relation restraint, hypothesis discrimination, and honest defer. It is not an autonomous tutor, a student-scoring system, a personality profiler, or an identity runtime.

The central safety rule is:

```text
adapter normalization != epistemic inference
```

A pilot adapter may translate an explicitly supplied learner field into an existing PCR/ATR/HDE contract field. It must not invent a missing source, scope, epistemic role, relation semantic, outcome prediction, basis reference, partition, or uncertainty.

If required meaning is absent, the only valid outcomes are `INCOMPLETE_INPUT`, `NOT_USED`, or human clarification before resubmission.

## 2. Authority boundary

```text
learner artifact != belief
learner artifact != identity
HDE class != truth
HDE class != grade
human rubric != intelligence score
receipt != pedagogical truth
metadata blinding != anonymity
attestation != privacy proof
```

The teacher/facilitator remains the only owner of teaching, feedback, and educational decisions.

## 3. Admission sequence

```text
Approved synthetic/open scenario
        ↓
Learner structured worksheet
        ↓
Human privacy/scope screening
        ↓
APPROVE_FOR_VALIDATION | REJECT_FOR_INGESTION
        ↓
Typed pilot forms
        ↓
PCR / optional ATR / optional HDE
        ↓
Validation bundle
        ↓
Metadata-blinded human review
        ↓
EDU_RUBRIC_V0_1
        ↓
Session receipt
```

The validator must never claim that it proved the absence of personal data. `no_personal_data_attestation=true` is only a learner/facilitator declaration and cannot substitute for human admission screening.

## 4. Typed learner forms

The v0.1 single `LearnerArtifactEnvelope` is replaced by explicit forms that preserve the semantics required by the owning Mentaury contracts.

### 4.1 LearnerClaimForm

A claim form must contain, or explicitly reference teacher-approved scenario values for, every PCR semantic field needed to construct:

- `ProvenanceSource`;
- `ClaimRepresentation`;
- `ClaimScope`.

At minimum the form must make explicit:

```text
source_ref
source_actor_ref (or explicit NONE where contract permits)
source_class
source_origin
provenance_state
publication_or_capture_context_ref
sensitivity
usage_boundary_ref
material_gaps
derivation_refs

claim_id
statement_ref
claim_class
claim_type
epistemic_role
directly_stated
speaker_ref
subject_ref
subject_relation
basis_refs
evidence_refs

applies_to
may_support
does_not_establish
unknowns
transfer_limits
```

A teacher-approved scenario template may pre-fill neutral source metadata, but it must remain visible in the learner packet and must not be silently supplied by the adapter.

### 4.2 LearnerRelationForm

ATR use is optional. It is valid only after the endpoint claims have valid PCR identities.

The learner-facing relation form must explicitly contain:

```text
left_claim_ref
right_claim_ref
relation_type
orientation
origin
origin_actor_ref
source_assertion_ref (optional)
basis_claim_refs
conditions
moderators
exceptions
unknowns
transfer_limits
```

The adapter resolves claim references to the exact `(claim_id, claim_input_fingerprint)` anchors produced by PCR. It must not infer a relation type or causal meaning from free text.

### 4.3 LearnerDiscriminationForm

HDE use is optional and requires two distinct valid PCR hypothesis records with `EpistemicRole.HYPOTHESIS`.

The form must explicitly contain:

```text
h1_claim_ref
h2_claim_ref
proposed_observation_ref
design_origin_ref
design_basis_refs
partition_scope_ref
partition_complete_for_scope
outcomes[]:
  outcome_ref
  h1_prediction
  h2_prediction
  expectation_basis_refs
```

If outcome predictions or partition completeness are not supplied, HDE must not run. The validator returns `INCOMPLETE_HDE_INPUT` or `HDE_NOT_USED`.

## 5. Validation result

A pilot validation result may report only representation/contract status and HDE structural classification.

```json
{
  "schema": "mentaury-education-validation/2",
  "scenario_id": "EDU-001",
  "artifact_digest": "sha256:<64-lowercase-hex>",
  "pcr_validation": {"status": "VALID|INVALID|NOT_USED", "issues": []},
  "atr_validation": {"status": "VALID|INVALID|NOT_USED", "issues": []},
  "hde_validation": {
    "status": "VALID|INVALID|NOT_USED|INCOMPLETE_INPUT",
    "classification": "DISCRIMINATING|NON_DISCRIMINATING|INCONCLUSIVE_STRUCTURE|null"
  },
  "authority": {
    "evidence_verdict": "NOT_COMPUTED",
    "belief_mutation": false,
    "identity_mutation": false,
    "relationship_mutation": false,
    "action_authority": false
  }
}
```

## 6. Human rubric boundary

The B0/B1/C1 model-output rehearsal rubric is not automatically a student rubric. Education uses a separate `EDU_RUBRIC_V0_1` aligned with the pilot learning objectives.

No aggregate cognition, intelligence, personality, engagement, or student ranking score is permitted.

## 7. Privacy and blinding

Raw learner identifiers are not admitted to PCR/ATR/HDE records, review packets, receipts, source control, Notion, or aggregate reports.

A local ephemeral alias may be used only to return formative feedback during the session and must be removed according to the local retention procedure.

Review packets are called **metadata-blinded**, not anonymous. Free-text content can still reveal identity, cohort, condition, or writing style.

A deletion action receipt may record that the approved deletion procedure was invoked. It must not claim proof of irreversible physical erasure from SSDs, backups, snapshots, or external organisational systems.

## 8. Canonicalization and receipts

Pilot receipts must use the repository canonical serialization contract (`MENTAURY_CANONICAL_JSON_V1`) rather than a pilot-specific `json.dumps` profile.

Domain separation remains explicit through receipt-specific hash-domain labels.

A receipt may bind:

- repository SHA;
- scenario manifest digest;
- admitted typed-form digests;
- PCR/ATR/HDE input fingerprints where applicable;
- validation-result digests;
- human rubric-result digests;
- expected and observed artifact counts;
- explicit missing-artifact list;
- completion state.

A missing artifact must never be synthesized.

## 9. Repository placement

No `src/mentaury/education_runtime/**` is authorized.

If executable pilot tooling is later implemented, use a clearly non-runtime research surface such as:

```text
research_tools/education_pilot/
    contracts.py
    validator.py
    receipts.py
    blind_packet.py

tests/research/education_pilot/
    test_contracts.py
    test_validator.py
    test_receipts.py
```

`research_tools` must not be imported by production runtime code or granted provider/network/tool credentials.

## 10. Experimental interpretation

The first cohort is a **feasibility, safety, and rubric-readability pilot**, not an efficacy claim.

Version 0.2 does not yet claim that Mentaury improves learning relative to a standard discussion exercise. A later comparative protocol would require a separately frozen design for control condition, assignment/counterbalancing, transfer tasks, reviewer agreement, confounders, and sample-size rationale.

Permitted first-cohort outcomes:

```text
PILOT_FEASIBLE_FOR_FURTHER_STUDY
PILOT_FEASIBLE_WITH_REVISIONS
PILOT_INVALID_OR_UNSAFE
NO_USEFUL_RESEARCH_SIGNAL
MORE_RESEARCH
```

## 11. Implementation gate

Implementation of education adapters is blocked until all of the following are true:

1. typed form schemas are frozen;
2. every mapping to PCR/ATR/HDE is field-for-field documented;
3. negative tests prove missing semantic fields are rejected rather than inferred;
4. human privacy admission precedes validator ingestion;
5. education rubric is independent from B0/B1/C1 model-output evaluation;
6. canonical receipts use `MENTAURY_CANONICAL_JSON_V1`;
7. no runtime/model/retrieval/tool/identity/action authority is introduced.

Only then may the project claim:

`OFFLINE_EDUCATION_RESEARCH_CONTRACT_READY`

This status still does not authorize a learner cohort or any external model call.
