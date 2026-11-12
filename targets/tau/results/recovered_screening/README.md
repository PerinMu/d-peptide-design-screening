# Recovered screening files

Per-batch `*_scores.csv` tables preserve reported metrics and replace machine
paths with basenames. `*_index.csv` records CIF SHA256 values and archive
members. `scored_sequence_links.csv` links deposited scored sequences to
structures. A blank location marks an unresolved link.
`archive.tar.gz::member` identifies an archive member.

`screening_inputs.tar.gz` contains validated per-design inputs.
`screening_inputs_index.csv` records original and portable SHA256 values.
Line endings were normalized and the template path reduced to its basename.
Place the template in the working directory or set its path before inference.

See the [recovery audit](../../../../docs/COMPUTATIONAL_DATA_RECOVERY.md)
for counts, provenance and remaining gaps.

Use [`target_5O3L.cif`](../../configs/target_5O3L.cif) as `PHF.cif`. The
deposited template matches the local input template after whitespace
normalization. Tau links use the original batch label and sample ID.
