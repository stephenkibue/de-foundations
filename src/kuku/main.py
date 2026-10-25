# Think Answer: When a module is executed directly via `python -m src.kuku.main`, Python sets its __name__ variable to "__main__" instead of its package module name (src.kuku.main).

import sys
from pathlib import Path
import logging
from collections import Counter
from src.kuku.validate import validate_row
from src.kuku.reader import read_csv, write_csv
from src.kuku.transform import missing_days, totals_by_flock

log = logging.getLogger(__name__)

RAW = Path("data") / "raw" / "eggs_raw.csv"
CLEAN_OUT = Path("data") / "clean" / "eggs_clean.csv"
REJECTS_OUT = Path("data") / "clean" / "eggs_rejects.csv"

def setup_logging():
    level = logging.DEBUG if "--debug" in sys.argv else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)-8s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("pipeline.log", mode="w")
        ]
    )

def main():
    setup_logging()
    clean = []
    rejects = []
    seen_pairs = set()
    reject_reasons = Counter()

    rows, raw_headers = read_csv(RAW)

    for i, row in enumerate(rows):
        line_num = i + 2
        try:
            clean_row = validate_row(row)
            pair = (clean_row["flock"], clean_row["date"])
            if pair in seen_pairs:
                raise ValueError(f"duplicate: flock {clean_row['flock']} on {clean_row['date']} already recorded")
            seen_pairs.add(pair)
            clean.append(clean_row)
            log.debug(f"Line {line_num} clean: {clean_row}")
        except ValueError as e:
            bad_row = row.copy()
            bad_row["line"] = line_num
            bad_row["reason"] = str(e)
            rejects.append(bad_row)
            log.warning(f"Line {line_num} rejected: {e}")
            
            reason_key = str(e).split(":")[0].strip()
            reject_reasons[reason_key] += 1

    log.info(f"Finished processing. Clean: {len(clean)}, Rejected: {len(rejects)}, Total: {len(rows)}")
    assert len(clean) + len(rejects) == len(rows)

    # Run missing days check
    missing_days(clean)

    # Calculate totals by flock
    flock_totals = totals_by_flock(clean)
    
    # Log summary statistics
    reasons_summary = ", ".join(f"{reason} {count}" for reason, count in reject_reasons.items())
    log.info(f"Reject reasons: {reasons_summary}")
    
    totals_str = ", ".join(f"{flock} {total:,}" for flock, total in sorted(flock_totals.items()))
    log.info(f"Eggs per flock: {totals_str}")

    # Write files
    write_csv(CLEAN_OUT, clean)
    
    reject_headers = ["line", "reason"] + list(raw_headers)
    write_csv(REJECTS_OUT, rejects, fieldnames=reject_headers)

if __name__ == "__main__":
    main()