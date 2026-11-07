# Tau PHF6 D-peptide design

This module contains the computational inputs, literature reference table,
Boltz-2 score tables, and structure outputs for reverse-D peptide design against
the Tau PHF6 fibril core. It is a target-specific companion to the hIAPP
workflow documented at the repository root.

## Target and workflow

The template is derived from PDB 5O3L, chain A, sequence
`VQIVYKPVDLSKVTSKC` (17 residues). BoltzGen was configured to design
6–12-residue peptides against residues 1–11 (`VQIVYKPVDLS`). Candidate L
sequences were reversed and written in lower case to encode the project’s
all-D convention, then converted to stereochemical SMILES for Boltz-2 complex
prediction.

The workflow is:

```text
PDB 5O3L → BoltzGen peptide design → CIF sequence extraction
→ reverse-D encoding → stereochemical SMILES → Boltz-2 prediction
→ multi-batch score table and structure review
```

BoltzGen generates L-peptide hypotheses; reversing the sequence and changing
stereochemistry does not establish that the original backbone geometry or
binding contacts are retained. Boltz-2 affinity-related outputs are used only
as relative ranking signals. They are not measured affinities, inhibition
values, or evidence of biological activity.

The remote BoltzGen environment metadata report version 0.2.0, and the April
run log invokes that environment's Python 3.12 executable. A timestamped
package freeze was not retained to confirm the historical version. The
recovered configuration records four GPUs, a batch size of one, `multiplicity=1000`,
`diffusion_samples=10`, 500 sampling steps, and three recycling steps. Its
Slurm job ended in a failed state after producing 9,990 CIF files. A
representative Boltz-2 array task completed on one RTX 4090; its exact Boltz
package version and random seed were not recoverable. See the
[run provenance](results/run_provenance.md) for the recovered job states,
resource allocations, artifact snapshots, and limitations.

## Released data

| File | Contents |
|---|---|
| [`configs/target_5O3L.cif`](configs/target_5O3L.cif) | Target structural template from PDB 5O3L |
| [`configs/boltzgen_input.yaml`](configs/boltzgen_input.yaml) | Sanitized BoltzGen target and design-region input |
| [`configs/boltz2_template.yaml`](configs/boltz2_template.yaml) | Boltz-2 target/template input with a replaceable ligand SMILES |
| [`data/designs/run_10000_seq.csv`](data/designs/run_10000_seq.csv) | 8,964 unique BoltzGen-derived L-sequences; `count` records CIF occurrences |
| [`data/designs/run_10000_seq_reversed.csv`](data/designs/run_10000_seq_reversed.csv) | The same sequences in the reverse-D convention |
| [`data/designs/run_10000_seq_reversed_smiles.csv`](data/designs/run_10000_seq_reversed_smiles.csv) | Reverse-D sequences and explicit stereochemical SMILES |
| [`data/reference/tau_literature_peptides.csv`](data/reference/tau_literature_peptides.csv) | 62 literature-compiled D- and L-peptide records; source fields are retained |
| [`results/boltz2_bg10000_scores.csv`](results/boltz2_bg10000_scores.csv) | 8,927 Boltz-2 score records for the BG_10000 batch, with local file paths removed |
| [`results/boltz2_merged_screening_scores.csv`](results/boltz2_merged_screening_scores.csv) | 9,473 merged score records across the retained Tau batches |
| [`results/structures/`](results/structures/README.md) | Compressed CIF outputs for the main BoltzGen and Boltz-2 campaigns |

The merged table contains 9,473 records, 9,348 unique `D_sequence` values, and
9,454 unique `sample_id` values. Its groups are 8,927 `BG_10000`, 335
`Test250_4`, 180 `Test5000`, 16 `Tau_17`, and 15 `sup_allo_ile` records. The
source workbook name says “Batch1to4” although it includes batch 5; counts here
follow its row-level `batch` and `description` fields. The 9,473 figure is a
record count, not a count of distinct sequences.

The main BoltzGen structure archive contains 9,990 CIF files, which yielded
8,964 unique sequences in the saved sequence table. The corresponding
BG_10000 Boltz-2 table contains 8,927 score records. The tables retain the
original identifiers and metric values; only machine-local JSON path columns
were removed from the public BG_10000 CSV.

See [data notes](data/README.md), [score and structure notes](results/README.md),
and the repository’s [open-source scope](../docs/OPEN_SOURCE_SCOPE.md) for
provenance and limitations.

## Reproducing sequence preparation

Extract the included BoltzGen structures, then use the shared scripts from the
repository root. The commands below write temporary outputs and do not replace
the saved release tables.

```bash
mkdir -p /tmp/tau_bg10000_cifs
tar -xzf tau/results/structures/boltzgen_bg10000_design_cifs.tar.gz \
  -C /tmp/tau_bg10000_cifs

python scripts/extract_cif_sequences.py \
  /tmp/tau_bg10000_cifs /tmp/tau_bg10000_sequences.csv
python scripts/reverse_sequences.py \
  /tmp/tau_bg10000_sequences.csv /tmp/tau_bg10000_reverse_d.csv
python scripts/peptide_to_smiles.py \
  /tmp/tau_bg10000_reverse_d.csv /tmp/tau_bg10000_reverse_d_smiles.csv
python scripts/make_boltz_yaml.py \
  /tmp/tau_bg10000_reverse_d_smiles.csv \
  tau/configs/boltz2_template.yaml /tmp/tau_bg10000_yaml \
  --id-column name --smiles-column smiles \
  --template-cif tau/configs/target_5O3L.cif
```

For GPU inference, install BoltzGen and Boltz in separate environments, supply
their model assets, and adapt the Slurm resource directives to the target
cluster. The repository’s path-configurable job templates and dispatcher are
documented in [`hpc/README.md`](../hpc/README.md). Large intermediate YAML
directories, model weights, caches, and scheduler logs are not included.

From a configured Slurm login node, the 8-job/20-second dispatcher and score
collector can be used with site-specific paths:

```bash
cd /path/to/repository
bash hpc/submit_keep8.sh \
  /path/to/yaml_batch 8 20 /path/to/dispatch_state \
  hpc/run_lig_array_large.slurm boltz_arr 1

python scripts/collect_boltz_scores.py \
  --outputs-dir /path/to/boltz_outputs \
  --output /path/to/boltz_scores.csv
python scripts/remove_local_path_columns.py \
  /path/to/boltz_scores.csv /path/to/public_boltz_scores.csv
```

## References and scope

The template structure is PDB 5O3L ([PDB DOI](https://doi.org/10.2210/pdb5O3L/pdb));
BoltzGen and Boltz-2 are cited in the shared
[references](../docs/REFERENCES.md). Literature peptide annotations retain the
source workbook text and are not an independently verified quantitative
benchmark. No project-generated assay results or laboratory records are part
of this module.
