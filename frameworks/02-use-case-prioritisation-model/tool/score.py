#!/usr/bin/env python3
"""
score.py — Monte Carlo portfolio scorer for Framework 02, the Use Case
Prioritisation Model (frameworks/02-use-case-prioritisation-model/).

This implements the deterministic composite score (§1.5), the
dependency-adjusted value for enablers (§1.8), and the rank-stability
Monte Carlo test (§1.9) described in that framework's README.

All numeric defaults below (axis weights, within-axis weights, the +3.0
presentation constant, the evidence-grade uncertainty widths, the Dirichlet
concentration, and the 0.30 dependency share) are calibration starting
points stated in the framework document, not empirical findings. Recalibrate
them locally once an organisation has its own realised-outcome data.

Usage:
    python3 score.py portfolio.csv [--iterations 10000] [--seed 42]

This tool implements the model. It does not replace the panel: it processes
the scores and evidence grades a cross-functional panel has already agreed;
it does not generate judgements of its own.
"""

import argparse
import csv
import sys
from dataclasses import dataclass, field

import numpy as np

# ---------------------------------------------------------------------------
# Constants — every one of these is a stated calibration default from the
# framework document, not a derived or empirical value. See the cited
# section in each comment.
# ---------------------------------------------------------------------------

# §1.3 / §1.5 — top-level axis weights. Control is subtracted, not added.
AXIS_WEIGHT_VALUE = 0.40
AXIS_WEIGHT_FEASIBILITY = 0.30
AXIS_WEIGHT_CONTROL = 0.30

# §1.5 — presentation constant. Keeps the composite positive and readable;
# carries no meaning of its own. Composite range is 0.5 .. 5.5.
COMPOSITE_OFFSET = 3.0

# §1.3 — within-axis criterion weights.
VALUE_WEIGHTS = {
    "value_netbenefit": 0.35,
    "value_strategicfit": 0.25,
    "value_mission": 0.20,
    "value_reuse": 0.20,
}
FEASIBILITY_WEIGHTS = {
    "feas_data": 0.30,
    "feas_complexity": 0.20,
    "feas_workflow": 0.25,
    "feas_sponsorship": 0.25,
}
CONTROL_WEIGHTS = {
    "ctrl_regulatory": 0.30,
    "ctrl_oversight": 0.25,
    "ctrl_assurance": 0.25,
    "ctrl_residual": 0.20,
}

# §1.9 step 1 — per-grade score uncertainty width (truncated to the 1..5
# scale). Used as the standard deviation of a normal distribution centred
# on the panel's point score.
GRADE_WIDTH = {"A": 0.25, "B": 0.4, "C": 0.6, "D": 0.9, "E": 1.3}

# Evidence grade mapped to a 1..5 confidence value, A best. §1.7 / §1.9.
GRADE_TO_CONFIDENCE = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}

# §1.9 step 2 — Dirichlet concentration for the three axis weights, chosen
# so each weight's sampled standard deviation is approximately ±5
# percentage points around its declared value (0.40 / 0.30 / 0.30).
DIRICHLET_CONCENTRATION = 90.0

# §1.9 step 3 — default iteration count.
DEFAULT_ITERATIONS = 10_000

# §1.9 interpretation rules.
TOP_QUARTILE_THRESHOLD = 0.75
DEPRIORITISED_THRESHOLD = 0.25

# §1.8 mechanism 2 — dependency-adjusted value share. A convention to stop
# enablers scoring zero, not a measurement; tune it locally.
DEPENDENCY_VALUE_SHARE = 0.30

VALUE_COLUMNS = list(VALUE_WEIGHTS)
FEASIBILITY_COLUMNS = list(FEASIBILITY_WEIGHTS)
CONTROL_COLUMNS = list(CONTROL_WEIGHTS)
ALL_SCORE_COLUMNS = VALUE_COLUMNS + FEASIBILITY_COLUMNS + CONTROL_COLUMNS


@dataclass
class Candidate:
    use_case_id: str
    name: str
    sponsor: str
    process_owner: str
    business_card_link: str
    scores: dict = field(default_factory=dict)   # column -> int 1..5
    grades: dict = field(default_factory=dict)   # column -> "A".."E"
    is_enabler: bool = False
    depends_on: list = field(default_factory=list)
    capacity_units: float = 0.0
    notes: str = ""


# ---------------------------------------------------------------------------
# Loading and validation
# ---------------------------------------------------------------------------

def load_portfolio(path):
    candidates = {}
    errors = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            use_case_id = (row.get("use_case_id") or "").strip()
            if not use_case_id:
                errors.append(f"row {row_num}: missing use_case_id")
                continue
            if use_case_id in candidates:
                errors.append(f"row {row_num}: duplicate use_case_id '{use_case_id}'")
                continue

            c = Candidate(
                use_case_id=use_case_id,
                name=(row.get("name") or "").strip(),
                sponsor=(row.get("sponsor") or "").strip(),
                process_owner=(row.get("process_owner") or "").strip(),
                business_card_link=(row.get("business_card_link") or "").strip(),
            )

            for col in ALL_SCORE_COLUMNS:
                raw = (row.get(col) or "").strip()
                if raw == "":
                    errors.append(f"row {row_num} ({use_case_id}): missing score '{col}'")
                    continue
                try:
                    val = int(raw)
                except ValueError:
                    errors.append(
                        f"row {row_num} ({use_case_id}): score '{col}' = '{raw}' is not an integer"
                    )
                    continue
                if not (1 <= val <= 5):
                    errors.append(
                        f"row {row_num} ({use_case_id}): score '{col}' = {val} is outside 1..5"
                    )
                    continue
                c.scores[col] = val

                grade_col = f"{col}_grade"
                grade_raw = (row.get(grade_col) or "").strip().upper()
                if grade_raw not in GRADE_WIDTH:
                    errors.append(
                        f"row {row_num} ({use_case_id}): grade '{grade_col}' = "
                        f"'{grade_raw}' is not one of A..E"
                    )
                    continue
                c.grades[col] = grade_raw

            enabler_raw = (row.get("is_enabler") or "").strip().lower()
            c.is_enabler = enabler_raw in ("true", "yes", "1")

            depends_raw = (row.get("depends_on") or "").strip()
            c.depends_on = [d.strip() for d in depends_raw.split(";") if d.strip()]

            cap_raw = (row.get("capacity_units") or "").strip()
            try:
                c.capacity_units = float(cap_raw) if cap_raw else 0.0
            except ValueError:
                errors.append(
                    f"row {row_num} ({use_case_id}): capacity_units '{cap_raw}' is not numeric"
                )

            c.notes = (row.get("notes") or "").strip()
            candidates[use_case_id] = c

    # Dependency references must resolve.
    for c in candidates.values():
        for dep in c.depends_on:
            if dep not in candidates:
                errors.append(
                    f"{c.use_case_id}: depends_on references unknown use_case_id '{dep}'"
                )

    # No dependency cycles (DFS, only over references that resolved).
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {cid: WHITE for cid in candidates}

    def visit(cid, stack):
        colour[cid] = GREY
        for dep in candidates[cid].depends_on:
            if dep not in candidates:
                continue
            if colour.get(dep) == GREY:
                cycle = " -> ".join(stack + [cid, dep])
                errors.append(f"dependency cycle detected: {cycle}")
            elif colour.get(dep) == WHITE:
                visit(dep, stack + [cid])
        colour[cid] = BLACK

    for cid in candidates:
        if colour[cid] == WHITE:
            visit(cid, [])

    return candidates, errors


# ---------------------------------------------------------------------------
# Deterministic scoring (§1.5)
# ---------------------------------------------------------------------------

def weighted_axis(scores, weights):
    return sum(scores[col] * w for col, w in weights.items())


def deterministic_axes(c):
    value = weighted_axis(c.scores, VALUE_WEIGHTS)
    feasibility = weighted_axis(c.scores, FEASIBILITY_WEIGHTS)
    control = weighted_axis(c.scores, CONTROL_WEIGHTS)
    return value, feasibility, control


def composite(value, feasibility, control):
    return (
        AXIS_WEIGHT_VALUE * value
        + AXIS_WEIGHT_FEASIBILITY * feasibility
        - AXIS_WEIGHT_CONTROL * control
        + COMPOSITE_OFFSET
    )


def confidence_index(grades):
    vals = [GRADE_TO_CONFIDENCE[g] for g in grades.values()]
    return sum(vals) / len(vals) if vals else 0.0


def value_axis_discovery_only(c):
    """§1.7 rule 1: a candidate whose Value axis is graded predominantly
    D-E cannot be selected for build; flag it as discovery-sprint-only."""
    value_grades = [c.grades[col] for col in VALUE_COLUMNS if col in c.grades]
    if not value_grades:
        return False
    de_count = sum(1 for g in value_grades if g in ("D", "E"))
    return (de_count / len(value_grades)) > 0.5


# ---------------------------------------------------------------------------
# Dependency-adjusted value (§1.8 mechanism 2)
# ---------------------------------------------------------------------------

def provisional_selection(candidates, base_composites):
    """A lightweight stand-in for the real, constraint-bound selection
    process in §1.10, used only to decide which downstream dependants
    count towards an enabler's dependency-adjusted value. No capacity
    constraint is available to this tool, so candidates at or above the
    portfolio's median base composite (and with no unmet dependency
    reference) are treated as 'provisionally selected'. This is a
    heuristic for the purpose of §1.8 mechanism 2 only — it is not the
    portfolio selection decision described in §1.10, which is a manual,
    constraint-bound step outside this tool's scope."""
    values = list(base_composites.values())
    median = float(np.median(values)) if values else 0.0
    selected = {cid for cid, score in base_composites.items() if score >= median}
    return selected, median


def dependants_of(candidates, cid):
    return [c.use_case_id for c in candidates.values() if cid in c.depends_on]


def dependency_adjusted_value(candidates, own_values, base_composites):
    selected, threshold = provisional_selection(candidates, base_composites)
    adjusted = {}
    for cid, c in candidates.items():
        bonus = 0.0
        for dep_id in dependants_of(candidates, cid):
            if dep_id in selected:
                bonus += DEPENDENCY_VALUE_SHARE * own_values[dep_id]
        adjusted[cid] = own_values[cid] + bonus
    return adjusted, selected, threshold


# ---------------------------------------------------------------------------
# Monte Carlo rank stability (§1.9)
# ---------------------------------------------------------------------------

def run_monte_carlo(candidates, adjusted_values, iterations, rng):
    ids = list(candidates.keys())
    n = len(ids)

    axis_weight_alpha = np.array(
        [
            AXIS_WEIGHT_VALUE * DIRICHLET_CONCENTRATION,
            AXIS_WEIGHT_FEASIBILITY * DIRICHLET_CONCENTRATION,
            AXIS_WEIGHT_CONTROL * DIRICHLET_CONCENTRATION,
        ]
    )

    composites = np.zeros((iterations, n))

    # Pre-compute score/width arrays per axis per candidate for vectorised
    # sampling: shape (n, n_criteria).
    def axis_arrays(columns):
        score_mat = np.array(
            [[candidates[cid].scores[col] for col in columns] for cid in ids]
        )
        width_mat = np.array(
            [[GRADE_WIDTH[candidates[cid].grades[col]] for col in columns] for cid in ids]
        )
        weight_vec = np.array([VALUE_WEIGHTS.get(col) or FEASIBILITY_WEIGHTS.get(col)
                                or CONTROL_WEIGHTS.get(col) for col in columns])
        return score_mat, width_mat, weight_vec

    v_scores, v_widths, v_weights = axis_arrays(VALUE_COLUMNS)
    f_scores, f_widths, f_weights = axis_arrays(FEASIBILITY_COLUMNS)
    c_scores, c_widths, c_weights = axis_arrays(CONTROL_COLUMNS)

    # Dependency bonus (fixed per iteration — the provisional selection is
    # a deterministic heuristic, not re-sampled) expressed as an addend to
    # the sampled Value axis, scaled proportionally to the Own Value share.
    own_value_axis = np.array(
        [weighted_axis(candidates[cid].scores, VALUE_WEIGHTS) for cid in ids]
    )
    value_bonus = np.array(
        [adjusted_values[cid] - own_value_axis[i] for i, cid in enumerate(ids)]
    )

    for it in range(iterations):
        v_sample = rng.normal(v_scores, v_widths)
        f_sample = rng.normal(f_scores, f_widths)
        c_sample = rng.normal(c_scores, c_widths)
        np.clip(v_sample, 1.0, 5.0, out=v_sample)
        np.clip(f_sample, 1.0, 5.0, out=f_sample)
        np.clip(c_sample, 1.0, 5.0, out=c_sample)

        value_axis = v_sample @ v_weights + value_bonus
        np.clip(value_axis, 1.0, 5.0, out=value_axis)
        feasibility_axis = f_sample @ f_weights
        control_axis = c_sample @ c_weights

        w_value, w_feas, w_ctrl = rng.dirichlet(axis_weight_alpha)
        composites[it] = (
            w_value * value_axis
            + w_feas * feasibility_axis
            - w_ctrl * control_axis
            + COMPOSITE_OFFSET
        )

    top_quartile_count = max(1, round(n * 0.25))
    top_quartile_hits = np.zeros(n)
    for it in range(iterations):
        order = np.argsort(-composites[it])
        top_quartile_hits[order[:top_quartile_count]] += 1
    p_top_quartile = top_quartile_hits / iterations

    median = np.median(composites, axis=0)
    p10 = np.percentile(composites, 10, axis=0)
    p90 = np.percentile(composites, 90, axis=0)

    results = {}
    for i, cid in enumerate(ids):
        results[cid] = {
            "median": median[i],
            "p10": p10[i],
            "p90": p90[i],
            "p_top_quartile": p_top_quartile[i],
        }
    return results


def band_for(p_top_quartile):
    if p_top_quartile > TOP_QUARTILE_THRESHOLD:
        return "Robustly prioritised"
    if p_top_quartile < DEPRIORITISED_THRESHOLD:
        return "Robustly deprioritised"
    return "Contested"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Framework 02 Monte Carlo portfolio scorer. "
        "Processes panel judgements; does not replace the panel."
    )
    parser.add_argument("portfolio_csv", help="Path to a portfolio register CSV")
    parser.add_argument("--iterations", type=int, default=DEFAULT_ITERATIONS)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    candidates, errors = load_portfolio(args.portfolio_csv)

    if errors:
        print("VALIDATION ERRORS", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    if not candidates:
        print("No candidates found in portfolio.", file=sys.stderr)
        sys.exit(1)

    rng = np.random.default_rng(args.seed)

    own_values = {}
    base_composites = {}
    axes = {}
    for cid, c in candidates.items():
        value, feasibility, control = deterministic_axes(c)
        axes[cid] = (value, feasibility, control)
        own_values[cid] = value
        base_composites[cid] = composite(value, feasibility, control)

    adjusted_values, provisional_selected, provisional_threshold = dependency_adjusted_value(
        candidates, own_values, base_composites
    )

    mc = run_monte_carlo(candidates, adjusted_values, args.iterations, rng)

    portfolio_confidence = sum(
        confidence_index(c.grades) for c in candidates.values()
    ) / len(candidates)

    ordered = sorted(candidates.keys(), key=lambda cid: -mc[cid]["median"])

    print("=" * 88)
    print("FRAMEWORK 02 — USE CASE PRIORITISATION MODEL — PORTFOLIO SCORE")
    print("=" * 88)
    print(f"Candidates: {len(candidates)}   Iterations: {args.iterations}   Seed: {args.seed}")
    print(f"Portfolio Confidence Index (mean evidence grade, A=5..E=1): {portfolio_confidence:.2f}")
    print(
        "Provisional selection for dependency-adjusted value (§1.8 mechanism 2): "
        f"base composite >= portfolio median ({provisional_threshold:.2f}). "
        "This is a heuristic used only to credit enablers — it is not the real, "
        "constraint-bound selection described in §1.10."
    )
    print()
    print("-" * 88)
    print(
        f"{'ID':<8}{'Name':<32}{'Median':>8}{'P10':>8}{'P90':>8}"
        f"{'P(TopQ)':>10}{'Conf':>6}  Band"
    )
    print("-" * 88)
    for cid in ordered:
        c = candidates[cid]
        r = mc[cid]
        conf = confidence_index(c.grades)
        band = band_for(r["p_top_quartile"])
        name = (c.name[:29] + "...") if len(c.name) > 32 else c.name
        print(
            f"{cid:<8}{name:<32}{r['median']:>8.2f}{r['p10']:>8.2f}{r['p90']:>8.2f}"
            f"{r['p_top_quartile']:>10.2f}{conf:>6.1f}  {band}"
        )

    print()
    print("-" * 88)
    print("PORTFOLIO BANDS")
    print("-" * 88)
    for band_name in ("Robustly prioritised", "Contested", "Robustly deprioritised"):
        members = [cid for cid in ordered if band_for(mc[cid]["p_top_quartile"]) == band_name]
        print(f"\n{band_name} ({len(members)}):")
        if members:
            for cid in members:
                print(f"  - {cid}  {candidates[cid].name}")
        else:
            print("  (none)")

    print()
    print("-" * 88)
    print("VALIDATION WARNINGS")
    print("-" * 88)
    warnings = []

    medians = [mc[cid]["median"] for cid in candidates]
    portfolio_median = float(np.median(medians))
    for cid, c in candidates.items():
        if c.is_enabler and mc[cid]["median"] < portfolio_median:
            warnings.append(
                f"{cid} ({c.name}): enabler scores below the portfolio median composite "
                f"({mc[cid]['median']:.2f} < {portfolio_median:.2f}). Check the minimum "
                f"enabler allocation policy (§1.11) before letting the score alone decide."
            )

    for cid, c in candidates.items():
        if value_axis_discovery_only(c):
            warnings.append(
                f"{cid} ({c.name}): Value axis is graded predominantly D-E. Per §1.7 rule 1, "
                f"this candidate cannot be selected for build — it may only be selected for a "
                f"discovery sprint whose deliverable is better evidence."
            )

    for cid, c in candidates.items():
        for dep_id in c.depends_on:
            dep_band = band_for(mc[dep_id]["p_top_quartile"])
            if dep_band != "Robustly prioritised":
                warnings.append(
                    f"{cid} ({c.name}): depends on {dep_id} ({candidates[dep_id].name}), "
                    f"which is '{dep_band}', not robustly prioritised. This dependency is "
                    f"unmet — {cid} cannot be sequenced ahead of it regardless of its own score."
                )

    if warnings:
        for w in warnings:
            print(f"  - {w}")
    else:
        print("  (none)")


if __name__ == "__main__":
    main()
