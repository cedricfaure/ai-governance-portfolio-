#!/usr/bin/env python3
"""
tier.py — deterministic tiering engine for Framework 03, the Model Risk
Tiering Scheme (frameworks/03-model-risk-tiering/).

Standard library only. No PyYAML, no numpy, no third-party dependency of
any kind, and no eval().

This module is the ENGINE, not the POLICY. It contains no dimension names,
no anchor text, no floor or cap conditions, no tier definitions and no
control obligations of its own — every one of those lives in the YAML rule
set under ../rules/ and is loaded at run time. A rule set a compliance
officer can read and amend in YAML is auditable; one buried in code is not.
That separation is a governance property this file exists to protect, not
an engineering preference, and is the reason it is deliberately written
against a small hand-rolled YAML-subset parser rather than reaching for a
convenient library or hard-coding shortcuts.

Usage:
    python3 tier.py <assessment.yaml> [--rules ../rules] [--json] [--obligations]
"""

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

TIER_ORDER = ["T0", "T1", "T2", "T3", "T4"]


def tier_rank(tier_id):
    return TIER_ORDER.index(tier_id)


def tier_max(a, b):
    return a if tier_rank(a) >= tier_rank(b) else b


# ---------------------------------------------------------------------------
# Minimal YAML-subset parser.
#
# Supports: block mappings (key: value, 2-space-indent nesting), block
# sequences (- item, including sequences of mappings), single/double-quoted
# scalar strings, unquoted scalar strings, integers, floats, booleans
# (true/false/True/False), null (null/~), the empty collections [] and {},
# and trailing '#' comments (only when preceded by whitespace or at the
# start of a line, and never inside a quoted string).
#
# Deliberately NOT supported: flow-style collections other than [] and {},
# multi-line scalars (| and >), anchors/aliases, tags. The rule set and
# assessment files in this framework are written to stay inside this
# subset; see tool/README.md for the documented grammar.
# ---------------------------------------------------------------------------

class YAMLParseError(Exception):
    def __init__(self, message, line_no=None, source=None):
        loc = f"{source or '<yaml>'}:{line_no}" if line_no else (source or "<yaml>")
        super().__init__(f"{loc}: {message}")


def _strip_comment(raw_line):
    in_single = False
    in_double = False
    for i, ch in enumerate(raw_line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            if i == 0 or raw_line[i - 1] in (" ", "\t"):
                return raw_line[:i]
    return raw_line


def _tokenize(text, source):
    lines = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        no_comment = _strip_comment(raw.rstrip("\n"))
        stripped = no_comment.rstrip()
        if stripped.strip() == "":
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        content = stripped.strip()
        lines.append((line_no, indent, content))
    return lines


def _parse_scalar(s):
    s = s.strip()
    if s == "" or s in ("null", "~", "Null", "NULL"):
        return None
    if s == "[]":
        return []
    if s == "{}":
        return {}
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1]
    if s in ("true", "True", "TRUE"):
        return True
    if s in ("false", "False", "FALSE"):
        return False
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _parse_block(lines, pos, indent, source):
    if pos >= len(lines):
        return None, pos
    _, first_indent, first_content = lines[pos]
    if first_indent != indent:
        raise YAMLParseError(
            f"unexpected indent {first_indent}, expected {indent}",
            lines[pos][0], source,
        )
    if first_content.startswith("- ") or first_content == "-":
        return _parse_sequence(lines, pos, indent, source)
    return _parse_mapping(lines, pos, indent, source)


def _parse_sequence(lines, pos, indent, source):
    result = []
    while pos < len(lines) and lines[pos][1] == indent:
        line_no, _, content = lines[pos]
        if not (content.startswith("- ") or content == "-"):
            break
        item_content = content[2:] if content.startswith("- ") else ""
        pos += 1
        if item_content == "":
            if pos < len(lines) and lines[pos][1] > indent:
                child_indent = lines[pos][1]
                val, pos = _parse_block(lines, pos, child_indent, source)
            else:
                val = None
            result.append(val)
            continue
        if ":" in item_content and not _looks_like_plain_scalar_with_colon(item_content):
            sub_lines = [(line_no, indent + 2, item_content)]
            while pos < len(lines) and lines[pos][1] > indent:
                sub_lines.append(lines[pos])
                pos += 1
            val, _ = _parse_mapping(sub_lines, 0, indent + 2, source)
            result.append(val)
        else:
            result.append(_parse_scalar(item_content))
    return result, pos


def _looks_like_plain_scalar_with_colon(item_content):
    # A quoted scalar may legitimately contain a colon, e.g. "op: value".
    # Only treat "- key: value" as a mapping item when it is NOT a quoted
    # string as a whole.
    s = item_content.strip()
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        return True
    return False


def _parse_mapping(lines, pos, indent, source):
    result = {}
    while pos < len(lines) and lines[pos][1] == indent:
        line_no, _, content = lines[pos]
        if content.startswith("- "):
            break
        if ":" not in content:
            raise YAMLParseError(f"expected 'key: value', got '{content}'", line_no, source)
        key, _, rest = content.partition(":")
        key = _parse_scalar(key.strip())
        key = str(key)
        rest = rest.strip()
        pos += 1
        if rest == "":
            if pos < len(lines) and lines[pos][1] > indent:
                child_indent = lines[pos][1]
                val, pos = _parse_block(lines, pos, child_indent, source)
            else:
                val = None
        else:
            val = _parse_scalar(rest)
        result[key] = val
    return result, pos


def parse_yaml(text, source="<yaml>"):
    lines = _tokenize(text, source)
    if not lines:
        return {}
    root_indent = lines[0][1]
    val, pos = _parse_block(lines, 0, root_indent, source)
    if pos != len(lines):
        raise YAMLParseError(f"unconsumed content at line {lines[pos][0]}", lines[pos][0], source)
    return val


def load_yaml_file(path):
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise YAMLParseError(f"cannot read file: {e}", source=str(path))
    return parse_yaml(text, source=str(path))


# ---------------------------------------------------------------------------
# Rule set
# ---------------------------------------------------------------------------

class RuleSetError(Exception):
    pass


def load_ruleset(rules_dir):
    rules_dir = Path(rules_dir)
    dimensions = load_yaml_file(rules_dir / "dimensions.yaml")
    floors_caps = load_yaml_file(rules_dir / "floors-and-caps.yaml")
    tiers = load_yaml_file(rules_dir / "tiers.yaml")
    obligations = load_yaml_file(rules_dir / "control-obligations.yaml")
    ruleset = {
        "version": dimensions.get("schema_version", "unknown"),
        "dimensions": dimensions,
        "floors_and_caps": floors_caps,
        "tiers": tiers,
        "obligations": obligations,
    }
    _validate_ruleset(ruleset)
    return ruleset


def _validate_ruleset(ruleset):
    errors = []
    families = ruleset["dimensions"].get("families", {})
    family_weight_total = 0.0
    dim_ids_seen = []
    for fam_key, fam in families.items():
        fam_weight = fam.get("weight")
        if fam_weight is None:
            errors.append(f"family '{fam_key}' has no weight")
            continue
        family_weight_total += fam_weight
        dim_weight_total = 0.0
        for dim in fam.get("dimensions", []):
            dim_ids_seen.append(dim["id"])
            dim_weight_total += dim.get("weight", 0.0)
            anchors = dim.get("anchors", {})
            for level in ("1", "2", "3", "4", "5"):
                if level not in anchors:
                    errors.append(f"{dim['id']}: missing anchor for level {level}")
        if abs(dim_weight_total - 1.0) > 1e-6:
            errors.append(
                f"family '{fam_key}': within-family dimension weights sum to "
                f"{dim_weight_total}, not 1.0"
            )
    if abs(family_weight_total - 1.0) > 1e-6:
        errors.append(f"family weights sum to {family_weight_total}, not 1.0")

    expected_dims = {f"D{i}" for i in range(1, 11)}
    if set(dim_ids_seen) != expected_dims:
        errors.append(f"dimensions found {sorted(dim_ids_seen)} != expected {sorted(expected_dims)}")

    bands = ruleset["tiers"].get("percentage_bands", [])
    if not bands:
        errors.append("no percentage_bands defined in tiers.yaml")

    if errors:
        raise RuleSetError("Rule set failed validation:\n  - " + "\n  - ".join(errors))


def dimension_defs(ruleset):
    """Flat dict: dimension id -> dimension definition dict."""
    out = {}
    for fam in ruleset["dimensions"]["families"].values():
        for dim in fam["dimensions"]:
            out[dim["id"]] = dim
    return out


# ---------------------------------------------------------------------------
# Assessment loading and validation
# ---------------------------------------------------------------------------

class AssessmentError(Exception):
    pass


def load_assessment(path):
    data = load_yaml_file(path)
    return data


def validate_assessment(assessment, ruleset, source="<assessment>"):
    errors = []
    dims = assessment.get("dimensions", {}) or {}
    for dim_id in dimension_defs(ruleset):
        if dim_id not in dims:
            errors.append(f"missing dimension score for {dim_id}")
            continue
        val = dims[dim_id]
        if not isinstance(val, int) or isinstance(val, bool) or not (1 <= val <= 5):
            errors.append(f"{dim_id} = {val!r} is not an integer 1..5")

    identity = assessment.get("identity", {}) or {}
    for field in ("system_id", "name"):
        if not identity.get(field):
            errors.append(f"identity.{field} is required")

    if errors:
        raise AssessmentError(f"{source}: assessment failed validation:\n  - " + "\n  - ".join(errors))


# ---------------------------------------------------------------------------
# Condition evaluation (floors and caps)
# ---------------------------------------------------------------------------

def _get_dotted(d, path):
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def _compare(score, op, value):
    if op == "==":
        return score == value
    if op == ">=":
        return score >= value
    if op == "<=":
        return score <= value
    raise RuleSetError(f"unsupported comparison operator: {op}")


def eval_condition(cond, ctx):
    """ctx: {'dimensions': {...}, 'flags': {...}, 'raw': assessment_dict}"""
    if not isinstance(cond, dict):
        raise RuleSetError(f"malformed condition: {cond!r}")
    if "all" in cond:
        return all(eval_condition(c, ctx) for c in cond["all"])
    if "any" in cond:
        return any(eval_condition(c, ctx) for c in cond["any"])
    if "dimension" in cond:
        dim_id = cond["dimension"]
        score = ctx["dimensions"].get(dim_id)
        return _compare(score, cond["op"], cond["value"])
    if "flag" in cond:
        expected = cond.get("value", True)
        actual = bool(ctx["flags"].get(cond["flag"], False))
        return actual == bool(expected)
    if "field_empty" in cond:
        val = _get_dotted(ctx["raw"], cond["field_empty"])
        if val is None:
            return True
        if isinstance(val, str) and val.strip() == "":
            return True
        return False
    raise RuleSetError(f"unknown condition type: {cond!r}")


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def compute_family_scores(dims, ruleset):
    families = ruleset["dimensions"]["families"]
    scores = {}
    for fam_key, fam in families.items():
        total = 0.0
        for dim in fam["dimensions"]:
            total += dims[dim["id"]] * dim["weight"]
        scores[fam["id"]] = total
    return scores  # {"A": ..., "B": ..., "C": ...}


def compute_raw_and_percentage(family_scores, ruleset):
    families = ruleset["dimensions"]["families"]
    raw = 0.0
    for fam in families.values():
        raw += family_scores[fam["id"]] * fam["weight"]
    percentage = ((raw - 1) / 4) * 100
    return raw, percentage


def provisional_tier(percentage, ruleset):
    bands = sorted(ruleset["tiers"]["percentage_bands"], key=lambda b: b["max_percentage"])
    for band in bands:
        if percentage <= band["max_percentage"]:
            return band["tier"]
    return bands[-1]["tier"]


# ---------------------------------------------------------------------------
# Floors and caps
# ---------------------------------------------------------------------------

def evaluate_floors(ctx, ruleset, trail):
    floors = ruleset["floors_and_caps"]["floors"]
    f0 = next(f for f in floors if f["id"] == "F0")
    if eval_condition(f0["condition"], ctx):
        trail.append(f"F0 FIRED — {f0['description']}")
        trail.append("T0: prohibited. No further processing.")
        return "T0", ["F0"], True
    trail.append("F0 not triggered.")

    fired = []
    highest = None
    for floor in floors:
        if floor["id"] == "F0":
            continue
        hit = eval_condition(floor["condition"], ctx)
        trail.append(f"{floor['id']} {'FIRED' if hit else 'not triggered'} — {floor['description']}")
        if hit:
            fired.append(floor["id"])
            highest = floor["effect"] if highest is None else tier_max(highest, floor["effect"])
    return highest, fired, False


def evaluate_caps(ctx, ruleset, trail, floors_fired_effects):
    caps = ruleset["floors_and_caps"]["caps"]
    fired = []
    for cap in caps:
        hit = eval_condition(cap["condition"], ctx)
        trail.append(f"{cap['id']} {'FIRED' if hit else 'not triggered'} — {cap['description']}")
        if hit:
            fired.append(cap)
    if not fired:
        return None, []
    max_floor_rank = max((tier_rank(e) for e in floors_fired_effects), default=None)
    ceiling = min(fired, key=lambda c: tier_rank(c["effect"]))
    if max_floor_rank is not None and tier_rank(ceiling["effect"]) < max_floor_rank:
        trail.append(
            f"Cap {ceiling['id']} would reduce below a triggered floor — floors always beat caps. Cap not applied."
        )
        return None, [c["id"] for c in fired]
    return ceiling["effect"], [c["id"] for c in fired]


# ---------------------------------------------------------------------------
# Composite systems (§1.11)
# ---------------------------------------------------------------------------

def _sibling_assessments(assessment_path):
    """Best-effort load of every other *.yaml file in the same directory as
    a candidate assessment. Files that do not parse as an assessment (e.g.
    the template, or a non-assessment YAML) are silently skipped."""
    assessment_path = Path(assessment_path)
    out = {}
    for p in sorted(assessment_path.parent.glob("*.yaml")):
        if p.resolve() == assessment_path.resolve():
            continue
        try:
            data = load_yaml_file(p)
        except YAMLParseError:
            continue
        sid = _get_dotted(data, "identity.system_id")
        if sid:
            out[sid] = {"path": p, "data": data}
    return out


def apply_downstream_inheritance(dims, assessment, siblings, trail):
    """§1.11 rule 1: inherits the max of own and upstream D7/D9/D10."""
    deps = assessment.get("dependencies") or []
    for dep_id in deps:
        dep = siblings.get(dep_id)
        if not dep:
            trail.append(f"Dependency '{dep_id}' not resolvable in this directory — inheritance skipped for it.")
            continue
        dep_dims = dep["data"].get("dimensions", {}) or {}
        for dim_id in ("D7", "D9", "D10"):
            if dim_id in dep_dims and dep_dims[dim_id] > dims[dim_id]:
                trail.append(
                    f"Downstream inheritance: {dim_id} raised from {dims[dim_id]} to "
                    f"{dep_dims[dim_id]} (upstream dependency '{dep_id}')."
                )
                dims[dim_id] = dep_dims[dim_id]
    return dims


def apply_chain_length(dims, assessment, trail):
    """§1.11 rule 4: chains of >=3 autonomous invocations add +1 to D4, capped at 5."""
    chain_length = _get_dotted(assessment, "composite.autonomous_chain_length") or 0
    if isinstance(chain_length, int) and chain_length >= 3:
        new_d4 = min(dims["D4"] + 1, 5)
        if new_d4 != dims["D4"]:
            trail.append(
                f"Chain length {chain_length} >= 3 with no intervening human checkpoint: "
                f"D4 raised from {dims['D4']} to {new_d4} (capped at 5)."
            )
            dims["D4"] = new_d4
    return dims


def apply_orchestrator_union(dims, assessment, siblings, trail):
    """§1.11 rule 3: an orchestrator is tiered on the union of all actions
    reachable through it. Approximated here as the maximum D4 across its
    direct dependencies (one level; see tool/README.md for the limitation)."""
    is_orchestrator = _get_dotted(assessment, "composite.is_orchestrator")
    if not is_orchestrator:
        return dims
    deps = assessment.get("dependencies") or []
    for dep_id in deps:
        dep = siblings.get(dep_id)
        if not dep:
            continue
        dep_d4 = _get_dotted(dep["data"], "dimensions.D4")
        if dep_d4 and dep_d4 > dims["D4"]:
            trail.append(
                f"Orchestrator rule: D4 raised from {dims['D4']} to {dep_d4} "
                f"(reachable action via dependency '{dep_id}')."
            )
            dims["D4"] = dep_d4
    return dims


def common_mode_dependency_check(system_id, inherent_tier, assessment_path, ruleset, trail):
    """§1.11 rule 5: a component depended on by 3+ T3-or-higher systems is
    tiered at the maximum of its dependants, irrespective of its own
    standalone score. Dependants' own tiers are computed non-recursively
    (their own common-mode check is skipped) to avoid unbounded recursion
    across a dependency graph that may itself have cycles."""
    siblings = _sibling_assessments(assessment_path)
    dependants = []
    for sid, entry in siblings.items():
        deps = entry["data"].get("dependencies") or []
        if system_id in deps:
            dependants.append(entry)

    if len(dependants) < 3:
        return inherent_tier, []

    dependant_tiers = []
    qualifying = []
    for entry in dependants:
        try:
            result = _tier_pipeline(entry["data"], entry["path"], ruleset, apply_common_mode=False)
        except (AssessmentError, RuleSetError):
            continue
        dependant_tiers.append(result["inherent_tier"])
        if tier_rank(result["inherent_tier"]) >= tier_rank("T3"):
            qualifying.append((entry["data"]["identity"]["system_id"], result["inherent_tier"]))

    if len(qualifying) < 3:
        return inherent_tier, []

    max_dependant_tier = max((t for _, t in qualifying), key=tier_rank)
    new_tier = tier_max(inherent_tier, max_dependant_tier)
    trail.append(
        f"Common-mode dependency (§1.11 rule 5): {len(qualifying)} dependants at T3 or "
        f"higher share this component ({', '.join(f'{sid}={t}' for sid, t in qualifying)}). "
        f"Tiered at the maximum of its dependants: {new_tier}."
    )
    return new_tier, [sid for sid, _ in qualifying]


# ---------------------------------------------------------------------------
# Mitigation credit (§1.9)
# ---------------------------------------------------------------------------

def evaluate_mitigation_credit(assessment, inherent_tier, floors_fired, ruleset, trail, today=None):
    today = today or date.today()
    mitigations = assessment.get("mitigations") or []

    if inherent_tier == "T4":
        if mitigations:
            trail.append("Mitigation credit not available: never from T4 (§1.9).")
        return inherent_tier, False

    if inherent_tier == "T0":
        return inherent_tier, False

    if not mitigations:
        return inherent_tier, False

    tier_defs = {t["id"]: t for t in ruleset["tiers"]["tiers"]}
    max_age_days = tier_defs[inherent_tier].get("mitigation_evidence_max_age_days")

    valid = []
    for m in mitigations:
        missing = [f for f in ("owner", "evidence_reference", "evidence_date", "addressed_dimension") if not m.get(f)]
        if missing:
            trail.append(f"Mitigation '{m.get('control', '?')}' incomplete (missing {missing}) — no credit.")
            continue
        try:
            ev_date = datetime.strptime(str(m["evidence_date"]), "%Y-%m-%d").date()
        except ValueError:
            trail.append(f"Mitigation '{m.get('control', '?')}': evidence_date not parseable — no credit.")
            continue
        age = (today - ev_date).days
        if max_age_days is not None and age > max_age_days:
            trail.append(
                f"Mitigation '{m['control']}' evidence is {age} days old, exceeding the "
                f"{inherent_tier} cadence of {max_age_days} days. LAPSED — no credit."
            )
            continue
        valid.append(m)

    if not valid:
        return inherent_tier, False

    current_rank = tier_rank(inherent_tier)
    floor_ranks = [tier_rank(ruleset_floor_effect(ruleset, fid)) for fid in floors_fired]
    min_allowed_rank = max(floor_ranks) if floor_ranks else tier_rank("T1")
    candidate_rank = max(current_rank - 1, min_allowed_rank, tier_rank("T1"))
    residual_tier = TIER_ORDER[candidate_rank]

    if residual_tier == inherent_tier:
        trail.append("Mitigation evidence is valid, but a floor or the T1 minimum prevents any reduction.")
        return residual_tier, False

    trail.append(
        f"Mitigation credit applied: {len(valid)} evidenced control(s) reduce residual tier "
        f"from {inherent_tier} to {residual_tier} (maximum one tier, never below a triggered floor, never below T1)."
    )
    return residual_tier, True


def ruleset_floor_effect(ruleset, floor_id):
    for f in ruleset["floors_and_caps"]["floors"]:
        if f["id"] == floor_id:
            return f["effect"]
    return "T1"


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def _tier_pipeline(assessment, assessment_path, ruleset, apply_common_mode=True, today=None):
    validate_assessment(assessment, ruleset, source=str(assessment_path))

    trail = []
    dims = dict(assessment["dimensions"])
    flags = dict(assessment.get("flags") or {})
    identity = assessment.get("identity", {})
    system_id = identity.get("system_id")

    siblings = _sibling_assessments(assessment_path)
    dims = apply_downstream_inheritance(dims, assessment, siblings, trail)
    dims = apply_chain_length(dims, assessment, trail)
    dims = apply_orchestrator_union(dims, assessment, siblings, trail)

    family_scores = compute_family_scores(dims, ruleset)
    raw, percentage = compute_raw_and_percentage(family_scores, ruleset)
    prov_tier = provisional_tier(percentage, ruleset)
    trail.append(
        f"Family scores — A(Impact)={family_scores['A']:.3f} "
        f"B(Agency)={family_scores['B']:.3f} C(Uncertainty)={family_scores['C']:.3f}"
    )
    trail.append(f"Raw score = {raw:.3f} -> Inherent Risk Percentage = {percentage:.1f}% -> provisional tier {prov_tier}")

    ctx = {"dimensions": dims, "flags": flags, "raw": assessment}

    t0_tier, floors_fired, is_t0 = evaluate_floors(ctx, ruleset, trail)
    if is_t0:
        result = {
            "system_id": system_id,
            "name": identity.get("name"),
            "dimensions": dims,
            "family_scores": family_scores,
            "raw": raw,
            "percentage": percentage,
            "provisional_tier": prov_tier,
            "floors_fired": ["F0"],
            "caps_fired": [],
            "cap_applied": None,
            "inherent_tier": "T0",
            "residual_tier": "T0",
            "mitigation_applied": False,
            "common_mode_dependants": [],
            "trail": trail,
            "ruleset_version": ruleset["version"],
        }
        return result

    inherent_tier = prov_tier
    if floors_fired:
        highest_floor_effect = t0_tier  # holds highest floor effect, name kept from evaluate_floors return
        inherent_tier = tier_max(prov_tier, highest_floor_effect)
        trail.append(f"Floors fired: {floors_fired}. Highest floor effect: {highest_floor_effect}.")
    else:
        trail.append("No floors fired.")
    trail.append(f"Inherent Tier (pre-cap) = max(provisional {prov_tier}, floors) = {inherent_tier}")

    floor_effects = [ruleset_floor_effect(ruleset, fid) for fid in floors_fired]
    cap_effect, caps_fired = evaluate_caps(ctx, ruleset, trail, floor_effects)
    if cap_effect and tier_rank(cap_effect) < tier_rank(inherent_tier):
        trail.append(f"Cap applied: Inherent Tier lowered from {inherent_tier} to {cap_effect}.")
        inherent_tier = cap_effect
    elif caps_fired:
        trail.append("Cap condition(s) matched but did not lower the tier (already at or below the cap).")

    common_mode_dependants = []
    if apply_common_mode and system_id:
        inherent_tier, common_mode_dependants = common_mode_dependency_check(
            system_id, inherent_tier, assessment_path, ruleset, trail
        )

    trail.append(f"FINAL INHERENT TIER: {inherent_tier}")

    residual_tier, mitigation_applied = evaluate_mitigation_credit(
        assessment, inherent_tier, floors_fired, ruleset, trail, today=today
    )
    trail.append(f"RESIDUAL TIER: {residual_tier}")

    return {
        "system_id": system_id,
        "name": identity.get("name"),
        "dimensions": dims,
        "family_scores": family_scores,
        "raw": raw,
        "percentage": percentage,
        "provisional_tier": prov_tier,
        "floors_fired": floors_fired,
        "caps_fired": caps_fired,
        "cap_applied": cap_effect,
        "inherent_tier": inherent_tier,
        "residual_tier": residual_tier,
        "mitigation_applied": mitigation_applied,
        "common_mode_dependants": common_mode_dependants,
        "trail": trail,
        "ruleset_version": ruleset["version"],
    }


def tier_assessment_file(assessment_path, ruleset, today=None):
    assessment = load_assessment(assessment_path)
    return _tier_pipeline(assessment, assessment_path, ruleset, apply_common_mode=True, today=today)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_report(result, ruleset, show_obligations=False):
    print("=" * 88)
    print(f"MODEL RISK TIERING — {result['name']} ({result['system_id']})")
    print("=" * 88)
    print()
    print("Rule trail:")
    for line in result["trail"]:
        print(f"  - {line}")
    print()
    print(f"Inherent Tier:  {result['inherent_tier']}")
    print(f"Residual Tier:  {result['residual_tier']}")
    print(f"Rule-set version: {result['ruleset_version']}")
    print()

    if show_obligations:
        print("-" * 88)
        print(f"CONTROL OBLIGATIONS — {result['inherent_tier']}")
        print("-" * 88)
        if result["inherent_tier"] == "T0":
            print("  Not applicable — T0 is a refusal, not a build tier.")
        else:
            for domain in ruleset["obligations"]["domains"]:
                obligation = domain.get(result["inherent_tier"], "(not specified)")
                print(f"  {domain['name']:<28} {obligation}")


def to_json_record(result):
    return {
        "system_id": result["system_id"],
        "name": result["name"],
        "dimensions": result["dimensions"],
        "family_scores": result["family_scores"],
        "raw_score": round(result["raw"], 3),
        "inherent_risk_percentage": round(result["percentage"], 1),
        "provisional_tier": result["provisional_tier"],
        "floors_fired": result["floors_fired"],
        "caps_fired": result["caps_fired"],
        "inherent_tier": result["inherent_tier"],
        "residual_tier": result["residual_tier"],
        "mitigation_applied": result["mitigation_applied"],
        "common_mode_dependants": result["common_mode_dependants"],
        "ruleset_version": result["ruleset_version"],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Framework 03 deterministic model risk tiering engine."
    )
    parser.add_argument("assessment", help="Path to a tiering-assessment YAML file")
    parser.add_argument(
        "--rules",
        default=str(Path(__file__).resolve().parent.parent / "rules"),
        help="Path to the rules/ directory (default: ../rules relative to this script)",
    )
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable JSON record")
    parser.add_argument("--obligations", action="store_true", help="Also print the full control obligation set")
    args = parser.parse_args(argv)

    try:
        ruleset = load_ruleset(args.rules)
    except (YAMLParseError, RuleSetError) as e:
        print(f"RULE SET ERROR: {e}", file=sys.stderr)
        return 2

    try:
        result = tier_assessment_file(args.assessment, ruleset)
    except (YAMLParseError, AssessmentError) as e:
        print(f"VALIDATION ERROR: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(to_json_record(result), indent=2))
    else:
        print_report(result, ruleset, show_obligations=args.obligations)

    if result["inherent_tier"] == "T0":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
