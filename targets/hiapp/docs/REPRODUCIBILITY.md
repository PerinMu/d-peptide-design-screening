# Reproducibility and data lineage

## Reproduce the screening results

```bash
conda env create -f targets/hiapp/environment.yml
conda activate dpeptide-screening
bash targets/hiapp/run.sh
```

This deterministic CPU entry point regenerates the screening tables and the
standardized `targets/hiapp/results/submission/results.csv`. It also writes runtime metadata
and SHA256 hashes. Neural design and prediction are separate stochastic GPU
stages documented in `targets/hiapp/notebooks/00_full_generation_to_selection.ipynb`.

## Count reconciliation

| Stage | Rows / designs | Unique / usable | Evidence in repository |
|---|---:|---:|---|
| BoltzGen requested | 2,000 | - | run configuration and lab record |
| BoltzGen completed CIF/NPZ pairs | 1,990 | - | retained source tree; extraction validation |
| BoltzGen sequence table | 1,990 | 1,956 | `targets/hiapp/data/designs/batch1_design.csv` |
| BoltzIF raw output | 7,960 | 7,854 | lab record; unique table committed |
| Merged design + IF | 9,810 | 9,808 | `targets/hiapp/data/designs/merged_designs.csv` |
| Analysis design/IF rows | 9,806 | 9,806 | `targets/hiapp/data/scored/merged_all_2_scored.csv` |
| Hard-gated candidates | - | 904 | recomputed in notebook |
| P1/P2/P3/P4 review | - | 12/12/8/10 | recomputed in notebook |
| Final computational shortlist | - | 12 | `targets/hiapp/results/final_candidates/final_12.csv` |

The merged table labels two cross-source duplicate sequences as
`design; IF_02`. The historical analysis selected exact source labels `design`
and `IF_02`, so these two shared-source rows were not included in the 9,806-row
analysis pool. This provenance-label decision, rather than a model-score gate,
explains the difference from 9,808 unique merged sequences. The notebook keeps
the recorded 9,806 denominator so that every published count is reproducible.

## Included artifacts

- 9ULZ structural template and BoltzGen YAML.
- Unique generation and inverse-folding sequence tables.
- Merged D-peptide sequence/SMILES table.
- Full 9,884-row scored CSV: 9,806 analyzed design/IF records, two merged
  shared-source records, and 76 literature references.
- 1,990 BoltzGen and 7,960 BoltzIF CIF/NPZ output pairs in
  `targets/hiapp/results/structures/`, with SHA-256 checksums.
- Final 12 predicted complex CIF files.
- Separate Boltz-2 follow-up structure/score archives for the two target
  contexts used in the manuscript; see `results/manuscript_predictions/`.
- Portable scripts for collection, merge, recovery and screening.
- Full GPU-server Notebook from official installation through structural review.

## Artifacts intentionally omitted

- The full raw Boltz-2 output tree with every prediction sidecar and the
  thousands of generated YAML input files.
- Separate small pilot and test runs outside the two main screening campaigns.

Neural generation and inference also require the corresponding model assets,
checkpoint files, and software environments; these are not redistributed.
Treat the committed score tables and structure archives as the recorded model
outputs for the analyses in this repository.

## Software and checkpoint provenance

Read-only recovery on 2026-08-15 verified the model environments, four
checkpoint hashes, the BoltzGen container hash, current GPU/CUDA stacks,
scheduler history, and production commands. The sanitized record is
[`PRODUCTION_ENVIRONMENT.md`](PRODUCTION_ENVIRONMENT.md), and full package
snapshots are under `targets/hiapp/environments/`. BoltzGen 0.2.0 is confirmed in a historical
job log; Boltz 2.2.1 is the still-installed environment and is labeled as
recovered because historical prediction logs did not print its version.

Upstream source Git revisions, production stochastic seeds, the exact GPU model
for the historical BoltzGen nodes, the MSA service-side version, and returned
alignment archives remain unavailable. The commands below are mandatory capture
steps for future campaigns.

For each independent generation or prediction run, record the exact software
environment, source revision, and checkpoint checksum alongside the results:

```bash
boltzgen --version
python -m pip freeze > environment-boltzgen.txt
python -m pip show boltz > environment-boltz.txt
git -C /path/to/boltzgen rev-parse HEAD
git -C /path/to/boltz rev-parse HEAD
sha256sum /path/to/checkpoint.ckpt
```

Preserve a release-safe environment record without credentials or
machine-specific access configuration.

## Determinism

Percentile scoring and greedy sequence selection are deterministic for a fixed
input table and stable sort order. Neural generation and structure prediction
may vary with software/checkpoint versions, random seeds and hardware. Preserve
the original result table as immutable evidence and write new reruns to a new
versioned directory.

## Portable HPC execution

The `hpc/` directory provides path-configurable Slurm templates for BoltzGen,
BoltzIF, bounded-concurrency Boltz-2 prediction, and resume-safe dispatch. The
retry extractor compares every expected YAML identifier against successful
model-0 CIF outputs, including inputs for which no output directory was created.
