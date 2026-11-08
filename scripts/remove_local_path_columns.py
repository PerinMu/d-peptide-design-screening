#!/usr/bin/env python3
"""Write a public CSV copy without machine-local path columns."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()
    if args.input_csv.resolve() == args.output_csv.resolve():
        raise ValueError("Input and output must differ; write the sanitized copy to a new path")

    with args.input_csv.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames or []
        public_fields = [name for name in fields if not name.lower().endswith("_path")]
        if not public_fields:
            raise ValueError("Input CSV has no fields after removing path columns")
        rows = list(reader)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=public_fields)
        writer.writeheader()
        writer.writerows(rows)

    removed = [name for name in fields if name not in public_fields]
    print(f"Wrote {len(rows)} rows to {args.output_csv}")
    print(f"Removed columns: {', '.join(removed) if removed else 'none'}")


if __name__ == "__main__":
    main()
