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
the `D-peptides` sheet of the local literature-compilation workbook. It includes
43 entries labeled D-peptide and 19 labeled L-peptide, representing 57 unique
sequence strings. The original reported sequence, SMILES, assay target, IC50
field, result text, and reference text are retained as source values; the
source row number points back to the sheet. Blank and non-numeric values such
as `ND`, `/`, `No`, and `<6.25` remain as recorded.

This is a literature-derived reference table, not a dataset of project
experiments. The source annotations and numeric values have not been
independently verified, so consult the cited papers before quantitative use.
The source sheet also contains entries labeled as negative controls and entries
without activity values. The table should not be interpreted as a complete,
uniformly measured positive-control benchmark.

## Provenance and licensing

The target structure is derived from PDB 5O3L. Generated sequences and model
outputs are project computational outputs. Third-party structure and article
data retain their original attribution and terms; see the source references in
the CSV and [`docs/REFERENCES.md`](../../docs/REFERENCES.md). No local absolute
paths or cloud account identifiers are needed to interpret these tables.
