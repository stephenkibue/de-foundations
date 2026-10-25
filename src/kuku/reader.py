import csv
from pathlib import Path
import logging

log = logging.getLogger(__name__)

def read_csv(filepath):
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames
    log.info(f"Read {len(rows)} rows from {filepath}.")
    return rows, headers

def write_csv(filepath, rows, fieldnames=None):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    if fieldnames is None:
        fieldnames = rows[0].keys()
    with open(filepath, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    log.info(f"Wrote {len(rows)} rows to {filepath}.")