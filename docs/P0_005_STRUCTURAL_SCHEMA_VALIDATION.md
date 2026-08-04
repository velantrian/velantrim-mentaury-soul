# 🧩 P0-005 — Structural Event / Payload Schema Validation

```text
Status:              P0-005
Scope:               fail-closed structural validation
Registry:            explicit and immutable
Authority checks:    NOT IMPLEMENTED
Domain semantics:    NOT IMPLEMENTED
Storage integration: NOT AUTOMATIC
Runtime authority:   NONE
```

## Purpose

P0-005 binds each admitted `event_type` to one payload-schema identity and a
strict recursive structural specification. Unknown event types fail closed.

```text
event_type
→ registered EventSchemaDefinition
→ exact payload_schema match
→ envelope-version check
→ affects-domain-state check
→ recursive payload validation
```

## Structural vocabulary

```text
StringSpec · IntegerSpec · BooleanSpec · NullSpec
ArraySpec · ObjectSpec · OneOfSpec
```

`ObjectSpec` snapshots caller-owned property mappings and rejects undeclared
fields by default.

## Registry and APIs

```text
EventSchemaDefinition · SchemaRegistry
ValidationIssue · ValidationCode · SchemaValidationError
```

The registry validates `PendingEvent`, `EventEnvelope` metadata, and an
`EventEnvelope` paired with externally loaded raw payload material. `validate_*`
returns stable issue collections; `require_*` raises one error containing them.

## Fail-closed rules

Explicit issue codes cover unknown event type, schema mismatch, unsupported
envelope version, state-effect mismatch, missing/forbidden fields, nested type
mismatch, unsupported numbers or values, invalid Unicode, non-string keys,
cycles, and minimum string/array constraints.

Portable numeric admission follows P0-003:

```text
float / Decimal → rejected
integer outside ±(2^53−1) → rejected
bool ≠ integer
```

## Boundary with P0-002

`PendingEvent` already rejects some invalid raw container shapes while freezing
its payload. Stored or externally supplied raw material therefore uses
`validate_event_payload()`; P0-002 is not weakened to make P0-005 observable.

## Deliberate non-claims

```text
Schema validity ≠ epistemic truth
Structural match ≠ semantic correctness
Registry definition ≠ Canon
Registered event ≠ authorized event
Valid payload ≠ permitted mutation
Validation result ≠ persistence
Validation result ≠ hash verification
```

P0-005 is not silently wired into P0-004 storage. Later command/batch handling
must invoke it explicitly, preventing a convenience method from becoming hidden
authority.

## Validation evidence

```text
structural validator → PASS
pytest → 43 passed
compileall → PASS
```

## Next milestone

```text
P0-006 REAL ATOMIC MULTI-EVENT BATCH
```
