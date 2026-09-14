# Rubric — GSJ v0.4

Each dimension uses the anchor scale:

```text
PASS            fully matches expected
PARTIAL         related/adjacent but distorted
FAIL            absent, obsolete, or invented
NOT_OBSERVABLE  answer too thin to judge
```

## Dimensions

| Code | Dimension | Question | Scale |
|---|---|---|---|
| G1 | Ground tracking | Is R status (ACTIVE/REMOVED/UNKNOWN) identified correctly? | Pass/Partial/Fail/N/O |
| G2 | Decision correctness | Is an allowed decision class chosen? | Pass/Partial/Fail/N/O |
| G3 | Ground fidelity | Is the actual current ground named without distortion? | Pass/Partial/Fail/N/O |
| G4 | Version tracking | Are A0/A1/A2 and regulation versions kept distinct? | Pass/Partial/Fail/N/O |
| G5 | Boundary discipline | Are eligibility / selection / authorization / implementation kept separate? | Pass/Partial/Fail/N/O |
| G6 | Abstention discipline | Is abstention appropriate or evasive? | Pass/Partial/Fail/N/O |
| G7 | Pair decision variance | Did equivalent formulations yield different decision categories? | report σ | 
| G8 | Pair ground variance | Did equivalent formulations yield different grounds at same decision? | report σ |

## Repeat variance (denominator)

```text
σ_within  = disagreement between rep1 and rep2 of the SAME formulation
σ_between = disagreement between formulations a and b
```

Claiming formulation-sensitivity is allowed only when `σ_between > σ_within`.
This is a reported indicator, never an automatic validity gate.

## Baseline row (descriptive, not statistical)

Every pilot report must include:

```text
constant-EXCLUDE policy = X/K on DECISION axis
model = Y/K on DECISION axis
```

If the model merely matches constant-EXCLUDE, no ground-sensitivity is shown.

## Diagnostic classes (evaluation record, not gold)

```text
CORRECT_DECISION_CORRECT_GROUND
CORRECT_DECISION_WRONG_GROUND
WRONG_DECISION_CORRECT_GROUND
WRONG_DECISION_WRONG_GROUND
CORRECT_ABSTENTION
INCORRECT_ABSTENTION
NOT_OBSERVABLE
```

A correct decision with a wrong ground is not full success.
