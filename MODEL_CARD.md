# Model Card

## Scope and components

This repository uses pretrained models and project scripts for de novo D-peptide
design and multi-parameter hierarchical virtual screening. No model is trained
or fine-tuned here.

| Component | Role | Target evidence in this release |
|---|---|---|
| BoltzGen | Target-conditioned L-peptide sequence and structure generation | Tau and hIAPP |
| BoltzIF | Backbone-conditioned sequence redesign | hIAPP artifacts are present; Tau contribution is unverified |
| Boltz-2 | Complex prediction, confidence metrics, and affinity-head outputs | Tau and hIAPP score tables |
| Sequence-property code | Descriptors and composite ranking heuristics | Deterministic CPU workflow |

Run-specific parameters and recovered software details are in
[Computational Methods](docs/PAPER_METHODS.md),
[hIAPP production provenance](targets/hiapp/docs/PRODUCTION_ENVIRONMENT.md), and
[Tau run provenance](targets/tau/results/run_provenance.md).

## Prediction limits

Boltz-2 confidence values describe model predictions. Its affinity outputs are
not measured binding constants or inhibition data. The upstream affinity module
is intended primarily for protein–small-molecule complexes; its documentation
advises against ligands substantially larger than 56 heavy atoms and imposes a
128-atom input limit. The Tau run log flags a peptide beyond the 56-heavy-atom
training range. These peptide affinity outputs are therefore used only as
within-campaign ranking signals, with limited applicability to larger ligands.

BoltzGen produces L-peptide hypotheses. Reversing the sequence and encoding D
stereochemistry is a retro-inverso design convention; it does not establish
that the original backbone geometry or binding contacts are preserved.

Project physicochemical composites are transparent, sequence-based heuristics,
not calibrated or experimentally validated predictors. Screening percentiles,
consensus values, and priority tiers are relative ranking criteria. Predicted
structures, scores, and manual inspection do not establish binding,
aggregation inhibition, selectivity, toxicity, mechanism, or therapeutic value.

## Reproducibility limits

The hIAPP CPU screening can be recomputed from deposited score data. The final
12 were selected after manual inspection of a 42-candidate review pool, but the
original review sheet and candidate-level decisions were not retained. The
Tau `filter_passed` values were copied from a source workbook; the rule
producing value 4 is unavailable. Neither target's missing production random
seed was recovered. The recovered hIAPP Boltz-2 package version is an
environment snapshot, not a per-job log entry; the exact Tau Boltz-2 package
version and checkpoint hash are unknown.

No assay measurements or laboratory records are included in this computational
release. Their absence here does not establish whether experiments were
performed. See [release scope](docs/OPEN_SOURCE_SCOPE.md) and
[literature-data notes](docs/LITERATURE_PEPTIDE_DATA.md) for the distinction
between computational outputs and literature annotations.
