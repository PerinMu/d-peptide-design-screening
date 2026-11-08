# hIAPP case study

This target module contains a de novo D-peptide design and multi-parameter
hierarchical virtual screening campaign against the hIAPP amyloid fibril. PDB
9ULZ chain D residues 19–37 were used as the template,
with residues 21–37 as the design region. BoltzGen generated initial L-peptide
hypotheses, and BoltzIF redesigned sequences on generated backbones.

## Screening counts

| Stage | Count |
|---|---:|
| Retained BoltzGen outputs / unique sequences | 1,990 / 1,956 |
| BoltzIF outputs / unique sequences | 7,960 / 7,854 |
| Merged records / unique sequences | 9,810 / 9,808 |
| Design/IF analysis pool | 9,806 |
| Main hard gate | 904 |
| Structure-review pool | 42 (12 P1, 12 P2, 8 P3, 10 P4) |
| Final manually selected computational candidates | 12 |

Two rows labeled `design; IF_02` are outside the historical 9,806-row analysis
pool. The 42-row review pool includes the top ten of 30 P4-eligible candidates.
The original 42-row review sheet and candidate-level decisions were not
retained, so the CPU workflow reproduces the ranking tables but not the complete
manual selection.

## Reproduce the CPU screening

From the repository root:

```bash
conda env create -f targets/hiapp/environment.yml
conda activate dpeptide-screening
bash targets/hiapp/run.sh --output-dir /tmp/hiapp-screening
python scripts/validate_submission.py --output-dir /tmp/hiapp-screening
```

This uses the deposited Boltz-2 scores and does not rerun model inference.
Detailed thresholds, score equations, and production provenance are in
[Computational Methods](../../docs/PAPER_METHODS.md) and
[Reproducibility](docs/REPRODUCIBILITY.md). Boltz-2 affinity outputs are relative
model signals, and descriptor composites are heuristics; neither is measured
affinity or biological activity. See the shared [Model Card](../../MODEL_CARD.md)
for interpretation limits.
