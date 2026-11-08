#!/usr/bin/env python3
"""Create the standardized computational candidate manifest and run metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata as package_metadata
from pathlib import Path

import pandas as pd

from peptide_to_smiles import peptide_to_smiles
from reverse_sequences import reverse_d_sequence
from screen_candidates import P4_SCORE_REQUIRED_COLUMNS, PRED_COLS, PROB_COLS, compute_scores


MODEL_VERSION = (
    "BoltzGen/BoltzIF 0.2.0; Boltz-2 2.2.1 "
    "(production environment recovered 2026-08-15)"
)
TARGET_SEQUENCE = "HSSNNFGAILSSTNVGSNTY"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def package_version(name: str) -> str:
    try:
        return package_metadata.version(name)
    except package_metadata.PackageNotFoundError:
        return "not-installed"


def git_revision(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "unavailable"


def require_unique(table: pd.DataFrame, column: str, label: str) -> None:
    if table[column].isna().any() or not table[column].is_unique:
        raise ValueError(f"{label} must contain non-null, unique {column} values")


def build_results(scores_path: Path, final_path: Path, structures_dir: Path) -> pd.DataFrame:
    raw = pd.read_csv(scores_path)
    scored = compute_scores(raw)
    final = pd.read_csv(final_path).sort_values("final_rank")
    require_unique(final, "d_peptide_sequence", "Final manifest")
    require_unique(scored, "d_sequence", "Scored design pool")

    selected = final.merge(
        scored,
        left_on="d_peptide_sequence",
        right_on="d_sequence",
        how="left",
        validate="one_to_one",
        suffixes=("_final", "_score"),
    )
    if selected["overall_score"].isna().any():
        missing = selected.loc[selected["overall_score"].isna(), "d_peptide_sequence"].tolist()
        raise ValueError(f"Final candidates missing from scored pool: {missing}")

    if not selected["d_peptide_sequence"].eq(selected["d_sequence"]).all():
        raise ValueError("Final D-sequences differ from the scored candidate sequences")
    if not selected["l_sequence_final"].str.upper().eq(selected["l_sequence_score"]).all():
        raise ValueError("Final L-sequences differ from the scored candidate sequences")
    expected_reverse = selected["l_sequence_final"].map(reverse_d_sequence)
    if not selected["d_peptide_sequence"].eq(expected_reverse).all():
        raise ValueError("Final D-sequences are not the reverse of their L-design sequences")
    expected_smiles = selected["d_peptide_sequence"].map(peptide_to_smiles)
    if not selected["smiles"].eq(expected_smiles).all():
        raise ValueError("Final stereochemical SMILES do not match the D-sequences")

    missing_structures = [
        name for name in selected["structure_file"] if not (structures_dir / name).is_file()
    ]
    if missing_structures:
        raise FileNotFoundError(f"Missing final structure files: {missing_structures[:3]}")

    for name in selected["structure_file"]:
        text = (structures_dir / name).read_text(encoding="utf-8")
        if "A 1 'Model subunit A'" not in text or "X 2 'Model subunit X'" not in text:
            raise ValueError(f"Unexpected chain convention in {name}")
        atom_elements = {
            line.split()[2]
            for line in text.splitlines()
            if line.startswith(("ATOM ", "HETATM ")) and len(line.split()) > 2
        }
        if "H" in atom_elements:
            raise ValueError(f"Expected heavy-atom-only deposited model, found hydrogen in {name}")

    result = pd.DataFrame({
        "candidate_id": selected["final_rank"].map(lambda value: f"HIAPP-DP-{int(value):03d}"),
        "final_rank": selected["final_rank"].astype(int),
        "selection_name": selected["name_final"],
        "priority_tier": selected["priority"],
        "candidate_type": "linear reverse-D peptide",
        "d_peptide_sequence": selected["d_peptide_sequence"],
        "l_design_sequence": selected["l_sequence_final"],
        "smiles": selected["smiles"],
        "target": "human islet amyloid polypeptide (hIAPP)",
        "target_sequence": TARGET_SEQUENCE,
        "target_template": "PDB 9ULZ, chain D residues 19-37",
        "intended_binding_region": "hIAPP residues 21-37",
        "structure_file": selected["structure_file"].map(
            lambda name: f"targets/hiapp/results/final_candidates/structures/{name}"
        ),
        "structure_format": "mmCIF",
        "coordinate_unit": "angstrom",
        "target_chain_id": "A",
        "ligand_chain_id": "X",
        "protonation_status": "not assigned",
        "hydrogen_representation": "heavy atoms only; no explicit hydrogens",
        "ptm": selected["ptm"],
        "iptm": selected["iptm"],
        "min_ptm_iptm": selected["structure_bottleneck"],
        "confidence_score": selected["confidence_score"],
        "complex_iplddt": selected["complex_iplddt"],
        "complex_ipde": selected["complex_ipde"],
        "affinity_pred_value_head_0": selected["affinity_pred_value"],
        "affinity_pred_value_head_1": selected["affinity_pred_value1"],
        "affinity_pred_value_head_2": selected["affinity_pred_value2"],
        "affinity_probability_head_0": selected["affinity_probability_binary"],
        "affinity_probability_head_1": selected["affinity_probability_binary1"],
        "affinity_probability_head_2": selected["affinity_probability_binary2"],
        "affinity_consensus_relative": selected["affinity_consensus"],
        "structure_quality_relative": selected["structure_quality"],
        "developability_relative": selected["developability_score"],
        "overall_priority_score": selected["overall_score"],
        "solubility_tendency_0_100": selected["solubility_tendency_score_0_100"],
        "aggregation_risk_0_100": selected["aggregation_risk_score_0_100"],
        "sequence_stability_0_100": selected["sequence_stability_score_0_100"],
        "peptide_drug_likeness_0_100": selected["peptide_drug_likeness_score_0_100"],
        "model_and_version": MODEL_VERSION,
        "experimental_status": "computational_shortlist_selected",
        "measured_activity": "not_included_in_computational_release",
        "remarks": (
            "Computational shortlist; relative model/heuristic scores are not measured affinity "
            "or aggregation inhibition."
        ),
    })
    numeric = result.select_dtypes(include="number").columns.difference(["final_rank"])
    result[numeric] = result[numeric].round(6)
    return result


def validate_screening(screening_dir: Path) -> None:
    expected = {
        "hard_gate_904.csv": 904,
        "p1_p2_p3_top32.csv": 32,
        "p4_top10.csv": 10,
    }
    for filename, rows in expected.items():
        path = screening_dir / filename
        if not path.is_file() or len(pd.read_csv(path)) != rows:
            raise ValueError(f"Screening artifact failed validation: {path} (expected {rows} rows)")
    hard = pd.read_csv(screening_dir / "hard_gate_904.csv")
    if not hard[PRED_COLS + PROB_COLS].notna().to_numpy().all():
        raise ValueError("Hard-gated candidates must have all six affinity-head values")
    main = pd.read_csv(screening_dir / "p1_p2_p3_top32.csv")
    if main["priority"].value_counts().to_dict() != {"P1": 12, "P2": 12, "P3": 8}:
        raise ValueError("P1/P2/P3 review pool must contain 12/12/8 candidates")
    p4 = pd.read_csv(screening_dir / "p4_top10.csv")
    if not p4[P4_SCORE_REQUIRED_COLUMNS].notna().to_numpy().all():
        raise ValueError("P4 candidates must have complete inputs for their ranking score")
    if main["d_sequence"].isin(p4["d_sequence"]).any():
        raise ValueError("P4 review pool must exclude all P1-P3 sequences")
    if main["d_sequence"].nunique() + p4["d_sequence"].nunique() != 42:
        raise ValueError("The P1-P3 and P4 review pools must contain 42 distinct sequences")


def validate_final_review(final_path: Path, screening_dir: Path) -> None:
    """Verify the historical human choices against the recomputed tier pools."""
    final = pd.read_csv(final_path).sort_values("final_rank")
    if final["final_rank"].tolist() != list(range(1, 13)):
        raise ValueError("Final ranks must be the consecutive integers 1 through 12")
    if final["priority"].value_counts().to_dict() != {"P1": 8, "P2": 1, "P3": 1, "P4": 2}:
        raise ValueError("Historical final tier composition must be P1/P2/P3/P4 = 8/1/1/2")
    main_review = pd.read_csv(screening_dir / "p1_p2_p3_top32.csv")
    p4_review = pd.read_csv(screening_dir / "p4_top10.csv")
    pools = {tier: set(main_review.loc[main_review["priority"] == tier, "d_sequence"])
             for tier in ("P1", "P2", "P3")}
    pools["P4"] = set(p4_review["d_sequence"])
    for row in final.itertuples():
        if row.d_peptide_sequence not in pools[row.priority]:
            raise ValueError(f"Candidate is outside its review tier: {row.d_peptide_sequence}")
        if row.d_peptide_sequence != row.l_sequence[::-1].lower():
            raise ValueError(f"Reverse-D sequence mismatch: {row.d_peptide_sequence}")


def validate_manifest_integrity(results: pd.DataFrame) -> None:
    """Check stable candidate identifiers, sequence encodings and release fields."""
    expected_ids = [f"HIAPP-DP-{rank:03d}" for rank in results["final_rank"]]
    if results["candidate_id"].tolist() != expected_ids:
        raise ValueError("Candidate identifiers must match final-rank order")
    if results["selection_name"].isna().any() or not results["selection_name"].is_unique:
        raise ValueError("Historical selection names must be non-null and unique")
    for row in results.itertuples(index=False):
        if row.d_peptide_sequence != reverse_d_sequence(row.l_design_sequence):
            raise ValueError(f"Sequence crosswalk mismatch for {row.candidate_id}")
        if row.smiles != peptide_to_smiles(row.d_peptide_sequence):
            raise ValueError(f"SMILES crosswalk mismatch for {row.candidate_id}")
    if not results["measured_activity"].eq("not_included_in_computational_release").all():
        raise ValueError("Wet-lab measurements must not be represented in this release")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--structures", type=Path, required=True)
    parser.add_argument("--screening-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()

    validate_screening(args.screening_dir)
    validate_final_review(args.final, args.screening_dir)
    results = build_results(args.scores, args.final, args.structures)
    if len(results) != 12 or not results["candidate_id"].is_unique:
        raise ValueError("Standardized output must contain exactly 12 unique candidates")
    validate_manifest_integrity(results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(args.output, index=False, encoding="utf-8")

    root = Path(__file__).resolve().parents[1]
    run_metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "entry_point": "bash targets/hiapp/run.sh",
        "repository_commit": git_revision(root),
        "target_case": "hIAPP",
        "model_and_version": MODEL_VERSION,
        "production_model_version_caveat": (
            "BoltzGen 0.2.0 is confirmed by the historical inverse-folding log. "
            "Boltz 2.2.1 is the still-installed environment recovered on 2026-08-15; "
            "historical prediction logs did not print its version. Checkpoint SHA256 values "
            "and remaining evidence are recorded in targets/hiapp/docs/MODEL_CARD.md."
        ),
        "inputs": {
            str(args.scores): sha256(args.scores),
            str(args.final): sha256(args.final),
        },
        "runtime": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "pandas": package_version("pandas"),
            "numpy": package_version("numpy"),
        },
        "randomness": (
            "No random operation is used by this CPU reproduction entry point. Neural generation "
            "and prediction are separate stochastic GPU stages documented in the full notebook."
        ),
        "code_sha256": {
            str(path.relative_to(root)): sha256(path)
            for path in [root / "targets/hiapp/run.sh", root / "scripts/screen_candidates.py",
                         root / "scripts/generate_submission_results.py"]
        },
        "structure_sha256": {
            name: sha256(args.structures / name)
            for name in pd.read_csv(args.final)["structure_file"]
        },
        "screening_sha256": {
            path.name: sha256(path) for path in sorted(args.screening_dir.glob("*.csv"))
        },
        "output_rows": len(results),
        "output_sha256": sha256(args.output),
    }
    args.metadata.write_text(json.dumps(run_metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(results)} candidates to {args.output}")


if __name__ == "__main__":
    main()
