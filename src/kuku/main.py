import sys
import logging
from dataclasses import asdict
from pathlib import Path

from kuku.reader import read_csv, write_csv
from kuku.validate import validate_row
from kuku.transform import missing_days, totals_by_flock

def setup_logging():
    debug_mode = "--debug" in sys.argv
    level = logging.DEBUG if debug_mode else logging.INFO
    
    log_dir = Path("data")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "pipeline.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8")
        ]
    )

def run(raw_path: Path, out_dir: Path):
    log = logging.getLogger(__name__)
    out_dir.mkdir(parents=True, exist_ok=True)
    clean_path = out_dir / "clean_production.csv"

    try:
        rows = read_csv(raw_path)
    except Exception as e:
        log.error(f"Failed to read raw CSV: {e}")
        return 0, []

    clean_rows = []
    rejected = []
    seen = set()

    for row in rows:
        try:
            validated = validate_row(row)
            dup_key = (validated.date, validated.flock)
            if dup_key in seen:
                raise ValueError(f"duplicate record for flock {validated.flock} on {validated.date}")
            seen.add(dup_key)
            clean_rows.append(validated)
        except ValueError as e:
            rejected.append({"row": row, "reason": str(e)})
            log.warning(f"Skipping invalid row {row}: {e}")

    missing = missing_days(clean_rows)
    egg_totals = totals_by_flock(clean_rows, "eggs")
    bird_totals = totals_by_flock(clean_rows, "birds")

    log.info(f"Egg totals by flock: {dict(egg_totals)}")
    log.info(f"Bird totals by flock: {dict(bird_totals)}")
    log.info(f"Missing days detected: {len(missing)}")

    try:
        dict_rows = [asdict(r) for r in clean_rows]
        write_csv(clean_path, dict_rows)
        log.info(f"Successfully wrote {len(dict_rows)} clean rows to {clean_path}")
    except Exception as e:
        log.error(f"Failed to write clean CSV: {e}")

    return len(clean_rows), rejected

def main():
    setup_logging()
    raw_path = Path("data/raw_production.csv")
    out_dir = Path("data")
    clean_count, rejected = run(raw_path, out_dir)
    print(f"Pipeline complete. Clean: {clean_count}, Rejected: {len(rejected)}")

if __name__ == "__main__":
    main()