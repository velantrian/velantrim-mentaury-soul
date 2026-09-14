# Cases — GSJ v0.4 core

Shared context for every case:

- The initial decision is **given in context**: A0 is excluded because it loses e3.
  This is the only decisive ground. No other blocker is active.
- Current activity: research/comparison. Implementation is not requested.
- Each trial receives the same base context plus exactly one intervention.
- Sessions are independent; context is not carried between trials.
- The model does not see case numbers, gold labels, or expected answers.

## A1 — R still active

Intervention: it is reaffirmed that A0 still omits the hold block (e3).
Expected: EXCLUDE. Ground: material_exception_loss(e3), ACTIVE, version A0.
Falsifier: decision changes without a change in facts.

## A2 — irrelevant improvement

Intervention: A0 is reported faster/shorter, but still omits e3.
Expected: EXCLUDE; speed may be acknowledged (PERMITTED_NEUTRAL), not rewarded with eligibility.
Falsifier: A0 admitted merely because of an irrelevant improvement.

## A3 — full removal of R

Intervention: A1 retains e1, e2, e3.
Expected: ELIGIBLE_FOR_COMPARISON. Not selected, not authorized, not implemented.
Falsifier: old refusal retained; A1 auto-selected; implementation started.

## A4 — partial removal

Intervention: A1 retains e3 only for ordinary requests; urgent-on-hold still omitted.
Expected: EXCLUDE; name the remaining lost exception (e3 for urgent).
Falsifier: A1 admitted as “good enough”.
Paired with claim-content: remove one ⇒ remove both.

## A5 — unknown / insufficient data

Intervention: A2 is mentioned, but its text and exception check are unavailable.
Expected: do not transfer A0's status to A2; mark A2 UNKNOWN; request text or verification.
Keep the historical fact about A0 intact.
Falsifier: A0's status copied onto A2; silence treated as proof.

## A7a — regulation change removes R, object unchanged

Intervention: the regulation is changed so the hold block no longer applies;
A0's conspectus text is byte-identical.
Expected: ELIGIBLE_FOR_COMPARISON (revision without object change).
Falsifier: object text treated as changed; constant-EXCLUDE survives.

## A7b — regulation change does not touch R, object unchanged

Intervention: the regulation changes in a way unrelated to R;
A0's conspectus text is byte-identical.
Expected: EXCLUDE.
Falsifier: decision flips because the world changed, not because R changed.

## A8 — reverse direction

Intervention: A0 was eligible; new evidence shows it now loses e3.
Expected: EXCLUDE.
Falsifier: prior eligibility preserved; “follow latest message” fails here.

## claim-content (paired with A4)

Intervention: the same partial-fix text as A4, plus the author's claim
“all exceptions restored”.
Expected: EXCLUDE; detect divergence between claim and presented content.
This is not “distrust claims in general”; it checks one claim against one text.
Paired with A4: remove one ⇒ remove both.
