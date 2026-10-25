from datetime import date
from src.kuku.validate import ProductionRecord
from src.kuku.transform import totals_by_flock, missing_days

ROWS = [
    ProductionRecord(flock="A", date=date(2026, 10, 1), eggs=970, birds=1200, recorded_by="Stevoh"),
    ProductionRecord(flock="A", date=date(2026, 10, 3), eggs=983, birds=1200, recorded_by="Stevoh"),
    ProductionRecord(flock="B", date=date(2026, 10, 1), eggs=641, birds=800, recorded_by="Stevoh"),
    ProductionRecord(flock="B", date=date(2026, 10, 2), eggs=617, birds=800, recorded_by="Stevoh"),
    ProductionRecord(flock="B", date=date(2026, 10, 3), eggs=654, birds=800, recorded_by="Stevoh"),
]

def test_totals_by_flock():
    assert totals_by_flock(ROWS, "eggs") == {"A": 1953, "B": 1912}

def test_missing_days_all():
    assert missing_days(ROWS) == [("A", date(2026, 10, 2))]

def test_missing_days_flock_b():
    rows_b = [r for r in ROWS if r.flock == "B"]
    assert missing_days(rows_b) == []