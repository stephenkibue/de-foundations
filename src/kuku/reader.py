import csv
from pathlib import Path

def read_csv(path: Path):
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(path: Path, rows):
    if not rows:
        return
    fieldnames = list(rows[0].keys()) if isinstance(rows[0], dict) else list(rows[0].__dict__.keys())
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)