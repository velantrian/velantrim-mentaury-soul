from __future__ import annotations

import base64
import io
import zipfile
from pathlib import Path

PARTS_DIR = Path("scripts/p015_payload")
EXPECTED = {
    "src/mentaury/evidence/__init__.py",
    "src/mentaury/evidence/contracts.py",
    "src/mentaury/evidence/gate.py",
    "src/mentaury/evidence/schemas.py",
    "src/mentaury/beliefs/__init__.py",
    "src/mentaury/beliefs/evidence_gate.py",
    "src/mentaury/beliefs/gated_reducer.py",
    "tests/test_evidence_gate.py",
    "docs/P0_015_EVIDENCE_GATE.md",
}

parts = sorted(PARTS_DIR.glob("part-*.txt"))
expected_names = [f"part-{index:02d}.txt" for index in range(10)]
if [part.name for part in parts] != expected_names:
    raise RuntimeError(
        f"expected payload parts {expected_names!r}, got {[part.name for part in parts]!r}"
    )

encoded = "".join(part.read_text(encoding="utf-8").strip() for part in parts)
raw = base64.b64decode(encoded, validate=True)
with zipfile.ZipFile(io.BytesIO(raw)) as archive:
    names = set(archive.namelist())
    if names != EXPECTED:
        raise RuntimeError(f"unexpected archive members: {sorted(names ^ EXPECTED)!r}")
    bad_member = archive.testzip()
    if bad_member is not None:
        raise RuntimeError(f"corrupt archive member: {bad_member}")
    for name in sorted(names):
        target = Path(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(name))

print(f"installed {len(EXPECTED)} P0-015 target files from {len(parts)} verified chunks")
