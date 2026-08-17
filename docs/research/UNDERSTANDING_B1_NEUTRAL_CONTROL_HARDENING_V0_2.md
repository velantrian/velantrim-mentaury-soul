# Understanding B1 Neutral Control Hardening v0.2

**Project:** Mentaury Soul  
**Scope:** research-only benchmark control hardening  
**Runtime authority:** NONE  
**Implementation authority:** NONE outside this research harness  
**Production source changes:** NONE (`src/mentaury/**` untouched)

## Purpose

B1 is the neutral structured-output control used between B0 (current governed synthesis) and C1 (candidate structured cognition policy). The purpose of this hardening is to prevent B1 from becoming a hidden cognitive policy through schema leakage, authority-shaped fields, free-form presentation, privileged model-facing reference labels, or a decision-bearing instruction template.

This artifact does **not** prove Understanding, does not authorize a new cognitive contract, and does not imply runtime Mentaury.

## Frozen safety properties for this research harness

1. Candidate semantic content is source-bound by exact IDs and a SHA-256 digest over the evaluator-side semantic payload.
2. Nested structures are recursively closed by explicit validator rules.
3. Candidate-added ranking, score, probability, verdict, selection, recommendation, authorization, action, tool, retrieval, deployment, identity or relationship update fields are rejected.
4. Duplicate IDs are rejected.
5. `next_discrimination_need` is limited to a frozen enum and source-bound critical-unknown references; free-form query text is forbidden.
6. `governed_conclusion` is limited to `CONDITIONAL | DEFER | NONE` plus the exact evaluator-side scope. `FINAL` and action authorization are forbidden.
7. `final_presentation` is forbidden. Presentation is produced only by a deterministic source-only renderer after validation.
8. Run/scenario identifiers are bounded identifiers and cannot serve as free-prose side channels.
9. Model-facing semantic input is separate from the evaluator reference frame and must remain identical across B0/B1/C1.
10. The B1 instruction profile is frozen by hash and must remain format/representation guidance only; positive decision heuristics are mechanically guarded and semantic review remains required.

## Adversarial mutation set

The test suite binds exact error-code expectations for B1-M-01…B1-M-16, including the previously observed nested leakage classes:

- nested `selected=true`;
- nested `verdict=SUPPORTED`;
- nested `probability=.99`;
- `governed_conclusion.authorized_action`;
- duplicate critical unknown;
- `situation_model.claim` invented semantic content;
- `next_discrimination_need.query` action-shaped prose;
- free `final_presentation` decision prose.

A parser crash is never counted as detector success.

## Anti-oracle / input-symmetry finding

The first repository fixture still grouped source text under evaluator-semantic labels such as `material_constraints`, `alternatives`, `consequences`, and `critical_unknowns`. If that grouped representation were passed directly to B1 while B0 or C1 received a less structured input, B1 would receive part of the reference situation model as an oracle. That would confound any B0/B1/C1 comparison.

The hardened split is therefore:

```text
shared model_input.json
  scenario_id
  atoms: [{id: A1, text: ...}, ...]
        |
        +--> B0 semantic input
        +--> B1 semantic input
        +--> C1 semantic input

hidden evaluator source_frame.json
  situation_model
  material_constraints
  alternatives
  consequences
  critical_unknowns
  allowed discrimination enum
  governed conclusion scope
```

The neutral atom IDs are intentionally role-free (`A1…A7` in the synthetic control fixture). Category membership exists only in the evaluator reference and is not model-facing.

`tests/research/understanding_b1/input_symmetry.py` enforces that the semantic projection supplied to B0/B1/C1 is byte-identical after canonicalization and that role/reference labels are absent from the shared model input. Any drift produces an invalid research run, not an interpretable performance delta.

Arm-specific instructions may differ by experimental definition; semantic evidence/input may not. The preregistration must freeze those instruction profiles separately so B1 remains neutral structured elicitation and C1 remains the only candidate cognition-policy arm.

## B1 instruction-profile boundary

The B1 profile is stored at `tests/research/understanding_b1/fixtures/b1_instruction_profile.txt` and frozen by SHA-256 in `test_instruction_profile.py`.

It may:

- request the required B1 fields;
- require source atom IDs only;
- state closed enums and structural prohibitions;
- prohibit invented facts, ranking, verdicts, recommendations, actions and free prose.

It may not:

- prefer/select an alternative;
- encode `if X then choose Y` decision rules;
- assign likelihood/probability/confidence;
- authorize publication/action/tool/retrieval;
- expose evaluator reference labels or Gold answers.

The keyword/pattern guard is only a mechanical tripwire. It does not prove absence of a semantically equivalent hidden heuristic. That remains a human/independent semantic-review responsibility before confirmatory use.

## Current readiness boundary

Mechanical B1 leakage hardening, semantic-input symmetry, and instruction-profile freeze can be checked in CI. They do not establish universal B1 neutrality or independent semantic validation.

Allowed next research outcomes remain:

- `B1_READY_FOR_B0_B1_C1_REHEARSAL`
- `MORE_RESEARCH`

For solo-maintainer / AI-reviewed work, `B1_READY_FOR_B0_B1_C1_REHEARSAL` means **exploratory/rehearsal readiness only**, not confirmatory evidence.

Not allowed from this artifact alone:

- `UNDERSTANDING_PROVEN`
- `NEW_COGNITIVE_CONTRACT_JUSTIFIED`
- runtime/tool/retrieval/identity/relationship authorization

## Files

- `tests/research/understanding_b1/b1_harness.py`
- `tests/research/understanding_b1/input_symmetry.py`
- `tests/research/understanding_b1/test_b1_harness.py`
- `tests/research/understanding_b1/test_input_symmetry.py`
- `tests/research/understanding_b1/test_instruction_profile.py`
- `tests/research/understanding_b1/fixtures/b1_instruction_profile.txt`
- `tests/research/understanding_b1/fixtures/model_input.json`
- `tests/research/understanding_b1/fixtures/source_frame.json`
- `tests/research/understanding_b1/fixtures/valid_b1.json`

## Provenance and non-claims

The repository-ready hardening originated from a reconstructed reference harness produced from the recorded B1 adversarial findings. It is not a claim that the historical ZIP itself was repaired or revalidated.

A green suite proves only the enumerated structural/input-symmetry/instruction-profile checks at the exact tested revision. It does not prove universal B1 neutrality, semantic Understanding, psychological understanding, causal truth, action permission, or runtime readiness.
