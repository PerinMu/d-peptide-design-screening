#!/usr/bin/env python3
"""Append a lower-case reverse-sequence D-peptide representation to a CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CANONICAL_AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWY")


def reverse_d_sequence(sequence: object) -> str:
    """Return the lowercase reverse-D sequence for a canonical L sequence."""
    normalized = "".join(str(sequence).split()).upper()
    if not normalized:
        raise ValueError("Empty sequence")
    unknown = set(normalized) - CANONICAL_AMINO_ACIDS
    if unknown:
        raise ValueError(f"Noncanonical amino-acid symbols: {''.join(sorted(unknown))}")
    return normalized[::-1].lower()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sequence-column", default="sequence")
    parser.add_argument("--output-column", default="seq_rev")
    args = parser.parse_args()

    with args.input.open(encoding="utf-8-sig", newline="") as src:
        reader = csv.DictReader(src)
        if args.sequence_column not in (reader.fieldnames or []):
            raise ValueError(f"Missing sequence column {args.sequence_column!r}")
        fields = list(reader.fieldnames or [])
        if args.output_column not in fields:
            fields.append(args.output_column)
        rows = []
        for row_number, row in enumerate(reader, 2):
            try:
                row[args.output_column] = reverse_d_sequence(row[args.sequence_column])
            except ValueError as exc:
                raise ValueError(f"{exc} at CSV row {row_number}") from exc
            rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} reverse D-peptide encodings to {args.output}")


if __name__ == "__main__":
    main()

