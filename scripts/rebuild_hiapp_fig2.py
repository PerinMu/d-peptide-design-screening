#!/usr/bin/env python3
"""Rebuild hIAPP Fig. 2b AUC data and Fig. 2c Prism tables from archived scores."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from screen_candidates import PRED_COLS, PROB_COLS, compute_scores

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "targets/hiapp"
DEFAULT_OUTPUT = TARGET / "results/figure2"
# Fixed before computing AUC. "increasing" is an orientation for descriptors
# without a general preference, with no implication of biological benefit.
METRICS = [
    ("confidence_score", "Confidence score", "higher"),
    ("ptm", "pTM", "higher"), ("iptm", "ipTM", "higher"),
    ("complex_plddt", "pLDDT", "higher"), ("complex_iplddt", "ipLDDT", "higher"),
    ("complex_pde", "PDE", "lower"), ("complex_ipde", "iPDE", "lower"),
    ("affinity_pred_value1", "Affinity pred value 1", "lower"),
    ("affinity_probability_binary1", "Affinity probability 1", "higher"),
    ("affinity_pred_value2", "Affinity pred value 2", "lower"),
    ("affinity_probability_binary2", "Affinity probability 2", "higher"),
    ("sequence_length_aa", "Sequence length", "increasing"),
    ("molecular_weight_da_est", "Molecular weight", "increasing"),
    ("net_charge_ph7_est", "Net charge at pH 7", "increasing"),
    ("absolute_charge_density", "Absolute charge density", "increasing"),
    ("isoelectric_point_est", "Isoelectric point", "increasing"),
    ("gravy_kd", "GRAVY hydropathy", "increasing"),
    ("polar_fraction", "Polar fraction", "increasing"),
    ("hydrophobic_fraction", "Hydrophobic fraction", "increasing"),
    ("aromatic_fraction", "Aromatic fraction", "increasing"),
    ("max_hydrophobic_run", "Max hydrophobic run", "increasing"),
    ("solubility_tendency_score_0_100", "Solubility tendency", "higher"),
    ("aggregation_risk_score_0_100", "Aggregation risk", "lower"),
    ("passive_permeability_tendency_0_100", "Passive permeability tendency", "higher"),
    ("sequence_liability_count", "Sequence liability count", "lower"),
    ("sequence_stability_score_0_100", "Sequence stability", "higher"),
    ("peptide_drug_likeness_score_0_100", "Drug likeness", "higher"),
    ("structure_bottleneck", "min(pTM, ipTM)", "higher"),
    ("affinity_consensus", "Affinity consensus", "higher"),
    ("structure_quality", "Structure quality", "higher"),
    ("developability_score", "Developability score", "higher"),
]
# Main-panel subset chosen by each metric's explicit role in the screen.
MAIN_PANEL = ["structure_bottleneck", "confidence_score", "complex_pde",
              "affinity_consensus", "solubility_tendency_score_0_100",
              "aggregation_risk_score_0_100", "sequence_liability_count",
              "sequence_stability_score_0_100", "peptide_drug_likeness_score_0_100"]
FIG2C = ["ptm", "iptm", "complex_pde", "complex_ipde", "gravy_kd",
         "solubility_tendency_score_0_100", "aggregation_risk_score_0_100",
         "peptide_drug_likeness_score_0_100"]
POS, ORIGINAL, REDESIGNED, ALL = ("Dataset positives", "Original designs",
                                  "Redesigned variants", "All designs")
CONTRASTS = [(POS, ORIGINAL), (POS, REDESIGNED), (ORIGINAL, REDESIGNED), (POS, ALL)]


def reference_crosswalk(table):
    literature = pd.read_csv(TARGET / "data/reference/hiapp_literature_peptides.csv",
                             usecols=["record_id", "reference_entry_id", "peptide_name", "activity_evidence_class"])
    inputs = pd.read_csv(TARGET / "data/designs/reference_inhibitors_smiles.csv",
                         usecols=["source", "seq_rev", "smiles"])
    inputs = inputs.loc[inputs["source"].eq("database"), ["seq_rev", "smiles"]]
    reference = table.loc[table["source"].eq("database")].copy()
    mapping = reference[["scored_csv_line", "seq_rev", "name", "smiles", "ptm", "confidence_json_path"]].merge(
        inputs.rename(columns={"smiles": "input_smiles"}), on="seq_rev", how="left", validate="one_to_one")
    mapping = mapping.merge(literature, left_on="seq_rev", right_on="reference_entry_id",
                            how="left", validate="one_to_one")
    mapping["input_smiles_match"] = mapping["smiles"].notna() & mapping["smiles"].eq(mapping["input_smiles"])
    mapping["exact_name_match"] = mapping["name"].eq(mapping["peptide_name"])
    mapping["has_boltz_ptm"] = mapping["ptm"].notna()
    mapping["prediction_id_match"] = (~mapping["has_boltz_ptm"] | mapping["confidence_json_path"].eq(
        "confidence_" + mapping["seq_rev"] + "_model_0.json"))
    matched = mapping["record_id"].notna() & mapping["input_smiles_match"] & mapping["prediction_id_match"]
    mapping["mapping_status"] = np.where(matched, "stable_id_verified", "unresolved")
    eligible = matched & mapping["activity_evidence_class"].eq("reported_inhibitory")
    mapping["included_as_positive"] = eligible
    positives = reference.loc[reference["scored_csv_line"].isin(mapping.loc[eligible, "scored_csv_line"])]
    columns = ["scored_csv_line", "seq_rev", "record_id", "name", "peptide_name",
               "activity_evidence_class", "has_boltz_ptm", "prediction_id_match", "input_smiles_match",
               "exact_name_match", "mapping_status", "included_as_positive"]
    return positives, mapping[columns].rename(columns={"seq_rev": "reference_entry_id"})


def fixed_percentile(values, design, higher=True):
    sign = 1 if higher else -1
    anchor = np.sort(sign * design.dropna().to_numpy())
    if not len(anchor):
        return pd.Series(np.nan, index=values.index)
    x = sign * values
    left = np.searchsorted(anchor, x, side="left")
    right = np.searchsorted(anchor, x, side="right")
    # Match the released average rank / n at design values. Between observed
    # values use the fraction of anchor observations below the query.
    ranks = np.where(right > left, (left + right + 1) / 2, left) / len(anchor)
    return pd.Series(ranks, index=values.index).where(values.notna())


def comparison_scores(table, designs):
    result = table.copy()
    result["structure_bottleneck"] = result[["ptm", "iptm"]].min(axis=1)
    anchor = result.loc[designs]

    def rank(column, higher=True):
        return fixed_percentile(result[column], anchor[column], higher)

    heads = [pd.concat([rank(v, False), rank(p)], axis=1).mean(axis=1)
             for v, p in zip(PRED_COLS, PROB_COLS)]
    result["affinity_consensus"] = pd.concat(heads, axis=1).median(axis=1)
    result["structure_quality"] = (0.60 * rank("structure_bottleneck")
                                   + 0.20 * rank("confidence_score")
                                   + 0.20 * rank("complex_pde", False))
    dev = {
        "solubility_tendency_score_0_100": True,
        "aggregation_risk_score_0_100": False,
        "sequence_liability_count": False,
        "sequence_stability_score_0_100": True,
        "peptide_drug_likeness_score_0_100": True,
    }
    result["developability_score"] = pd.concat(
        [rank(column, higher) for column, higher in dev.items()], axis=1).mean(axis=1)
    # Use the original implementation for the design values themselves,
    # preserving its floating-point ties. No selection is run.
    components = ["structure_bottleneck", "affinity_consensus", "structure_quality", "developability_score"]
    result.loc[designs, components] = compute_scores(table)[components]
    return result


def finite(values):
    return values.loc[np.isfinite(values)].reset_index(drop=True)


def directional_auc(first, second, direction):
    if not len(first) or not len(second):
        return np.nan
    sign = -1 if direction == "lower" else 1
    second = np.sort(sign * second.to_numpy())
    x = sign * first.to_numpy()
    left = np.searchsorted(second, x, side="left")
    right = np.searchsorted(second, x, side="right")
    return float((left + right).sum() / (2 * len(first) * len(second)))


def main(output):
    table = pd.read_csv(TARGET / "data/scored/merged_all_2_scored.csv")
    table["scored_csv_line"] = np.arange(2, len(table) + 2)
    positive, mapping = reference_crosswalk(table)
    original = table.index[table["source"].eq("design")]
    redesigned = table.index[table["source"].eq("IF_02")]
    all_designs = original.union(redesigned)
    if table.loc[all_designs, "seq_rev"].duplicated().any():
        raise ValueError("Duplicate sequence in the documented design comparison pool")
    calculated = comparison_scores(table, all_designs)
    cohorts = {POS: positive.index, ORIGINAL: original, REDESIGNED: redesigned, ALL: all_designs}
    output.mkdir(parents=True, exist_ok=True)
    prism = output / "prism"
    prism.mkdir(exist_ok=True)
    auc_rows, count_rows, plot_rows = [], [], []
    for column, metric, direction in METRICS:
        vectors = {name: finite(calculated.loc[indices, column]) for name, indices in cohorts.items()}
        for name, values in vectors.items():
            count_rows.append(dict(field=column, metric=metric, cohort=name, cohort_n=len(cohorts[name]),
                                   effective_n=len(values), missing_n=len(cohorts[name])-len(values)))
        for first, second in CONTRASTS:
            a, b = vectors[first], vectors[second]
            auc_rows.append(dict(field=column, metric=metric, direction=direction,
                                 comparison=f"{first} vs {second}", first_n=len(a), second_n=len(b),
                                 auc=directional_auc(a, b, direction)))
        if column in FIG2C:
            pd.DataFrame({name: vectors[name] for name in (POS, ORIGINAL, REDESIGNED)}).to_csv(
                prism / f"{column}.csv", index=False)
            for group in (POS, ORIGINAL, REDESIGNED):
                for idx, value in calculated.loc[cohorts[group], column].items():
                    if np.isfinite(value):
                        plot_rows.append(dict(field=column, cohort=group,
                                              scored_csv_line=int(table.at[idx, "scored_csv_line"]), value=value))
    auc = pd.DataFrame(auc_rows)
    auc.to_csv(output / "fig2b_auc_long.csv", index=False)
    matrix = auc.pivot(index=["field", "metric", "direction"], columns="comparison", values="auc")
    matrix = matrix.reindex(index=METRICS, columns=[f"{a} vs {b}" for a, b in CONTRASTS])
    matrix.to_csv(output / "fig2b_auc_matrix.csv")
    by_field = {row[0]: row for row in METRICS}
    matrix.reindex(index=[by_field[field] for field in MAIN_PANEL]).to_csv(
        output / "fig2b_recommended_main_matrix.csv")
    pd.DataFrame(count_rows).to_csv(output / "effective_sample_sizes.csv", index=False)
    pd.DataFrame(plot_rows).to_csv(output / "fig2c_values.csv", index=False)
    mapping.to_csv(output / "reference_mapping.csv", index=False)
    mapping.loc[mapping["mapping_status"].eq("unresolved")].to_csv(output / "unresolved_reference_rows.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    main(parser.parse_args().output_dir)
