# Contributing

Keep computational predictions, raw wet-lab data and interpreted results in
separate directories. Do not edit raw measurements in place. New analysis must
record its input checksum, software environment and parameter changes. Never
commit access tokens, private proxy addresses or user-specific cluster paths.

Before opening a pull request:

```bash
python -m compileall scripts
python -c "import ast,json,pathlib; [ast.parse(''.join(c['source'])) for p in pathlib.Path('targets/hiapp/notebooks').glob('*.ipynb') for c in json.loads(p.read_text())['cells'] if c['cell_type']=='code']"
for file in targets/hiapp/run.sh hpc/*.sh hpc/*.slurm; do bash -n "$file" || exit; done
bash targets/hiapp/run.sh --output-dir /tmp/hiapp-results
python scripts/validate_submission.py --output-dir /tmp/hiapp-results
jupyter nbconvert --to notebook --execute targets/hiapp/notebooks/01_reproduce_screening.ipynb \
  --output /tmp/01_reproduce_screening.executed.ipynb \
  --ExecutePreprocessor.timeout=600
```

Repository-facing prose, notebook text, user-visible code messages, and data
annotations must remain in English, except for the short Chinese navigation
in the root `README.md`. Scientific notation such as Greek letters may
be retained when it is part of a molecule or method name. Update
`targets/hiapp/data/designs/reference_inhibitor_sources.csv` whenever the reference set
changes, and ensure that every usable reference ID remains covered exactly.
