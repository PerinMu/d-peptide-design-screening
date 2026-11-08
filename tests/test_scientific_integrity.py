from __future__ import annotations

import sys
import unittest
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_submission_results import validate_manifest_integrity  # noqa: E402
from peptide_to_smiles import peptide_to_smiles  # noqa: E402
from reverse_sequences import reverse_d_sequence  # noqa: E402
from screen_candidates import (  # noqa: E402
    P4_SCORE_REQUIRED_COLUMNS,
    compute_scores,
    p4_eligibility_mask,
    select,
)


def invert_smiles_chirality(smiles: str) -> str:
    return smiles.replace("@@", "TEMP").replace("@", "@@").replace("TEMP", "@")


class SequenceEncodingTests(unittest.TestCase):
    def test_reverse_d_sequence_normalizes_and_reverses(self) -> None:
        self.assertEqual(reverse_d_sequence(" A C\nD "), "dca")

    def test_reverse_d_sequence_rejects_noncanonical_symbols(self) -> None:
        with self.assertRaisesRegex(ValueError, "Noncanonical"):
            reverse_d_sequence("ACX")
        with self.assertRaisesRegex(ValueError, "Empty"):
            reverse_d_sequence("  \n")

    def test_ile_and_thr_encode_both_alpha_and_beta_stereocentres(self) -> None:
        # The L forms match the stereochemistry in PubChem's amino-acid records;
        # the lower-case D forms invert every defined centre.
        expected_l = {
            "I": "N[C@@H]([C@@H](C)CC)C(=O)O",
            "T": "N[C@@H]([C@H](O)C)C(=O)O",
        }
        for l_residue, d_residue in (("I", "i"), ("T", "t")):
            with self.subTest(residue=l_residue):
                l_smiles = peptide_to_smiles(l_residue)
                d_smiles = peptide_to_smiles(d_residue)
                self.assertEqual(l_smiles, expected_l[l_residue])
                self.assertEqual(d_smiles, invert_smiles_chirality(l_smiles))
                self.assertEqual(len(re.findall(r"\[C(?:@|@@)H\]", l_smiles)), 2)

    def test_glycine_remains_achiral(self) -> None:
        self.assertEqual(peptide_to_smiles("G"), "NCC(=O)O")
        self.assertEqual(peptide_to_smiles("g"), "NCC(=O)O")


class P4CompletenessTests(unittest.TestCase):
    def test_missing_affinity_or_score_input_fails_p4_gate(self) -> None:
        row = {column: 1.0 for column in P4_SCORE_REQUIRED_COLUMNS}
        row.update({
            "length_aa": 11,
            "structure_bottleneck": 0.80,
            "solubility_tendency_score_0_100": 55.0,
            "aggregation_risk_score_0_100": 20.0,
        })
        complete = pd.DataFrame([row])
        self.assertTrue(bool(p4_eligibility_mask(complete).iloc[0]))

        for missing_column in ("affinity_pred_value1", "confidence_score",
                               "sequence_liability_count"):
            with self.subTest(column=missing_column):
                incomplete = complete.copy()
                incomplete.loc[0, missing_column] = float("nan")
                self.assertFalse(bool(p4_eligibility_mask(incomplete).iloc[0]))


class DepositedDataIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = pd.read_csv(ROOT / "targets/hiapp/data/scored/merged_all_2_scored.csv")
        cls.scored = compute_scores(cls.raw)

    def test_historical_screening_counts_are_reproducible(self) -> None:
        hard_gate, top32, p4 = select(self.scored)
        self.assertEqual(len(self.scored), 9806)
        self.assertEqual(len(hard_gate), 904)
        self.assertEqual(top32["priority"].value_counts().to_dict(),
                         {"P1": 12, "P2": 12, "P3": 8})
        self.assertEqual(len(p4), 30)
        self.assertTrue(p4[P4_SCORE_REQUIRED_COLUMNS].notna().to_numpy().all())
        self.assertFalse(top32["d_sequence"].isin(p4["d_sequence"]).any())
        self.assertEqual(top32["d_sequence"].nunique() + p4.head(10)["d_sequence"].nunique(), 42)

    def test_final_manifest_sequences_smiles_and_scores_match_source(self) -> None:
        manifest = pd.read_csv(ROOT / "targets/hiapp/results/submission/results.csv")
        validate_manifest_integrity(manifest)
        final = pd.read_csv(ROOT / "targets/hiapp/results/final_candidates/final_12.csv")
        by_sequence = self.scored.set_index("d_sequence")
        self.assertEqual(len(manifest), 12)
        self.assertEqual(manifest["candidate_id"].tolist(),
                         [f"HIAPP-DP-{rank:03d}" for rank in range(1, 13)])
        self.assertEqual(final["priority"].value_counts().to_dict(),
                         {"P1": 8, "P2": 1, "P3": 1, "P4": 2})
        for row in manifest.itertuples(index=False):
            with self.subTest(candidate=row.candidate_id):
                history = final.loc[final["final_rank"].eq(row.final_rank)].iloc[0]
                source = by_sequence.loc[row.d_peptide_sequence]
                self.assertEqual(row.d_peptide_sequence, history["d_peptide_sequence"])
                self.assertEqual(row.l_design_sequence, history["l_sequence"])
                self.assertEqual(row.selection_name, history["name"])
                self.assertEqual(row.smiles, peptide_to_smiles(row.d_peptide_sequence))
                self.assertAlmostEqual(row.ptm, source["ptm"], places=6)
                self.assertAlmostEqual(row.iptm, source["iptm"], places=6)
                self.assertAlmostEqual(row.overall_priority_score, source["overall_score"], places=6)


if __name__ == "__main__":
    unittest.main()
