# Tau score and structure outputs

## Score tables

### `boltz2_merged_screening_scores.csv`

CSV conversion of the saved merged result workbook. It has 9,473 records and
the source columns `D_sequence`, `sample_id`, `batch`, `description`, model
confidence metrics, three affinity heads, and `filter_passed`. The groups are:

| `description` | Records |
|---|---:|
| `BG_10000` | 8,927 |
| `Test250_4` | 335 |
| `Test5000` | 180 |
| `Tau_17` | 16 |
| `sup_allo_ile` | 15 |

There are 9,348 distinct D-sequences and 9,454 distinct sample identifiers.
Repeated sequences or identifiers across source groups are retained as
separate records. `filter_passed` is copied from the source workbook; its
criteria were not recoverable from the retained table and should not be
reinterpreted.

### `boltz2_bg10000_scores.csv`

The 8,927-row BG_10000 confidence and affinity table. It retains the source
metric values and identifiers but omits `confidence_json_path` and
`affinity_json_path`, which contained machine-local paths. The confidence and
affinity JSON files themselves were not retained in the local release copy.
Use [`scripts/remove_local_path_columns.py`](../../scripts/remove_local_path_columns.py)
to make the same kind of public copy from a locally collected score CSV.

Boltz-2 `affinity_pred_value*` and `affinity_probability_binary*` fields are
model outputs used for relative ranking in this campaign. They are not
calibrated peptide-binding affinities or experimental inhibition values.

## CIF archives

| Archive | Contents | Files |
|---|---|---:|
| `structures/boltzgen_bg10000_design_cifs.tar.gz` | CIF design outputs from the main BoltzGen run | 9,990 |
| `structures/boltz2_bg10000_model0_cifs.tar.gz` | Collected Boltz-2 model-0 complex structures | 8,927 |

Both archives contain only CIF files, retain original file basenames, and can
be extracted into separate directories with `tar -xzf`. They do not include
model weights, input YAML batches, JSON sidecars, logs, or unrelated pilot and
follow-up files. SHA-256 checksums are listed in
[`structures/SHA256SUMS.txt`](structures/SHA256SUMS.txt).

## Run provenance

The [Tau run provenance record](run_provenance.md) summarizes the recovered
BoltzGen environment metadata, Boltz-2 runtime details, Slurm resource
allocations and task states, artifact snapshot identifiers, output counts, and
known reproducibility limits. The BoltzGen scheduler job failed after
producing the archived CIFs;
the Boltz-2 Slurm record describes one completed representative array task,
not the status of the full batch. The April Boltz-2 task log also records an
affinity-model ligand-size warning.
