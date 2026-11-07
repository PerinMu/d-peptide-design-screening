# Open-source scope and provenance

This repository publishes computational methods and outputs for Tau and hIAPP
D-peptide design. The latest repository tree excludes project wet-lab
measurements, laboratory notebooks, assay images, plate maps, Prism files,
experiment-derived labels, and manuscript drafts.

## Included

- Shared sequence extraction, reverse-D encoding, stereochemical SMILES,
  Boltz-input, score collection, and screening code.
- Target structures and input configurations for PDB 5O3L and PDB 9ULZ.
- Project-generated sequence tables and model score tables.
- Selected hIAPP predicted structures and the two compressed Tau campaign CIF
  archives described in `tau/results/README.md`.
- A literature-derived Tau peptide reference table and the existing hIAPP
  literature reference data, with provenance notes.
- Path-configurable HPC/Slurm templates and available environment records.

## Excluded

- Experimental measurements, raw assay files, images, lab notebooks, and
  experiment-specific planning or handoff documents.
- Any score table or model-selection artifact whose labels depend on project
  wet-lab outcomes.
- Manuscript drafts, presentation decks, PyMOL session files, model caches,
  credentials, and private workstation paths.

The `wetlab/` template files present in the older repository tree have been
removed from the current published tree. Normal Git commits do not erase prior
repository history.

## Provenance limits

The Tau cloud directories and scheduler records were inspected read-only to
cross-check the released file counts and recover sanitized run metadata. The
Tau module records BoltzGen environment-version evidence, runtime parameters,
artifact snapshot identifiers, Slurm task states and allocations, and runtime
details available in a representative Boltz-2 task log. See
`tau/results/run_provenance.md`. The exact historical Boltz-2 package version,
checkpoint-file hashes, and random seeds remain unverified; the representative
Boltz-2 task must not be read as a completion record for the entire batch.

Raw cloud logs and JSON sidecars are not redistributed because they contain
cluster-specific paths and environment details. The public score tables and
CIF archives retain the computational outputs selected for release, with
archive checksums recorded alongside them.

Some HPC collection scripts retain site-specific default paths; they collect
provenance locally and warn users to review any generated bundle before sharing.
The raw collector bundles and logs are not included in the release payload.

The shared MIT license applies to repository code. PDB entries, upstream
models, and literature-derived data retain their own attribution and terms;
refer to the linked source records before redistribution or reuse.
