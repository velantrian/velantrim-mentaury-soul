# Solo maintainer review checklist

Use this checklist for risk-sensitive pull requests while the repository operates without
an independent human reviewer.

## 1. Identity and evidence boundary

```text
Review mode: SOLO_MAINTAINER
Independent human review claimed: NO
PR: <NUMBER>
Reviewed head: <SHA>
Base: <BRANCH / SHA>
Risk tier: A / B / C
```

- [ ] The review is explicitly attributed to the maintainer/operator.
- [ ] Automated analysis is treated as supporting evidence, not independent approval.
- [ ] The review is bound to the exact current head SHA.

## 2. Scope

- [ ] All changed filenames were enumerated.
- [ ] The complete final diff was inspected.
- [ ] No unrelated change is hidden in the PR.
- [ ] The stated title and description match the actual diff.
- [ ] The highest-risk semantic effect determines the tier.

## 3. Multi-agent execution preflight

Use this section whenever more than one AI or automation session may have write-capable
access through the operator identity.

```text
Multi-agent writer state: SERIALIZED / NOT_APPLICABLE / CONCERN
Active writer: <SESSION / TOOL LABEL OR UNKNOWN>
Baseline main: <SHA>
Competing same-scope PR/write detected: NO / YES
Main drift reconciled: YES / NOT_APPLICABLE / NO
```

- [ ] One bounded milestone has only one active writer.
- [ ] Parallel read/audit is allowed, but no second agent is mutating the same milestone.
- [ ] The baseline `main` SHA and relevant open PRs/issues were re-read before first write.
- [ ] Current contract/authorization state was re-read before an authority-sensitive write.
- [ ] If `main` changed after baseline, the new state was compared and reconciled before continuing.
- [ ] If competing same-scope work appeared, mutation stopped until reconciliation.
- [ ] Writer transfer, if any, was followed by a fresh live-state preflight.
- [ ] A second AI agent is not being counted as independent human review.
- [ ] Authority milestones are not overlapped with another authority transition.

Any unresolved `CONCERN` or `Main drift reconciled: NO` is a merge stop for Tier A.

## 4. Correctness pass

- [ ] The root problem or intended outcome is reproduced or clearly established.
- [ ] The design preserves repository architecture and contracts.
- [ ] Compatibility and migration effects are understood.
- [ ] Tests cover the changed behavior and important regressions.
- [ ] Documentation claims match the implemented state.
- [ ] No dead code, duplicate logic, or misleading error state is introduced.

```text
Correctness pass: PASS / CONCERNS
Notes: <SUMMARY>
```

## 5. Adversarial pass

- [ ] Fail-closed behavior remains fail-closed.
- [ ] Integrity, hashes, versions, ordering, atomicity, replay, and rollback are preserved
      where applicable.
- [ ] Authority, capability, identity, truth, and external-action boundaries are not
      silently widened.
- [ ] No new secret access, token permission, writable automation, or bypass is introduced.
- [ ] Resource exhaustion, malformed input, concurrency, and partial failure were considered.
- [ ] Multi-agent races, stale-main assumptions, and conflicting authority transitions were considered.
- [ ] Green CI is not being used to dismiss an unresolved material concern.

```text
Adversarial pass: PASS / CONCERNS
Authorization boundary: PRESERVED / CHANGED
Notes: <SUMMARY>
```

## 6. GitHub gates

- [ ] Required exact-head CI completed successfully.
- [ ] The branch is up to date with `main`.
- [ ] All review conversations are resolved.
- [ ] No requested change remains unresolved.
- [ ] The PR head did not change after the recorded review.

```text
Exact-head CI: <RUN / RESULT>
Conversation state: RESOLVED
Head unchanged: YES / NO
```

## 7. Decision

```text
Decision: ACCEPTED_FOR_MERGE / STOP
Reason: <CONCISE RATIONALE>
Independent assurance: NOT CLAIMED
```

After merge:

- [ ] Verify the resulting `main` SHA.
- [ ] Verify post-merge `main` CI.
- [ ] Check for new review comments or failures.
- [ ] Synchronize authoritative Notion status only after GitHub evidence is complete.