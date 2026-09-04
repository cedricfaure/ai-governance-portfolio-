# tier.py — deterministic tiering engine

Implements the scoring, floors and caps, residual-tier mitigation credit,
and composite-system inheritance rules from the
[Model Risk Tiering Scheme](../README.md) (Framework 03).

## Policy lives in YAML. Logic lives in Python. They must not mix.

`tier.py` contains no dimension names, no anchor text, no floor or cap
conditions, no tier definitions and no control obligations of its own —
every one of those is loaded at run time from `../rules/`. Changing the
scheme is a YAML edit that requires no code change and no Python knowledge.

This is a governance property, not an engineering preference: a rule set a
compliance officer can read and amend is auditable, and one buried in code
is not. If you find yourself wanting to add a dimension name, an anchor, a
threshold or an obligation string to `tier.py`, that value belongs in
`../rules/*.yaml` instead.

## Running it

```bash
python3 tier.py <assessment.yaml> [--rules ../rules] [--json] [--obligations]
```

- `--rules` — path to the rules directory (defaults to `../rules` relative
  to this script).
- `--obligations` — also prints the full control obligation set for the
  assigned inherent tier.
- `--json` — emits a machine-readable record instead of the human-readable
  report, suitable for populating `../template/system-register.csv`.

Exit code is non-zero on a validation failure or a T0 (refused) result;
zero otherwise.

## The YAML subset this tool accepts

No PyYAML, no third-party dependency of any kind — `tier.py` includes a
small hand-rolled parser (~150 lines) for a deliberately restricted subset
of YAML, sufficient for every file in `../rules/`, `../template/` and
`../examples/`:

- Block mappings (`key: value`), nested by 2-space indentation.
- Block sequences (`- item`), including sequences of mappings.
- Scalars: single- or double-quoted strings, unquoted strings, integers,
  floats, `true`/`false`, `null`/`~`.
- The empty collections `[]` and `{}`.
- Trailing `#` comments (only when preceded by whitespace, or at the start
  of a line; never inside a quoted string).

**Not supported:** flow-style collections other than `[]`/`{}`, multi-line
scalars (`|` and `>`), anchors and aliases, tags. Every file this framework
ships stays inside this subset. Malformed input fails loudly with the
source file and line number — it is never silently accepted.

## What the engine does, in order

1. Loads and validates the rule set (dimension weights sum to 1.0 within
   each family and across families; every dimension has all five anchors).
2. Loads the assessment and validates all ten dimension scores are present
   and in range 1–5.
3. Applies composite-system adjustments (§1.11) where dependencies are
   declared and resolvable as sibling `*.yaml` files in the same directory:
   downstream inheritance of D7/D9/D10, the chain-length adjustment to D4,
   and the orchestrator D4 union.
4. Computes the family scores, the raw score, the inherent risk percentage,
   and the provisional tier.
5. Evaluates F0 first; if it fires, stops immediately with T0.
6. Evaluates the remaining floors and takes the highest triggered.
7. Sets the Inherent Tier to the maximum of the provisional tier and the
   highest triggered floor.
8. Evaluates the caps; applies the most restrictive one only if doing so
   would not drop the tier below any triggered floor — floors always beat
   caps, unconditionally.
9. Checks the common-mode dependency rule (§1.11 rule 5) by scanning
   sibling assessment files for three or more T3-or-higher dependants.
10. Evaluates mitigation credit against the Inherent Tier to produce the
    Residual Tier — maximum one tier, never below a triggered floor, never
    from T4, never below T1, and only for mitigations with a named owner,
    an evidence reference and an evidence date inside the tier's staleness
    window (see the note on cadence below).
11. Prints the complete rule trail — every rule evaluated, whether it
    fired, and why — so a tier assignment is a decision that can be
    reviewed and re-run, not an assertion.

## A translation this tool had to make, and says so

Framework 03 §1.9 requires mitigation evidence to be dated "within the
tier's monitoring cadence" to earn credit. Part 1 states that cadence in
words only — Annual / Quarterly / Monthly / Continuous (see
`../rules/control-obligations.yaml`) — which is not by itself something
code can compare a date against. `../rules/tiers.yaml` adds an explicit
`mitigation_evidence_max_age_days` field per tier (365 / 90 / 30 / 7) as
the number that operationalises those words, documented there as exactly
what it is: an implementation translation, not additional authored policy.
Recalibrate it locally if your organisation's cadence differs.

## A limitation of the composite-system handling, stated plainly

Downstream inheritance and the orchestrator union are computed one level
deep against each declared dependency's own scores — not recursively
through the full transitive graph. The common-mode dependency check
likewise computes each candidate dependant's tier with its own common-mode
check turned off, to keep the check bounded on a dependency graph that may
contain cycles. For a portfolio small enough to review by eye this is
adequate; a large or deeply chained estate would need a proper graph
traversal with cycle detection built out further than this reference
implementation provides.

## What this tool does not do

It implements the model. It does not replace the assessor or the second-
party reviewer required by §1.13. It computes the tier a given set of
scores and flags produces under the current rule set — it does not decide
what those scores should be, and a tier without a human assessor and
reviewer behind it is not a valid assessment regardless of what the tool
prints.
