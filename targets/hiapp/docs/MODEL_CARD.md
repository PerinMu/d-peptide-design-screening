# hIAPP model record

This file records target-specific settings. Interpretation limits are collected
in the [shared Model Card](../../../MODEL_CARD.md); recovered environments,
checkpoint hashes, and resource requests are in
[Production Environment](PRODUCTION_ENVIRONMENT.md).

- **Generation:** BoltzGen 1 (`boltzgen` 0.2.0 recovered environment),
  `peptide-anything` protocol; 2,000 requested designs, 1,990 retained CIF/NPZ
  pairs, 1,956 unique extracted sequences.
- **Redesign:** BoltzIF (`boltzgen` 0.2.0 recovered environment), four
  sequences per backbone, temperature 0.2, cysteine excluded; 7,960 outputs and
  7,854 unique sequences.
- **Complex prediction:** Boltz-2 (`boltz` 2.2.1 recovered environment), three
  diffusion samples, MSA server option, and explicit stereochemical D-peptide
  ligand SMILES. The prediction log did not record the package version, so
  2.2.1 is an environment snapshot rather than a confirmed per-job version.
- **Target:** PDB 9ULZ, chain D residues 19–37; residues 21–37 were the intended
  design region.
- **Selection:** confidence, affinity-head outputs, and sequence heuristics
  feed the documented screening. These are model outputs and ranking criteria,
  not experimental measurements.

The scoring equations, thresholds, and evidence limits are in
[Computational Methods](../../../docs/PAPER_METHODS.md). The original 42-row
manual-review sheet was not retained.
