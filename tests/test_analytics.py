"""Synthetic data only: verify arithmetic, provenance, privacy, and portable execution."""

from datetime import date, timedelta
import hashlib
import io
import json
from pathlib import Path
import random
import statistics
import subprocess
import sys
import tempfile
import unittest
import zipfile

from scripts.records import Source, selected_sources
from scripts.analyze_weight_history import (KG_PER_LB, observations_from, conditions,
                                           analyze, regression)
from scripts.audit_week import audit
from scripts.import_research import preserve_source
from scripts.build_starter import ROOT, render_outputs


def table(headers, rows):
    return "| " + " | ".join(headers) + " |\n|" + "|".join("---" for _ in headers) + "|\n" + "\n".join(
        "| " + " | ".join(map(str, row)) + " |" for row in rows) + "\n"


def weights(values, unit="kg", conditions_values=None):
    rows = []
    for i, value in enumerate(values):
        context = conditions_values or ["waking", "nude", "pre-intake", "after urination", ""]
        rows.append([(date(2026, 1, 1)+timedelta(days=i)).isoformat(), value, unit] + context)
    return Source("synthetic.md", table(
        ["Date", "Weight", "Unit", "Time/context", "Clothing", "Intake", "Bathroom", "Notes"], rows))


WORK_HEADERS = ["Date", "ID", "Status", "Required", "Category", "Modality", "Active min", "Min low",
                "Min high", "Distance km", "Z1", "Z2", "Z3", "Z4", "Z5", "Unclassified min",
                "Race-specific min", "Elapsed min", "Evidence", "Assumptions", "Plan status", "Plan version"]


def work_row(day, identifier, status, required, category, minutes, evidence="reported"):
    return [day, identifier, status, required, category, "synthetic", minutes, "", "", "",
            "", "", "", "", "", "", "", "", evidence, "", "adopted", "synthetic-v1"]


class WeightTests(unittest.TestCase):
    def test_units_preserve_raw_values_and_produce_equivalent_models(self):
        kg = observations_from([weights([70, 70.1, 70.2])])
        lb = observations_from([weights([value/KG_PER_LB for value in (70, 70.1, 70.2)], "lb")])
        first, second = analyze(kg, draws=1000), analyze(lb, draws=1000)
        self.assertNotEqual(first["latest_measured"], second["latest_measured"])
        self.assertAlmostEqual(first["scale_only"]["current_level"]["median"],
                               second["scale_only"]["current_level"]["median"], places=8)
        imperial = analyze(kg, draws=1000, unit="lb")
        self.assertAlmostEqual(imperial["scale_only"]["weekly_change"]["median"]*KG_PER_LB,
                               first["scale_only"]["weekly_change"]["median"], places=8)

    def test_ambiguous_units_fail_instead_of_guessing(self):
        with self.assertRaisesRegex(ValueError, "Explicit lb or kg"):
            observations_from([weights([70, 71], "")])
        source = weights([70, 71])
        source = Source(source.name, source.text.replace("| 70 | kg", "| 70 lb | kg"))
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            observations_from([source])

    def test_exercise_load_table_is_not_a_bodyweight_table(self):
        source = Source("synthetic.md", "## Lifts\n" + table(["Date", "Weight", "Reps"],
                        [["2026-01-05", "80 kg", 5]]))
        self.assertEqual(observations_from([source]), [])

    def test_negation_and_fluid_units_are_not_misread(self):
        items = observations_from([weights([70, 70], conditions_values=["waking", "underwear only",
            "8 US fl oz water", "after urination", "not dehydrated"])])
        flags = conditions(items[0])
        self.assertFalse(flags["dehydration_reported"])
        self.assertAlmostEqual(flags["water_kg"], 8*.0295735295625)
        mass_ounces = observations_from([weights([70], conditions_values=["waking", "unknown", "8 oz water", "unknown", ""])])[0]
        self.assertIsNone(conditions(mass_ounces)["water_kg"])

    def test_reproducibility_and_prior_does_not_change_scale_only_result(self):
        items = observations_from([weights([70, 70.1, 70.2, 70.3])])
        result = analyze(items, draws=1000)
        self.assertEqual(result, analyze(items, draws=1000))
        informed = analyze(items, draws=1000, expected_change=-.2, expected_sd=.2,
                           prior_basis="Synthetic adopted expectation for testing")
        self.assertEqual(result["scale_only"], informed["scale_only"])
        self.assertIn("prior_informed", informed)
        with self.assertRaisesRegex(ValueError, "Both expected"):
            analyze(items, draws=1000, expected_change=-.2)
        with self.assertRaisesRegex(ValueError, "explicit prior basis"):
            analyze(items, draws=1000, expected_change=-.2, expected_sd=.2)

    def test_regression_recovers_synthetic_slope_and_aggregates_dates(self):
        daily = {date(2026, 1, 1)+timedelta(days=i): [70+.1*i] for i in range(10)}
        duplicate = {day: values*20 for day, values in daily.items()}
        rng_a, rng_b = random.Random(9), random.Random(9)
        first = [regression(daily, rng_a, .01)[1] for _ in range(2000)]
        second = [regression(duplicate, rng_b, .01)[1] for _ in range(2000)]
        self.assertEqual(first, second)
        self.assertAlmostEqual(statistics.mean(first), .7, delta=.01)

    def test_sparse_data_invalid_settings_and_interval_order(self):
        with self.assertRaisesRegex(ValueError, "two distinct"):
            analyze(observations_from([weights([70])]), draws=1000)
        items = observations_from([weights([70, 70.1])])
        for settings in ({"day_sd_kg": float("nan")}, {"draws": 0}, {"unit": "stone"}):
            with self.assertRaises(ValueError):
                analyze(items, **settings)
        result = analyze(items, draws=1000)
        summary = result["scale_only"]["current_level"]
        self.assertLessEqual(summary["interval_95"][0], summary["interval_90"][0])
        self.assertLessEqual(summary["interval_90"][0], summary["interval_68"][0])
        self.assertLessEqual(summary["interval_68"][0], summary["median"])
        self.assertGreaterEqual(summary["interval_95"][1], summary["interval_90"][1])


class AuditTests(unittest.TestCase):
    def test_russian_notebook_remains_readable_by_shared_analysis_tools(self):
        notebook = render_outputs()["starter/ru/MY-TRAINER.md"].decode("utf-8")
        blank = Source("synthetic-russian.md", notebook)
        self.assertEqual(observations_from([blank]), [])
        blank_audit = audit([blank], date(2026, 1, 5), date(2026, 1, 7))
        self.assertEqual(blank_audit["completed_workload"]["segments"], 0)
        # Insert synthetic rows into the actual translated template tables.
        for section, row in (
            ("Workload segments", work_row("2026-01-05", "ru-test", "completed", "yes", "conditioning", 20)),
            ("Nutrition days", ["2026-01-05", "complete", 2000, 100, 250, 67, "unknown", "unknown", "синтетический пример"]),
            ("Bodyweight", ["2026-01-05", 70.5, "kg", "unknown", "unknown", "unknown", "unknown", "тестовая запись"]),
        ):
            start = notebook.index("### " + section)
            separator = notebook.index("\n|---", start)
            insert_at = notebook.index("\n", separator + 1)
            notebook = notebook[:insert_at] + "\n| " + " | ".join(map(str, row)) + " |" + notebook[insert_at:]
        source = Source("synthetic-russian.md", notebook)
        result = audit([source], date(2026, 1, 5), date(2026, 1, 7))
        self.assertEqual(result["completed_workload"]["active_minutes"]["known_total"], 20)
        self.assertEqual(observations_from([source])[0].kg, 70.5)
        self.assertEqual(observations_from([source])[0].notes, "тестовая запись")

    def test_draft_and_unversioned_plans_never_enter_projections(self):
        draft = work_row("2026-01-08", "draft", "planned", "yes", "conditioning", 30, "projected")
        draft[-2] = "draft"
        no_version = work_row("2026-01-08", "unversioned", "planned", "yes", "conditioning", 30, "projected")
        no_version[-1] = "unknown"
        result = audit([Source("synthetic.md", table(WORK_HEADERS, [draft, no_version]))],
                       date(2026, 1, 5), date(2026, 1, 7))
        self.assertEqual(len(result["unresolved_segments"]), 2)
        self.assertEqual(result["remaining_required"]["segments"], 0)

    def test_actuals_projections_optional_and_unknown_are_separate(self):
        rows = [work_row("2026-01-05", "a", "completed", "yes", "conditioning", 30),
                work_row("2026-01-06", "b", "partial", "yes", "strength", 10),
                work_row("2026-01-08", "c", "planned", "yes", "conditioning", 20, "projected"),
                work_row("2026-01-08", "d", "planned", "conditional", "conditioning", 15, "projected"),
                work_row("2026-01-06", "e", "planned", "yes", "conditioning", 40, "projected"),
                work_row("2026-01-06", "f", "completed", "yes", "conditioning", "unknown")]
        rows[0][11] = 10  # Z2; remaining known minutes must remain unclassified.
        result = audit([Source("synthetic.md", table(WORK_HEADERS, rows))], date(2026, 1, 5), date(2026, 1, 7))
        self.assertEqual(result["completed_workload"]["active_minutes"],
                         {"known_total": 40, "covered_segments": 2, "total_segments": 3})
        self.assertEqual(result["projected_required_baseline"]["active_minutes"]["known_total"], 60)
        self.assertEqual(len(result["optional_or_conditional_segments"]), 1)
        self.assertEqual(len(result["unresolved_segments"]), 1)
        self.assertEqual(result["completed_workload"]["conditioning_zones"]["z2"], 10)
        self.assertEqual(result["completed_workload"]["conditioning_unclassified_min"], 20)
        self.assertEqual(result["completed_workload"]["conditioning_segments_missing_active_time"], 1)

    def test_duplicate_ids_zone_overflow_and_future_actuals_fail(self):
        row = work_row("2026-01-05", "a", "completed", "yes", "conditioning", 30)
        for rows in ([row, row], [row[:10]+[40]+row[11:]],
                     [work_row("2026-01-10", "a", "completed", "yes", "conditioning", 30)]):
            with self.assertRaises(ValueError):
                audit([Source("synthetic.md", table(WORK_HEADERS, rows))], date(2026, 1, 5), date(2026, 1, 7))

    def test_complete_nutrition_denominators_and_per_day_weight_averages(self):
        nutrition = table(["Date", "Status", "Calories", "Protein g", "Carbohydrate g", "Fat g", "Target calories", "Target version", "Basis"],
            [["2026-01-05", "complete", 2000, "unknown", 200, 70, 2100, "v1", "reported"],
             ["2026-01-06", "partial", 800, 40, 80, 20, 2100, "v1", "estimated"],
             ["2026-01-07", "complete", 2200, 100, 250, 80, 2200, "v2", "reported"]])
        result = audit([Source("synthetic.md", nutrition)], date(2026, 1, 5), date(2026, 1, 7))
        averages = result["nutrition"]["averages_complete_days_only"]
        self.assertEqual(averages["calories"], {"mean": 2100, "days": 2})
        self.assertEqual(averages["protein_g"], {"mean": 100, "days": 1})
        with self.assertRaisesRegex(ValueError, "Multiple nutrition"):
            audit([Source("one.md", nutrition), Source("two.md", nutrition)], date(2026, 1, 5), date(2026, 1, 7))
        first = weights([70, 71]).text
        doubled = first + "\n" + weights([72]).text
        result = audit([Source("synthetic.md", doubled)], date(2026, 1, 1), date(2026, 1, 7))
        self.assertEqual(result["comparable_weights"]["days"], 2)
        self.assertEqual(result["comparable_weights"]["mean_kg"], 71)

    def test_empty_or_narrative_records_do_not_create_zero_work(self):
        result = audit([Source("logs/workouts/2026-01-05.md", "I exercised; duration not reported.",
                               date(2026, 1, 5), "workouts")], date(2026, 1, 5), date(2026, 1, 11))
        self.assertIsNone(result["completed_workload"]["active_minutes"]["known_total"])
        self.assertEqual(result["coverage"][0]["domains"], ["workouts"])
        self.assertTrue(result["open_items"])
        self.assertEqual(result["nutrition"]["averages_complete_days_only"]["calories"]["days"], 0)


class PortableToolsTests(unittest.TestCase):
    def test_extracted_tools_run_without_checkout_and_do_not_mutate_input(self):
        outputs = render_outputs()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with zipfile.ZipFile(io.BytesIO(outputs["starter/trainer-tools.zip"])) as archive:
                archive.extractall(root)
            notebook = root / "private-notebook.md"
            notebook.write_text(weights([70, 70.1, 70.2]).text, encoding="utf-8")
            original = notebook.read_bytes()
            commands = [
                ["scripts/analyze_weight_history.py", "--notebook", str(notebook), "--draws", "1000", "--format", "json"],
                ["scripts/audit_week.py", "--notebook", str(notebook), "--week-start", "2026-01-01", "--as-of", "2026-01-07", "--format", "json"],
            ]
            for command in commands:
                result = subprocess.run([sys.executable]+command, cwd=root, capture_output=True, text=True, check=True)
                self.assertIsInstance(json.loads(result.stdout), dict)
            self.assertEqual(notebook.read_bytes(), original)
            self.assertFalse((root / "personal").exists())

    def test_research_import_preserves_source_bytes_and_adopts_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "private/logs").mkdir(parents=True)
            source = root / "source.txt"
            payload = b"Synthetic research claim\r\nNot verified.\r\n"
            source.write_bytes(payload)
            result = preserve_source(root / "private", source, "synthetic-topic", date(2026, 1, 1),
                                     "Synthetic claim", "ai-synthesis")
            self.assertEqual((root / "private" / result["source"]).read_bytes(), payload)
            self.assertEqual(result["sha256"], hashlib.sha256(payload).hexdigest())
            note = (root / "private" / result["note"]).read_text(encoding="utf-8")
            self.assertIn("unverified import", note)
            self.assertIn("research only", note)
            self.assertEqual(list((root / "private/logs").iterdir()), [])
            self.assertEqual(source.read_bytes(), payload)
            with self.assertRaisesRegex(ValueError, "already exists"):
                preserve_source(root / "private", source, "synthetic-topic", date(2026, 1, 1),
                                "Synthetic claim", "ai-synthesis")
            with self.assertRaises(ValueError):
                preserve_source(root / "private", source, "../escape", date(2026, 1, 1),
                                "Synthetic claim", "ai-synthesis")
            with self.assertRaisesRegex(ValueError, "private workspace"):
                preserve_source(ROOT / "templates/workspace", source, "synthetic-topic", date(2026, 1, 1),
                                "Synthetic claim", "ai-synthesis")

    def test_explicit_input_required(self):
        with self.assertRaises(ValueError):
            selected_sources()


if __name__ == "__main__":
    unittest.main()
