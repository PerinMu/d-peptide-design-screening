# De novo D-peptide design and multidimensional virtual screening

This repository documents a computational workflow for reverse-D peptide
candidate generation and prioritization. It combines target-conditioned
design, sequence redesign, stereochemistry-aware encoding, complex prediction,
sequence-property assessment, and layered candidate screening.

The framework is evaluated in two parallel target case studies: human islet
amyloid polypeptide (hIAPP) and Tau PHF6. Each target has its own structures,
inputs, scores, and run record. Target-specific scores are not directly
comparable. The release contains computational materials only; it excludes
laboratory records and measured assay outcomes.

## Workflow

```text
Target structure and site
  → BoltzGen design / BoltzIF sequence redesign
  → reverse-D sequence and stereochemical SMILES
  → Boltz-2 complex prediction
  → confidence, affinity-head, and sequence-property assessment
  → filtering, diversity prioritization, and structure review
```

The exact stages and filters differ between the two case studies. Boltz-2
affinity outputs and project physicochemical scores are relative
prioritization signals, not measured binding or inhibition values. See the
[model card](MODEL_CARD.md) and [release scope](docs/OPEN_SOURCE_SCOPE.md) for
interpretation and provenance limits.

## Target case studies

| Target | Template | Released results |
|---|---|---|
| hIAPP | [PDB 9ULZ](https://doi.org/10.2210/pdb9ULZ/pdb) | 9,806 ranked design/sequence-redesign records, layered screening tables, and 12 manually reviewed computational candidates. See [the hIAPP case study](targets/hiapp/README.md). |
| Tau PHF6 | [PDB 5O3L](https://doi.org/10.2210/pdb5O3L/pdb) | 9,473 merged screening records and compressed BoltzGen/Boltz-2 structure collections. See [the Tau case study](targets/tau/README.md). |

## Reproduce the saved hIAPP screening

The hIAPP CPU workflow recomputes the published ranking from the included score
table. It does not rerun the GPU models or automatically choose the manually
reviewed final set.

```bash
git clone https://github.com/PerinMu/d-peptide-design-screening.git
cd d-peptide-design-screening
conda env create -f targets/hiapp/environment.yml
conda activate dpeptide-screening
bash targets/hiapp/run.sh --output-dir /tmp/hiapp-screening
python scripts/validate_submission.py --output-dir /tmp/hiapp-screening
```

See [the hIAPP README](targets/hiapp/README.md) for data, candidate counts,
models, and target-specific reproduction notes. The Tau README describes its
inputs, released score tables, structures, and recovered run provenance.

## Repository layout

| Path | Contents |
|---|---|
| `targets/hiapp/` | hIAPP inputs, screening data, results, notebooks, and environment records |
| `targets/tau/` | Tau inputs, reference peptides, scores, structures, and run provenance |
| `scripts/` | Shared sequence, model-input, collection, scoring, and release utilities |
| `hpc/` | Slurm templates and provenance collectors; configure paths for your cluster |
| `docs/` | Shared references and release-scope notes |

## Citation and license

See [CITATION.cff](CITATION.cff) and [References](docs/REFERENCES.md). Repository
code is available under the [MIT License](LICENSE); upstream models, structures,
and literature data retain their own terms.
