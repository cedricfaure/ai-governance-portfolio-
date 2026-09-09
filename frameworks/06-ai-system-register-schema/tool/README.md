# register.py, register validation, health and dependency tooling

Implements schema and rule validation, the register health metrics, and dependency-graph analysis from the [AI System Register Schema](../README.md) (Framework 06).

## Policy lives in JSON. Logic lives in Python. They must not mix.

`register.py` contains no field names hard-coded to a data type, no taxonomy values and no rule descriptions or thresholds of its own. Field type coercion is driven entirely by reading each property's `type` and `format` out of `../schema/register-schema.json` at run time, and every check the `validate` command runs is read from `../schema/validation-rules.json`. Changing a rule, adding a taxonomy value, or changing which layer a field belongs to is a JSON edit, not a code change.

## Running it

```bash
python3 register.py validate <register.csv> [--schema ../schema] [--json]
python3 register.py health <register.csv> [--schema ../schema]
python3 register.py graph <register.csv> [--schema ../schema]
```

`--schema` defaults to `../schema` relative to this script.

### validate

Checks every entry against `register-schema.json`, including the layer conditionality (a `risk_tier` of T2 or above requires every Layer 2 field; `registration_required: true` requires the core Layer 3 fields), then evaluates every rule in `validation-rules.json`. Prints every error and warning with the `system_id`, the rule identifier, and the rule's description. Exits non-zero if any error is found; warnings alone do not fail the run. `--json` emits a machine-readable record instead.

A finding can come from two places, and both are legitimate: `[SCHEMA]` findings are the JSON Schema's own structural checks (a required field is missing, a value is not a valid enum member), and `[R1]` through `[R10]` findings are the named governance rules in `validation-rules.json`. Because `business_owner` is both a Layer 1 required field and the specific subject of rule R4 (the orphan rule), an entry missing it will correctly produce both a `[SCHEMA]` finding and an `[R4]` finding. This is not a bug: they are two different validation layers answering two different questions ("is this record structurally complete" and "does this record violate a named governance rule"), and R4 exists to give the orphan case a name and a citation, not merely a schema error.

### health

Prints all eight metrics from the framework's register health section, each against its stated target with a pass or attention flag. Two of the eight (coverage confidence, attestation rate) are printed as explicitly not computable from this schema and this tool alone, see the note below, rather than a fabricated number. A third (undeclared discovery rate) is printed as a single-snapshot proxy, flagged as a trend metric that needs a time series to interpret properly.

### graph

Walks the `depends_on` field across every entry and prints the dependency edges, any cycles, and every component with two or more dependants. For each shared component it prints the component's own `risk_tier` against the highest `risk_tier` among its dependants, and flags a tier inversion where a dependant carries a higher tier than the shared component itself, the composite-systems pattern Framework 03 section 1.11 rule 5 describes. Text output only.

## Two metrics this tool is honest about not being able to compute

The register health section defines **coverage confidence** as the share of entries corroborated by two or more independent discovery sources, and **attestation rate** as the share of owners confirming their entries within cadence. Neither is computable from the 45-field schema and a single CSV snapshot: the schema records one `discovery_source` per entry (correlation across sources is expected to happen before an entry is created, not after), and there is no attestation-date field in the schema at all. Rather than approximate these with a number that would look authoritative and mean nothing, `health` prints them as not applicable and says why. A programme that wants these two metrics needs to capture the underlying data (multi-source correlation records, an attestation log) outside, or in addition to, this register schema.

## What this tool does not do

It validates and reports. It does not populate the register, it does not run discovery, and it does not decide what an entry's risk tier should be, that is Framework 03's job, consumed here as a value. A clean `validate` run means the data is structurally sound and internally consistent by the rules encoded so far, not that the register is complete, discovery has finished, or every classification on it is correct.
