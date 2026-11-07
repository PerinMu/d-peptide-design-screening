# Computational D-peptide design for Tau and hIAPP

[![Validation](https://github.com/PerinMu/hIAPP-D-peptide-design/actions/workflows/validate.yml/badge.svg)](https://github.com/PerinMu/hIAPP-D-peptide-design/actions/workflows/validate.yml)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Code, target inputs, model scores, and computational structures for de novo
reverse-D peptide design and layered virtual screening against Tau and hIAPP.
The repository combines two target-specific workflows and shared utilities for
sequence extraction, reverse-D encoding, stereochemical SMILES, model-input
generation, score collection, screening, and result export. No project wet-lab
measurements, laboratory records, or assay-derived training labels are included.

| Target | Structural template | Main computational release |
|---|---|---|
| Tau PHF6 | [PDB 5O3L](https://doi.org/10.2210/pdb5O3L/pdb) | [Tau workflow and data](tau/README.md): 9,473 merged screening records, 9,348 unique D-sequences, and archived BoltzGen/Boltz-2 structures |
| hIAPP | [PDB 9ULZ](https://doi.org/10.2210/pdb9ULZ/pdb) | [CPU screening workflow](README.md#quick-start-hiapp-screening-reproduction), notebooks, score tables, and predicted structures |

The two target-specific score sets use different inputs and screening stages;
their scores should not be compared directly. See the [open-source scope and
provenance note](docs/OPEN_SOURCE_SCOPE.md) for data boundaries and sources.

## Quick start: hIAPP screening reproduction

The screening step runs on CPU using the score table included in this repository.

```bash
git clone https://github.com/PerinMu/hIAPP-D-peptide-design.git
cd hIAPP-D-peptide-design
conda env create -f environment.yml
conda activate hiapp-d-peptide-analysis
bash run.sh
```

Expected output:

```text
Analysis rows: 9806
Hard gate: 904
P1/P2/P3: {'P1': 12, 'P2': 12, 'P3': 8}
P4 hard pass: 30; exported top 10
Wrote 12 candidates to .../results/submission/results.csv
```

This recomputes the ranking and exports the 12 candidates selected in the saved
manual structure-review record. It does not rerun the neural models or select
the final 12 automatically. After installation, it normally takes less than a
minute.

To write results elsewhere and compare them with the saved tables:

```bash
bash run.sh --output-dir /tmp/hiapp-results
python scripts/validate_submission.py --output-dir /tmp/hiapp-results
```

The validator checks candidate identities, ranks, review tiers, screening tables,
CSV/Excel agreement, structure files, and run checksums.

## hIAPP inputs and outputs

`run.sh` accepts `--scores`, `--final`, and `--output-dir`. Its defaults are:

| Argument | Default | Contents |
|---|---|---|
| `--scores` | `data/scored/merged_all_2_scored.csv` | Model outputs and sequence properties |
| `--final` | `results/final_candidates/final_12.csv` | Saved manual selection |
| `--output-dir` | `results/submission` | Generated CSV, screening tables, and metadata |

Each run writes:

- `results.csv`: candidate sequences, SMILES, scores, model versions, and structure paths.
- `screening/`: the hard-filter, P1–P3, and P4 candidate tables.
- `run_metadata.json`: runtime versions, Git revision, and input, output, code,
  and structure SHA256 hashes.

The committed [results.xlsx](results/submission/results.xlsx) contains the same
candidate table and a field guide. `run.sh` generates CSV, not Excel.
Structure paths in the table are relative to the repository root.
See the [output field descriptions](results/submission/README.md) for units and
missing-value conventions.

The entry point and validator check the saved hIAPP run. A new campaign needs
its own review record and expected counts.

## hIAPP installation

### Analysis

The Conda environment above specifies Python 3.11.9 and the direct package
versions. Alternatively, install the same direct dependencies with pip:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The CPU scripts run on macOS and Linux. GitHub Actions uses Ubuntu and Python
3.11.9. CUDA is not needed for screening. `requirements.txt` pins direct
packages; it is not a complete transitive dependency lock.

### Model inference

Install BoltzGen and Boltz in separate environments on a Linux system with
NVIDIA GPUs. The commands below use the package versions recorded for this run:

```bash
conda create -n boltzgen python=3.12 -y
conda run -n boltzgen python -m pip install boltzgen==0.2.0
conda run -n boltzgen boltzgen --help

conda create -n boltz python=3.10.20 -y
conda run -n boltz python -m pip install 'boltz[cuda]==2.2.1'
conda run -n boltz boltz predict --help
```

Follow the upstream [BoltzGen](https://github.com/HannesStark/boltzgen) and
[Boltz](https://github.com/jwohlwend/boltz) instructions for model assets and
platform-specific installation. BoltzGen assets can be downloaded with:

```bash
conda run -n boltzgen boltzgen download all --cache /path/to/boltzgen_cache
export BOLTZ_CACHE=/path/to/boltz_cache
```

Model weights are not included. The full notebook specifies checkpoint and
molecule-cache paths. On clusters without compute-node internet access, prepare
model assets and required MSA inputs before submitting prediction jobs.

The recorded BoltzGen and BoltzIF jobs each requested four GPUs. Boltz-2 used
one RTX 4090, six CPU cores, and 60 GB RAM per job, with up to eight concurrent
jobs. The [production environment record](docs/PRODUCTION_ENVIRONMENT.md)
contains OS, CUDA, driver, checkpoint, and timing information; package snapshots
are in [environments/](environments/).

BoltzGen 0.2.0 is confirmed in a historical log. Boltz 2.2.1 was recovered from
the surviving environment after the run. A fresh install of these packages does
not reproduce every historical dependency.

## hIAPP notebooks

| Notebook | Use |
|---|---|
| [00_full_generation_to_selection.ipynb](notebooks/00_full_generation_to_selection.ipynb) | Configure and run design, sequence redesign, reverse-D encoding, prediction, screening, and structure review on a GPU/Slurm system |
| [01_reproduce_screening.ipynb](notebooks/01_reproduce_screening.ipynb) | Recompute the saved screening results on CPU |

```bash
jupyter lab notebooks/00_full_generation_to_selection.ipynb
```

The first parameter cell sets server paths, environments, caches, and checkpoints.
`RUN_CPU_STEPS=False` and `SUBMIT_GPU_STEPS=False` print commands without running
them. Enable each switch only after configuring the paths, and wait for each
Slurm stage to finish before processing its outputs.

For an installation check, use `NUM_DESIGNS=2` and `DIFFUSION_BATCH_SIZE=1`
in a new output directory, then test prediction on one candidate. Keep
`VERIFY_HISTORICAL_COUNTS=False` for new stochastic runs. A small test is not
expected to reproduce the saved counts or produce 12 passing candidates.

To execute the CPU notebook from the command line:

```bash
jupyter nbconvert --to notebook --execute \
  notebooks/01_reproduce_screening.ipynb \
  --output /tmp/01_reproduce_screening.executed.ipynb \
  --ExecutePreprocessor.timeout=600
```

## hIAPP workflow

```text
9ULZ target → BoltzGen → BoltzIF → reverse-D SMILES → Boltz-2
→ sequence properties → ranking and filtering → structure review
```

1. Use PDB 9ULZ chain D residues 19–37 as the target, with residues 21–37
   specified as the binding region.
2. Generate L-peptide sequence/structure pairs and redesign their sequences.
3. Reverse the sequences and encode D stereochemistry in isomeric SMILES.
4. Predict target–peptide complexes with Boltz-2.
5. Rank candidates using affinity-related outputs, structure confidence, and
   sequence-property scores. Apply filters and sequence-diversity selection.
6. Inspect the predicted complexes and record the final selection.

The main filters require complete affinity outputs, `min(pTM, ipTM) >= 0.65`,
solubility tendency `>= 40`, and aggregation risk `<= 65`. The main ranking
combines affinity, structure, and developability scores with weights of
0.55, 0.30, and 0.15. P4 is a separate 11–12-residue branch with a structure
threshold of 0.75. Equations and tier definitions are in
[Methods](docs/METHODS.md).

| Stage | Count |
|---|---:|
| Requested / completed BoltzGen designs | 2,000 / 1,990 |
| Unique BoltzGen sequences | 1,956 |
| Raw / unique BoltzIF sequences | 7,960 / 7,854 |
| Unique merged sequences | 9,808 |
| Sequences entering ranking | 9,806 |
| Candidates passing the main filters | 904 |
| Candidates reviewed, including P4 | 42 |
| Final candidates | 12 |

Two sequences with combined source labels were excluded from the historical
ranking pool. See [count reconciliation](docs/REPRODUCIBILITY.md) for details.

## Repository layout

| Directory | Contents |
|---|---|
| `configs/` | Target structures and BoltzGen/Boltz-2 input templates |
| `scripts/` | Conversion, collection, scoring, screening, and review scripts |
| `hpc/` | Slurm job and batch-submission scripts |
| `notebooks/` | Full workflow and CPU reproduction |
| `data/` | Sequence tables, reference entries, and saved scores |
| `results/` | Screening tables, final candidates, and predicted structures |
| `environments/` | Recovered GPU package lists |
| `tau/` | Tau PHF6 inputs, literature reference peptides, screening scores, and structure archives |

## hIAPP notes

The 12 sequences are computational candidates awaiting experimental validation.
Boltz-2 affinity outputs are used for relative ranking, and the sequence-property
scores are project heuristics. Neither is a measured binding or inhibition value.
Reverse-D conversion does not guarantee that the original backbone contacts are
preserved.

Historical random seeds and MSA response files were not retained. New model runs
can produce different candidates and require a new structure review. For the
hIAPP campaign, model caches and bulk intermediate outputs are omitted; saved
tables and selected predicted structures support reproduction of the screening
results. The Tau module includes compressed CIF outputs for its main BoltzGen
and Boltz-2 campaigns.

## Documentation

- [Model versions, parameters, and limitations](MODEL_CARD.md)
- [Methods](docs/METHODS.md)
- [Sequence-property equations](docs/PHYSICOCHEMICAL.md)
- [Data dictionary](docs/DATA_DICTIONARY.md)
- [Data sources and preprocessing](docs/DATA_PROVENANCE.md)
- [Reproducibility](docs/REPRODUCIBILITY.md)
- [Production environment](docs/PRODUCTION_ENVIRONMENT.md)
- [References](docs/REFERENCES.md)
- [Open-source scope and provenance](docs/OPEN_SOURCE_SCOPE.md)

## Citation and license

See [CITATION.cff](CITATION.cff) for repository citation metadata. Please also
cite the models and source structures used in your analysis; references are
listed [here](docs/REFERENCES.md).

Repository code is available under the [MIT License](LICENSE). Third-party
models, software, and data retain their own licenses and terms.
