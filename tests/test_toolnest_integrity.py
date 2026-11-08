"""Check optional archives without weakening validation of the source corpus."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


SOURCE = Path(__file__).resolve().parents[1] / "datasets/part4-dataset"
sys.path.insert(0, str(SOURCE / "scripts"))
try:
    from dataset_integrity import content_hash, file_hash

    spec = importlib.util.spec_from_file_location("toolnest_validator", SOURCE / "scripts/validate_dataset.py")
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
finally:
    sys.path.pop(0)


def manifest(root):
    return {"hash_format": "sha256-text-lf-v1",
            "files": {p.relative_to(root).as_posix(): file_hash(p)
                      for p in root.rglob("*") if p.is_file()}}


class ToolNestIntegrityTests(unittest.TestCase):
    def test_text_newlines_are_portable_but_content_changes_fail(self):
        self.assertEqual(content_hash(b"first\r\nsecond\r\n", ".md"),
                         content_hash(b"first\nsecond\n", ".md"))
        self.assertNotEqual(content_hash(b"first\r\n", ".zip"), content_hash(b"first\n", ".zip"))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "source.md"
            path.write_bytes(b"original\n")
            expected = manifest(root)
            path.write_bytes(b"original\r\n")
            validator.validate_packaging(root, expected)
            path.write_bytes(b"changed\n")
            with self.assertRaisesRegex(ValueError, "Integrity hash mismatch"):
                validator.validate_packaging(root, expected)

    def test_missing_required_file_is_not_treated_as_optional(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            expected = {"hash_format": "sha256-text-lf-v1", "files": {"corpus/documents.jsonl": "missing"}}
            with self.assertRaisesRegex(ValueError, "inventory differs"):
                validator.validate_packaging(root, expected)

    def test_stale_archive_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "docs").mkdir()
            (root / "docs/example.md").write_bytes(b"current\n")
            with ZipFile(root / "toolnest-docs.zip", "w") as archive:
                archive.writestr("docs/example.md", b"stale\n")
            with self.assertRaisesRegex(ValueError, "Stale archive entry"):
                validator.validate_packaging(root, manifest(root))

    def test_builder_and_validator_with_and_without_archives(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for folder in ("scripts", "source"):
                shutil.copytree(SOURCE / folder, root / folder, ignore=shutil.ignore_patterns("__pycache__"))
            def run(name):
                result = subprocess.run([sys.executable, str(root / "scripts" / name)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return json.loads(result.stdout)
            run("build_dataset.py")
            self.assertEqual(run("validate_dataset.py")["optional_archives_absent"], [])
            # Remove only the two generated convenience files inside this temporary fixture.
            for name in ("toolnest-docs.zip", "toolnest-tickets.zip"):
                (root / name).unlink()
            result = run("validate_dataset.py")
            self.assertEqual(result["result"], "PASS")
            self.assertEqual(len(result["optional_archives_absent"]), 2)


if __name__ == "__main__":
    unittest.main()
