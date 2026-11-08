from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from collect_model0_cif import collect_model0_cifs  # noqa: E402
from make_boltz_yaml import set_template_cif  # noqa: E402


class ScriptSafetyTests(unittest.TestCase):
    def test_cif_collector_refuses_to_overwrite_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outputs = root / "outputs"
            source = outputs / "sampleA" / "seed_0" / "sampleA_model_0.cif"
            source.parent.mkdir(parents=True)
            source.write_text("new structure", encoding="utf-8")
            destination = root / "collected"
            destination.mkdir()
            existing = destination / "sampleA_model_0.cif"
            existing.write_text("keep original", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                collect_model0_cifs(outputs, destination)
            self.assertEqual(existing.read_text(encoding="utf-8"), "keep original")
            self.assertFalse((destination / "manifest.tsv").exists())

    def test_cif_collector_writes_portable_relative_source_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outputs = root / "outputs"
            source = outputs / "sampleA" / "seed_0" / "sampleA_model_0.cif"
            source.parent.mkdir(parents=True)
            source.write_text("structure", encoding="utf-8")
            destination = root / "collected"

            self.assertEqual(collect_model0_cifs(outputs, destination), 1)
            manifest = (destination / "manifest.tsv").read_text(encoding="utf-8")
            self.assertIn("sampleA/seed_0/sampleA_model_0.cif", manifest)
            self.assertNotIn(str(root), manifest)

    def test_cif_collector_rejects_a_destination_inside_source_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outputs = Path(tmp) / "outputs"
            outputs.mkdir()
            with self.assertRaisesRegex(ValueError, "outside the source output tree"):
                collect_model0_cifs(outputs, outputs / "collected")

    def test_template_cif_windows_path_is_not_interpreted_as_regex_escape(self) -> None:
        template = "templates:\n  - cif: old.cif\n    chain_id: A\n"
        updated = set_template_cif(template, r"C:\models\template.cif")
        self.assertIn(r'cif: "C:\\models\\template.cif"', updated)


if __name__ == "__main__":
    unittest.main()
