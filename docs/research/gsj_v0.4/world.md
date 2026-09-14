# World — GSJ v0.4

## Two-level ontology (normative)

1. **Regulation (world).** A fixed set of rules for handling fictional application requests.
2. **Object versions.** A0, A1, A2 are versions of a *summary/conspectus* of that regulation, not the live request handler.

The experiment evaluates whether a conspectus version is **eligible for comparison** against the regulation.
It does **not** choose a project winner, authorize implementation, or execute a request.

## Regulation R0

Ordinary requests are processed in arrival order.
Urgent requests are processed before ordinary ones.
Cancelled requests are not processed, including urgent ones.
Requests on hold are not processed until the hold is lifted, including urgent ones.

## Material exceptions E (fixed set)

```text
e1 = urgent requests have priority over ordinary ones
e2 = cancelled requests are excluded, including urgent ones
e3 = requests on hold are blocked, including urgent ones
```

## Ground status R

- `R_ACTIVE`: the object version loses at least one required element of E.
- `R_REMOVED`: the object version retains all elements of E.
- `R_UNKNOWN`: available data are insufficient **or** sources conflict.
- `R_REPLACED`: old ground removed and a new ground R2 explicitly introduced (extension only).

## Decision classes (allowed)

```text
EXCLUDE
ELIGIBLE_FOR_COMPARISON
REQUEST_CLARIFICATION
SUSPEND_JUDGMENT
```

## Boundary constraints (always)

```text
selection_not_implied
authorization_not_implied
implementation_not_requested
```

## What is evaluated

Eligibility of the conspectus version relative to R0.
Not which real application to process.
