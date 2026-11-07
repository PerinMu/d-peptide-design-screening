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
- Main hIAPP BoltzGen/BoltzIF CIF+NPZ result archives, selected hIAPP
  candidate structures, and a separate Boltz-2 follow-up prediction archive.
- The two compressed Tau campaign CIF archives and a separate Tau Boltz-2
  follow-up prediction archive.
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
`targets/tau/results/run_provenance.md`. The exact historical Boltz-2 package version,
checkpoint-file hashes, and random seeds remain unverified; the representative
Boltz-2 task must not be read as a completion record for the entire batch.

Cluster logs, absolute-path collector bundles, and the full Boltz-2 inference
tree are not redistributed. The manuscript-targeted follow-up archives retain
only predicted CIFs and confidence/affinity JSON outputs, with local paths
removed and checksums recorded alongside them.

HPC scripts use caller-supplied paths and environment names. Provenance
collectors write locally; review generated bundles for machine-specific runtime
details before sharing. Raw collector bundles and logs are not part of this
release.

The shared MIT license applies to repository code. PDB entries, upstream
models, and literature-derived data retain their own attribution and terms;
refer to the linked source records before redistribution or reuse.
