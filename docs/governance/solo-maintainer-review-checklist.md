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

## 3. Correctness pass

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

## 4. Adversarial pass

- [ ] Fail-closed behavior remains fail-closed.
- [ ] Integrity, hashes, versions, ordering, atomicity, replay, and rollback are preserved
      where applicable.
- [ ] Authority, capability, identity, truth, and external-action boundaries are not
      silently widened.
- [ ] No new secret access, token permission, writable automation, or bypass is introduced.
- [ ] Resource exhaustion, malformed input, concurrency, and partial failure were considered.
- [ ] Green CI is not being used to dismiss an unresolved material concern.

```text
Adversarial pass: PASS / CONCERNS
Authorization boundary: PRESERVED / CHANGED
Notes: <SUMMARY>
```

## 5. GitHub gates

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

## 6. Decision

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