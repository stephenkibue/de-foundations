import csv
from pathlib import Path

RAW = Path("data") / "raw" / "eggs_raw.csv"
CLEAN_OUT = Path("data") / "clean" / "eggs_clean.csv"
REJECTS_OUT = Path("data") / "clean" / "eggs_rejects.csv"

def parse_count(text, name):
    text = text.strip().replace(",", "")
    
    if not text:
        raise ValueError(f"{name} is missing")
        
    try:
        val = int(text)
    except ValueError:
        raise ValueError(f"{name} is not a number: '{text}'")
        
    if val < 0:
        raise ValueError(f"{name} is negative: {val}")
        
    return val

def check():
    assert parse_count("970", "eggs") == 970
    assert parse_count(" 405 ", "eggs") == 405
    assert parse_count("1,010", "eggs") == 1010
    
    try:
        parse_count("", "birds")
    except ValueError as e:
        assert str(e) == "birds is missing"
        
    try:
        parse_count("n/a", "eggs")
    except ValueError as e:
        assert str(e) == "eggs is not a number: 'n/a'"
        
    try:
        parse_count("-40", "eggs")
    except ValueError as e:
        assert str(e) == "eggs is negative: -40"
        
    print("parse_count passed all tests!")

if __name__ == "__main__":
    check()

def parse_date(text):
    if text.count("-") == 2:
        return text
    elif text.count("/") == 2:
        parts = text.split("/")
        return f"{parts[2]}-{parts[1]}-{parts[0]}"
    else:
        raise ValueError(f"date is not in a known format: '{text}'")

def parse_flock(text):
    clean_val = text.strip().upper()
    if clean_val not in ["A", "B", "C"]:
        raise ValueError(f"unknown flock: '{text}'")
    return clean_val

def check():
    # Previous tests...
    assert parse_count("970", "eggs") == 970
    
    # parse_date tests
    assert parse_date("2026-10-01") == "2026-10-01"
    assert parse_date("01/10/2026") == "2026-10-01"
    
    try:
        parse_date("1 Oct")
    except ValueError as e:
        assert str(e) == "date is not in a known format: '1 Oct'"
        
    # parse_flock tests
    assert parse_flock("B ") == "B"
    assert parse_flock("c") == "C"
    
    try:
        parse_flock("D")
    except ValueError as e:
        assert str(e) == "unknown flock: 'D'"
        
    print("All tests passed perfectly!")

if __name__ == "__main__":
    check()

def validate_row(row):
    clean_date = parse_date(row["date"])
    clean_flock = parse_flock(row["flock"])
    clean_eggs = parse_count(row["eggs"], "eggs")
    clean_birds = parse_count(row["birds"], "birds")
    
    if clean_birds == 0:
        raise ValueError("birds cannot be zero")
        
    if clean_eggs > clean_birds:
        raise ValueError("eggs cannot exceed birds")
        
    return {
        "date": clean_date,
        "flock": clean_flock,
        "eggs": clean_eggs,
        "birds": clean_birds,
        "recorded_by": row["recorded_by"].strip()
    }

def check():
    # Previous tests...
    assert parse_count("970", "eggs") == 970
    assert parse_date("2026-10-01") == "2026-10-01"
    assert parse_flock("B ") == "B"
    
    # validate_row tests
    good_row = {
        "date": "01/10/2026", 
        "flock": " A ", 
        "eggs": "950", 
        "birds": "1,000", 
        "recorded_by": "Wanjiku"
    }
    expected = {
        "date": "2026-10-01", 
        "flock": "A", 
        "eggs": 950, 
        "birds": 1000, 
        "recorded_by": "Wanjiku"
    }
    assert validate_row(good_row) == expected
    
    bad_row_zero = good_row.copy()
    bad_row_zero["birds"] = "0"
    try:
        validate_row(bad_row_zero)
    except ValueError as e:
        assert str(e) == "birds cannot be zero"
        
    bad_row_excess = good_row.copy()
    bad_row_excess["eggs"] = "1050"
    try:
        validate_row(bad_row_excess)
    except ValueError as e:
        assert str(e) == "eggs cannot exceed birds"

    print("All tests passed perfectly!")

if __name__ == "__main__":
    check()

import csv
from pathlib import Path

# Paths
RAW = Path("data") / "raw" / "eggs_raw.csv"

def main():
    clean = []
    rejects = []
    seen_pairs = set()

    with open(RAW, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print("\n=== PROCESSING ROWS ===")
    
    for i, row in enumerate(rows):
        line_num = i + 2
        
        # The Trap: The try block must be INSIDE the loop so the loop keeps running!
        try:
            clean_row = validate_row(row)
            
            # Duplicate check using the clean flock and clean date
            pair = (clean_row["flock"], clean_row["date"])
            if pair in seen_pairs:
                raise ValueError("duplicate record for this flock and date")
                
            seen_pairs.add(pair)
            clean.append(clean_row)
            
        except ValueError as e:
            # We copy the original raw dictionary so we don't mutate the list in place
            bad_row = row.copy()
            bad_row["line"] = line_num
            bad_row["reason"] = str(e)
            rejects.append(bad_row)

    total_rows = len(rows)
    print(f"Total raw rows read: {total_rows}")
    print(f"Clean rows: {len(clean)}")
    print(f"Rejected rows: {len(rejects)}")
    
    # Assert that no rows disappeared into thin air
    assert len(clean) + len(rejects) == total_rows

    return clean, rejects

if __name__ == "__main__":
    check()
    clean_data, reject_data = main()

def main():
    clean = []
    rejects = []
    seen_pairs = set()

    with open(RAW, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        # Save the original headers so we can append them to the reject file
        raw_headers = reader.fieldnames

    print("\n=== PROCESSING ROWS ===")
    
    for i, row in enumerate(rows):
        line_num = i + 2
        
        try:
            clean_row = validate_row(row)
            
            pair = (clean_row["flock"], clean_row["date"])
            if pair in seen_pairs:
                # Updated to match the exact required error message
                raise ValueError(f"duplicate: flock {clean_row['flock']} on {clean_row['date']} already recorded")
                
            seen_pairs.add(pair)
            clean.append(clean_row)
            
        except ValueError as e:
            bad_row = row.copy()
            bad_row["line"] = line_num
            bad_row["reason"] = str(e)
            rejects.append(bad_row)

    total_rows = len(rows)
    print(f"Total raw rows read: {total_rows}")
    print(f"Clean rows: {len(clean)}")
    print(f"Rejected rows: {len(rejects)}")
    assert len(clean) + len(rejects) == total_rows

    # --- Step 5: Write the Files ---
    CLEAN_OUT.parent.mkdir(parents=True, exist_ok=True)
    
    # Write Clean File
    if clean:
        with open(CLEAN_OUT, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=clean[0].keys())
            writer.writeheader()
            writer.writerows(clean)

    # Write Rejects File
    if rejects:
        reject_headers = ["line", "reason"] + raw_headers
        with open(REJECTS_OUT, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=reject_headers)
            writer.writeheader()
            writer.writerows(rejects)
            
    print("\nFiles written successfully!")
    return clean, rejects

def classify(rate):
    return "good" if rate >= 0.8 else "watch"

def prove_it(clean_rows):
    print("\n=== STEP 6: PROVE IT ===")
    flock_stats = {}
    total_eggs = 0
    
    for row in clean_rows:
        flock = row["flock"]
        if flock not in flock_stats:
            flock_stats[flock] = {"rows": 0, "eggs": 0, "birds": 0}
            
        flock_stats[flock]["rows"] += 1
        flock_stats[flock]["eggs"] += row["eggs"]
        flock_stats[flock]["birds"] += row["birds"]
        total_eggs += row["eggs"]
        
    print(f"{'Flock':<5} | {'Clean rows':<10} | {'Eggs':<6} | {'Bird-days':<9} | {'Laying rate':<11} | Label")
    print("-" * 65)
    
    for flock in sorted(flock_stats.keys()):
        stats = flock_stats[flock]
        rate = stats["eggs"] / stats["birds"]
        label = classify(rate)
        print(f"{flock:<5} | {stats['rows']:<10} | {stats['eggs']:<6,} | {stats['birds']:<9,} | {rate*100:>10.1f}% | {label}")
        
    print(f"{'All':<5} | {len(clean_rows):<10} | {total_eggs:<6,}")