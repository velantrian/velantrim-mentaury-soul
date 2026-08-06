from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{path}: expected exactly one marker, found {count}: {old!r}"
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


readme = Path("README.md")
replace_once(
    readme,
    "P0-001…P0-011_IMPLEMENTED_IN_MAIN",
    "P0-001…P0-012_IMPLEMENTED_IN_MAIN",
)
replace_once(
    readme,
    "P0-011_FINAL_EXACT_HEAD_VALIDATION_PASS",
    "P0-012_PERMANENT_CI_PR_AND_MAIN_VALIDATION_PASS",
)
replace_once(
    readme,
    "P0-012…P0-015_NOT_IMPLEMENTED",
    "P0-013…P0-015_NOT_IMPLEMENTED",
)
replace_once(
    readme,
    "PERMANENT_GITHUB_ACTIONS_NOT_PRESENT",
    "PERMANENT_GITHUB_ACTIONS_PRESENT_AND_VALIDATED",
)
replace_once(
    readme,
    "│   ├── P0-012 permanent CI\n",
    "│   ├── P0-012 permanent CI ✅\n",
)
replace_once(
    readme,
    "P0-011 → adversarial integrity gate + request-bound idempotency receipts\n",
    "P0-011 → adversarial integrity gate + request-bound idempotency receipts\n"
    "P0-012 → permanent read-only exact-revision GitHub Actions CI\n",
)
replace_once(
    readme,
    "P0-001…P0-011 ✅\n"
    "→ P0-012 Permanent GitHub Actions CI\n"
    "→ P0-013 R1 Deterministic Replay",
    "P0-001…P0-012 ✅\n"
    "→ P0-013 R1 Deterministic Replay",
)
replace_once(
    readme,
    "- [🧨 P0-011 Adversarial Integrity Suite](docs/P0_011_ADVERSARIAL_INTEGRITY_SUITE.md)\n",
    "- [🧨 P0-011 Adversarial Integrity Suite](docs/P0_011_ADVERSARIAL_INTEGRITY_SUITE.md)\n"
    "- [⚙️ P0-012 Permanent GitHub Actions CI](docs/P0_012_PERMANENT_CI.md)\n",
)
replace_once(readme, "❌ permanent GitHub Actions CI\n", "")
replace_once(readme, "❌ governed payload redaction\n", "")
replace_once(
    readme,
    "работающий инфраструктурный P0-фундамент до P0-009.",
    "работающий инфраструктурный P0-фундамент до P0-012.",
)

status = Path("docs/CURRENT_STATUS.md")
replace_once(
    status,
    "Verified implementation head:  5640bd6ce650818c731e09391434ac12a0aec5e6",
    "Verified implementation head:  a536ea0afa526e86827f5ce9d5aa6fd5b7170fab",
)
replace_once(
    status,
    "P0-001…P0-011_IMPLEMENTED_IN_MAIN",
    "P0-001…P0-012_IMPLEMENTED_IN_MAIN",
)
replace_once(
    status,
    "P0-011_FINAL_EXACT_HEAD_VALIDATION_PASS",
    "P0-012_PERMANENT_CI_PR_AND_MAIN_VALIDATION_PASS",
)
replace_once(
    status,
    "P0-012…P0-015_NOT_IMPLEMENTED",
    "P0-013…P0-015_NOT_IMPLEMENTED",
)
replace_once(
    status,
    "PERMANENT_GITHUB_ACTIONS_NOT_PRESENT",
    "PERMANENT_GITHUB_ACTIONS_PRESENT_AND_VALIDATED",
)
replace_once(
    status,
    "| P0-011 Adversarial Integrity Suite | ✅ Implemented | adversarial PASS ≠ total-database authenticity |\n",
    "| P0-011 Adversarial Integrity Suite | ✅ Implemented | adversarial PASS ≠ total-database authenticity |\n"
    "| P0-012 Permanent GitHub Actions CI | ✅ Implemented | green CI ≠ branch protection or runtime safety |\n",
)
section = '''
# ✅ P0-012 — Permanent GitHub Actions CI

Merged PR and retained workflow:

```text
PR:                  #25
Final tested head:   49d752285e4c1c3fdb59382e916e32e9862d5f89
Merge SHA:           a536ea0afa526e86827f5ce9d5aa6fd5b7170fab
PR workflow run:     31085542227
Main push run:       31085727308
Python:              CPython 3.13.14
Full pytest:         163 passed on PR and main
Token permissions:  contents: read · metadata: read
```

Реализовано:

- retained `.github/workflows/ci.yml` on pull requests and pushes to `main`;
- explicit immutable PR-head or push-SHA checkout;
- `persist-credentials: false`;
- full commit-SHA pins for checkout and Python setup actions;
- locked development-tool installation and `pip check`;
- structural validator, complete pytest and compileall;
- concurrency cancellation and bounded job timeout;
- no secrets, artifacts, deployments or repository writes.

```text
Green CI ≠ epistemic truth
Green CI ≠ authority approval
P0-012 ≠ branch-protection enforcement
GitHub-hosted runner ≠ production substrate
P0-012 merged ≠ R1 deterministic replay
P0-012 merged ≠ domain runtime authorization
```

---

'''
replace_once(status, "# 🔴 Не реализовано\n", section + "# 🔴 Не реализовано\n")
replace_once(
    status,
    "P0-012 Permanent GitHub Actions CI     → NOT IMPLEMENTED\n",
    "",
)
replace_once(
    status,
    "P0-001…P0-011 ✅ merged in main\n"
    "→ P0-012 permanent GitHub Actions CI\n"
    "→ P0-013 R1 deterministic replay",
    "P0-001…P0-012 ✅ merged in main\n"
    "→ P0-013 R1 deterministic replay",
)
replace_once(
    status,
    "P0-012 PERMANENT GITHUB ACTIONS CI\n"
    "Status: NOT IMPLEMENTED\n"
    "Precondition: retain the proven Python 3.13 validator + full pytest + compileall commands as read-only pull-request and main gates",
    "P0-013 R1 DETERMINISTIC REPLAY\n"
    "Status: NOT IMPLEMENTED\n"
    "Precondition: define deterministic projection input/output contracts and replay-equivalence evidence without treating R0 PASS as state equivalence",
)

spec = Path("docs/P0_012_PERMANENT_CI.md")
replace_once(
    spec,
    "Status: IMPLEMENTATION PR\n"
    "Base: main@2a6938b2a71d56f608b52c761a6f39849f844385",
    "Status: MERGED · MAIN PUSH VALIDATED · POST-MERGE SYNCED\n"
    "Base: main@2a6938b2a71d56f608b52c761a6f39849f844385\n"
    "Final tested head: 49d752285e4c1c3fdb59382e916e32e9862d5f89\n"
    "Merge SHA: a536ea0afa526e86827f5ce9d5aa6fd5b7170fab\n"
    "PR run: 31085542227 · PASS\n"
    "Main push run: 31085727308 · PASS",
)
checkpoint = '''
## ✅ Final merge checkpoint

```text
Merged PR                #25
Final tested PR head     49d752285e4c1c3fdb59382e916e32e9862d5f89
Merge SHA                a536ea0afa526e86827f5ce9d5aa6fd5b7170fab
PR retained CI run       31085542227 · PASS
Main retained CI run     31085727308 · PASS
CPython                  3.13.14
Full pytest              163 passed on both revisions
Validator / compileall   PASS
Permissions              contents: read · metadata: read
```

Both runs checked out the exact named revision. The merged workflow is retained
in `main`; no temporary validation workflow is required for subsequent PRs.
Branch-protection enforcement remains a separate repository-setting decision.

'''
replace_once(
    spec,
    "## ➡️ Next controlled milestone\n",
    checkpoint + "## ➡️ Next controlled milestone\n",
)
