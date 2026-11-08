#!/usr/bin/env python3
"""Compare the deposited hIAPP CPU reproduction with committed release outputs.

The historical filename and results/submission path remain for compatibility.
Run after run.sh. Paths may be absolute or relative to the current directory.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from generate_submission_results import sha256, validate_final_review, validate_manifest_integrity, validate_screening
from screen_candidates import compute_scores, select


def validate(output_dir: Path, root: Path) -> None:
    generated = pd.read_csv(output_dir / "results.csv")
    committed = pd.read_csv(root / "targets/hiapp/results/submission/results.csv")
    validate_manifest_integrity(generated)
    # Preserve row/column ordering and compare numerical values to CSV precision.
    pd.testing.assert_frame_equal(generated, committed, check_dtype=False,
                                  rtol=0, atol=1e-6)
    validate_screening(output_dir / "screening")
    validate_final_review(root / "targets/hiapp/results/final_candidates/final_12.csv",
                          output_dir / "screening")
    for name in ("hard_gate_904.csv", "p1_p2_p3_top32.csv", "p4_top10.csv"):
        pd.testing.assert_frame_equal(
            pd.read_csv(output_dir / "screening" / name),
            pd.read_csv(root / "targets/hiapp/results/screening" / name),
            check_dtype=False, rtol=0, atol=1e-10,
        )
    metadata = json.loads((output_dir / "run_metadata.json").read_text())
    if metadata["output_rows"] != 12 or metadata["output_sha256"] != sha256(output_dir / "results.csv"):
        raise ValueError("Output metadata mismatch")
    # Input hashes must match this deposited campaign, not merely files named by the run.
    expected_inputs = {
        sha256(root / "targets/hiapp/data/scored/merged_all_2_scored.csv"),
        sha256(root / "targets/hiapp/results/final_candidates/final_12.csv"),
    }
    if set(metadata["inputs"].values()) != expected_inputs:
        raise ValueError("Run inputs differ from the deposited campaign")
    raw_scores = pd.read_csv(root / "targets/hiapp/data/scored/merged_all_2_scored.csv")
    scored = compute_scores(raw_scores)
    hard_gate, main_review, p4_eligible = select(scored)
    if (len(scored), len(hard_gate), len(main_review), len(p4_eligible)) != (9806, 904, 32, 30):
        raise ValueError("Recomputed hIAPP counts differ from 9806 analysis, 904 hard gate, 32 P1-P3 and 30 P4")
    if main_review["d_sequence"].nunique() + pd.read_csv(
            output_dir / "screening/p4_top10.csv")["d_sequence"].nunique() != 42:
        raise ValueError("The P1-P3 and P4 review pools must contain 42 distinct sequences")
    structures = {Path(name).name: sha256(root / name) for name in generated["structure_file"]}
    if metadata["structure_sha256"] != structures:
        raise ValueError("Structure hashes differ from the current deposited structures")
    code = {name: sha256(root / name) for name in (
        "targets/hiapp/run.sh", "scripts/screen_candidates.py", "scripts/generate_submission_results.py")}
    if metadata["code_sha256"] != code:
        raise ValueError("Generation code has changed since the recorded run")
    screening = {p.name: sha256(p) for p in sorted((output_dir / "screening").glob("*.csv"))}
    if metadata["screening_sha256"] != screening:
        raise ValueError("Screening hashes differ from the recorded run")
    print("PASS: 9,806 analyzed; 904 hard gate; 42 review candidates; 12 final; sequence/SMILES crosswalk; structures; hashes")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("targets/hiapp/results/submission"))
    args = parser.parse_args()
    validate(args.output_dir, Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    main()
