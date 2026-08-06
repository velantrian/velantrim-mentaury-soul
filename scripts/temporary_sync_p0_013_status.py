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
    "P0-001…P0-012_IMPLEMENTED_IN_MAIN",
    "P0-001…P0-013_IMPLEMENTED_IN_MAIN",
)
replace_once(
    readme,
    "P0-012_PERMANENT_CI_PR_AND_MAIN_VALIDATION_PASS",
    "P0-013_R1_PR_AND_MAIN_VALIDATION_PASS",
)
replace_once(
    readme,
    "P0-013…P0-015_NOT_IMPLEMENTED",
    "P0-014…P0-015_NOT_IMPLEMENTED",
)
replace_once(readme, "│   ├── P0-013 replay\n", "│   ├── P0-013 replay ✅\n")
replace_once(
    readme,
    "P0-012 → permanent read-only exact-revision GitHub Actions CI\n",
    "P0-012 → permanent read-only exact-revision GitHub Actions CI\n"
    "P0-013 → neutral R1 deterministic full-replay ↔ snapshot-tail equivalence\n",
)
replace_once(
    readme,
    "P0-001…P0-012 ✅\n"
    "→ P0-013 R1 Deterministic Replay\n"
    "→ P0-014 Minimal Belief Lifecycle",
    "P0-001…P0-013 ✅\n"
    "→ P0-014 Minimal Belief Lifecycle",
)
replace_once(
    readme,
    "- [⚙️ P0-012 Permanent GitHub Actions CI](docs/P0_012_PERMANENT_CI.md)\n",
    "- [⚙️ P0-012 Permanent GitHub Actions CI](docs/P0_012_PERMANENT_CI.md)\n"
    "- [🔁 P0-013 R1 Deterministic Replay](docs/P0_013_R1_DETERMINISTIC_REPLAY.md)\n",
)
replace_once(
    readme,
    "работающий инфраструктурный P0-фундамент до P0-012.",
    "работающий инфраструктурный P0-фундамент до P0-013.",
)

status = Path("docs/CURRENT_STATUS.md")
replace_once(
    status,
    "Verified implementation head:  a536ea0afa526e86827f5ce9d5aa6fd5b7170fab",
    "Verified implementation head:  cd069e97200d6381806642a438ec2bc64b71571e",
)
replace_once(
    status,
    "P0-001…P0-012_IMPLEMENTED_IN_MAIN",
    "P0-001…P0-013_IMPLEMENTED_IN_MAIN",
)
replace_once(
    status,
    "P0-012_PERMANENT_CI_PR_AND_MAIN_VALIDATION_PASS",
    "P0-013_R1_PR_AND_MAIN_VALIDATION_PASS",
)
replace_once(
    status,
    "P0-013…P0-015_NOT_IMPLEMENTED",
    "P0-014…P0-015_NOT_IMPLEMENTED",
)
replace_once(
    status,
    "| P0-012 Permanent GitHub Actions CI | ✅ Implemented | green CI ≠ branch protection or runtime safety |\n",
    "| P0-012 Permanent GitHub Actions CI | ✅ Implemented | green CI ≠ branch protection or runtime safety |\n"
    "| P0-013 R1 Deterministic Replay | ✅ Implemented | deterministic replay ≠ epistemic truth |\n",
)
section = '''
# ✅ P0-013 — R1 Deterministic Replay

Merged PR and retained workflow evidence:

```text
PR:                  #27
Final tested head:   d5be2702f71a800c6d171a2c4cbea2cd449a2e64
Merge SHA:           cd069e97200d6381806642a438ec2bc64b71571e
PR workflow run:     31087648122
Main push run:       31087777833
Python:              CPython 3.13.14
Full pytest:         186 passed on PR and main
Review:              exact-head two-pass audit 4872928159
```

Реализовано:

- neutral versioned `ReplayReducer`, immutable `ReplaySnapshot`, `ReplayStateBudget` and `R1ReplayReport`;
- bounded R0 prerequisite and domain-separated canonical projection-state hash;
- one SQLite read snapshot across R0, event capture, metadata, payload reads and replay;
- fail-closed refusal to certify outer uncommitted transactions;
- exact verified-prefix version and tail-event-hash reporting under concurrent append;
- snapshot reducer/stream/version/anchor/hash verification;
- full-replay checkpoint equality before snapshot-tail replay;
- replay-time canonical payload and immutable digest verification;
- fail-closed state-affecting redaction boundary;
- immutable reducer inputs and dual transition execution;
- observable nondeterminism, input reuse, reducer exception and invalid-state rejection;
- caller-supplied event/payload and projection-state resource budgets;
- 23 replay-specific tests within the permanent 186-test suite.

```text
R1 PASS ≠ epistemic truth
R1 PASS ≠ reducer semantic correctness
R1 PASS ≠ hidden-side-effect proof
R1 PASS ≠ snapshot persistence authorization
P0-013 merged ≠ P0-014 belief lifecycle
P0-013 merged ≠ domain runtime authorization
```

Automated external code review remained unavailable because the connected review
quota was exhausted. Review `4872928159` records a second-pass exact-head audit
without claiming independent external approval.

---

'''
replace_once(status, "# 🔴 Не реализовано\n", section + "# 🔴 Не реализовано\n")
replace_once(
    status,
    "P0-013 R1 Deterministic Replay         → NOT IMPLEMENTED\n",
    "",
)
replace_once(
    status,
    "P0-001…P0-012 ✅ merged in main\n"
    "→ P0-013 R1 deterministic replay\n"
    "→ P0-014 minimal belief lifecycle",
    "P0-001…P0-013 ✅ merged in main\n"
    "→ P0-014 minimal belief lifecycle",
)
replace_once(
    status,
    "P0-013 R1 DETERMINISTIC REPLAY\n"
    "Status: NOT IMPLEMENTED\n"
    "Precondition: define deterministic projection input/output contracts and replay-equivalence evidence without treating R0 PASS as state equivalence",
    "P0-014 MINIMAL BELIEF LIFECYCLE\n"
    "Status: NOT IMPLEMENTED\n"
    "Precondition: define evidence-referenced belief commands/events, deterministic lifecycle transitions and R1-compatible projection state without granting truth or identity authority",
)

spec = Path("docs/P0_013_R1_DETERMINISTIC_REPLAY.md")
replace_once(
    spec,
    "Status: FINAL CANDIDATE · EXACT-HEAD CI REQUIRED\n"
    "Base: main@dda1604253a49f0d88c77d01491a44cc3f09fe53\n"
    "Hardened lineage through: 4cfa6d8714bfa3a889e7b95c44cf2824345a1251",
    "Status: MERGED · MAIN PUSH VALIDATED · POST-MERGE SYNCED\n"
    "Base: main@dda1604253a49f0d88c77d01491a44cc3f09fe53\n"
    "Final tested head: d5be2702f71a800c6d171a2c4cbea2cd449a2e64\n"
    "Merge SHA: cd069e97200d6381806642a438ec2bc64b71571e\n"
    "PR run: 31087648122 · PASS\n"
    "Main push run: 31087777833 · PASS",
)
replace_once(
    spec,
    "The final owner-authored candidate must pass retained\n"
    "`Mentaury CI` on its exact immutable head before merge.",
    "The owner-authored final head passed retained `Mentaury CI` in run\n"
    "`31087648122`; the squash merge passed again on exact `main` SHA\n"
    "`cd069e97200d6381806642a438ec2bc64b71571e` in run `31087777833`.",
)
checkpoint = '''
## ✅ Final merge checkpoint

```text
Merged PR                #27
Final tested PR head     d5be2702f71a800c6d171a2c4cbea2cd449a2e64
Merge SHA                cd069e97200d6381806642a438ec2bc64b71571e
PR retained CI run       31087648122 · PASS
Main retained CI run     31087777833 · PASS
CPython                  3.13.14
Full pytest              186 passed on both revisions
Validator / compileall   PASS
Exact-head audit         4872928159
```

The final diff contained only the replay contracts, engine, exports, replay test
matrix and this specification. No snapshot persistence, domain lifecycle,
background replay worker or runtime integration was introduced.

'''
replace_once(
    spec,
    "## ➡️ Next controlled milestone\n",
    checkpoint + "## ➡️ Next controlled milestone\n",
)
