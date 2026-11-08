# Tau data notes

## Design tables

The sequence tables were extracted from the local BoltzGen `phf_10000_pep`
campaign. `run_10000_seq.csv` contains one row per unique L-sequence;
`count` is the number of CIF structures in which that sequence occurred.
`seq_rev` is the reversed, lower-case all-D representation. `smiles` encodes
that sequence with explicit stereochemistry and free termini.

| Table | Rows | Description |
|---|---:|---|
| `designs/run_10000_seq.csv` | 8,964 | Unique L-sequences extracted from 9,990 CIF files |
| `designs/run_10000_seq_reversed.csv` | 8,964 | Reverse-D sequence representation |
| `designs/run_10000_seq_reversed_smiles.csv` | 8,964 | Reverse-D sequence plus stereochemical SMILES |

## Literature reference peptides

`reference/tau_literature_peptides.csv` contains the 62 populated records from
the `D-peptides` sheet of the source workbook. It includes 43 records labeled
D-peptide and 19 labeled L-peptide, representing 57 distinct sequence
notations. Each output row maps to a source worksheet row. The table uses
English field names and summaries, stable release record IDs, source citations,
and an activity-evidence annotation that preserves negative controls,
non-inhibitory entries, and missing activity information.

The original worksheet labels its measurement column `IC50/µM`, but some cells
contain other endpoints or free text. `source_metric_text` therefore remains
text and is not a harmonized potency value. Some citations were linked from an
explicit source serial group when the row citation cell was blank; the status
is shown in `citation_status` and the assignment is described in
[`docs/LITERATURE_PEPTIDE_DATA.md`](../../../docs/LITERATURE_PEPTIDE_DATA.md).
Ten rows have no sufficiently clear row-level or group citation. Source SMILES
are transcribed, not independently chemically validated. This is a
literature-derived reference collection, not project experimental data or a
uniform benchmark.

## Provenance and licensing

The target structure is derived from PDB 5O3L. Generated sequences and model
outputs are project computational outputs. Third-party structure and article
data retain their original attribution and terms; see the source references in
the CSV and [`docs/REFERENCES.md`](../../../docs/REFERENCES.md). No local absolute
paths or cloud account identifiers are needed to interpret these tables.
