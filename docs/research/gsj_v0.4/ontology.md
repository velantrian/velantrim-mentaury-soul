# Ontology — GSJ v0.4

## Objects

- `A0` — initial conspectus; loses e3 (hold block). Decisive ground R = material_exception_loss(e3).
- `A1` — revised conspectus; retains e1, e2, e3.
- `A2` — new conspectus; text/evidence insufficient to transfer A0's status.

## Modes covered by core

| State | Core case | Extension case |
|---|---|---|
| R_ACTIVE | A1, A2, A4 | — |
| R_REMOVED | A3, A7a | — |
| R_UNKNOWN | A5 | — |
| R_REPLACED | — | A6 |
| reverse direction | A8 | — |
| claim vs content | claim-content | — |
| world change, object unchanged | A7a, A7b | — |

## Coverage rule

A case may be removed before freeze only if another case covers the same mode.
Cases 4 and claim-content are paired: remove one ⇒ remove both.
A3 and A7a are paired against constant-EXCLUDE.
A2, A4, claim-content are paired against “follow latest message”.
