#!/usr/bin/env python3
"""Collect model_0 CIF files and write a manifest without overwriting outputs."""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


def collect_model0_cifs(outputs_dir: Path, destination: Path) -> int:
    if not outputs_dir.is_dir():
        raise FileNotFoundError(outputs_dir)
    source_root = outputs_dir.resolve()
    output_root = destination.resolve()
    if output_root == source_root or source_root in output_root.parents:
        raise ValueError("Destination must be outside the source output tree")
    destination.mkdir(parents=True, exist_ok=True)

    plan = []
    for task in sorted(x for x in outputs_dir.iterdir() if x.is_dir()):
        cifs = sorted(task.glob("**/*_model_0.cif"))
        for index, source in enumerate(cifs, 1):
            suffix = "" if len(cifs) == 1 else f"_{index}"
            name = f"{task.name}{suffix}_model_0.cif"
            plan.append((task.name, name, source))

    names = [name for _, name, _ in plan]
    if len(names) != len(set(names)):
        raise ValueError("Multiple source CIFs map to the same destination filename")
    collisions = [destination / name for name in names if (destination / name).exists()]
    manifest_path = destination / "manifest.tsv"
    if manifest_path.exists():
        collisions.append(manifest_path)
    if collisions:
        raise FileExistsError(f"Refusing to overwrite existing outputs: {collisions[:3]}")

    for _, name, source in plan:
        shutil.copy2(source, destination / name)
    rows = [{"task_dir": task, "copied_name": name,
             "source_cif_relative": source.relative_to(outputs_dir).as_posix()}
            for task, name, source in plan]
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["task_dir", "copied_name", "source_cif_relative"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("outputs_dir", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    count = collect_model0_cifs(args.outputs_dir, args.destination)
    print(f"Copied {count} model_0 structures to {args.destination}")


if __name__ == "__main__":
    main()

