# 🏁 Mentaury Soul V1 Research/Core — Release Candidate Status

```text
Status date:                  2026-08-22
V1 completion route:         STAGE 4 / 5
Release candidate version:   1.0.0rc1
Runtime authorization:       NOT_GRANTED
Deployment authorization:    NOT_GRANTED
Independent human review:    NOT_CLAIMED
```

## Completed V1 capability gates

- Stage 1 — CBP-v0.1 claim→belief provenance binding: MERGED via PR #147.
- Stage 2 — EPR-v0.1 pure epistemic router: MERGED via PR #148.
- Stage 3 — offline epistemic end-to-end acceptance: MERGED via PR #150.
- Stage 3 exact-head evidence: Python 3.13 install PASS, validator PASS, doc freshness PASS, 1228 tests PASS, compileall PASS.

Primary accepted flow:

```text
PCR
→ EPR binding prerequisite
→ CBP / P0-014 belief genesis
→ provenance binding retained
→ EPR route to P0-015
→ P0-014 evidence attachment
→ P0-015 Evidence Gate
→ SUPPORTED terminal belief
→ EPR refuses in-place terminal revision
```

## Reliability disposition

Issue #133 contained evidence-driven hardening candidates, explicitly not confirmed defects. No listed candidate was reproduced as a P0/P1 blocker during the V1 completion route. It is therefore closed `not_planned` for V1; future concrete evidence may reopen bounded work in V1.1/V2.

```text
P0 reproduced: 0
P1 reproduced from reliability tracker: 0
Additional mandatory hardening: NONE
```

## Deferred outside V1

Terminal reconsideration/successor lineage remains future work. PR #149 was closed without merge after detecting roadmap/denominator drift. Retrieval, tools, autonomous inquiry, scheduler, identity/relationship runtime, M3 mutation, Action Gate and deployment remain outside this V1 Research/Core release.

## Remaining Stage 4 release blockers

1. Current-status/derived documentation must be reconciled from the historical pre-EPR state to merged CBP + EPR + V1 E2E reality.
2. Package version must leave placeholder `0.0.0`; this branch uses `1.0.0rc1` until final acceptance.
3. License/distribution state requires an explicit owner decision. This repository is public, but the package metadata currently says `Research-only; license not yet selected` and there is no `LICENSE` file. Engineering automation must not choose MIT/Apache/proprietary terms on the owner's behalf.

## License decision boundary

Exactly one owner decision is required before Stage 5 final release:

```text
A. choose an open-source license explicitly;
B. choose an explicit proprietary/source-available license explicitly;
C. keep no public license grant and state that distribution/use rights are not granted by publication alone.
```

The decision affects legal/distribution metadata only. It does not grant runtime, deployment or action authority.

## Stage 4 exit criteria

```text
reliability P0/P1 = 0
release-candidate package install = PASS
current docs/machine state = reconciled
license/distribution state = explicit owner decision
release candidate CI = PASS
```

Only after those are satisfied may Stage 5 set the final V1 version and perform final acceptance/release closure.
