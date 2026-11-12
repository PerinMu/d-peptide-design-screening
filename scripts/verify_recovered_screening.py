#!/usr/bin/env python3
"""Verify the candidate crosswalk and recovered screening archive indices."""
from collections import Counter
import csv
from functools import lru_cache
import hashlib
from pathlib import Path, PurePosixPath
import re
import tarfile

ROOT = Path(__file__).resolve().parents[1]


@lru_cache
def rows(path):
    with (ROOT / path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def sha(data):
    return hashlib.sha256(data).hexdigest()


@lru_cache
def archive_hashes(path):
    hashes = {}
    with tarfile.open(ROOT / path, "r|gz") as archive:
        for member in archive:
            name = PurePosixPath(member.name)
            if (not member.isfile() or name.is_absolute() or ".." in name.parts
                    or str(name) in hashes):
                raise ValueError(f"Invalid archive member: {member.name}")
            hashes[str(name)] = sha(archive.extractfile(member).read())
    return hashes


def location_hash(location):
    path, _, member = location.partition("::")
    if member:
        return archive_hashes(path)[member]
    return sha((ROOT / path).read_bytes())


def check_target(target, source, counts):
    base = f"targets/{target}/results/recovered_screening"
    checksums = (ROOT / base / "SHA256SUMS.txt").read_text().splitlines()
    for entry in checksums:
        expected, name = entry.split("  ")
        assert location_hash(f"{base}/{name}") == expected, name
    indexed = set()
    by_batch = {}
    for index in sorted((ROOT / base).glob("*_index.csv")):
        group = index.name.removesuffix("_index.csv")
        data = rows(index)
        if group == "screening_inputs":
            content = archive_hashes(f"{base}/screening_inputs.tar.gz")
            assert {r["archive_member"]: r["released_sha256"] for r in data} == content
            continue
        for row in data:
            location = row["cif_location"]
            assert location and location_hash(location) == row["sha256"], row
            indexed.add(location)
        if target == "hiapp":
            by_batch[group] = {r["model0_basename"]: r["cif_location"] for r in data}
    links = rows(f"{base}/scored_sequence_links.csv")
    scored = rows(source)
    assert len(links) == len(scored)
    statuses = Counter()
    for line, (link, score) in enumerate(zip(links, scored), 2):
        assert int(link["scored_csv_line"]) == line
        expected_seq = score["D_sequence"].lower().removeprefix("d-") if target == "tau" else score["seq_rev"]
        expected_id = score["sample_id"] if target == "tau" else score["name"]
        assert (link["d_sequence"], link["source_id"]) == (expected_seq, expected_id)
        location = link["cif_location"]
        if location:
            assert location in indexed
            if target == "hiapp":
                batch = "batch" + link["prediction_batch"]
                raw = rows(f"{base}/{batch}_scores.csv")[int(link["raw_score_csv_line"]) - 2]
                assert raw["source_id"] == link["raw_prediction_id"]
                assert raw["confidence_json_basename"] == score["confidence_json_path"]
                assert by_batch[batch][raw["model0_basename"]] == location
                for key in raw:
                    if key.startswith(("confidence_score", "ptm", "iptm", "affinity_pred_value", "affinity_probability_binary")):
                        assert abs(float(raw[key]) - float(score[key])) < 1e-10
            statuses["linked"] += 1
        else:
            statuses["unlinked"] += 1
    assert (len(indexed), statuses["linked"], statuses["unlinked"]) == counts
    print(f"{target}: {len(indexed)} indexed structures, {statuses['linked']} linked and "
          f"{statuses['unlinked']} unlinked score rows")


def main():
    check_target("tau", "targets/tau/results/boltz2_merged_screening_scores.csv", (9473, 9473, 0))
    check_target("hiapp", "targets/hiapp/data/scored/merged_all_2_scored.csv", (9768, 9766, 118))
    crosswalk = rows("docs/CANDIDATE_ID_CROSSWALK.csv")
    assert Counter(row["target"] for row in crosswalk) == {"Tau": 10, "hIAPP": 12}
    assert len({(row["target"], row["manuscript_alias"]) for row in crosswalk}) == 22
    for row in crosswalk:
        if row["source_csv_line"]:
            source = rows(row["source_file"])[int(row["source_csv_line"]) - 2]
            key = "D_sequence" if row["target"] == "Tau" else "seq_rev"
            assert source[key].lower().removeprefix("d-") == row["d_sequence"]
            assert source[row["source_id_field"]] == row["source_id"]
            assert re.fullmatch(r"[a-f0-9]{64}", location_hash(row["cif_location"]))
        else:
            assert row["mapping_status"] == "score_source_unresolved" and not row["cif_location"]
    print("Candidate crosswalk: 22 rows verified")


if __name__ == "__main__":
    main()
