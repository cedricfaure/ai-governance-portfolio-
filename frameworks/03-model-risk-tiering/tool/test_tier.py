#!/usr/bin/env python3
"""Test suite for tier.py (Framework 03 tiering engine). Standard library
unittest only. Run with:  python3 -m unittest tool.test_tier  (from the
framework root) or  python3 -m unittest test_tier  (from tool/)."""

import sys
import tempfile
import unittest
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tier as T  # noqa: E402

RULES_DIR = Path(__file__).resolve().parent.parent / "rules"

DIM_KEYS = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"]

DEFAULT_FLAGS = {
    "prohibited_practice": False,
    "organisational_red_line": False,
    "determines_essential_service": False,
    "vulnerable_or_dependent_subjects": False,
    "external_high_risk_classification": False,
    "safety_or_critical_infrastructure": False,
    "no_personal_data": False,
    "no_external_effect": False,
    "no_regulatory_purpose": False,
    "is_sandbox": False,
    "no_production_data": False,
    "no_production_output": False,
    "has_declared_expiry": False,
}


def _yaml_bool(v):
    return "true" if v else "false"


def write_assessment(
    path,
    system_id="SYS-TEST",
    name="Test System",
    owner="Owner Name",
    process_owner="Process Owner Name",
    dims=None,
    flags=None,
    dependencies=None,
    is_orchestrator=False,
    autonomous_chain_length=1,
    mitigations=None,
):
    dims = dims or {k: 1 for k in DIM_KEYS}
    flags = {**DEFAULT_FLAGS, **(flags or {})}
    dependencies = dependencies or []

    lines = []
    lines.append("identity:")
    lines.append(f'  system_id: "{system_id}"')
    lines.append(f'  name: "{name}"')
    lines.append(f'  owner: "{owner}"' if owner is not None else '  owner: ""')
    lines.append(
        f'  process_owner: "{process_owner}"' if process_owner is not None else '  process_owner: ""'
    )
    lines.append('  type: "Test"')
    lines.append('  description: "Test fixture."')
    lines.append("dimensions:")
    for k in DIM_KEYS:
        lines.append(f"  {k}: {dims[k]}")
    lines.append("flags:")
    for k, v in flags.items():
        lines.append(f"  {k}: {_yaml_bool(v)}")
    lines.append("regimes_in_scope: []")
    if dependencies:
        lines.append("dependencies:")
        for d in dependencies:
            lines.append(f'  - "{d}"')
    else:
        lines.append("dependencies: []")
    lines.append("composite:")
    lines.append(f"  is_orchestrator: {_yaml_bool(is_orchestrator)}")
    lines.append(f"  autonomous_chain_length: {autonomous_chain_length}")
    if mitigations:
        lines.append("mitigations:")
        for m in mitigations:
            lines.append(f'  - control: "{m["control"]}"')
            lines.append(f'    owner: "{m["owner"]}"')
            lines.append(f'    evidence_reference: "{m["evidence_reference"]}"')
            lines.append(f'    evidence_date: "{m["evidence_date"]}"')
            lines.append(f'    addressed_dimension: "{m["addressed_dimension"]}"')
    else:
        lines.append("mitigations: []")
    lines.append('assessor: "Assessor Name"')
    lines.append('reviewer: "Reviewer Name"')
    lines.append('assessment_date: "2026-08-01"')

    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


class TestYAMLParser(unittest.TestCase):
    def test_round_trip_nested_structures(self):
        text = """\
a: 1
b:
  c: "hello: world"
  d:
    - 1
    - 2
e:
  - x: 1
    y: 2
  - x: 3
    y: 4
f: []
g: true
"""
        val = T.parse_yaml(text)
        self.assertEqual(val["a"], 1)
        self.assertEqual(val["b"]["c"], "hello: world")
        self.assertEqual(val["b"]["d"], [1, 2])
        self.assertEqual(val["e"], [{"x": 1, "y": 2}, {"x": 3, "y": 4}])
        self.assertEqual(val["f"], [])
        self.assertTrue(val["g"])


class TestRuleSet(unittest.TestCase):
    def test_ruleset_loads(self):
        ruleset = T.load_ruleset(RULES_DIR)
        self.assertEqual(len(T.dimension_defs(ruleset)), 10)

    def test_weights_validation_catches_malformed_ruleset(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "dimensions.yaml").write_text(
                """\
schema_version: "1.0.0"
families:
  impact:
    id: "A"
    name: "Impact"
    weight: 0.40
    dimensions:
      - id: "D1"
        name: "Consequence severity"
        weight: 0.40
        anchors:
          1: "a"
          2: "b"
          3: "c"
          4: "d"
          5: "e"
      - id: "D2"
        name: "Affected parties"
        weight: 0.30
        anchors:
          1: "a"
          2: "b"
          3: "c"
          4: "d"
          5: "e"
""",
                encoding="utf-8",
            )
            # deliberately incomplete — only 2 of 10 dimensions, weights
            # inside the family also do not sum to 1.0 (0.40 + 0.30 = 0.70)
            (d / "floors-and-caps.yaml").write_text(
                'schema_version: "1.0.0"\nfloors: []\ncaps: []\n', encoding="utf-8"
            )
            (d / "tiers.yaml").write_text(
                'schema_version: "1.0.0"\npercentage_bands:\n  - tier: "T1"\n'
                "    min_percentage: 0\n    max_percentage: 100\ntiers: []\n",
                encoding="utf-8",
            )
            (d / "control-obligations.yaml").write_text(
                'schema_version: "1.0.0"\ndomains: []\n', encoding="utf-8"
            )
            with self.assertRaises(T.RuleSetError):
                T.load_ruleset(d)


class TestAssessmentValidation(unittest.TestCase):
    def setUp(self):
        self.ruleset = T.load_ruleset(RULES_DIR)

    def test_out_of_range_dimension_score_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "bad.yaml"
            dims = {k: 1 for k in DIM_KEYS}
            dims["D1"] = 9
            write_assessment(path, dims=dims)
            with self.assertRaises(T.AssessmentError):
                T.tier_assessment_file(path, self.ruleset)


class TestFloorsAndCaps(unittest.TestCase):
    def setUp(self):
        self.ruleset = T.load_ruleset(RULES_DIR)

    def test_f0_short_circuits(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "prohibited.yaml"
            dims = {k: 1 for k in DIM_KEYS}
            write_assessment(path, dims=dims, flags={"prohibited_practice": True})
            result = T.tier_assessment_file(path, self.ruleset)
            self.assertEqual(result["inherent_tier"], "T0")
            self.assertEqual(result["residual_tier"], "T0")
            # nothing beyond F0 was evaluated
            trail_text = " ".join(result["trail"])
            self.assertNotIn("F1 ", trail_text)
            self.assertNotIn("F1 not", trail_text)
            self.assertNotIn("F10", trail_text)

    def test_low_score_floored_by_essential_service(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "floored.yaml"
            dims = {k: 1 for k in DIM_KEYS}  # would score T1 on its own
            write_assessment(path, dims=dims, flags={"determines_essential_service": True})
            result = T.tier_assessment_file(path, self.ruleset)
            self.assertEqual(result["provisional_tier"], "T1")
            self.assertIn("F1", result["floors_fired"])
            self.assertEqual(result["inherent_tier"], "T3")

    def test_cap_cannot_lower_below_triggered_floor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "floor_beats_cap.yaml"
            dims = {k: 1 for k in DIM_KEYS}
            # Satisfies every C1 condition (D3<=1, D4<=2, D5<=2, and the
            # three C1 flags) AND F1 (essential service) simultaneously.
            flags = {
                "determines_essential_service": True,
                "no_personal_data": True,
                "no_external_effect": True,
                "no_regulatory_purpose": True,
            }
            write_assessment(path, dims=dims, flags=flags)
            result = T.tier_assessment_file(path, self.ruleset)
            self.assertIn("F1", result["floors_fired"])
            self.assertIn("C1", result["caps_fired"])
            self.assertEqual(result["inherent_tier"], "T3")


class TestMitigationCredit(unittest.TestCase):
    def setUp(self):
        self.ruleset = T.load_ruleset(RULES_DIR)

    def test_never_reduces_from_t4(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "t4.yaml"
            dims = {k: 1 for k in DIM_KEYS}
            dims["D3"] = 5
            dims["D2"] = 4  # F9: D3==5 and D2>=4 -> T4
            mitigations = [{
                "control": "Some control",
                "owner": "Owner",
                "evidence_reference": "REF-1",
                "evidence_date": date.today().isoformat(),
                "addressed_dimension": "D3",
            }]
            write_assessment(path, dims=dims, mitigations=mitigations)
            result = T.tier_assessment_file(path, self.ruleset)
            self.assertEqual(result["inherent_tier"], "T4")
            self.assertEqual(result["residual_tier"], "T4")
            self.assertFalse(result["mitigation_applied"])

    def test_stale_evidence_refused_and_warns(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "stale.yaml"
            dims = {k: 1 for k in DIM_KEYS}
            dims["D4"] = 5  # F2 -> T3, cadence 30 days
            mitigations = [{
                "control": "Stale control",
                "owner": "Owner",
                "evidence_reference": "REF-2",
                "evidence_date": "2020-01-01",
                "addressed_dimension": "D4",
            }]
            write_assessment(path, dims=dims, mitigations=mitigations)
            result = T.tier_assessment_file(path, self.ruleset)
            self.assertEqual(result["inherent_tier"], "T3")
            self.assertEqual(result["residual_tier"], "T3")
            self.assertFalse(result["mitigation_applied"])
            self.assertTrue(any("LAPSED" in line for line in result["trail"]))

    def test_fresh_evidence_grants_one_tier_credit(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fresh.yaml"
            # Scores into the T3 band (51-75%) on the raw percentage alone,
            # with every dimension held below every floor threshold, so
            # there is no triggered floor limiting how far credit can
            # reduce the residual tier.
            dims = {
                "D1": 4, "D2": 3, "D3": 3, "D4": 3, "D5": 3,
                "D6": 3, "D7": 3, "D8": 3, "D9": 3, "D10": 3,
            }
            mitigations = [{
                "control": "Fresh control",
                "owner": "Owner",
                "evidence_reference": "REF-3",
                "evidence_date": date.today().isoformat(),
                "addressed_dimension": "D4",
            }]
            write_assessment(path, dims=dims, mitigations=mitigations)
            result = T.tier_assessment_file(path, self.ruleset)
            self.assertEqual(result["inherent_tier"], "T3")
            self.assertEqual(result["residual_tier"], "T2")
            self.assertTrue(result["mitigation_applied"])

    def test_credit_never_below_a_triggered_floor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "floor_credit.yaml"
            dims = {k: 1 for k in DIM_KEYS}
            # F1 -> minimum T3. Provisional tier stays T1 so there is
            # nothing above T3 for mitigation to "spend" — credit must not
            # push the residual tier below the floor.
            mitigations = [{
                "control": "Control",
                "owner": "Owner",
                "evidence_reference": "REF-4",
                "evidence_date": date.today().isoformat(),
                "addressed_dimension": "D1",
            }]
            write_assessment(
                path, dims=dims, flags={"determines_essential_service": True}, mitigations=mitigations
            )
            result = T.tier_assessment_file(path, self.ruleset)
            self.assertEqual(result["inherent_tier"], "T3")
            self.assertEqual(result["residual_tier"], "T3")
            self.assertFalse(result["mitigation_applied"])


class TestCompositeSystems(unittest.TestCase):
    def setUp(self):
        self.ruleset = T.load_ruleset(RULES_DIR)

    def test_orchestrator_inherits_max_reachable_action_tier(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            action_path = d / "action.yaml"
            dims_action = {k: 1 for k in DIM_KEYS}
            dims_action["D4"] = 5
            write_assessment(action_path, system_id="SYS-ACTION", dims=dims_action)

            orch_path = d / "orchestrator.yaml"
            dims_orch = {k: 1 for k in DIM_KEYS}
            write_assessment(
                orch_path,
                system_id="SYS-ORCH",
                dims=dims_orch,
                dependencies=["SYS-ACTION"],
                is_orchestrator=True,
            )
            result = T.tier_assessment_file(orch_path, self.ruleset)
            self.assertEqual(result["dimensions"]["D4"], 5)
            self.assertIn("F2", result["floors_fired"])
            self.assertEqual(result["inherent_tier"], "T3")

    def test_chain_of_three_adds_one_to_d4_capped_at_five(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "chain.yaml"
            dims = {k: 1 for k in DIM_KEYS}
            dims["D4"] = 4
            write_assessment(path, dims=dims, autonomous_chain_length=3)
            result = T.tier_assessment_file(path, self.ruleset)
            self.assertEqual(result["dimensions"]["D4"], 5)

            path2 = Path(d) / "chain2.yaml"
            dims2 = {k: 1 for k in DIM_KEYS}
            dims2["D4"] = 5
            write_assessment(path2, system_id="SYS-CHAIN2", dims=dims2, autonomous_chain_length=4)
            result2 = T.tier_assessment_file(path2, self.ruleset)
            self.assertEqual(result2["dimensions"]["D4"], 5)  # stays capped, does not go to 6

    def test_shared_dependency_tiers_at_max_of_dependants(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            shared_path = d / "shared.yaml"
            dims_shared = {k: 1 for k in DIM_KEYS}
            write_assessment(shared_path, system_id="SYS-SHARED", dims=dims_shared)

            for i in range(3):
                dep_path = d / f"dependant{i}.yaml"
                dims_dep = {k: 1 for k in DIM_KEYS}
                write_assessment(
                    dep_path,
                    system_id=f"SYS-DEP-{i}",
                    dims=dims_dep,
                    flags={"determines_essential_service": True},  # -> T3
                    dependencies=["SYS-SHARED"],
                )

            result = T.tier_assessment_file(shared_path, self.ruleset)
            self.assertEqual(result["provisional_tier"], "T1")
            self.assertEqual(result["inherent_tier"], "T3")
            self.assertEqual(len(result["common_mode_dependants"]), 3)

    def test_downstream_inheritance_of_opacity_volatility_dependency(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            upstream_path = d / "upstream.yaml"
            dims_up = {k: 1 for k in DIM_KEYS}
            dims_up["D7"] = 5
            dims_up["D9"] = 4
            dims_up["D10"] = 4
            write_assessment(upstream_path, system_id="SYS-UP", dims=dims_up)

            downstream_path = d / "downstream.yaml"
            dims_down = {k: 1 for k in DIM_KEYS}
            write_assessment(
                downstream_path, system_id="SYS-DOWN", dims=dims_down, dependencies=["SYS-UP"]
            )
            result = T.tier_assessment_file(downstream_path, self.ruleset)
            self.assertEqual(result["dimensions"]["D7"], 5)
            self.assertEqual(result["dimensions"]["D9"], 4)
            self.assertEqual(result["dimensions"]["D10"], 4)


if __name__ == "__main__":
    unittest.main()
