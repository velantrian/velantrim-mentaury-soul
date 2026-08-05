"""Offline structural validation for P0-009 R0 integrity."""
from __future__ import annotations
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "pyproject.toml", "requirements-dev.lock",
    "docs/ENVIRONMENT_MANIFEST.md", "docs/P0_008_TRANSACTIONAL_CONCURRENCY.md",
    "docs/P0_009_R0_INTEGRITY.md", "src/mentaury/__init__.py",
    "src/mentaury/py.typed", "src/mentaury/contracts/primitives.py",
    "src/mentaury/contracts/envelopes.py", "src/mentaury/contracts/canonical_json.py",
    "src/mentaury/storage/__init__.py", "src/mentaury/storage/sqlite_store.py",
    "src/mentaury/storage/atomic_batch.py", "src/mentaury/storage/idempotency.py",
    "src/mentaury/storage/concurrency.py", "src/mentaury/storage/stream_meta.py",
    "src/mentaury/storage/sealing.py", "src/mentaury/storage/integrity.py",
    "src/mentaury/validation/__init__.py", "src/mentaury/validation/issues.py",
    "src/mentaury/validation/specs.py", "src/mentaury/validation/validator.py",
    "src/mentaury/validation/registry.py", "tests/test_skeleton.py",
    "tests/test_envelopes.py", "tests/test_canonical_json.py",
    "tests/test_sqlite_store.py", "tests/test_schema_validation.py",
    "tests/test_atomic_batch.py", "tests/test_idempotency.py",
    "tests/test_concurrency.py", "tests/test_integrity.py",
    "tests/fixtures/canonical_json_v1_vectors.json",
)
FORBIDDEN_RUNTIME_MODULES = (
    "identity_engine.py", "relationship_runtime.py", "character_engine.py",
    "curiosity_controller.py", "exo_cortex_runtime.py",
)
def main() -> int:
    if sys.version_info[:2] != (3, 13):
        print(f"unsupported Python: {sys.version.split()[0]} (expected 3.13.x)")
        return 1
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if missing:
        print("missing required paths:")
        for path in missing: print(f"- {path}")
        return 1
    found = [p.name for p in (ROOT / "src").rglob("*.py") if p.name in FORBIDDEN_RUNTIME_MODULES]
    if found:
        print("forbidden domain runtime modules found:")
        for name in found: print(f"- {name}")
        return 1
    print("P0-009 full R0 integrity structural validation: PASS")
    return 0
if __name__ == "__main__": raise SystemExit(main())
