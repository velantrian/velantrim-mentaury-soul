# 🧱 P0-001 Environment Manifest

```text
Status:             P0-001
Profile:            Python + standard-library SQLite
Python:             3.13.x
Runtime deps:       NONE
Network at import:  FORBIDDEN
Persistence import: FORBIDDEN
Domain runtime:     FORBIDDEN
```

## Purpose

This manifest records the first replaceable implementation profile for the neutral Mentaury infrastructure skeleton. It is not part of the substrate-neutral Canon.

## Runtime boundary

The package uses no third-party runtime dependencies at P0-001. Python's standard library is the only runtime base. SQLite integration begins only in a later sequential P0 commit.

## Development lock

`requirements-dev.lock` pins the validation environment used for local tests. The lock is development-only and does not grant runtime authority to any tool.

## Supported local commands

```bash
python3 scripts/validate.py
PYTHONPATH=src python3 -m pytest
make check
```

## Directory ownership

```text
src/mentaury/core        substrate-level primitives only
src/mentaury/contracts   typed infrastructure contracts
src/mentaury/storage     replaceable storage ports/adapters
src/mentaury/validation  fail-closed structural validation
scripts                  offline repository validation
tests                    deterministic offline tests
```

## Explicit exclusions

P0-001 contains no identity engine, relationship runtime, Character Engine, Curiosity Controller, Exo-Cortex runtime, autonomous loop, background worker, network connector, persistent self-state, or direct M3 interface.

## Reproducibility note

The implementation profile is intentionally narrow. Any future Python or tool version change requires an explicit manifest and lock update with validation.
