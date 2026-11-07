# Model card

## Scope

This repository applies pretrained protein-design and structure-prediction
models to reverse-D peptide candidate generation. It does not train or
fine-tune these models. Target-specific inputs, parameters, score records, and
reproducibility limits are documented under [`targets/`](targets/).

## Computational components

| Component | Role in the workflow |
|---|---|
| BoltzGen | Target-conditioned peptide sequence and structure generation |
| BoltzIF | Backbone-conditioned sequence redesign where used |
| Reverse-D conversion | Sequence reversal and stereochemistry-aware SMILES generation |
| Boltz-2 | Complex prediction, confidence metrics, and affinity-head outputs |
| Sequence-property scoring | Transparent composition-based developability heuristics |
| Layered screening | Filtering, multi-metric prioritization, sequence diversity, and structure review |

The target-specific production settings and evidence are in the
[hIAPP model card](targets/hiapp/docs/MODEL_CARD.md) and the
[Tau run record](targets/tau/results/run_provenance.md).

## Interpretation

Boltz-2 affinity outputs are treated as relative ranking signals. Its affinity
module was not trained as a quantitative peptide-binding assay, and the Tau
run log flags at least one ligand beyond the 56-heavy-atom training range.
Project physicochemical scores are heuristics rather than calibrated
predictors. Predicted structures and scores do not establish binding,
aggregation inhibition, selectivity, toxicity, or therapeutic value.

BoltzGen generates L-amino-acid hypotheses before the project applies reverse-D
encoding. This transformation does not prove that the original backbone
geometry or interface contacts are retained. Experimental validation requires
separately controlled studies; experimental records and outcomes are outside
this repository.

## Target-specific evidence

- [hIAPP methods and production evidence](targets/hiapp/docs/METHODS.md)
- [Tau inputs and results](targets/tau/README.md)
- [Shared release scope and provenance](docs/OPEN_SOURCE_SCOPE.md)
