# De novo D-peptide design and multi-parameter hierarchical virtual screening

Code and computational data for structure-guided D-peptide design and
screening against Tau and hIAPP amyloid fibrils. The targets are parallel case
studies with distinct generation records and screening workflows.

## Workflow

```text
Fibril structure and binding region
  → BoltzGen design (both targets; BoltzIF redesign is documented for hIAPP)
  → retro-inverso sequence conversion and stereochemical SMILES
  → Boltz-2 complex prediction
  → sequence descriptors and multi-parameter hierarchical virtual screening
  → candidate structure review
```

Boltz-2 outputs and sequence-property scores are computational prioritization
signals, not experimental measurements. The affinity module has limited
validation for peptide-sized ligands; see the [Model Card](MODEL_CARD.md).

## Data

| Target | Template | Released screening records |
|---|---|---|
| Tau PHF6 | [PDB 5O3L](https://doi.org/10.2210/pdb5O3L/pdb) | 9,473 score records, 9,348 distinct D sequences; 123 records have `filter_passed=4` (106 distinct sequences). The original filter rule is unavailable. See [Tau](targets/tau/README.md). |
| hIAPP | [PDB 9ULZ](https://doi.org/10.2210/pdb9ULZ/pdb) | 9,806 analysis rows → 904 hard-gate candidates → 42 structure-review candidates → 12 manually selected computational candidates. See [hIAPP](targets/hiapp/README.md). |

Target inputs, score tables, structures, literature-derived reference tables,
and run records are under [`targets/`](targets/). Manuscript aliases FI-11 and
KV-12 are linked to the released records in the
[candidate ID crosswalk](docs/CANDIDATE_ID_CROSSWALK.csv). LG-11 remains
unmapped.

The manuscript draft includes an ROC analysis, but this release has no ROC
script or complete positive-label definition. It contains 54 literature
records with Boltz-2 metrics and 76 sequence-reference records; the recorded
evidence classes do not identify 54 unambiguous positives. See the
[Methods audit](docs/PAPER_METHODS.md#release-audit-notes).

## Reproduce the hIAPP CPU screening

This regenerates the saved ranking from the released score table. It does not
rerun BoltzGen, BoltzIF, or Boltz-2, and it cannot reproduce the full manual
selection from the 42-row review pool because that original review sheet and
candidate-level decisions were not retained.

```bash
git clone https://github.com/PerinMu/d-peptide-design-screening.git
cd d-peptide-design-screening
conda env create -f targets/hiapp/environment.yml
conda activate dpeptide-screening
bash targets/hiapp/run.sh --output-dir /tmp/hiapp-screening
python scripts/validate_submission.py --output-dir /tmp/hiapp-screening
```

Detailed parameters and equations are in [Computational Methods](docs/PAPER_METHODS.md).
The [release scope](docs/OPEN_SOURCE_SCOPE.md) describes included data and
provenance. Cluster templates are documented under [`hpc/`](hpc/README.md).

## Citation and license

See [CITATION.cff](CITATION.cff) and [References](docs/REFERENCES.md). Repository
code is distributed under the [MIT License](LICENSE); upstream models, PDB
structures, and literature-derived data retain their respective terms.
