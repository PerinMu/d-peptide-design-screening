# Literature-curated peptide reference data

## Files and counts

| Target | File | Records | Distinct sequence notations |
|---|---|---:|---:|
| Tau | [`targets/tau/data/reference/tau_literature_peptides.csv`](../targets/tau/data/reference/tau_literature_peptides.csv) | 62 | 57 |
| hIAPP | [`targets/hiapp/data/reference/hiapp_literature_peptides.csv`](../targets/hiapp/data/reference/hiapp_literature_peptides.csv) | 76 | 76 |

Each row represents one populated record from the source workbook. Repeated
sequences are retained when the source lists separate records or target
constructs. The Tau source contains 43 records labeled D-peptide and 19 labeled
L-peptide. The hIAPP table includes L-, D-, mixed-stereochemistry, cyclic, and
chemically modified peptide records, as well as comparators with negative,
mixed, or aggregation-promoting source annotations.

The Tau table was prepared from the `D-peptides` worksheet only. The separate
Tau `Inhibitors` and `Info` worksheets mix therapeutic modalities or target
descriptions and do not provide a consistent sequence-level peptide table; they
are outside this release. The hIAPP table was prepared from populated records
in `Sheet1`. The source workbooks themselves are not included.

## Fields

The Tau and hIAPP tables share the source-row fields, with target-specific
structure and citation fields:

- `record_id`: stable release-row identifier; it is not a designed-candidate ID.
- `target`: Tau or hIAPP.
- `source_sheet_row` and `source_record_id`: row number and original record
  identifier from the source worksheet. A source record identifier may repeat.
- `reference_entry_id`: original hIAPP source-workbook reference key. It is
  retained for crosswalking to the supplied workbook. `citation_id` joins to
  the normalized bibliography in
  [`reference_inhibitor_sources.csv`](../targets/hiapp/data/designs/reference_inhibitor_sources.csv).
  These fields are blank for Tau, whose citations are row-level.
- `peptide_name`, `peptide_class`, and `sequence_notation`: source peptide
  identity and sequence notation, translated or standardized only where needed
  for English text and consistent formatting.
- `l_sequence_reference`: the source `L-SEQ` field. It is retained as supplied
  and is not guaranteed to be a canonical parent sequence for every analogue.
- Tau `source_smiles`: SMILES transcribed from the source workbook; these were
  not independently validated for structure or stereochemistry.
- hIAPP `smiles`: isomeric SMILES computed from the curated sequence and
  modification annotations with the reproducible script
  [`build_hiapp_reference_smiles.py`](../scripts/build_hiapp_reference_smiles.py)
  and RDKit 2025.9.2. The hIAPP workbook supplied no SMILES. These strings are
  therefore generated representations, not source-reported chemical records.
- hIAPP `smiles_status` and `smiles_note`: identify records that require a
  structural assumption and record that assumption, including unreported
  termini, unspecified sugar anomers, dehydrophenylalanine alkene geometry,
  or a source-sequence discrepancy. `computed_from_explicit_annotations`
  means the reported sequence, stereochemistry, and modifications specify the
  encoded structure; `computed_with_assumptions` means at least one structural
  feature was not explicit in the source and is listed in `smiles_note`.
- `target_region` and `assay_target`: source binding-region and assay-construct
  annotations. Inferred regions are explicitly labeled `Inferred`.
- `source_metric_header` and `source_metric_text`: the original metric-field
  heading and its reported text. The workbooks label the field as IC50 (µM),
  but cells also contain Kd, lag time, t50, percent inhibition, ThT summaries,
  non-numeric values, and placeholders. Values are therefore retained as text
  and are not treated as one harmonized IC50 endpoint. Empty cells represent
  blank or placeholder-only source entries such as `/`, `-`, or `ND`; values
  such as `No` and `<6.25` remain explicit.
- `design_method` and `reported_effects`: English summaries of the source
  annotations. These are literature-reported statements, not results from the
  present project.
- `activity_evidence_class`: a text-based label, defined below.
- `source_citation` and `citation_status`: standardized citation text and its
  provenance/verification status. For hIAPP, `citation_id` provides a stable
  key to the unique-source bibliography; repeated source entries share the same
  key.
- `data_quality_note`: row-level source inconsistencies or transparent
  annotations inherited from a clearly identified source group.

The hIAPP `AP5` source row placed a ThT inhibition result in the binding-site
column. That text was moved into `source_metric_text`, and the move is recorded
in `data_quality_note`.

## Activity annotations and limitations

`activity_evidence_class` uses only the source workbook text and does not
represent independent validation:

- `reported_inhibitory`: the source summary describes an inhibitory effect.
- `reported_measurement`: the source metric field contains a value, but the
  row-level outcome summary does not state an inhibitory effect.
- `reported_noninhibitory`: the source explicitly reports no inhibition.
- `aggregation_promoting`: the source reports accelerated aggregation.
- `mixed_or_adverse`: an inhibitory effect is reported alongside an adverse or
  conflicting outcome, such as cytotoxicity or increased membrane damage.
- `negative_control`: the source explicitly labels the entry as a negative
  control.
- `activity_not_reported`: the source row does not give an outcome or usable
  measurement for that record.

Tau citations were resolved to DOI-bearing primary records where available.
For records with blank citation cells, some references were linked from an
explicit source serial group; these rows are marked
`serial_group_reference_verified`. Ten Tau rows still have no row-level
citation or sufficiently clear group assignment. The hIAPP source table
contains 37 unique normalized references linked to all 76 source-entry IDs.
Statuses distinguish DOI-verified primary papers, a review, and UniProt
sequence records. Two source groups that referred to the same human IAPP
UniProt record were merged. The PACE entries were resolved from a research
briefing to the underlying primary paper. The dfPSMα3 hIAPP row was corrected
from a related 2024 insulin study to the 2025 hIAPP primary study. Pramlintide's
source is explicitly identified as a review.

SMILES are calculated as neutral, canonical isomeric structures. When a source
does not specify terminal chemistry, the script represents an uncapped peptide
with a free N-terminal amine and C-terminal carboxylic acid. Mature IAPP
analogues use a C-terminal amide and the Cys2-Cys7 disulfide where both cysteines
are present. O-glycan anomeric stereochemistry and the ΔPhe alkene geometry are
left unspecified when absent from the cited source. The MCIP-2a source sequence
is retained as transcribed and flagged because its residue count differs from
the paper's text description.

This is a manually assembled reference collection, not a systematic review,
uniformly tested benchmark, or project activity dataset. It contains no
experimental measurements from the present project. Literature-reported
results may depend on assay construct, concentration, ratio, and protocol, so
the records should not be ranked quantitatively across studies without
rechecking the primary papers.

The hIAPP screening input
[`reference_inhibitors_smiles.csv`](../targets/hiapp/data/designs/reference_inhibitors_smiles.csv)
was not changed. It remains the 76-entry descriptor reference used by the P3
novelty calculation; `reference_entry_id` links those entries to the richer
literature table. The new annotations do not affect any screening score or
historical result.

Regenerate the hIAPP literature SMILES and bibliography with
`python -m pip install -r requirements-reference-smiles.txt` followed by
`python scripts/build_hiapp_reference_smiles.py`. The pinned RDKit version and
structure specifications are kept with the generation script.

## Methods text

The following paragraph can be adapted for the manuscript:

> Literature-reported peptide reference records were curated from target-specific source spreadsheets. The released collection contains 62 Tau records (43 source-labeled D-peptides and 19 L-peptides, representing 57 sequence notations) and 76 hIAPP records (76 distinct sequence notations) linked to 37 unique hIAPP references. Records were retained at source-row granularity, including repeated sequences reported against different Tau constructs, negative controls, and peptide analogues with mixed or non-inhibitory annotations. Sequence and assay metadata, source-reported measurement strings, outcome summaries, and citations were normalized into English. hIAPP SMILES were computed from the curated sequence and modification annotations using RDKit 2025.9.2 because the source workbook did not supply SMILES; records with unresolved structural details are annotated. The source spreadsheets label the measurement field as IC50 (µM), although some entries report other endpoints, including Kd, lag time, t50, percentage inhibition, or ThT assay summaries. Because assay constructs and conditions differ, reported values were retained as text and were not harmonized or compared across studies. These literature annotations are not measurements from the present study and do not constitute a systematic review.
