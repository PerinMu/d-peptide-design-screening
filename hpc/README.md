# Slurm templates

The scripts in this directory are starting points for GPU inference on a
Slurm cluster. Review the resource directives, model environments, cache
locations, and project paths before use.

## Target inputs

- hIAPP BoltzGen input: `targets/hiapp/configs/boltzgen/9ULZ.yaml`.
- Tau BoltzGen input: `targets/tau/configs/boltzgen_input.yaml`.
- The hIAPP end-to-end order and parameter switches are documented in
  `targets/hiapp/notebooks/00_full_generation_to_selection.ipynb`.
- Tau sequence preparation and released results are documented in
  `targets/tau/README.md`.

The reusable Slurm templates cover BoltzGen design, inverse folding,
single-ligand prediction, bounded batch dispatch, and result collection. Set
`REPO_ROOT`, input paths, environment names, caches, and output directories for
the current cluster. The dispatcher records submitted input stems in its state
directory and limits the number of active jobs. It does not delete or overwrite
prediction results.

## Provenance collection

The read-only collectors recover package, model-file, GPU, and scheduler
metadata without rerunning inference:

- `collect_provenance_boltzgen.sh`
- `collect_provenance_boltz2.sh`

Set the required environment and project paths before running a collector on a
configured login node. Each collector submits itself as a short Slurm job and
writes its bundle under the chosen project provenance directory. Review the
bundle before sharing; raw records can include hostnames and filesystem paths.

Sanitized hIAPP environment facts are in
`targets/hiapp/docs/PRODUCTION_ENVIRONMENT.md`; Tau run-specific records are in
`targets/tau/results/run_provenance.md`. Raw collector archives, checksum
sidecars, and logs are not part of the release.
