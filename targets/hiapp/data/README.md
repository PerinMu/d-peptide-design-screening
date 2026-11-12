# Data layout

- `designs/batch1_design.csv`: 1,956 unique BoltzGen design sequences.
- `designs/batch1_IF_02.csv`: 7,854 unique BoltzIF redesign sequences.
- `designs/merged_designs.csv`: 9,808 unique sequences after cross-source merge.
- `designs/merged_designs_reversed_smiles.csv`: D-sequence encoding and SMILES.
- `designs/reference_inhibitors_smiles.csv`: literature/reference set used by
  the committed P3 descriptor novelty calculation. The separate
  [Fig. 2 analysis](../results/figure2/README.md) uses the curated evidence labels.
- `designs/reference_inhibitor_sources.csv`: normalized bibliography with one row
  per unique source, stable `reference_id`, DOI/accession, citation status, and a
  crosswalk to all 76 hIAPP source-entry IDs.
- `reference/hiapp_literature_peptides.csv`: English-normalized, row-level
  peptide, assay-summary, and citation records transcribed from the source
  inhibitor-information workbook. Its `citation_id` values join to the
  bibliography above; `reference_entry_id` preserves the source-workbook
  crosswalk. It contains 76 computed isomeric `smiles` strings and row-level
  structure assumptions. This descriptive table is separate from the
  computational input table and does not alter screening scores.
- `scored/merged_all_2_scored.csv`: 9,884-row structure, affinity and
  sequence-property table used by the reproducible notebook. It contains 9,806
  analyzed design/IF records, two merged shared-source records and 76 literature
  references.

Treat `targets/hiapp/data/scored/` as immutable analysis input. Reruns should
write new outputs under `targets/hiapp/results/screening/` and document the
source file checksum.

The hIAPP source workbook did not contain SMILES. The released SMILES were
computed from its sequence and modification annotations by
`scripts/build_hiapp_reference_smiles.py` using RDKit 2025.9.2. The script marks
assumptions such as unspecified termini, sugar anomers, and source-record
discrepancies. Citation statuses distinguish primary research papers, a review,
and sequence-database records. Literature activity annotations remain source
summaries, not project measurements or a uniformly tested benchmark.

To regenerate the literature table and its bibliography, install the pinned
dependency with `python -m pip install -r requirements-reference-smiles.txt`
and run `python scripts/build_hiapp_reference_smiles.py` from the repository
root. This does not regenerate or modify the P3 descriptor input.

For the complete schema, activity-evidence labels, source-field caveats, and
copy-ready manuscript wording, see
[`docs/LITERATURE_PEPTIDE_DATA.md`](../../../docs/LITERATURE_PEPTIDE_DATA.md).
