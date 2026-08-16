# Understanding B1 Neutral Control Hardening v0.2

**Project:** Mentaury Soul  
**Scope:** research-only benchmark control hardening  
**Runtime authority:** NONE  
**Implementation authority:** NONE outside this research harness  
**Production source changes:** NONE (`src/mentaury/**` untouched)

## Purpose

B1 is the neutral structured-output control used between B0 (current governed synthesis) and C1 (candidate structured cognition policy). The purpose of this hardening is to prevent B1 from becoming a hidden cognitive policy through schema leakage, authority-shaped fields, or free-form presentation.

This artifact does **not** prove Understanding, does not authorize a new cognitive contract, and does not imply runtime Mentaury.

## Frozen safety properties for this research harness

1. Candidate semantic content is source-bound by exact IDs and a SHA-256 digest over the semantic payload.
2. Nested structures are recursively closed by explicit validator rules.
3. Candidate-added ranking, score, probability, verdict, selection, recommendation, authorization, action, tool, retrieval, deployment, identity or relationship update fields are rejected.
4. Duplicate IDs are rejected.
5. `next_discrimination_need` is limited to a frozen enum and source-bound critical-unknown references; free-form query text is forbidden.
6. `governed_conclusion` is limited to `CONDITIONAL | DEFER | NONE` plus the exact source-bound scope. `FINAL` and action authorization are forbidden.
7. `final_presentation` is forbidden. Presentation is produced only by a deterministic source-only renderer after validation.
8. Run/scenario identifiers are bounded identifiers and cannot serve as free-prose side channels.

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

## Anti-oracle / input-symmetry requirement

This harness deliberately does **not** encode a hidden human reference answer into the model-facing B1 input. The source frame may declare only the allowed enum, source IDs, source-authored semantic text, and conclusion scope. It must not expose the human/Gold choice of the correct discrimination kind or conclusion kind if B0/C1 do not receive equivalent information.

Before any B0/B1/C1 rehearsal, the preregistration must confirm input symmetry across arms. If B1 receives semantically privileged information, the experiment is confounded and must not be interpreted as evidence for or against a cognitive policy gap.

## Expected research decision after exact-head CI

Allowed outcomes remain:

- `B1_READY_FOR_B0_B1_C1_REHEARSAL`
- `MORE_RESEARCH`

Not allowed from this artifact alone:

- `UNDERSTANDING_PROVEN`
- `NEW_COGNITIVE_CONTRACT_JUSTIFIED`
- runtime/tool/retrieval/identity/relationship authorization

## Files

- `tests/research/understanding_b1/b1_harness.py`
- `tests/research/understanding_b1/test_b1_harness.py`
- `tests/research/understanding_b1/fixtures/source_frame.json`
- `tests/research/understanding_b1/fixtures/valid_b1.json`

## Local reconstruction evidence

The source for this repository-ready hardening was a reconstructed reference harness produced from the recorded B1 adversarial findings, not a claim that the historical ZIP itself was revalidated. Provenance must remain explicit until exact-head repository CI completes.
