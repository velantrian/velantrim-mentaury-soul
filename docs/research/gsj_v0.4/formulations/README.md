# Formulations — GSJ v0.4

Each case has two formulations: **a** and **b**.
They are equivalent only if all of the following match:

1. set and quantifiers of material exceptions ("all" vs "some" matter);
2. ground status: ACTIVE / REMOVED / UNKNOWN / REPLACED;
3. object version: A0 / A1 / A2;
4. regulation version;
5. modality: assertion / question / absence of data;
6. scope of negation;
7. document completeness;
8. applicability of the evidence;
9. source status and origin.

Difference may exist only in lexicon, syntax, and sentence order.

## Certification procedure

A second reviewer receives both formulations and derives allowed answers
**without** seeing gold. The pair is certified only if the sets of allowed
substantive answers coincide. If they differ, the texts are two separate
cases or are rewritten before freeze.

Pre-written formulation files will be added after authoring; placeholders:

```text
01a.md  01b.md
02a.md  02b.md
03a.md  03b.md
04a.md  04b.md
05a.md  05b.md
07a.md  07b.md   # A7a
07b.md  07b2.md  # A7b (naming to avoid clash)
08a.md  08b.md   # A8
cc_a.md cc_b.md  # claim-content
```

No model output is viewed before certification.
