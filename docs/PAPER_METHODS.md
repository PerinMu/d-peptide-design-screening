# Computational Methods

This document describes the computational workflow represented by the released
inputs, scripts, score tables, and run records. It does not describe wet-lab
experiments; no assay measurements or laboratory records are included here.

## Target preparation

Tau designs used chain A of the paired-helical-filament structure PDB 5O3L. The
17-residue chain sequence in the design input is `VQIVYKPVDLSKVTSKC`, with
residues 1–11 (`VQIVYKPVDLS`; PHF6, corresponding to Tau 306–316) specified as
the binding region. The BoltzGen input restricted peptide lengths to 6–12
residues. The Boltz-2 template used the same target chain and a fixed-template
restraint (`force: true`, threshold 0.1 Å).

hIAPP designs used the patient-derived fibril structure PDB 9ULZ, chain D. The
BoltzGen input retained chain-D residues 19–37 and specified residues 21–37 as
the binding region. Boltz-2 inputs represented the target by the 20-residue
sequence `HSSNNFGAILSSTNVGSNTY`, with a fixed 9ULZ template (`force: true`,
threshold 0.1 Å). The 6Y1A comparison described in the manuscript draft is not
part of the deposited design or screening workflow.

## BoltzGen generation and BoltzIF redesign

BoltzGen [11] generated L-amino-acid sequence–structure hypotheses using the
`peptide-anything` design protocol. The hIAPP campaign requested 2,000 designs
with diffusion batch size 10; 1,990 paired CIF/NPZ outputs were retained and
the extracted design table contained 1,956 unique sequences. BoltzIF redesign
[11] was run for hIAPP at four sequences per backbone, sampling temperature 0.2,
with cysteine excluded. It yielded 7,960 raw outputs and 7,854 unique
sequences. The merged table contains 9,810 rows and 9,808 distinct sequences;
two rows labeled `design; IF_02` were excluded from the recorded 9,806-row
analysis pool, which uses the exact source labels `design` and `IF_02`.

The Tau BoltzGen input records `multiplicity=1000`, 10 diffusion samples, batch
size 1, 500 sampling steps, and three recycling steps. Its scheduler job ended
in a failed state after 9,990 CIF files had been retained; the extracted
sequence table contains 8,964 unique L-sequences. The released Tau screening
table has 9,473 score records across five batches, 9,348 distinct D-sequences,
and 9,454 distinct sample identifiers. The 9,473 value is a record count, not
an independent-sequence count. No Tau BoltzIF input, output table, or structure
archive is present in this release, so a BoltzIF contribution to the Tau
records cannot be established from the repository.

## Retro-inverso conversion and stereochemical encoding

For an input L-sequence `s`, following the retro-inverso design convention
[7], the project defines the reverse-D sequence as `lowercase(reverse(s))`.
This is a sequence convention; lower case alone does not encode stereochemistry.
The resulting sequence is converted to a linear
SMILES with explicit L/D stereochemical markers at every chiral center. Ile and
Thr beta-carbon stereocentres are encoded separately; glycine remains achiral.
The generated SMILES use a free N-terminus and a free C-terminal carboxylate
representation. This retro-inverso transformation is a design hypothesis and
does not guarantee that a D-peptide preserves the original L-backbone geometry
or contacts.

## Boltz-2 complex prediction

The released complex predictions use Boltz-2 [13], with target structures supplied
as templates and the reverse-D peptide supplied as a stereochemical ligand
SMILES. hIAPP prediction inputs use chain A for the target and chain X for the
peptide. The deposited candidate structures are model-0 mmCIF files. The
recovered hIAPP production configuration records three diffusion samples,
potentials, and the MSA server option; the server version and returned
alignments were not retained. Tau's main campaign contains 8,927 Boltz-2 score
records and model-0 CIFs for the `BG_10000` batch. Separate 2026-10-31 Tau and
hIAPP target-context predictions are archived independently from the main
screening runs.

Boltz-2 reports structural-confidence indicators and three affinity heads.
These are model outputs, not measured binding constants or inhibition data. The
upstream Boltz documentation describes the affinity module for protein–small
molecule prediction, advises against ligands substantially larger than 56
atoms, and sets a 128-atom input limit. The Tau task log records a warning that
its peptide ligand exceeded the 56-heavy-atom training range. Because the
screened ligands are peptides, affinity-head values are used only as
within-campaign ranking signals; their applicability to these larger ligands
is limited. See the [official Boltz prediction guide](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md).

## Physicochemical descriptor calculation

The CPU scripts calculate sequence-level molecular mass (residue masses plus
terminal water), estimated net charge at pH 7, estimated isoelectric point,
Kyte–Doolittle mean hydropathy [14], polar/hydrophobic/aromatic fractions, longest
hydrophobic run, and sequence-liability counts. Five deterministic
0–100 heuristic scores summarize solubility tendency, aggregation risk,
passive-permeability tendency, sequence stability, and peptide drug-likeness.
Their formulae, residue constants, and assumptions are listed in
[`targets/hiapp/docs/PHYSICOCHEMICAL.md`](../targets/hiapp/docs/PHYSICOCHEMICAL.md).
They are study-specific heuristics, not validated property predictions or
measurements.

## Literature-derived peptide reference set

Literature-reported peptide records were curated from the populated Tau
`D-peptides` worksheet and hIAPP inhibitor-information worksheet. The release
contains 62 Tau records (43 source-labeled D-peptides and 19 L-peptides,
representing 57 sequence notations) and 76 hIAPP records (76 distinct sequence
notations). Records remain at source-row granularity, so repeated Tau sequences
reported against different constructs are traceable. The tables retain
negative controls, non-inhibitory or mixed-evidence records, and modified
peptide analogues. English summaries, source metric strings, and citations are
provided in [`docs/LITERATURE_PEPTIDE_DATA.md`](LITERATURE_PEPTIDE_DATA.md).

The source spreadsheets label the measurement field as IC50 (µM), but its cells
also contain Kd, lag time, t50, inhibition percentages, ThT summaries, and
non-numeric entries. Measurements were retained as text rather than
harmonized across studies. These are literature annotations, not measurements
from this project or a systematic review. The hIAPP bibliography resolves 76
source entries to 37 unique sources. Because the source workbook supplied no
SMILES, the descriptive hIAPP literature table adds RDKit 2025.9.2 isomeric
SMILES computed from its retained sequence and modification annotations; its
row-level notes expose structural assumptions. The 76 hIAPP entries used as
the P3 descriptor reference set remain in
[`reference_inhibitors_smiles.csv`](../targets/hiapp/data/designs/reference_inhibitors_smiles.csv);
the descriptive table's generated SMILES do not replace those historical
inputs or change screening scores. `reference_entry_id` preserves the source
workbook crosswalk and `citation_id` joins to the normalized bibliography.

## Hierarchical screening and candidate selection

The hIAPP analysis pool contains 9,806 design/IF rows. For each of three
affinity heads, the implementation averages the lower-is-better percentile
rank of `affinity_pred_value` and the higher-is-better percentile rank of
`affinity_probability_binary`; ties use average ranks. For head `h`, define
`H_h = [R−(pred_h) + R+(prob_h)] / 2`, affinity consensus `A = median(H_0,
H_1, H_2)`, and disagreement `ΔH = max(H_h) − min(H_h)`. All percentiles are
calculated within the 9,806-row analysis pool.

The structure bottleneck is `B = min(pTM, ipTM)`. Structure quality is
`S = 0.60 R+(B) + 0.20 R+(confidence_score) + 0.20 R−(complex_pde)`. The
developability score is the mean of the directionally aligned percentile ranks
for solubility tendency, aggregation risk, sequence stability, drug-likeness,
and liability count. The overall score is `O = 0.55 A + 0.30 S + 0.15 D`.

The main hard gate required all six affinity values, `B ≥ 0.65`, solubility
tendency ≥ 40, and aggregation risk ≤ 65. It retained 904 candidates. P1
required `B ≥ 0.70` and `ΔH ≤ 0.35`; 12 candidates were greedily ranked by `O`,
preferring normalized Levenshtein similarity below 0.85 to already selected
sequences. P2 selected the next 12 by `O` with the same diversity preference.
For P3, novelty was the median absolute distance from the 76-entry reference
set median, scaled by its interquartile range, across aromatic fraction,
estimated charge, estimated pI, and GRAVY. Remaining candidates entered P3 if
`ΔH > 0.35` or novelty was at or above the hard-gated pool's 75th percentile.
The exploration score was `E = 0.75 O + 0.25 R+(novelty)`; eight candidates
were selected.

P4 excluded P1–P3 candidates and required length 11 or 12, `B ≥ 0.75`,
solubility tendency ≥ 40, aggregation risk ≤ 65, and complete inputs for the
P4 ranking score. The structure-emphasis score was `S_P4 = 0.70 R+(B) + 0.20
R+(mean(pTM, ipTM)) + 0.10 R+(confidence_score)`. The P4 score was
`O_P4 = 0.50 S_P4 + 0.35 A + 0.15 D`. Thirty candidates passed; the top ten
were included in the structural-review pool. The P1–P3 and P4 review pools are
disjoint and contain 42 sequences in total. The automated output comprised 12
P1, 12 P2, 8 P3, and 10 P4 review candidates.

Manual structure review considered occupancy of the intended target region,
interface contacts, clashes, chain continuity, sequence redundancy, and
synthetic tractability. The recorded hIAPP shortlist contains 12 candidates
(P1 × 8, P2 × 1, P3 × 1, P4 × 2). The original 42-row review sheet and
candidate-level inclusion/exclusion reasons were not retained, so the manual
decisions cannot be fully reconstructed. Tau's `filter_passed` field was
copied from its source workbook; the rule definitions were not recovered. The
123 records with value 4 comprise 106 distinct D-sequences and must not be
interpreted as 123 independent sequences or as a fully reproducible threshold
without the missing rule provenance.

## Software, hardware, and reproducibility

The recovered hIAPP environments report BoltzGen/BoltzIF `boltzgen` 0.2.0 and
Boltz-2 `boltz` 2.2.1. The BoltzGen version is supported by a historical job
log; Boltz-2 2.2.1 is a recovered post-campaign environment because the
prediction logs did not print the package version. BoltzGen/BoltzIF used
Python 3.12 and PyTorch 2.9.1+cu128; Boltz-2 used Python 3.10 and PyTorch
2.10.0+cu128. BoltzGen and BoltzIF jobs requested four GPUs, 24 CPUs, and
240 GB RAM. Boltz-2 jobs used one RTX 4090, six CPUs, and 60 GB RAM, with up to
eight dispatched concurrently. The exact GPU model for historical BoltzGen
jobs is unavailable.

Tau's April 2026 BoltzGen record reports Python 3.12, CUDA 12.4.1 in the
container, four GPUs, 24 CPUs, and 240 GB RAM; the recovered environment
metadata reports BoltzGen 0.2.0, but the exact run-date package version is not
independently established. The job ended as `FAILED` after producing retained
structures. A representative Tau Boltz-2 task reports
Python 3.10, CUDA 12.8, one RTX 4090, six CPUs, and 60 GB RAM. Its exact Boltz
package version, checkpoint hash, and random seed were not recovered. No
production random seed was found for either target.

The deterministic hIAPP CPU reproduction uses the package pins in
[`targets/hiapp/requirements.txt`](../targets/hiapp/requirements.txt). Run
`bash targets/hiapp/run.sh --output-dir /tmp/dpeptide-reproduction`, then
`python scripts/validate_submission.py --output-dir /tmp/dpeptide-reproduction`.
This verifies the saved 9,806 → 904 → 42 → 12 screening sequence and candidate
crosswalks without rerunning GPU inference. Reproduction of neural generation
or prediction requires the upstream model assets and environments; random
seeds, the MSA service-side version, and some exact production package
versions were not retained. See the target-specific
[`hIAPP provenance`](../targets/hiapp/docs/PRODUCTION_ENVIRONMENT.md) and
[`Tau run record`](../targets/tau/results/run_provenance.md).

### Release audit notes

The manuscript draft uses “Boltz-2x,” but released configurations, predictions,
and score tables identify Boltz-2; the authors have confirmed that Boltz-2 was
used. No separate Boltz-2x implementation or the described cross-model
stereochemistry benchmark is present in this repository. The draft's ROC
analysis is also not represented by code or results here; the released
reference set is documented as a descriptor-space source for P3 novelty, not as
a labeled ROC benchmark. The draft's Tau claim that 9,473 candidates were
generated by BoltzGen and BoltzIF is not supported by the deposited Tau files.
The manuscript aliases KV-12, FI-11, and LG-11 have no crosswalk to the released
candidate names or sequence/SMILES tables. These claims require author-side
correction or additional source records before submission.
