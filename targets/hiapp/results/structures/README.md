# hIAPP generation structure archives

These compressed archives preserve the main BoltzGen and BoltzIF CIF/NPZ
outputs used to build the released hIAPP sequence tables.

| Archive | Contents | CIF/NPZ pairs |
|---|---|---:|
| `boltzgen_designs_1990_raw.tar.gz` | BoltzGen-generated design structures and intermediate arrays | 1,990 |
| `boltzif_redesigns_7960_raw.tar.gz` | BoltzIF inverse-folded structures and intermediate arrays | 7,960 |

Each archive contains a `hparams.yaml` runtime-parameter record and retains the
original relative output filenames. No cluster logs, credentials, or absolute
workstation paths are included. The archives contain model outputs, not model
weights. Verify the files with `SHA256SUMS.txt` before extraction.

```bash
mkdir -p /tmp/hiapp_boltzgen /tmp/hiapp_boltzif
tar -xzf boltzgen_designs_1990_raw.tar.gz -C /tmp/hiapp_boltzgen
tar -xzf boltzif_redesigns_7960_raw.tar.gz -C /tmp/hiapp_boltzif
```
