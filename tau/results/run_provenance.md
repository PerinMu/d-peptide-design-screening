# Tau campaign run provenance

This record summarizes metadata recovered by read-only inspection of the
Paracloud Tau run directories and scheduler records. Account names, hostnames,
absolute paths, raw scheduler logs, and model caches are intentionally omitted.

## BoltzGen PHF design

| Field | Recorded value |
|---|---|
| Run date | 2026-04-11 |
| Slurm job | `5151271` (`boltzgen_PHF`) |
| Scheduler state | `FAILED`, elapsed `01:21:02`; the log ends with a distributed PyTorch/NCCL TCPStore broken-pipe error |
| Allocated resources | `gpu` partition, 4 GPUs, 24 CPUs, 240 GB memory, 1 node |
| Software metadata | The referenced environment reports BoltzGen `0.2.0`; the run log invokes that environment's Python `3.12` executable |
| Container label in log | CUDA `12.4.1`, cuDNN development image, Ubuntu `22.04` |
| Design settings | `multiplicity=1000`, `diffusion_samples=10`, batch size `1`, 4 devices, `bf16-mixed`, 500 sampling steps, 3 recycling steps |
| Dataset snapshot | `c3d36fd276e9caf098c75d4113c6d5eb320b1a4c` |
| BoltzGen model snapshot | `c1be29e1f82ffcc72264f64b993c43fb4e0d17f0` |
| Retained output | 9,990 design CIF files in the public BoltzGen archive |

The run's public input is [`configs/boltzgen_input.yaml`](../configs/boltzgen_input.yaml).
The recovered configuration points to PDB 5O3L chain A, with binding residues
1–11. The output count is reported independently of the failed scheduler state;
the log does not establish that the configured campaign completed successfully.
Snapshot identifiers identify upstream artifacts but are not checkpoint file
SHA-256 hashes. The `0.2.0` package metadata came from the remote environment
after the run and was not preserved in a timestamped package freeze, so the
exact package version used on the run date is not independently verified. A
random seed was not recovered.

## Boltz-2 BG10000 scoring

| Field | Recorded value |
|---|---|
| Run date | 2026-04-11 |
| Representative Slurm array task | `282475_1` (`boltz_arr`) |
| Task state | `COMPLETED`, exit code `0`, elapsed `00:08:04`; log reports zero failed examples |
| Allocated resources | `gpu_4090` partition, 1 NVIDIA GeForce RTX 4090 GPU, 6 CPUs, 60 GB memory, 1 node |
| Runtime reported in task log | Python `3.10`; CUDA `12.8` |
| Campaign inputs and retained outputs | 8,964 YAML inputs; 8,927 score records and 8,927 collected model-0 CIFs |

The cited Slurm record is one representative array task, not a campaign-wide
completion record. Its log warns that the affinity ligand exceeded the model's
56-heavy-atom training range and that the affinity output may therefore be
inaccurate. The exact Boltz package version, checkpoint hash, and random seed
for this April task could not be established from the retained task log. The
separate hIAPP environment record is not used as a substitute for Tau-specific
version evidence.

## Reuse and limitations

The included input templates, score tables, sequence files, and CIF archives
are the public computational release. Raw logs, JSON sidecars, model weights,
and cluster-specific paths are not redistributed. The score values remain
model predictions for relative screening and are not experimental affinity or
activity measurements. For archive integrity checks, see
[`structures/SHA256SUMS.txt`](structures/SHA256SUMS.txt).
