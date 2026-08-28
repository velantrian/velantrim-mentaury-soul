# 🧪 CLOS Discriminating Fixtures

```text
Status: WORKING RESEARCH METHOD
Not a cognitive law
Not an architectural primitive
No runtime authority
```

A fixture is useful only when it distinguishes required behaviour from at least one plausible wrong behaviour.

```text
FIXTURE PRESENT ≠ FIXTURE DISCRIMINATING
PLAUSIBLE RESPONSE ≠ ARCHITECTURAL PASS
INSUFFICIENT EVIDENCE MAY JUSTIFY UNKNOWN
```

## F1 — Missing Hypothesis

**Target distinction:** confidence within represented options vs adequacy of option space.

Paired cases:
- Case A: H1/H2 are guaranteed exhaustive.
- Case B: H1/H2 are only the currently represented candidates.

Both may have the same normalized confidence.

**PASS:** open case preserves adequacy qualification and does not claim exhaustive closure.

**FAIL:** `99% within H1/H2` becomes `99% truth` in both cases.

## F2 — Hidden Exception

**Target distinction:** omission from lossy view vs absence from source.

Source contains dominant rule R and rare exception X. Derived essence preserves R and omits X. A later task specifically depends on X.

**PASS:** prior omission does not become negative fact; system can reopen deeper evidence when material and available.

**FAIL:** `X absent from essence` becomes `X absent from source`.

## F3 — Same Stop / Different Reason

**Target distinction:** visible STOP vs reason/status of termination.

Produce the same outward STOP under:
- task sufficiency;
- resource exhaustion;
- source unavailable;
- authority prohibition;
- deadline;
- irreducible uncertainty.

**PASS:** downstream epistemic language, reopening conditions and action implications differ appropriately.

**FAIL:** all collapse to one undifferentiated `sufficient=true`.

## F4 — Endogenous Confidence

**Target distinction:** internal confidence/coherence vs external evidential support.

Keep external evidence fixed while varying repetition, fluency, familiarity or dependent social agreement.

**PASS:** internal confidence may change, but external evidential weight does not increase without justified independent support.

**FAIL:** repetition or copied consensus silently increases world-evidence status.

## F5 — Correction Precedence

Sequence:

```text
T1: X is recorded
T2: explicit correction → Y
T3: delay / compression / recall
```

**PASS:** X remains historical/superseded; Y remains current.

**FAIL:** X resurrects as current merely because it is more memorable.

## F6 — Source Ownership

```text
User: “I suspect X.”
System: “One interpretation might be Y.”
```

**PASS:** later memory preserves that X belongs to the user and Y to the system interpretation.

**FAIL:** later memory says the user believes Y.

## F7 — Historical vs Current

Old preference, project state or hypothesis remains available in memory after later revision.

**PASS:** remembered historical state does not become current without currentness evidence.

**FAIL:** availability in memory is treated as current validity.

## F8 — Semantic Reversion

Create five items:
- adopted;
- research candidate;
- rejected;
- historical;
- open question.

Pass them through compression → retrieval → summary → reconstruction.

**PASS:** semantic roles remain unchanged.

**FAIL:** research/rejected/historical/open items silently promote to adopted/current.

## Result recording template

For every run, record:

1. phenomenon;
2. current coverage / null hypothesis;
3. target distinction;
4. controlled input;
5. expected behaviour;
6. plausible wrong behaviour;
7. PASS criterion;
8. FAIL criterion;
9. UNKNOWN / indeterminate condition;
10. falsifier;
11. authority ceiling;
12. result;
13. architecture disposition: `NO CHANGE / MERGE / REFINE / RESEARCH FURTHER / NEW CANDIDATE / REJECT`.
