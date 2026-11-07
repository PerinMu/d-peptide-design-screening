# Follow-up Boltz-2 predictions

This separate 2026-10-31 prediction set supplies structure-model outputs for the manuscript. It is not part of the original target-wide screening ranking and contains no assay measurements or laboratory records. The peptides are represented only by their computational inputs and model predictions.

## Inputs and runs

- Template: PDB 5O3L in `configs/target_5O3L.cif`; target segment VQIVYKPVDLSKVTSKC; three-chain and five-chain contexts.
- Input configurations: `fibril_segment_3chain.yaml`, `fibril_segment_5chain.yaml`.
- Runs:
- `fragment_3chain`: five seed directories × five models = 25 predicted complexes.
- `fibril_5chain`: five seed directories × five models = 25 predicted complexes.
- Every run contains five seed directories (`seed_0`–`seed_4`), each with five model structures. The exact stochastic seed values and per-run package/checkpoint versions were not preserved with this output set.

`model_scores.csv` gives one row per predicted structure and includes the corresponding confidence and affinity JSON values. Affinity values repeat across the five models from the same seed because Boltz-2 writes one affinity JSON per seed. The raw mmCIF structures and score JSON files are in `structures_and_raw_scores.tar.gz`; archive paths match the CSV paths.

These are model predictions and do not establish binding or biological activity. Target-wide screening scores and the main candidate-selection workflow remain documented in the target README.
