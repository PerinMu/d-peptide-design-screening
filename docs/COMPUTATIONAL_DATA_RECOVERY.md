# Computational data recovery

The source workbooks were inspected locally. The candidate roster and crosswalk
contain computational fields from Supplementary Tables 1 and 3. The original
workbooks and other source materials are kept outside the release.

## Candidate mapping

The [crosswalk](CANDIDATE_ID_CROSSWALK.csv) contains one row per named
candidate. Source CSV lines count the header as line 1. Scores were checked
after matching the full D sequence. Where the supplement displays fewer
decimal places, values were compared at that precision. An integer confidence
of 1 was compared as reported.

- **hIAPP.** All 12 Supplementary Table 3 candidates match the deposited
  screening scores and final manifest. FI-11 is `ITSSGEITLSF_1`
  (`HIAPP-DP-003`). LG-11 is `GATTLSISVNL_1`, sequence `lnvsislttag`.
- **Tau.** AT-9, CE-12, ST-10, SI-9 and KV-12 match batch 5 across the
  supplementary metrics. KV-12's batch 2 record has different scores.
  Both model-0 structures are indexed as alternative records. The batch 5
  link identifies the source of the table scores. It does not identify the
  structure used in every manuscript panel or in later follow-up runs.
- **EG-9.** Twelve metrics match `GLVVQTVVE_1` at table precision. The table
  gives confidence 1, while the screening record gives 0.805804431438446.
  Both values are preserved in their respective tables.
- **AA-10, AP-10, SA-9 and DV-9.** Each has two same-sequence score records.
  Neither record reproduces the supplementary score vector. Their table
  scores are retained and their source IDs and CIFs remain unassigned.
  The [Tau alternative table](../targets/tau/results/final_candidates/score_alternatives.csv)
  exposes both source records for each candidate.

## Coverage and gaps

| Stage | Tau | hIAPP |
|---|---|---|
| Primary generation | 9,990 BoltzGen CIFs in the existing archive | 1,990 BoltzGen and 7,960 BoltzIF CIF/NPZ pairs in the existing archives |
| Main prediction | 9,473 merged score rows, 9,348 distinct D sequences. Model-0 CIFs are indexed by batch and ID. | 9,806 design/IF rows, of which 9,710 link to score exports and model-0 CIFs. The 96 unlinked rows lack the deposited model scores. |
| Recovered prediction collections | 546 model-0 CIFs in four supplemental batches, plus an index of 8,927 previously released BG10000 CIFs | 9,768 indexed model-0 records across three batches, including reference and mixed-source rows. Twelve existing final CIFs are referenced by identical content hash. |
| Portable inputs | 9,517 YAML files across five batches | 9,884 YAML files across two collections |
| Later manuscript predictions | 50 CIFs in the existing follow-up archive | 75 CIFs in the existing follow-up archive |

The [local inventory](LOCAL_COMPUTE_INVENTORY.csv) counts file types in the
inspected computational directories. Its scopes overlap and include pilot runs,
parallel copies, archives and postprocessed exports. These counts cannot be
summed into a count of unique predictions. Supplementary Table 1 Full and the deposited Tau
merged table agree across all 9,473 rows at the workbook’s numeric precision. The
[Tau](../targets/tau/results/recovered_screening/README.md) and
[hIAPP](../targets/hiapp/results/recovered_screening/README.md) indices give
the released file-level records and SHA256 values.

The collected screening CIFs are model 0 only. The bulk screening output
directories with original confidence/affinity JSON, NPZ and all model samples
were not present in the inspected production collections. Score exports retain
the JSON basenames and reported metrics. Other local outputs include
exploratory and follow-up runs that could not be attributed to the main screen.
The 9,990 Tau primary BoltzGen NPZ files were inventoried separately. Inspection
found an object array in a sample, so the set is outside this release pending
payload verification. Tau pilot directories contain inverse-folding labels,
which do not establish BoltzIF use in the main Tau production run.

The available campaign failure and retry evidence is limited to the existing
[run provenance](../targets/tau/results/run_provenance.md) and
[hIAPP production notes](../targets/hiapp/docs/PRODUCTION_ENVIRONMENT.md).
Input and output counts alone cannot distinguish failed tasks, missing
downloads, retries or intentional exclusions. The archive manifests contain
relative names and SHA256 values. Compressed files are below GitHub's
single-file limit, so the release uses standard Git for these archives.

## Verification

Run `python3 scripts/verify_recovered_screening.py` from the repository root.
It checks candidate references, archive members, source-row links and
checksums. The existing hIAPP CPU reproduction remains the entry point for the
9,806 → 904 → 42 → 12 screening workflow.
