from datetime import datetime, date

VALID_FLOCKS = {"A", "B", "C"}

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

def parse_date(text):
    text = text.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"date is not a real date: {text!r}")

def parse_flock(text):
    clean_val = text.strip().upper()
    if clean_val not in VALID_FLOCKS:
        raise ValueError(f"unknown flock: '{text}'")
    return clean_val

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
    assert parse_date("2026-10-01") == date(2026, 10, 1)
    assert parse_date("01/10/2026") == date(2026, 10, 1)
    assert parse_date("10/14/2026") == date(2026, 10, 14)
    
    try:
        parse_date("2026-02-31")
    except ValueError as e:
        assert str(e) == "date is not a real date: '2026-02-31'"
        
    try:
        parse_date("1 Oct")
    except ValueError as e:
        assert str(e) == "date is not a real date: '1 Oct'"
        
    print("All date validation tests passed!")

if __name__ == "__main__":
    check()