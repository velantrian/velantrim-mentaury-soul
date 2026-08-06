# ⚙️ P0-012 — Permanent GitHub Actions CI

```text
Status: IMPLEMENTATION PR
Base: main@f5dc8d6ffdd864174a7dd01a91c7e4c9526dbd4e
Scope: retained repository validation only
P0-013 R1 replay: NOT INCLUDED
Domain runtime: NOT AUTHORIZED
```

## 🎯 Goal

P0-012 converts the repeatedly proven temporary validation sequence into a
retained, read-only GitHub Actions workflow. It makes repository integrity
checks automatic on every pull request and every push to `main`.

```text
exact PR head SHA / exact push SHA
→ Python 3.13
→ locked development dependencies
→ editable package without dependency re-resolution
→ pip check
→ structural validator
→ complete pytest suite
→ compileall
```

Pull-request runs explicitly check out `github.event.pull_request.head.sha`.
Push and manual runs check out `github.sha`. The job therefore validates a
named immutable revision rather than relying on GitHub's synthetic PR merge ref.
Mergeability against the current base remains a separate GitHub property, and
the merged `main` revision must pass its own push-triggered run.

## 🔒 Security and reproducibility boundary

The workflow uses:

- top-level `permissions: contents: read`;
- explicit immutable revision checkout;
- `persist-credentials: false` during checkout;
- no repository, issue, pull-request, package or deployment writes;
- no secrets;
- no external application credentials;
- no artifact publication;
- no runtime database or user data;
- pinned action commit SHAs with release-tag comments;
- `requirements-dev.lock` for the development toolchain;
- `--no-build-isolation --no-deps` for the editable local package install;
- a 15-minute job timeout;
- concurrency cancellation for superseded commits on the same ref.

Pinned actions at implementation time:

```text
actions/checkout v7.0.1
→ 3d3c42e5aac5ba805825da76410c181273ba90b1

actions/setup-python v7.0.0
→ 5fda3b95a4ea91299a34e894583c3862153e4b97
```

A later action upgrade requires a normal reviewed PR and a new exact commit
pin. Floating branches such as `@main` are not accepted.

## 🧪 Required gates

The retained workflow must prove itself on its own pull request:

```text
GitHub parses and schedules .github/workflows/ci.yml
checked-out revision equals the current PR head
Python resolves to CPython 3.13.x
locked dependency installation succeeds
pip check succeeds
python scripts/validate.py succeeds
full pytest succeeds
compileall succeeds
```

The P0-011 adversarial module is part of the normal full pytest collection; it
is not executed through a separate privileged workflow.

## ⚖️ Preserved boundaries

```text
Green CI ≠ epistemic truth
Green CI ≠ authority approval
Green CI ≠ runtime safety proof
Exact PR-head PASS ≠ automatic proof of conflict-free merge
GitHub-hosted runner ≠ production substrate
Locked Python dev tools ≠ fully reproducible operating-system image
P0-012 ≠ R1 deterministic replay
P0-012 ≠ domain runtime authorization
```

P0-012 validates the exact repository revision selected by the workflow. It
does not protect against compromised GitHub infrastructure, a malicious action
pin, a coherent rewrite of all trust anchors or production configuration drift.

## ➡️ Next controlled milestone

After the workflow is merged, required on `main`, and status documentation is
synchronized:

```text
P0-013 → R1 Deterministic Replay
```

R1 must be designed as a separate state-projection equivalence contract. It
must not be smuggled into CI configuration or inferred from R0 PASS.
