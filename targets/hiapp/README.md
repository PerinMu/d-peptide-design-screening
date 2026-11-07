# hIAPP case study

This target-specific release is one of two parallel applications of the
repository's computational D-peptide design and layered virtual-screening
workflow. It contains the hIAPP inputs, source and scored sequences, screening
tables, selected predicted complexes, and CPU reproduction environment.

## Target and workflow

PDB 9ULZ chain D residues 19–37 were used as the hIAPP fibril template, with
residues 21–37 specified as the design binding region. The workflow is:

```text
9ULZ → BoltzGen generation → BoltzIF redesign → reverse-D encoding
→ Boltz-2 prediction → physicochemical scoring → layered screening
→ candidate diversity and structure review
```

BoltzGen/BoltzIF produce L-amino-acid sequence and structure hypotheses. The
project reverses the sequence and encodes D stereochemistry in SMILES. This
retro-inverso conversion does not guarantee preservation of backbone geometry
or binding contacts.

## Main campaign counts

| Stage | Count |
|---|---:|
| Requested / completed BoltzGen designs | 2,000 / 1,990 |
| Unique BoltzGen sequences | 1,956 |
| Raw / unique BoltzIF sequences | 7,960 / 7,854 |
| Merged rows / unique sequences | 9,810 / 9,808 |
| Rows in the scored design/IF analysis pool | 9,806 |
| Candidates passing the main filters | 904 |
| Final computational candidates after structure review | 12 |

The main priority score combines affinity-head consensus, structure quality,
and sequence developability with weights 0.55, 0.30, and 0.15. Hard filters,
priority tiers, P4 criteria, reference-set handling, and count reconciliation
are described in [Methods](docs/METHODS.md) and
[Reproducibility](docs/REPRODUCIBILITY.md).

## Reproduce the saved CPU screening

From the repository root:

```bash
conda env create -f targets/hiapp/environment.yml
conda activate dpeptide-screening
bash targets/hiapp/run.sh --output-dir /tmp/hiapp-screening
python scripts/validate_submission.py --output-dir /tmp/hiapp-screening
```

This recomputes the saved tables and exports the included manually reviewed
candidate set. It does not rerun BoltzGen, BoltzIF, or Boltz-2. New stochastic
inference requires separate model assets and cluster resources; configure the
[HPC templates](../../hpc/README.md) for the local environment.

## Contents

- `configs/`: PDB 9ULZ structures and BoltzGen/Boltz-2 inputs.
- `data/`: design sequences, reference-inhibitor metadata, and model scores.
- `results/`: screening tables, final candidate manifest, selected CIFs, raw
  BoltzGen/BoltzIF structure archives, and separate follow-up Boltz-2 models.
- `notebooks/`: full GPU workflow and CPU ranking reproduction.
- `environments/`: sanitized production package snapshots.
- `docs/`: hIAPP methods, data provenance, environment, and model card.

## Interpretation and limitations

Affinity-head predictions and sequence-property scores are relative ranking
signals, not calibrated affinity, aggregation-inhibition, or activity values.
The final 12 are computational candidates, not evidence of biological effect.
No assay measurements or laboratory records are part of this target release.
For model versions, structures, leakage controls, and evidence boundaries, see
the [hIAPP model card](docs/MODEL_CARD.md),
[data provenance](docs/DATA_PROVENANCE.md), and
[shared project references](../../docs/REFERENCES.md).
