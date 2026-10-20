import csv
from pathlib import Path 
RAW = Path("data/raw/eggs_raw.csv")
CLEAN = Path("data/clean/eggs_copy.csv")

print(f"RAW exists: {RAW.exists()}")

with open(RAW, mode="r", encoding= "utf-8") as f:
    text = f.read()

lines = text.splitlines()

print(f"\n--- Step 2: Text Reading ---")
print(f"Total lines: {len(lines)}")
print(f"First line (header): {lines[0]}")

with open(RAW, mode= "r", encoding= "utf-8") as f:
    reader= csv.DictReader(f)
    rows= list(reader)
    columns= reader.fieldnames
print(f"\n--- Step 3: CSV DictReader ---")
print(f"Total rows: {len(rows)}")
print(f"Columns: {columns}")

print("\nFirst three rows:")
for r in rows[:3]:
    print(r)

print(f"\Row 22 eggs: {rows[22]['eggs']}")

print(f"\n--- Step 4: Data Quality Checks ---")
blank_eggs = 0
blank_birds = 0
needs_trimming = 0
print(f"{'Line':<5} | {'Column':<6} | Value as typed")
print("-" * 35)
for i, r in enumerate(rows):
    line_num = i + 2
    
    for col in ["eggs", "birds"]:
        raw_val = r[col]
        clean_val = raw_val.strip()
        if clean_val == "":
            if col == "eggs":
                blank_eggs += 1
            elif col == "birds":
                blank_birds += 1
        if raw_val != clean_val and clean_val.isdigit():
            needs_trimming += 1
        if not clean_val.isdigit():
            print(f"{line_num:<5} | {col:<6} | {repr(raw_val)}")

print(f"\nSummary:")
print(f"Blank eggs: {blank_eggs}")
print(f"Blank birds: {blank_birds}")
print(f"Values needing trimming: {needs_trimming}")

print(f"\n--- Step 5: Text Column Profiling ---")

flock_counts = {}
recorder_counts = {}
dash_dates = 0
slash_dates = 0
slash_writers = {} 

for i, r in enumerate(rows):
    flock = r["flock"]
    recorder = r["recorded_by"]
    date = r["date"]
    line_num = i + 2

    if flock not in flock_counts:
        flock_counts[flock] = 0
    flock_counts[flock] += 1

    if flock in ['a', 'B ', 'c']:
        print(f"Odd flock {repr(flock)} found on line {line_num}")

    if recorder not in recorder_counts:
        recorder_counts[recorder] = 0
    recorder_counts[recorder] += 1

    if "-" in date:
        dash_dates += 1
    elif "/" in date:
        slash_dates += 1  
        if recorder not in slash_writers:
            slash_writers[recorder] = 0
        slash_writers[recorder] += 1

print("\nResults:")
flocks_str = ", ".join([f"{repr(k)} {v}" for k, v in flock_counts.items()])
recorders_str = ", ".join([f"{k} {v}" for k, v in recorder_counts.items()])

print(f"flock: {flocks_str}")
print(f"recorded_by: {recorders_str}")

slash_guy = list(slash_writers.keys())[0]
print(f"date: {dash_dates} as 2026-10-01, {slash_dates} as 01/10/2026, all of the slashes from {slash_guy}")

print(f"\n--- Step 6: Duplicates and Copy ---")
seen = set()
duplicates = 0

for i, r in enumerate(rows):
    line_num = i + 2
    row_tuple = tuple(r.values())
    
    if row_tuple in seen:
        print(f"Exact duplicate found on line {line_num}")
        duplicates += 1
    else:
        seen.add(row_tuple)

CLEAN.parent.mkdir(parents=True, exist_ok=True)

with open(CLEAN, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

with open(CLEAN, mode="r", encoding="utf-8") as f:
    clean_count = len(list(csv.DictReader(f)))

other_non_num_eggs = sum(1 for r in rows if not r["eggs"].strip().isdigit() and r["eggs"].strip() != "")
other_non_num_birds = sum(1 for r in rows if not r["birds"].strip().isdigit() and r["birds"].strip() != "")
odd_flocks = sum(1 for r in rows if r["flock"] not in ["A", "B", "C"])

print("\n--- Final Data Profile ---")
print(f"{'Check':<45} Result")
print("-" * 55)
print(f"{'Data rows':<45} {len(rows)}")
print(f"{'Blank eggs / blank birds':<45} {blank_eggs} / {blank_birds}")
print(f"{'Other non-numeric eggs / birds':<45} {other_non_num_eggs} / {other_non_num_birds}")
print(f"{'Eggs needing trimming':<45} {needs_trimming}")
print(f"{'Flock values that are not exactly A, B or C':<45} {odd_flocks}")
print(f"{'Dates in day/month/year format':<45} {slash_dates}")
print(f"{'Exact duplicate rows':<45} {duplicates}")
print(f"{'Rows written to the copy':<45} {clean_count}")

# ==========================================
# Step 7: Data Cleaning Rules (The Contract)
# ==========================================
# 1. Duplicates: Check the row tuple against a seen set; drop exact duplicates.
# 2. Date: Check for slashes (/). If found, split and rearrange DD/MM/YYYY into YYYY-MM-DD.
# 3. Flock: Trim spaces and make uppercase. If the result is not exactly 'A', 'B', or 'C', reject the row.
# 4. Eggs: Trim spaces. If blank, negative, or not a perfect digit string, reject the row.
# 5. Birds: Trim spaces. If blank, negative, or not a perfect digit string, reject the row.


# ==========================================
# Stretch Goal: Reusable Profiling Function
# ==========================================
print(f"\n--- Stretch Goal: Column Profiling ---")

def profile_column(rows, column):
    blanks = 0
    value_counts = {}
    
    for r in rows:
        val = r[column]
        
        if val.strip() == "":
            blanks += 1
            
        if val not in value_counts:
            value_counts[val] = 0
        value_counts[val] += 1
        
    distinct_count = len(value_counts)
    sorted_values = sorted(value_counts.items(), key=lambda item: item[1], reverse=True)
    top_5 = sorted_values[:5]
    
    return {
        "blanks": blanks,
        "distinct": distinct_count,
        "top_5": top_5
    }
for col in columns:
    profile = profile_column(rows, col)
    print(f"\nColumn: {col}")
    print(f"  Blanks: {profile['blanks']}")
    print(f"  Distinct values: {profile['distinct']}")
    print(f"  Top 5 (value, count): {profile['top_5']}")

