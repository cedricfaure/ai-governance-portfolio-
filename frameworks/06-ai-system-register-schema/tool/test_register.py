#!/usr/bin/env python3
"""Test suite for register.py (Framework 06 register tooling). Standard
library unittest only. Run with: python3 -m unittest tool.test_register
(from the framework root) or python3 -m unittest test_register (from
tool/)."""

import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import register as R  # noqa: E402

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schema"

BASE_FIELDS = {
    "system_id": "SYS-TEST", "name": "Test System", "description": "A test fixture.",
    "purpose": "Testing.", "business_owner": "Owner Name", "technical_owner": "Tech Owner",
    "system_type": "predictive_model", "provenance": "built_in_house", "decision_role": "informs",
    "affects_people": "no", "data_categories": "test data", "lifecycle_status": "in_use",
    "discovery_source": "intake_process", "date_registered": "2026-01-01",
}


def write_register(path, rows):
    schema, _, _ = R.load_policy(SCHEMA_DIR)
    fieldnames = list(schema["properties"].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            full = {k: "" for k in fieldnames}
            full.update(row)
            w.writerow(full)


def entry(**overrides):
    e = dict(BASE_FIELDS)
    e.update(overrides)
    return e


class TestSchemaLoading(unittest.TestCase):
    def test_policy_loads(self):
        schema, taxonomies, rules = R.load_policy(SCHEMA_DIR)
        self.assertIn("properties", schema)
        self.assertEqual(len(schema["properties"]), 45)
        self.assertIn("taxonomies", taxonomies)
        self.assertEqual(len(rules["rules"]), 10)

    def test_no_unsupported_schema_keywords(self):
        schema, _, _ = R.load_policy(SCHEMA_DIR)
        R.check_unsupported_schema_keys(schema)  # must not raise


class TestCoercion(unittest.TestCase):
    def setUp(self):
        self.schema, _, _ = R.load_policy(SCHEMA_DIR)

    def test_array_field_split_on_semicolon(self):
        prop = self.schema["properties"]["data_categories"]
        self.assertEqual(R.coerce_value("a; b ;c", prop), ["a", "b", "c"])

    def test_integer_field(self):
        prop = self.schema["properties"]["autonomy_level"]
        self.assertEqual(R.coerce_value("4", prop), 4)

    def test_boolean_field(self):
        prop = self.schema["properties"]["registration_required"]
        self.assertIs(R.coerce_value("true", prop), True)
        self.assertIs(R.coerce_value("false", prop), False)

    def test_empty_string_is_none(self):
        prop = self.schema["properties"]["vendor"]
        self.assertIsNone(R.coerce_value("", prop))
        self.assertIsNone(R.coerce_value(None, prop))


class TestSchemaValidation(unittest.TestCase):
    def setUp(self):
        self.schema, self.taxonomies, self.rules = R.load_policy(SCHEMA_DIR)

    def run_validate(self, rows):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "register.csv"
            write_register(path, rows)
            entries = R.load_register(path, self.schema)
            all_errors = []
            for e in entries:
                all_errors.extend(R.validate_entry_against_schema(e, self.schema))
            return entries, all_errors

    def test_missing_layer1_field_is_schema_error(self):
        rows = [entry()]
        rows[0]["name"] = ""
        _, errors = self.run_validate(rows)
        self.assertTrue(any("name" in e for e in errors))

    def test_invalid_enum_value_is_schema_error(self):
        rows = [entry(system_type="not_a_real_type")]
        _, errors = self.run_validate(rows)
        self.assertTrue(any("system_type" in e for e in errors))

    def test_t2_plus_requires_layer2_fields(self):
        rows = [entry(risk_tier="T3")]  # no Layer 2 fields populated
        _, errors = self.run_validate(rows)
        self.assertTrue(any("tier_date" in e for e in errors))
        self.assertTrue(any("process_owner" in e for e in errors))

    def test_t1_does_not_require_layer2_fields(self):
        rows = [entry(risk_tier="T1")]
        _, errors = self.run_validate(rows)
        self.assertEqual(errors, [])

    def test_registration_required_true_requires_layer3_fields(self):
        rows = [entry(registration_required="true")]
        _, errors = self.run_validate(rows)
        self.assertTrue(any("regimes_in_scope" in e for e in errors))
        self.assertTrue(any("registration_reference" in e for e in errors))


class TestValidationRules(unittest.TestCase):
    def setUp(self):
        self.schema, self.taxonomies, self.rules = R.load_policy(SCHEMA_DIR)
        self.rules["_taxonomies"] = self.taxonomies

    def findings_for(self, rows):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "register.csv"
            write_register(path, rows)
            entries = R.load_register(path, self.schema)
            return R.run_validation_rules(entries, self.rules)

    def test_r1_in_the_loop_and_makes(self):
        rows = [entry(human_oversight_model="in_the_loop", decision_role="makes")]
        findings = self.findings_for(rows)
        self.assertTrue(any(f[1] == "R1" and f[0] == "error" for f in findings))

    def test_r2_supports_genuine_without_monitoring_evidence(self):
        rows = [entry(decision_role="supports_genuine", monitoring_in_place="")]
        findings = self.findings_for(rows)
        self.assertTrue(any(f[1] == "R2" for f in findings))

    def test_r2_does_not_fire_when_monitoring_evidenced(self):
        rows = [entry(decision_role="supports_genuine", monitoring_in_place="drift_and_subgroup")]
        findings = self.findings_for(rows)
        self.assertFalse(any(f[1] == "R2" for f in findings))

    def test_r3_external_individuals_makes_no_layer3(self):
        rows = [entry(affects_people="external_individuals", decision_role="makes")]
        findings = self.findings_for(rows)
        self.assertTrue(any(f[1] == "R3" for f in findings))

    def test_r4_no_business_owner(self):
        rows = [entry(business_owner="")]
        findings = self.findings_for(rows)
        self.assertTrue(any(f[1] == "R4" and f[0] == "error" for f in findings))

    def test_r5_stale_review(self):
        rows = [entry(lifecycle_status="in_use", next_review_due="2020-01-01")]
        findings = self.findings_for(rows)
        self.assertTrue(any(f[1] == "R5" for f in findings))

    def test_r5_does_not_fire_for_future_date(self):
        rows = [entry(lifecycle_status="in_use", next_review_due="2099-01-01")]
        findings = self.findings_for(rows)
        self.assertFalse(any(f[1] == "R5" for f in findings))

    def test_r6_high_autonomy_no_oversight_affects_people(self):
        rows = [entry(autonomy_level="5", human_oversight_model="none", affects_people="external_individuals")]
        findings = self.findings_for(rows)
        self.assertTrue(any(f[1] == "R6" and f[0] == "error" for f in findings))

    def test_r6_does_not_fire_when_affects_people_no(self):
        rows = [entry(autonomy_level="5", human_oversight_model="none", affects_people="no")]
        findings = self.findings_for(rows)
        self.assertFalse(any(f[1] == "R6" for f in findings))

    def test_r7_broken_dependency(self):
        rows = [entry(system_id="SYS-A", depends_on="SYS-GHOST")]
        findings = self.findings_for(rows)
        hits = [f for f in findings if f[1] == "R7"]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0][2], "SYS-A")

    def test_r7_does_not_fire_when_dependency_resolves(self):
        rows = [
            entry(system_id="SYS-A", depends_on="SYS-B"),
            entry(system_id="SYS-B"),
        ]
        findings = self.findings_for(rows)
        self.assertFalse(any(f[1] == "R7" for f in findings))

    def test_r8_embedded_feature_without_vendor(self):
        rows = [entry(provenance="embedded_feature", vendor="")]
        findings = self.findings_for(rows)
        self.assertTrue(any(f[1] == "R8" for f in findings))

    def test_r9_agentic_without_systems_integrated(self):
        rows = [entry(system_type="agent", systems_integrated="")]
        findings = self.findings_for(rows)
        self.assertTrue(any(f[1] == "R9" for f in findings))

    def test_r9_does_not_fire_for_non_agentic_type(self):
        rows = [entry(system_type="predictive_model", systems_integrated="")]
        findings = self.findings_for(rows)
        self.assertFalse(any(f[1] == "R9" for f in findings))

    def test_r10_in_trial_without_tier(self):
        rows = [entry(lifecycle_status="in_trial", risk_tier="")]
        findings = self.findings_for(rows)
        self.assertTrue(any(f[1] == "R10" for f in findings))


class TestHealthAndGraph(unittest.TestCase):
    def setUp(self):
        self.schema, self.taxonomies, self.rules = R.load_policy(SCHEMA_DIR)

    def test_orphan_rate_computation(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "register.csv"
            write_register(path, [entry(system_id="SYS-A"), entry(system_id="SYS-B", business_owner="")])
            entries = R.load_register(path, self.schema)
            orphans = sum(1 for e in entries if not R.is_field_present(e, "business_owner"))
            self.assertEqual(orphans, 1)
            self.assertEqual(R.pct(orphans, len(entries)), 50.0)

    def test_graph_cycle_detection(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "register.csv"
            write_register(path, [
                entry(system_id="SYS-A", depends_on="SYS-B"),
                entry(system_id="SYS-B", depends_on="SYS-A"),
            ])
            entries = R.load_register(path, self.schema)
            by_id = {e["system_id"]: e for e in entries}
            # replicate the cycle-detection logic path used in cmd_graph
            colour = {sid: 0 for sid in by_id}
            found_cycle = []

            def visit(sid, stack):
                colour[sid] = 1
                for dep in R.entry_list(by_id[sid], "depends_on"):
                    if dep not in by_id:
                        continue
                    if colour.get(dep) == 1:
                        found_cycle.append(stack + [sid, dep])
                    elif colour.get(dep) == 0:
                        visit(dep, stack + [sid])
                colour[sid] = 2

            for sid in by_id:
                if colour[sid] == 0:
                    visit(sid, [])
            self.assertTrue(len(found_cycle) >= 1)

    def test_shared_component_dependant_count(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "register.csv"
            write_register(path, [
                entry(system_id="SYS-SHARED"),
                entry(system_id="SYS-DEP-1", depends_on="SYS-SHARED"),
                entry(system_id="SYS-DEP-2", depends_on="SYS-SHARED"),
            ])
            entries = R.load_register(path, self.schema)
            dependants = {}
            for e in entries:
                for dep in R.entry_list(e, "depends_on"):
                    dependants.setdefault(dep, []).append(e["system_id"])
            self.assertEqual(len(dependants["SYS-SHARED"]), 2)


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.example_csv = Path(__file__).resolve().parent.parent / "examples" / "sample-register.csv"

    def test_sample_register_validates_with_exactly_three_expected_errors(self):
        schema, taxonomies, rules = R.load_policy(SCHEMA_DIR)
        entries = R.load_register(self.example_csv, schema)
        schema_errors = []
        for e in entries:
            schema_errors.extend(R.validate_entry_against_schema(e, schema))
        rules["_taxonomies"] = taxonomies
        rule_findings = R.run_validation_rules(entries, rules)
        rule_ids_that_errored = {f[1] for f in rule_findings if f[0] == "error"}
        self.assertEqual(rule_ids_that_errored, {"R1", "R4", "R7"})


if __name__ == "__main__":
    unittest.main()
