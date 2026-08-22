# 🏁 Mentaury Soul V1 Research/Core — Final Acceptance

```text
Status date:                    2026-08-22
Target version:                 1.0.0
Completion route:               STAGE 5 / 5
Final acceptance:               PENDING_EXACT_HEAD_CI
Distribution posture:           PROPRIETARY · ALL RIGHTS RESERVED
Runtime authorization:          NOT_GRANTED
Deployment authorization:       NOT_GRANTED
Independent human review:       NOT_CLAIMED
```

## V1 Definition of Done

Mentaury Soul V1 Research/Core is bounded to the already accepted research/core architecture and its offline epistemic flow. It is **not** a deployed autonomous runtime.

Completed V1 gates:

1. P0 foundation and bounded P1 components are implemented and retained by repository validation.
2. PCR-v0.1 represents attributed provenance-bearing claims.
3. CBP-v0.1 preserves exact PCR identity at belief genesis.
4. EPR-v0.1 routes the next epistemic owner without executing it.
5. P0-014 owns ordinary belief lifecycle and evidence attachment.
6. P0-015 alone owns `SUPPORTED` / `CONTRADICTED` Evidence Gate decisions.
7. ATR-v0.1 and HDE-v0.1 remain bounded representation/discrimination primitives without truth or runtime authority.
8. The agreed offline epistemic E2E flow is verified.
9. Reliability review produced no reproduced V1-blocking P0/P1.
10. Distribution posture is explicit: proprietary / all rights reserved.

## Accepted offline flow

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

Negative acceptance retains fail-closed behavior for provenance mismatch and stale revision.

## Explicitly outside the V1 denominator

The following remain future or separately authorized work and do **not** block V1 Research/Core:

- terminal reconsideration / successor lineage;
- retrieval execution;
- tool execution;
- autonomous inquiry or scheduler behavior;
- Action Gate runtime;
- identity or relationship runtime;
- direct or indirect M3 mutation;
- domain runtime activation;
- production deployment.

PR #149 remains closed without merge as deferred terminal-lineage work.

## Distribution boundary

The repository uses the root `LICENSE` notice with a proprietary / all-rights-reserved posture. Publication of source does not grant a general license to copy, modify, distribute, sublicense, commercialize, or create derivative works beyond rights that cannot lawfully be restricted or rights necessarily provided by the hosting platform.

```text
source visibility != open-source license
release != deployment authority
license decision != runtime GO
```

## Final acceptance gate

This document does not declare final acceptance complete until the exact final PR head passes the permanent CI path:

```text
package install / pip check
repository validator
doc freshness
complete pytest suite
compileall
```

After exact-head CI succeeds, this record and the machine/current status may be changed from `PENDING_EXACT_HEAD_CI` to `COMPLETE`, followed by one final exact-head verification. No new cognitive capability may be added inside that closure step.
