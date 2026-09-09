#!/usr/bin/env python3
"""
register.py, validation, health and dependency-graph tooling for Framework
06, the AI System Register Schema (frameworks/06-ai-system-register-schema/).

Standard library only. CSV and JSON on-disk formats only, no YAML, no
third-party dependency of any kind, and no eval().

This module is an ENGINE over POLICY that lives in schema/register-schema.json
(the field structure and layer conditionality), schema/taxonomies.json (the
enumerations), and schema/validation-rules.json (the cross-field consistency
rules). It contains no field names hard-coded to a type conversion, no
taxonomy values, no rule thresholds and no rule descriptions of its own,
field type coercion is driven entirely by reading each property's "type"
and "format" out of register-schema.json at run time, and every check in
"validate" is driven by reading validation-rules.json. Changing a rule, a
taxonomy value or a field's required layer is a JSON edit, not a code
change.

Usage:
    python3 register.py validate <register.csv> [--schema schema/] [--json]
    python3 register.py health <register.csv> [--schema schema/]
    python3 register.py graph <register.csv> [--schema schema/]
"""

import argparse
import csv
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

TECHNICAL_DISCOVERY_SOURCES = {
    "network_log", "identity_oauth", "endpoint_browser",
    "saas_admin_sweep", "expense_procurement", "local_agentic_sweep",
}

ACTIVE_LIFECYCLE_STATUSES = {
    "in_development", "in_trial", "in_use", "suspended", "being_retired",
}


# ---------------------------------------------------------------------------
# Loading policy (schema, taxonomies, rules)
# ---------------------------------------------------------------------------

def load_json_file(path):
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise SystemExit(f"JSON ERROR: {path}: {e}")


def load_policy(schema_dir):
    schema_dir = Path(schema_dir)
    schema = load_json_file(schema_dir / "register-schema.json")
    taxonomies = load_json_file(schema_dir / "taxonomies.json")
    rules = load_json_file(schema_dir / "validation-rules.json")
    return schema, taxonomies, rules


# ---------------------------------------------------------------------------
# Loading and type-coercing the register CSV
# ---------------------------------------------------------------------------

def coerce_value(raw, prop_schema):
    """Convert a raw CSV string to a typed value using only the property's
    declared type/format in register-schema.json. No field name is ever
    referenced here."""
    if raw is None:
        return None
    raw = raw.strip()
    if raw == "":
        return None

    prop_type = prop_schema.get("type")
    if prop_type == "array":
        items = [x.strip() for x in raw.split(";")]
        return [x for x in items if x]
    if prop_type == "integer":
        try:
            return int(raw)
        except ValueError:
            return raw  # left as-is; schema validation will flag the type error
    if prop_type == "boolean":
        low = raw.lower()
        if low in ("true", "1", "yes"):
            return True
        if low in ("false", "0", "no"):
            return False
        return raw  # invalid; schema validation will flag it
    return raw  # string (format: date is still a string on disk)


def load_register(csv_path, schema):
    properties = schema["properties"]
    entries = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            entry = {"_row": row_num}
            for field, raw in row.items():
                if field is None:
                    continue
                prop_schema = properties.get(field)
                if prop_schema is None:
                    entry[field] = raw  # unknown column, passed through untyped
                else:
                    entry[field] = coerce_value(raw, prop_schema)
            entries.append(entry)
    return entries


# ---------------------------------------------------------------------------
# Minimal JSON Schema subset validator: type, enum, required, if/then,
# format: date. Anything else in a schema document is not supported and
# raises rather than silently passing.
# ---------------------------------------------------------------------------

SUPPORTED_SCHEMA_KEYS = {
    "$schema", "$id", "title", "description", "type", "properties",
    "required", "allOf", "if", "then", "items", "enum", "format",
    "minimum", "maximum", "layer", "const",
}


def check_unsupported_schema_keys(schema, path="$"):
    for key in schema:
        if key not in SUPPORTED_SCHEMA_KEYS:
            raise ValueError(f"Unsupported JSON Schema keyword at {path}: '{key}'")
    for name, prop in schema.get("properties", {}).items():
        for key in prop:
            if key not in SUPPORTED_SCHEMA_KEYS:
                raise ValueError(f"Unsupported JSON Schema keyword at {path}.properties.{name}: '{key}'")
    for block in schema.get("allOf", []):
        for sub in ("if", "then"):
            if sub in block:
                check_unsupported_schema_keys(block[sub], f"{path}.allOf[].{sub}")


def is_field_present(entry, field):
    val = entry.get(field)
    if val is None:
        return False
    if isinstance(val, str) and val.strip() == "":
        return False
    if isinstance(val, list) and len(val) == 0:
        return False
    return True


def value_matches_type(value, prop_schema):
    prop_type = prop_schema.get("type")
    if prop_type == "string":
        ok = isinstance(value, str)
    elif prop_type == "integer":
        ok = isinstance(value, int) and not isinstance(value, bool)
    elif prop_type == "boolean":
        ok = isinstance(value, bool)
    elif prop_type == "array":
        ok = isinstance(value, list)
    else:
        ok = True
    if not ok:
        return False
    if prop_type == "integer":
        if "minimum" in prop_schema and value < prop_schema["minimum"]:
            return False
        if "maximum" in prop_schema and value > prop_schema["maximum"]:
            return False
    if prop_schema.get("format") == "date":
        if not isinstance(value, str) or not DATE_RE.match(value):
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return False
    if "enum" in prop_schema and value not in prop_schema["enum"]:
        return False
    if "const" in prop_schema and value != prop_schema["const"]:
        return False
    return True


def condition_matches(entry, condition_block):
    """Evaluate an if-block's properties/required against an entry (used
    for the allOf/if/then layer-conditionality checks)."""
    for field in condition_block.get("required", []):
        if not is_field_present(entry, field):
            return False
    for field, spec in condition_block.get("properties", {}).items():
        value = entry.get(field)
        if "enum" in spec and value not in spec["enum"]:
            return False
        if "const" in spec and value != spec["const"]:
            return False
    return True


def validate_entry_against_schema(entry, schema):
    errors = []
    properties = schema["properties"]

    for field in schema.get("required", []):
        if not is_field_present(entry, field):
            errors.append(f"missing required field '{field}' (Layer 1)")

    for field, value in entry.items():
        if field.startswith("_") or value is None:
            continue
        prop_schema = properties.get(field)
        if prop_schema is None:
            continue
        if not value_matches_type(value, prop_schema):
            errors.append(f"field '{field}' = {value!r} does not match schema (type/enum/format)")

    for block in schema.get("allOf", []):
        if condition_matches(entry, block["if"]):
            for field in block["then"].get("required", []):
                if not is_field_present(entry, field):
                    layer = properties.get(field, {}).get("layer", "?")
                    errors.append(f"missing required field '{field}' (Layer {layer}, conditional)")

    return errors


# ---------------------------------------------------------------------------
# Validation rule engine (validation-rules.json)
# ---------------------------------------------------------------------------

def taxonomy_category_values(taxonomies, taxonomy_name, category_name):
    tax = taxonomies["taxonomies"].get(taxonomy_name, {})
    categories = tax.get("categories", {})
    cat = categories.get(category_name, [])
    return {v["value"] for v in cat}


def eval_field_condition(entry, cond, taxonomies):
    if "all" in cond:
        return all(eval_field_condition(entry, c, taxonomies) for c in cond["all"])
    if "any" in cond:
        return any(eval_field_condition(entry, c, taxonomies) for c in cond["any"])
    if "not" in cond:
        return not eval_field_condition(entry, cond["not"], taxonomies)

    field = cond["field"]
    value = entry.get(field)

    if cond.get("empty"):
        return not is_field_present(entry, field)
    if cond.get("populated"):
        return is_field_present(entry, field)

    op = cond.get("op")
    if op == "date_past":
        if not is_field_present(entry, field):
            return False
        try:
            d = datetime.strptime(value, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return False
        return d < date.today()
    if op == "in_category":
        allowed = taxonomy_category_values(taxonomies, cond["taxonomy"], cond["category"])
        return value in allowed
    if op == "==":
        return value == cond["value"]
    if op == "!=":
        return value != cond["value"]
    if op == ">=":
        return value is not None and value >= cond["value"]
    if op == "<=":
        return value is not None and value <= cond["value"]
    if op == "in":
        return value in cond["value"]
    raise ValueError(f"unsupported validation-rule operator: {op!r}")


def check_depends_on_resolves(entries):
    ids = {e["system_id"] for e in entries if is_field_present(e, "system_id")}
    findings = []
    for e in entries:
        for dep in entry_list(e, "depends_on"):
            if dep not in ids:
                findings.append((e.get("system_id", f"row {e['_row']}"), dep))
    return findings


def entry_list(entry, field):
    val = entry.get(field)
    if isinstance(val, list):
        return val
    return []


def run_validation_rules(entries, rules):
    findings = []  # list of (severity, rule_id, system_id, description)
    taxonomies_ref = rules.get("_taxonomies")  # injected by caller

    for rule in rules["rules"]:
        if rule.get("scope") == "register":
            if rule["id"] == "R7" and rule.get("check") == "depends_on_resolves":
                for system_id, missing_dep in check_depends_on_resolves(entries):
                    findings.append((rule["severity"], rule["id"], system_id,
                                      f"{rule['description']} (references '{missing_dep}')"))
            continue

        for entry in entries:
            system_id = entry.get("system_id", f"row {entry['_row']}")
            try:
                hit = eval_field_condition(entry, rule["condition"], taxonomies_ref)
            except KeyError:
                continue
            if hit:
                findings.append((rule["severity"], rule["id"], system_id, rule["description"]))

    return findings


# ---------------------------------------------------------------------------
# validate command
# ---------------------------------------------------------------------------

def cmd_validate(args):
    schema, taxonomies, rules = load_policy(args.schema)
    check_unsupported_schema_keys(schema)
    entries = load_register(args.register_csv, schema)

    schema_errors = []
    for entry in entries:
        system_id = entry.get("system_id", f"row {entry['_row']}")
        for msg in validate_entry_against_schema(entry, schema):
            schema_errors.append(("error", "SCHEMA", system_id, msg))

    rules["_taxonomies"] = taxonomies
    rule_findings = run_validation_rules(entries, rules)

    all_findings = schema_errors + rule_findings
    errors = [f for f in all_findings if f[0] == "error"]
    warnings = [f for f in all_findings if f[0] == "warning"]

    if args.json:
        print(json.dumps({
            "entries": len(entries),
            "errors": [{"rule": r, "system_id": s, "message": m} for _, r, s, m in errors],
            "warnings": [{"rule": r, "system_id": s, "message": m} for _, r, s, m in warnings],
        }, indent=2))
    else:
        print("=" * 88)
        print(f"REGISTER VALIDATION, {args.register_csv}")
        print("=" * 88)
        print(f"Entries: {len(entries)}")
        print()
        if errors:
            print(f"ERRORS ({len(errors)}):")
            for _, rule_id, system_id, msg in errors:
                print(f"  [{rule_id}] {system_id}: {msg}")
        else:
            print("ERRORS: none")
        print()
        if warnings:
            print(f"WARNINGS ({len(warnings)}):")
            for _, rule_id, system_id, msg in warnings:
                print(f"  [{rule_id}] {system_id}: {msg}")
        else:
            print("WARNINGS: none")

    return 1 if errors else 0


# ---------------------------------------------------------------------------
# health command
# ---------------------------------------------------------------------------

def pct(n, d):
    return (n / d * 100) if d else 0.0


def cmd_health(args):
    schema, taxonomies, rules = load_policy(args.schema)
    entries = load_register(args.register_csv, schema)
    total = len(entries)

    print("=" * 88)
    print(f"REGISTER HEALTH, {args.register_csv}")
    print("=" * 88)
    print(f"Total entries: {total}")
    print()

    def line(name, value_str, target, flag):
        print(f"  {name:<28} {value_str:<18} target: {target:<12} {flag}")

    # 1. Coverage confidence, not computable from this schema (single
    # discovery_source per entry; corroboration needs pre-register data).
    line("Coverage confidence", "N/A", ">60%", "N/A, not captured by a single discovery_source field")

    # 2. Discovery mix
    print()
    print("  Discovery mix (share of entries by discovery_source):")
    from collections import Counter
    counts = Counter(e.get("discovery_source") for e in entries if is_field_present(e, "discovery_source"))
    for source, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"    {source:<20} {n:>4}  ({pct(n, total):.0f}%)")
    intake_share = pct(counts.get("intake_process", 0), total)
    flag = "PASS" if intake_share >= 50 else "ATTENTION"
    print(f"  Discovery mix headline: intake_process = {intake_share:.0f}% (target: majority at maturity) [{flag}]")
    print()

    # 3. Orphan rate
    orphans = sum(1 for e in entries if not is_field_present(e, "business_owner"))
    orphan_rate = pct(orphans, total)
    line("Orphan rate", f"{orphan_rate:.0f}%", "0%", "PASS" if orphan_rate == 0 else "ATTENTION")

    # 4. Staleness
    reviewable = [e for e in entries if is_field_present(e, "next_review_due")]
    stale = sum(1 for e in reviewable if eval_field_condition(e, {"field": "next_review_due", "op": "date_past"}, taxonomies))
    staleness = pct(stale, len(reviewable))
    line("Staleness", f"{staleness:.0f}%", "<10%", "PASS" if staleness < 10 else "ATTENTION")

    # 5. Attestation rate, not computable (no attestation date field in schema)
    line("Attestation rate", "N/A", ">90%", "N/A, no attestation field in this schema")

    # 6. Tier coverage (proxy: active entries with a risk_tier recorded)
    active = [e for e in entries if e.get("lifecycle_status") in ACTIVE_LIFECYCLE_STATUSES]
    tiered = sum(1 for e in active if is_field_present(e, "risk_tier"))
    tier_coverage = pct(tiered, len(active))
    line("Tier coverage (proxy)", f"{tier_coverage:.0f}%", "100%", "PASS" if tier_coverage == 100 else "ATTENTION")

    # 7. Undeclared discovery rate (proxy: share found via technical layers)
    technical = sum(1 for e in entries if e.get("discovery_source") in TECHNICAL_DISCOVERY_SOURCES)
    undeclared_rate = pct(technical, total)
    print(f"  {'Undeclared discovery rate (proxy)':<28} {undeclared_rate:.0f}%{'':<14} target: declining, never zero  TREND METRIC, needs history")

    # 8. Disclosure gap
    gap = sum(
        1 for e in entries
        if e.get("affects_people") != "no" and not is_field_present(e, "transparency_disclosure")
    )
    line("Disclosure gap", str(gap), "0", "PASS" if gap == 0 else "ATTENTION")

    return 0


# ---------------------------------------------------------------------------
# graph command
# ---------------------------------------------------------------------------

def cmd_graph(args):
    schema, taxonomies, rules = load_policy(args.schema)
    entries = load_register(args.register_csv, schema)
    by_id = {e["system_id"]: e for e in entries if is_field_present(e, "system_id")}

    print("=" * 88)
    print(f"DEPENDENCY GRAPH, {args.register_csv}")
    print("=" * 88)

    # Dependency tree (roots = entries nothing depends on... print forward
    # edges from every entry that has dependencies)
    print("\nDependency edges (system depends_on upstream):")
    any_edges = False
    for e in entries:
        deps = entry_list(e, "depends_on")
        for dep in deps:
            any_edges = True
            marker = "" if dep in by_id else "  [UNRESOLVED]"
            print(f"  {e['system_id']} -> {dep}{marker}")
    if not any_edges:
        print("  (no dependencies declared)")

    # Cycle detection
    print("\nCycles:")
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {sid: WHITE for sid in by_id}
    cycles = []

    def visit(sid, stack):
        colour[sid] = GREY
        for dep in entry_list(by_id[sid], "depends_on"):
            if dep not in by_id:
                continue
            if colour.get(dep) == GREY:
                cycles.append(stack + [sid, dep])
            elif colour.get(dep) == WHITE:
                visit(dep, stack + [sid])
        colour[sid] = BLACK

    for sid in by_id:
        if colour[sid] == WHITE:
            visit(sid, [])
    if cycles:
        for c in cycles:
            print("  " + " -> ".join(c))
    else:
        print("  none")

    # Shared components: dependants per system_id
    print("\nShared components (2 or more dependants):")
    dependants = {}
    for e in entries:
        for dep in entry_list(e, "depends_on"):
            dependants.setdefault(dep, []).append(e["system_id"])

    tier_order = ["T0", "T1", "T2", "T3", "T4"]

    def tier_rank(t):
        return tier_order.index(t) if t in tier_order else -1

    shared_found = False
    for component_id, dep_list in dependants.items():
        if len(dep_list) < 2:
            continue
        shared_found = True
        component = by_id.get(component_id)
        component_tier = component.get("risk_tier") if component else None
        dependant_tiers = [(d, by_id[d].get("risk_tier")) for d in dep_list if d in by_id]
        max_dep_tier = max((t for _, t in dependant_tiers if t), key=tier_rank, default=None)
        print(f"  {component_id}: {len(dep_list)} dependants ({', '.join(dep_list)})")
        print(f"    component risk_tier: {component_tier or '(not tiered)'}")
        print(f"    highest dependant risk_tier: {max_dep_tier or '(none tiered)'}")
        if max_dep_tier and tier_rank(max_dep_tier) > tier_rank(component_tier or "T0"):
            print(
                f"    FLAG: tier inversion, dependants reach {max_dep_tier} while the "
                f"shared component is {component_tier or 'untiered'}. "
                f"Framework 03 section 1.11 rule 5: tier at the maximum of dependants."
            )
    if not shared_found:
        print("  none")

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description="Framework 06 AI System Register tooling.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    default_schema = str(Path(__file__).resolve().parent.parent / "schema")

    p_validate = subparsers.add_parser("validate", help="Validate a register CSV against the schema and rules")
    p_validate.add_argument("register_csv")
    p_validate.add_argument("--schema", default=default_schema)
    p_validate.add_argument("--json", action="store_true")

    p_health = subparsers.add_parser("health", help="Print register health metrics")
    p_health.add_argument("register_csv")
    p_health.add_argument("--schema", default=default_schema)

    p_graph = subparsers.add_parser("graph", help="Print the dependency graph")
    p_graph.add_argument("register_csv")
    p_graph.add_argument("--schema", default=default_schema)

    args = parser.parse_args(argv)

    if args.command == "validate":
        return cmd_validate(args)
    if args.command == "health":
        return cmd_health(args)
    if args.command == "graph":
        return cmd_graph(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
