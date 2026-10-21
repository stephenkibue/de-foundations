import json
import csv
from pathlib import Path

RAW = Path("data") / "raw" / "farm.json"
OUT = Path("data") / "clean" / "farm_records.csv"

with open(RAW, mode="r", encoding="utf-8") as f:
    data = json.load(f)

print("\n=== FARM INFO ===")
print(f"Name: {data['farm']['name']}")
print(f"County: {data['farm']['county']}")

print("\n=== FLOCK SUMMARY ===")
print(f"{'Flock':<6} | {'Breed':<10} | {'House':<6} | Records")
print("-" * 40)

all_dates = set()
c_dates = set()

for flock in data["flocks"]:
    print(f"{flock['id']:<6} | {flock['breed']:<10} | {flock['house']:<6} | {len(flock['records'])}")
    
    for record in flock["records"]:
        all_dates.add(record["date"])
        if flock["id"] == "C":
            c_dates.add(record["date"])

print("\n=== DATA QUALITY CHECK ===")
missing_from_c = all_dates - c_dates
print(f"Missing date(s) for Flock C: {', '.join(missing_from_c)}")
print("\n=== FLATTENING RECORDS ===")
rows = []

for flock in data["flocks"]:
    flock_id = flock["id"]
    breed = flock["breed"]
    house = flock["house"]
    
    for record in flock["records"]:
        row = {
            "flock": flock_id,
            "breed": breed,
            "house": house,
            "date": record["date"],
            "eggs": record["eggs"],
            "birds": record["birds"],
            "feed_kg": record.get("feed_kg"),
            "notes": record.get("notes")
        }
        rows.append(row)

print(f"\nTotal flattened rows: {len(rows)}")
print(f"First row: {rows[0]}")
print(f"Last row: {rows[-1]}")

OUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUT, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

with open(OUT, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    csv_rows = list(reader)
    csv_cols = reader.fieldnames

print("\n=== CSV VERIFICATION ===")
print(f"Total rows read: {len(csv_rows)}")
print(f"Columns: {csv_cols}")

print("\n=== FARM PERFORMANCE PROOF ===")

def classify(rate):
    return "good" if rate >= 0.8 else "watch"

flock_stats = {}
farm_eggs = 0
farm_feed = 0
feed_records = 0

for row in rows:
    flock = row["flock"]
    if flock not in flock_stats:
        flock_stats[flock] = {"eggs": 0, "birds": 0}
        
    # Aggregate per flock
    flock_stats[flock]["eggs"] += row["eggs"]
    flock_stats[flock]["birds"] += row["birds"]
    
    # Aggregate for the farm
    farm_eggs += row["eggs"]
    
    # Safely aggregate feed, ignoring None values
    if row["feed_kg"] is not None:
        farm_feed += row["feed_kg"]
        feed_records += 1

print(f"{'Flock':<6} | {'Eggs':<6} | {'Bird-days':<10} | {'Rate':<6} | Label")
print("-" * 45)

for flock in sorted(flock_stats.keys()):
    stats = flock_stats[flock]
    rate = stats["eggs"] / stats["birds"]
    label = classify(rate)
    print(f"{flock:<6} | {stats['eggs']:<6,} | {stats['birds']:<10,} | {rate*100:>4.1f}% | {label}")

print(f"\nFarm Eggs: {farm_eggs:,}")
print(f"Total feed: {farm_feed:,.1f} kg, from {feed_records} of {len(rows)} records.")

print("\n=== STRETCH GOAL: VACCINATIONS ===")
VAC_OUT = Path("data") / "clean" / "farm_vaccinations.csv"
vac_rows = []

for flock in data["flocks"]:
    flock_id = flock["id"]
    for vac in flock["vaccinations"]:
        row = {
            "flock": flock_id,
            "vaccine": vac["vaccine"],
            "date": vac["date"]
        }
        vac_rows.append(row)

# Write the vaccinations CSV
with open(VAC_OUT, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["flock", "vaccine", "date"])
    writer.writeheader()
    writer.writerows(vac_rows)

print(f"Vaccinations flattened: {len(vac_rows)} rows written to {VAC_OUT.name}.")