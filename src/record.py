records= [
    {"Flock": "A", "Date": "2026-10-12", "Eggs": 980, "Birds": 1200},
    {"Flock": "B", "Date": "2026-10-12", "Eggs": 610, "Birds": 800},
    {"Flock": "C", "Date": "2026-10-12", "Eggs": 410, "Birds": 600},
    {"Flock": "A", "Date": "2026-10-13", "Eggs": 1010, "Birds": 1200},
    {"Flock": "B", "Date": "2023-10-13", "Eggs": 650, "Birds": 800},
    {"Flock": "C", "Date": "2026-10-13", "Eggs": 380, "Birds": 598},
    {"Flock": "A", "Date": "2026-10-14", "Eggs": 870, "Birds": 1199},
    {"Flock": "B", "Date": "2026-10-14", "Eggs": 700, "Birds": 800},
    {"Flock": "C", "Date": "2026-10-14", "Eggs": 455, "Birds": 598},
    {"Flock": "A", "Date": "2026-10-15", "Eggs": 1050, "Birds": 1199},
]
print(f"Total records: {len(records)}")
print(f"First record eggs: {records[0]['Eggs']}")
print(f"Last record flock: {records[-1]['Flock']}")
print( "\n---Full Data Table---")
for r in records:
    print(f"{r['Flock']} {r['Date']} {r['Eggs']} eggs, {r['Birds']} birds")

print ("\n---First 3 Records---")
first_three = records[:3]
for r in first_three:
    print(f"{r['Flock']} {r['Date']} {r['Eggs']} eggs, {r['Birds']} birds")

print("\n--- Checking for Flock D ---")
has_d = "D" in records
print(f"Is 'D' in the records? {has_d}")

Flock_totals = {}
for r in records:
    flock = r["Flock"]
    eggs = r["Eggs"]
    if flock not in Flock_totals:
        Flock_totals[flock] = eggs
    else:
        Flock_totals[flock] = Flock_totals[flock] + eggs

print ("\n--- Total eggs per flock ---")
grand_total = 0
for flock, total in Flock_totals.items():
    print(f"{flock}: {total} eggs")
    grand_total = grand_total + total
print(f"Grand total: {grand_total} eggs")
# 1. Use a set to find distinct flocks
distinct_flocks = set()
for r in records:
    distinct_flocks.add(r["Flock"])

print(f"\n--- Distinct Flocks ---")
print(f"Total distinct flocks: {len(distinct_flocks)}")

# 2. Build a dictionary to count records per flock
record_counts = {}

for r in records:
    flock = r["Flock"]
    
    # If we haven't seen this flock, start its count at 1
    if flock not in record_counts:
        record_counts[flock] = 1
    # If we have, add 1 to its count
    else:
        record_counts[flock] = record_counts[flock] + 1

# 3. Print the record counts
print("\n--- Records per Flock ---")
for flock, count in record_counts.items():
    print(f"Flock {flock}: {count} records")
    
# 1. Add the "rate" key to every dictionary in the list
for r in records:
    r["rate"] = r["Eggs"] / r["Birds"]

# 2. Find the top 3 by eggs
# We use 'key=lambda r: r["Eggs"]' to tell Python: "Sort these dictionaries based on the 'Eggs' number"
# reverse=True makes it sort from highest to lowest
records_by_eggs = sorted(records, key=lambda r: r["Eggs"], reverse=True)
top_3_eggs = records_by_eggs[:3]

print("\n--- Top 3 Days by Eggs ---")
rank = 1
for r in top_3_eggs:
    print(f"Rank {rank}: Flock {r['Flock']}, {r['Date']}, {r['Eggs']:,} eggs")
    rank = rank + 1

# 3. Find the top 3 by laying rate
records_by_rate = sorted(records, key=lambda r: r["rate"], reverse=True)
top_3_rate = records_by_rate[:3]

print("\n--- Top 3 Days by Laying Rate ---")
rank = 1
for r in top_3_rate:
    rate_pct = r['rate'] * 100
    print(f"Rank {rank}: Flock {r['Flock']}, {r['Date']}, {rate_pct:.1f}%")
    rank = rank + 1
# 1. Set up our Group-By accumulators
flock_eggs = {}
flock_bird_days = {}

# 2. Accumulate both eggs and bird-days per flock
for r in records:
    flock = r["Flock"]
    
    # If it's a new flock, initialize its buckets at 0
    if flock not in flock_eggs:
        flock_eggs[flock] = 0
        flock_bird_days[flock] = 0
        
    # Add today's numbers to the flock's running totals
    flock_eggs[flock] = flock_eggs[flock] + r["Eggs"]
    flock_bird_days[flock] = flock_bird_days[flock] + r["Birds"]

print("\n--- Laying Rate per Flock ---")

# 3. Calculate and classify the final rates
# We sort the flocks so they print in alphabetical order (A, B, C)
for flock in sorted(flock_eggs.keys()):
    total_eggs = flock_eggs[flock]
    total_bd = flock_bird_days[flock]
    
    rate = total_eggs / total_bd
    
    if rate >= 0.80:
        label = "good"
    elif rate >= 0.60:
        label = "watch"
    else:
        label = "act now"
        
    rate_pct = rate * 100
    print(f"Flock {flock}: {total_eggs:,} eggs | {total_bd:,} bird-days | {rate_pct:.1f}% | {label}")

# Think: B produced half of A's eggs but has the better rate.
# Owner comment: Flock C is severely underperforming the rest of the farm at 69.3% efficiency and requires immediate investigation into their feed, water, or health.
print("\n--- Birds Lost per Flock ---")

# 1. Group records by flock into separate lists
records_by_flock = {}

for r in records:
    flock = r["Flock"]
    
    # If it is a new flock, start an empty list
    if flock not in records_by_flock:
        records_by_flock[flock] = []
        
    # Append the entire row (dictionary) to the flock's list
    records_by_flock[flock].append(r)

# 2. Sort each flock's list by date to find the true first and last day
for flock in sorted(records_by_flock.keys()):
    flock_data = records_by_flock[flock]
    
    # Sort this specific flock's data by date
    sorted_flock_data = sorted(flock_data, key=lambda r: r["Date"])
    
    # The first record is at index 0, the last is at index -1
    first_birds = sorted_flock_data[0]["Birds"]
    last_birds = sorted_flock_data[-1]["Birds"]
    
    birds_lost = first_birds - last_birds
    
    print(f"Flock {flock} lost {birds_lost}")