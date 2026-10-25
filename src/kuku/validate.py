from datetime import datetime, date
from dataclasses import dataclass, asdict
import re

@dataclass
class ProductionRecord:
    date: date
    flock: str
    eggs: int
    birds: int
    recorded_by: str

    def laying_rate(self):
        if self.birds == 0:
            return 0.0
        return self.eggs / self.birds

def parse_date(text):
    if text is None or not str(text).strip():
        raise ValueError(f"date is not a real date: '{text}'")
    cleaned = str(text).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            dt = datetime.strptime(cleaned, fmt)
            return dt.date()
        except ValueError:
            continue
    raise ValueError(f"date is not a real date: '{text}'")

def parse_count(text, name):
    if text is None or str(text).strip() == "":
        raise ValueError(f"{name} is missing")
    cleaned = str(text).strip().replace(",", "")
    if not re.match(r"^-?\d+$", cleaned):
        raise ValueError(f"{name} is not a number: '{text}'")
    val = int(cleaned)
    if val < 0:
        raise ValueError(f"{name} is negative: {val}")
    return val

def parse_flock(text):
    if not text or not str(text).strip():
        raise ValueError("flock is missing")
    cleaned = str(text).strip().upper()
    if cleaned not in ("A", "B", "C"):
        raise ValueError(f"unknown flock: '{text}'")
    return cleaned

def validate_row(row):
    date_val = parse_date(row.get("date"))
    flock_val = parse_flock(row.get("flock"))
    eggs_val = parse_count(row.get("eggs"), "eggs")
    birds_val = parse_count(row.get("birds"), "birds")

    if birds_val == 0:
        raise ValueError("birds is zero")
    if eggs_val > birds_val:
        raise ValueError("more eggs than birds")

    return ProductionRecord(
        date=date_val,
        flock=flock_val,
        eggs=eggs_val,
        birds=birds_val,
        recorded_by=row.get("recorded_by", "").strip()
    )