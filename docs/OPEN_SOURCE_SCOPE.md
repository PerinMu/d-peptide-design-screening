# Open-source scope and provenance

This repository releases computational methods and data for Tau and hIAPP
de novo D-peptide design. It does not include project assay measurements or
laboratory records.

## Included

- Sequence, stereochemical SMILES, input-generation, collection, scoring, and
  screening scripts.
- Target structures and model input configurations for PDB 5O3L and PDB 9ULZ.
- Project-generated sequence tables, model score tables, predicted structures,
  and sanitized run provenance.
- English-normalized literature peptide records with citations and source-text
  evidence annotations. These are literature data, not project measurements.
- HPC templates, computational environments, and checksums where retained.

## Excluded

- Assay files, images, laboratory notebooks, plate maps, and experiment-derived
  labels.
- Manuscript drafts, presentation files, PyMOL sessions, model caches,
  credentials, private paths, and cluster logs containing machine-specific
  identifiers.

Normal Git commits do not erase files from repository history. The `wetlab/`
template files in older commits are absent from the current tree.

## Provenance limits

The Tau and hIAPP run records summarize available configurations, artifacts,
and scheduler evidence. Exact production seeds were not retained; the Tau
Boltz-2 package version and checkpoint hash are unknown. The hIAPP Boltz-2
version is based on a recovered environment rather than a per-job log. The
full Boltz-2 inference tree and service-side MSA records are not redistributed.

The manuscript draft contains an ROC analysis, but the release has no ROC code,
complete positive-label definition, or derived ROC result table. The score table
contains 54 literature-reference rows with Boltz-2 metrics, while the literature
table contains 76 records with heterogeneous source annotations. See the
[Methods audit](PAPER_METHODS.md#release-audit-notes) before describing the ROC figure
as reproducible.

The repository code is under MIT. PDB structures, upstream models, and
literature-derived data retain their respective attribution and terms; consult
the linked source records before reuse.
