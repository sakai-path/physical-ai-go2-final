#!/usr/bin/env python3
"""Verify the recorded Phase56 Genesis evaluation ZIP without rerunning physics."""
import argparse
import csv
import io
import zipfile
from collections import Counter

def read_csv(z, name):
    matches = [n for n in z.namelist() if n.endswith("/" + name) or n == name]
    if len(matches) != 1:
        raise ValueError(f"Expected one {name}, found {len(matches)}")
    with z.open(matches[0]) as f:
        return list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")))

def verify(path):
    with zipfile.ZipFile(path) as z:
        trajectory = read_csv(z, "trajectory.csv")
        events = read_csv(z, "tag_events.csv")
    counts = Counter(row["robot"] for row in trajectory)
    steps = {robot: {int(row["step"]) for row in trajectory if row["robot"] == robot} for robot in counts}
    print("Robot row counts:", dict(counts))
    print("Unique steps:", {k: len(v) for k, v in steps.items()})
    print("Role switches:", len(events))
    print("Duration from steps:", max(map(len, steps.values())) * 0.02, "s")
    assert len(counts) == 2, "Expected two robots"
    assert all(len(v) == 3000 for v in steps.values()), "Not a 3000-step run"
    assert all(len(v) == 3000 for v in counts.values()), "Duplicate or missing rows"
    assert len(events) == 8, "Role-switch count differs from recorded Phase56 result"
    print("PASS: Phase56 60s / 8 switches structural verification")
    print("Note: this checks CSV structure, not model correctness or simulation reproducibility.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_file", help="Phase56 evaluation results ZIP")
    verify(parser.parse_args().zip_file)
