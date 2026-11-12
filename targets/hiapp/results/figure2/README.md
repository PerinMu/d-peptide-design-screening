# hIAPP Fig. 2b and 2c

From the repository root, run `python scripts/rebuild_hiapp_fig2.py` in the
hIAPP CPU environment. Use `--output-dir` to write a separate copy. The
analysis uses deposited predictions and sequence descriptors.

## Cohorts and labels

Dataset positives are the 73 records classified as `reported_inhibitory`
in the curated hIAPP literature table. The analysis joins database
`seq_rev` to `reference_entry_id` and verifies the prediction filename ID
where available and the original scoring input SMILES. All 76 entries and
all 54 Boltz-scored entries resolve to a stable literature record.
Two scored modified entries (30-1 and 30-2) have name-format differences
and resolve by ID. The three excluded scored entries are 5-1 (aggregation
promoting), 15-1 (mixed/adverse), and 32-3 (reported noninhibitory). The
label is a literature annotation from heterogeneous studies.

| Cohort | Sequence-derived metrics | Boltz-2 metrics |
|---|---:|---:|
| Dataset positives | 73 | 51 |
| Original designs | 1,954 | 1,934 |
| Redesigned variants | 7,852 | 7,776 |
| All designs | 9,806 | 9,710 |

Original and redesigned groups use the exact archived source labels
`design` and `IF_02`. All designs is their union. The two dual-source
records are outside these groups, consistent with the archived analysis
pool. Missing values are excluded per metric. The original 54/76 values
count all scored/all reference records, including the three excluded
records. The 22 inhibitory entries without model predictions contribute to
sequence-derived metrics.

## Directional AUC

The full matrix covers 31 metric rows and four comparisons as labeled in
the original figure. The first cohort in each comparison is the focal
cohort. AUC is the fraction of cross-group pairs in which its value ranks
higher in the declared orientation, with half credit for ties. AUC below
0.5 favors the second cohort in that orientation. Directions follow the
screening definitions where available. Descriptors without a preferred
direction use increasing numerical values. Directions are held fixed
across comparisons. These results quantify group separation because the
designed sequences have unknown experimental activity.

The original plot shows affinity outputs 1 and 2 as separate rows. The
affinity consensus uses the released three-entry rule: the unsuffixed
aggregate output and the two numbered prediction outputs. Structure quality
and developability also follow the released scoring formulas. For
cross-cohort composite comparisons, favorable percentiles use the full
9,806-design pool as a frozen reference. Average ranks divided by the
number of observed design values are used at ties. For a value between
observed design values, the percentile is the fraction of design values
below it in the oriented metric. Reference observations do not alter the
design scores. This analysis replaces the historical AUC values using
explicit labels, directions and composite definitions.

## Recommended main panel

The [nine-row main-panel matrix](fig2b_recommended_main_matrix.csv) follows
the scoring rules. It shows the structure bottleneck, confidence and PDE
(the three inputs to structure quality), affinity consensus, and the five
developability inputs. Keep the [complete matrix](fig2b_auc_matrix.csv)
as supplementary data. This retains pTM/ipTM, interface errors, model
outputs and descriptors for inspection while giving each main-panel row
a distinct role. Fig. 2c already shows pTM, ipTM, PDE and iPDE separately.
Keep the four P3 novelty descriptors in the supplement with their
non-preferential orientation. Passive permeability and related descriptors
can also remain there. The composite S and D rows summarize inputs already
shown in the proposed panel. Individual affinity outputs support the
supplementary head comparison. The Boltz-2 affinity and sequence scores
are predictions or heuristics. Group separation, including high AUCs for
individual physicochemical descriptors, does not establish biological
importance.

In Fig. 2a, update the affinity-consensus annotation to reflect the three
output entries and use the repository model label Boltz-2 for the
released predictions. The raw head 1 and head 2 rows remain in the
supplementary matrix to match the original Fig. 2b scope.

## Files

- [Full AUC matrix](fig2b_auc_matrix.csv) and [long AUC table](fig2b_auc_long.csv)
- [Effective sample sizes for each metric and cohort](effective_sample_sizes.csv)
- [Reference crosswalk](reference_mapping.csv) and [unresolved records](unresolved_reference_rows.csv)
- [Fig. 2c values with scored CSV line numbers](fig2c_values.csv)
- [Prism CSVs](prism/) for the eight Fig. 2c panels. Import each into a
  Column table, with each cohort in a separate column. Blank cells pad
  shorter columns and should remain blank. These are untransformed values.
