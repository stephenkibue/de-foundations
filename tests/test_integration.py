import csv
from pathlib import Path
from src.kuku.main import run

def test_pipeline_integration(tmp_path):
    raw_csv = tmp_path / "raw_production.csv"
    
    # 4 rows: 2 valid, 1 duplicate, 1 bad row (negative eggs)
    data = [
        ["date", "flock", "eggs", "birds", "recorded_by"],
        ["2026-10-01", "A", "970", "1200", "Wanjiku"],
        ["2026-10-02", "A", "980", "1200", "Wanjiku"],
        ["2026-10-01", "A", "950", "1200", "Wanjiku"],  # Duplicate
        ["2026-10-03", "A", "-50", "1200", "Wanjiku"],   # Bad row
    ]
    
    with open(raw_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)
        
    clean_count, rejected = run(raw_csv, tmp_path)
    
    assert clean_count == 2
    assert len(rejected) == 2
    
    reasons = [r["reason"] for r in rejected]
    assert any("duplicate record" in r for r in reasons)
    assert any("eggs is negative" in r for r in reasons)