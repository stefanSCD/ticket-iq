"""Integration and boundary checks for the real dataset conversion."""

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.normalize_datasets import ROOT, Normalizer, category, normalized_ticket


class NormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = Normalizer(ROOT / "datasets").run()

    def test_counts_and_categories(self):
        self.assertEqual(len(self.data.documents), 590)
        self.assertEqual(len(self.data.tickets), 1100)
        self.assertEqual(len(self.data.history), 40)
        self.assertEqual(len(self.data.golden), 1100)
        self.assertEqual(sum(len(r["decisions"]) for r in self.data.golden), 900)
        self.assertEqual(Counter(r["category"] for r in self.data.golden), {
            "resolved_by_documentation": 330, "unresolved": 330,
            "partially_resolved": 220, "conflicting_documentation": 110,
            "already_clear": 110,
        })
        self.assertEqual(self.data.warnings, [])

    def test_inputs_contain_no_answer_fields_or_aliases(self):
        forbidden = {"summary", "labels", "jira_labels", "document_id", "source_id",
                     "category", "ground_truth_ticket_class", "class", "annotation_ids",
                     "expected_questions", "expected_behavior", "evidence", "registry_refs",
                     "relevant_pages", "difficulty_level", "split"}
        for row in self.data.tickets + self.data.history:
            self.assertFalse(forbidden & row.keys())
            self.assertIsInstance(row["label"], list)
        self.assertEqual(len({frozenset(r) for r in self.data.tickets + self.data.history}), 1)
        self.assertEqual(len({frozenset(r) for r in self.data.documents}), 1)
        self.assertEqual(len({frozenset(r) for r in self.data.golden}), 1)
        for doc in self.data.documents:
            self.assertNotIn("knowledge-registry", doc["source_path"])

    def test_combined_input_does_not_leak_new_golden_fields(self):
        row = {"ticket_id": "EX-1", "summary": "Example", "labels": ["feature"],
               "category": "unresolved", "future_answer_key": "secret", "evidence": "secret"}
        result = normalized_ticket(row, "test", "example", "source.jsonl")
        self.assertEqual(result["title"], "Example")
        self.assertEqual(result["label"], ["feature"])
        self.assertNotIn("secret", json.dumps(result))

    def test_existing_splits_and_unknown_values_are_preserved(self):
        self.assertEqual(Counter(r["split"] for r in self.data.golden), {
            "train": 400, "validation": 160, "test": 140, None: 400,
        })
        pcon = [r for r in self.data.golden if r["project_id"] == "pcon"]
        self.assertTrue(all(e["quote"] is None for r in pcon for e in r["evidence"]))
        self.assertTrue(any(r["evidence_summary"] for r in pcon))
        self.assertTrue(all(r["snapshot_at"] is None for r in self.data.tickets
                            if r["project_id"] == "teamflow"))
        self.assertEqual(len([d for d in self.data.documents if d["project_id"] == "teamflow"]), 100)

    def test_invalid_categories_and_cross_project_references_fail(self):
        with self.assertRaises(ValueError):
            category("new_unreviewed_category")
        broken = copy.deepcopy(self.data)
        record = next(r for r in broken.golden if r["project_id"] == "pcon")
        record["evidence"] = [{"doc_id": "TN-OV-01", "quote": None, "passage_id": None}]
        with self.assertRaisesRegex(ValueError, "cross-project"):
            broken.validate()

    def test_duplicate_tickets_fail(self):
        broken = copy.deepcopy(self.data)
        broken.tickets.append(broken.tickets[0])
        with self.assertRaisesRegex(ValueError, "Duplicate ID"):
            broken.validate()

    def test_reproducible_outputs_and_untouched_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            manifest = self.data.write(destination)
            before = {p.name: p.read_bytes() for p in destination.iterdir()}
            self.data.write(destination)
            self.assertEqual(before, {p.name: p.read_bytes() for p in destination.iterdir()})
            for name, expected in manifest["output_hashes"].items():
                self.assertEqual(hashlib.sha256(before[name]).hexdigest(), expected)
        for name, expected in self.data.inputs.items():
            self.assertEqual(hashlib.sha256((self.data.root / name).read_bytes()).hexdigest(), expected)
        with self.assertRaisesRegex(ValueError, "outside"):
            self.data.write(self.data.root / "part1-dataset")


if __name__ == "__main__":
    unittest.main()
