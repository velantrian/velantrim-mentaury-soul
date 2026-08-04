"""Offline structural validation for P0-007 idempotency."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "pyproject.toml",
    "requirements-dev.lock",
    "docs/ENVIRONMENT_MANIFEST.md",
    "docs/P0_006_ATOMIC_MULTI_EVENT_BATCH.md",
    "docs/P0_007_EVENT_AWARE_IDEMPOTENCY.md",
    "src/mentaury/__init__.py",
    "src/mentaury/py.typed",
    "src/mentaury/contracts/primitives.py",
    "src/mentaury/contracts/envelopes.py",
    "src/mentaury/contracts/canonical_json.py",
    "src/mentaury/storage/__init__.py",
    "src/mentaury/storage/sqlite_store.py",
    "src/mentaury/storage/atomic_batch.py",
    "src/mentaury/storage/idempotency.py",
    "src/mentaury/validation/__init__.py",
    "src/mentaury/validation/issues.py",
    "src/mentaury/validation/specs.py",
    "src/mentaury/validation/validator.py",
    "src/mentaury/validation/registry.py",
    "tests/test_skeleton.py",
    "tests/test_envelopes.py",
    "tests/test_canonical_json.py",
    "tests/test_sqlite_store.py",
    "tests/test_schema_validation.py",
    "tests/test_atomic_batch.py",
    "tests/test_idempotency.py",
    "tests/fixtures/canonical_json_v1_vectors.json",
)
FORBIDDEN_RUNTIME_MODULES = (
    "identity_engine.py",
    "relationship_runtime.py",
    "character_engine.py",
    "curiosity_controller.py",
    "exo_cortex_runtime.py",
)


def main() -> int:
    if sys.version_info[:2] != (3, 13):
        print(f"unsupported Python: {sys.version.split()[0]} (expected 3.13.x)")
        return 1
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if missing:
        print("missing required paths:")
        for path in missing:
            print(f"- {path}")
        return 1
    found_forbidden = [
        path.name
        for path in (ROOT / "src").rglob("*.py")
        if path.name in FORBIDDEN_RUNTIME_MODULES
    ]
    if found_forbidden:
        print("forbidden domain runtime modules found:")
        for name in found_forbidden:
            print(f"- {name}")
        return 1
    print("P0-007 event-aware idempotency validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
