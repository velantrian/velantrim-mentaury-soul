from __future__ import annotations

from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


readme = Path("README.md")
replace_once(readme, "P0-001…P0-010_IMPLEMENTED_IN_MAIN", "P0-001…P0-011_IMPLEMENTED_IN_MAIN")
replace_once(readme, "P0-010_FINAL_EXACT_HEAD_VALIDATION_PASS", "P0-011_FINAL_EXACT_HEAD_VALIDATION_PASS")
replace_once(readme, "P0-011…P0-015_NOT_IMPLEMENTED", "P0-012…P0-015_NOT_IMPLEMENTED")
replace_once(readme, "│   ├── P0-011 adversarial suite\n", "│   ├── P0-011 adversarial suite ✅\n")
replace_once(
    readme,
    "P0-010 → atomic same-stream redaction + complete governed-evidence linkage\n",
    "P0-010 → atomic same-stream redaction + complete governed-evidence linkage\nP0-011 → adversarial integrity gate + request-bound idempotency receipts\n",
)
replace_once(
    readme,
    "P0-001…P0-010 ✅\n→ P0-011 Adversarial Integrity Suite\n→ P0-012 Permanent GitHub Actions CI",
    "P0-001…P0-011 ✅\n→ P0-012 Permanent GitHub Actions CI",
)
replace_once(
    readme,
    "- [🗑️ P0-010 Atomic Same-Stream Redaction](docs/P0_010_ATOMIC_SAME_STREAM_REDACTION.md)\n",
    "- [🗑️ P0-010 Atomic Same-Stream Redaction](docs/P0_010_ATOMIC_SAME_STREAM_REDACTION.md)\n- [🧨 P0-011 Adversarial Integrity Suite](docs/P0_011_ADVERSARIAL_INTEGRITY_SUITE.md)\n",
)

status = Path("docs/CURRENT_STATUS.md")
replace_once(status, "Verified implementation head:  7f78dd2c7db45206f293f0278a51033474db4918", "Verified implementation head:  5640bd6ce650818c731e09391434ac12a0aec5e6")
replace_once(status, "P0-001…P0-010_IMPLEMENTED_IN_MAIN", "P0-001…P0-011_IMPLEMENTED_IN_MAIN")
replace_once(status, "P0-010_FINAL_EXACT_HEAD_VALIDATION_PASS", "P0-011_FINAL_EXACT_HEAD_VALIDATION_PASS")
replace_once(status, "P0-011…P0-015_NOT_IMPLEMENTED", "P0-012…P0-015_NOT_IMPLEMENTED")
replace_once(
    status,
    "| P0-010 Atomic Same-Stream Redaction | ✅ Implemented | payload removal ≠ event-provenance deletion |\n",
    "| P0-010 Atomic Same-Stream Redaction | ✅ Implemented | payload removal ≠ event-provenance deletion |\n| P0-011 Adversarial Integrity Suite | ✅ Implemented | adversarial PASS ≠ total-database authenticity |\n",
)
section = '''
# ✅ P0-011 — Adversarial Integrity Suite

Merged PR:

```text
PR:                #21
Final tested head: c21fe2503a31a73e1fe17e89dc92841ed35a65f3
Merge SHA:         5640bd6ce650818c731e09391434ac12a0aec5e6
Validation run:    31084297081
Python:            CPython 3.13.14
Full pytest:       163 passed
Review:            two-pass exact-head audit; automated review quota unavailable
```

Реализовано:

- 19 adversarial attack families across R0, governed redaction and idempotency receipts;
- actual middle/tail event-deletion detection;
- malformed, noncanonical and forged payload/chain proofs;
- redacted-payload reappearance and linked-audit corruption proofs;
- controlled `IdempotencyReceiptIntegrityError`;
- canonical stored receipt shape and version-span validation;
- receipt binding to command target, expected version and fingerprinted pending batch;
- event existence, batch shape/order, semantics, payload digest, initiator and authority checks;
- rollback without replacement writes on corrupted replay evidence.

```text
Adversarial R0 PASS ≠ epistemic truth
Idempotency receipt verification ≠ full R0 verification
Local unkeyed hash chain ≠ total-database authenticity
P0-011 merged ≠ permanent CI
P0-011 merged ≠ R1 replay
```

---

'''
replace_once(status, "# 🔴 Не реализовано\n", section + "# 🔴 Не реализовано\n")
replace_once(status, "P0-011 Adversarial Integrity Suite     → NOT IMPLEMENTED\n", "")
replace_once(
    status,
    "P0-001…P0-010 ✅ merged in main\n→ P0-011 adversarial integrity suite\n→ P0-012 permanent GitHub Actions CI",
    "P0-001…P0-011 ✅ merged in main\n→ P0-012 permanent GitHub Actions CI",
)
replace_once(
    status,
    "P0-011 ADVERSARIAL INTEGRITY SUITE\nStatus: NOT IMPLEMENTED\nPrecondition: combine tampering, migration, concurrency, redaction and resource-boundary proofs into one controlled matrix",
    "P0-012 PERMANENT GITHUB ACTIONS CI\nStatus: NOT IMPLEMENTED\nPrecondition: retain the proven Python 3.13 validator + full pytest + compileall commands as read-only pull-request and main gates",
)

spec = Path("docs/P0_011_ADVERSARIAL_INTEGRITY_SUITE.md")
replace_once(spec, "Status: READY FOR FINAL REVIEW", "Status: MERGED · POST-MERGE SYNCED")
replace_once(
    spec,
    "Base: main@d05319cdcae0eb6421c6ad60649fb8ed57feba08\nScope: P0-011 only",
    "Base: main@d05319cdcae0eb6421c6ad60649fb8ed57feba08\nFinal tested head: c21fe2503a31a73e1fe17e89dc92841ed35a65f3\nMerge SHA: 5640bd6ce650818c731e09391434ac12a0aec5e6\nValidation run: 31084297081 · CPython 3.13.14 · 163 passed\nScope: P0-011 only",
)
replace_once(
    spec,
    "independent final-head review\ntemporary validation workflow absent from final diff",
    "two-pass exact-head audit completed\nautomated external review unavailable because code-review quota was exhausted\ntemporary validation workflow absent from final diff",
)
replace_once(
    spec,
    "The production and test tree passed these commands in temporary validation run\n`31083981202` with CPython `3.13.14` and `163 passed`. A final exact-head proof\nmust include this synchronized specification and remove its temporary workflow\nbefore merge.",
    "The synchronized final tree passed these commands in temporary exact-head run\n`31084297081` with CPython `3.13.14` and `163 passed`; the workflow removed\nitself before merge. Automated external review could not run because the\nconnected code-review quota was exhausted, so review `4872555946` records the\ntwo-pass exact-head audit without claiming independent approval.",
)
