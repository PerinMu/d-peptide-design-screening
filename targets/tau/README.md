# Tau PHF6 case study

This target module contains computational inputs and results for de novo
D-peptide design and multi-parameter hierarchical virtual screening against
the Tau PHF6 core. The template is PDB 5O3L chain A;
residues 1–11 (`VQIVYKPVDLS`, Tau 306–316) define the design region. The
released generation record documents BoltzGen. No Tau BoltzIF inputs or outputs
are present, so the release cannot establish whether BoltzIF contributed to
other historical records.

## Screening data

| Record | Count |
|---|---:|
| Merged Boltz-2 score records | 9,473 |
| Distinct `D_sequence` values | 9,348 |
| Distinct `sample_id` values | 9,454 |
| Records with `filter_passed=4` | 123 |
| Distinct sequences among those records | 106 |

The merged records span `BG_10000` (8,927), `Test250_4` (335), `Test5000`
(180), `Tau_17` (16), and `sup_allo_ile` (15). A 9,473 record count is not a
count of independent sequences. `filter_passed` was copied from the source
workbook; the rule that produced value 4 was not recovered.

The design input requested 1,000 multiplicities and retained 9,990 CIF files;
the released extraction table contains 8,964 unique L sequences. These counts
describe separate stages and should not be conflated with the five-batch
Boltz-2 table.

## Files and reproduction

- [`data/designs/`](data/designs/): extracted sequences and reverse-D SMILES.
- [`results/boltz2_merged_screening_scores.csv`](results/boltz2_merged_screening_scores.csv):
  merged score records.
- [`results/structures/`](results/structures/README.md): compressed generation
  and prediction structures.
- [`results/run_provenance.md`](results/run_provenance.md): recovered cluster
  settings and artifact counts.

Sequence preparation can be repeated from the released CIF archive using the
shared scripts from the repository root:

```bash
mkdir -p /tmp/tau_bg10000_cifs
tar -xzf targets/tau/results/structures/boltzgen_bg10000_design_cifs.tar.gz \
  -C /tmp/tau_bg10000_cifs
python scripts/extract_cif_sequences.py /tmp/tau_bg10000_cifs /tmp/tau_l.csv
python scripts/reverse_sequences.py /tmp/tau_l.csv /tmp/tau_d.csv
python scripts/peptide_to_smiles.py /tmp/tau_d.csv /tmp/tau_d_smiles.csv
```

The historical 123-record filter cannot be reproduced from the available rule
provenance. Shared parameters, formulae, limitations, and references are in
[Computational Methods](../../docs/PAPER_METHODS.md) and the
[Model Card](../../MODEL_CARD.md). HPC templates are under
[`hpc/`](../../hpc/README.md).
