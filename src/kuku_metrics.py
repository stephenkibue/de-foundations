records = [
    {"flock": "A", "date": "2026-10-12", "eggs": 980, "birds": 1200},
    {"flock": "B", "date": "2026-10-12", "eggs": 610, "birds": 800},
    {"flock": "C", "date": "2026-10-12", "eggs": 410, "birds": 600},
    {"flock": "A", "date": "2026-10-13", "eggs": 1010, "birds": 1200},
    {"flock": "B", "date": "2026-10-13", "eggs": 650, "birds": 800},
    {"flock": "C", "date": "2026-10-13", "eggs": 380, "birds": 598},
    {"flock": "A", "date": "2026-10-14", "eggs": 870, "birds": 1199},
    {"flock": "B", "date": "2026-10-14", "eggs": 700, "birds": 800},
    {"flock": "C", "date": "2026-10-14", "eggs": 455, "birds": 598},
    {"flock": "A", "date": "2026-10-15", "eggs": 1050, "birds": 1199}
]
def trays_and_loose(eggs, eggs_per_tray=30):
    trays = eggs // eggs_per_tray
    loose = eggs % eggs_per_tray
    return trays, loose

def revenue(eggs, price_per_tray, eggs_per_tray=30):
    trays, loose = trays_and_loose(eggs, eggs_per_tray)
    return trays * price_per_tray

def check():
    assert trays_and_loose(1000) == (33, 10)
    assert trays_and_loose(29) == (0, 29)
    assert trays_and_loose(100, eggs_per_tray=12) == (8, 4)
    assert revenue(1000, 450) == 14850
    assert revenue(1000, 450, eggs_per_tray=12) == 37350
    print("All tests passed!")

check()

def laying_rate(eggs, birds):
    if birds <= 0:
        return None
    return eggs / birds
def check():
    assert laying_rate(960, 1200) == 0.8
    assert laying_rate(0, 1200) == 0.0
    assert laying_rate(500, 0) == None
    print("laying_rate tests passed!")

check()

def classify(rate):
    if rate is None:
        return "no data"

    if rate >= 0.8:
        return "good"
    elif rate >= 0.60:
        return "watch"
    else:
        return "act now"

def check():
    assert classify(0.833) == "good"
    assert classify(0.80) == "good"
    assert classify(0.792) == "watch"
    assert classify(0.60) == "watch"
    assert classify(0.583) == "act now"
    assert classify(None) == "no data"
    print("classify tests passed!")

check()

def totals_by_flock(records, field):
    totals = {}
    for r in records:
        flock = r["flock"]
        value = r[field]

        if flock not in totals:
            totals[flock] = 0

        totals[flock] = totals[flock] + value
    return totals

def check():
    assert totals_by_flock(records, "eggs") == {"A": 3910, "B": 1960, "C": 1245}
    assert totals_by_flock(records, "birds") == {"A": 4798, "B": 2400, "C": 1796}
    print("totals_by_flock tests passed!")

check()

def flock_rates(records):
    total_eggs = totals_by_flock(records, "eggs")
    total_birds = totals_by_flock(records, "birds")

    return {flock: laying_rate(total_eggs[flock], total_birds[flock]) for flock in total_eggs.keys()}

def check():
    rates = flock_rates(records)
    assert round(rates["A"], 3) == 0.815
    assert round(rates["B"], 3) == 0.817   
    assert round(rates["C"], 3) == 0.693
    print("flock_rates tests passed!")

check()

def below_good(records):
    return[
        r for r in records
        if laying_rate(r["eggs"], r["birds"]) is not None
        and laying_rate(r["eggs"], r["birds"]) < 0.80
    ]
def check():
    bad_days = below_good(records)
    assert len(bad_days) == 5
    assert bad_days[0] == {"flock": "B", "date": "2026-10-12", "eggs": 610, "birds": 800}
    assert bad_days[1] == {"flock": "C", "date": "2026-10-12", "eggs": 410, "birds": 600}
    assert bad_days[2] == {"flock": "C", "date": "2026-10-13", "eggs": 380, "birds": 598}
    assert bad_days[3] == {"flock": "A", "date": "2026-10-14", "eggs": 870, "birds": 1199}
    assert bad_days[4] == {"flock": "C", "date": "2026-10-14", "eggs": 455, "birds": 598}
    print( "bad_days checks passed")

check()

def flock_report(records, flock):
    flock_records = [r for r in records if r["flock"] == flock]
    total_eggs = sum(r["eggs"] for r in flock_records)
    total_birds = sum(r["birds"] for r in flock_records)
    rate = laying_rate(total_eggs, total_birds)

    sorted_days = sorted(flock_records, key=lambda r: laying_rate(r["eggs"], r["birds"]))
    return {
        "total_eggs": total_eggs,
        "rate": rate,
        "label": classify(rate),
        "worst_day": sorted_days[0]["date"],
        "best_day": sorted_days[-1]["date"]
    }

def main():
    print("\n=== KUKU FARM PERFORMANCE REPORT ===")

    print("\n1. FLOCK SUMMARIES")
    distinct_flocks = sorted(set(r["flock"] for r in records))
    
    for flock in distinct_flocks:
        report = flock_report(records, flock)
        
        rate_pct = report["rate"] * 100
        print(f"Flock {flock}: {report['total_eggs']:,} eggs | {rate_pct:.1f}% | {report['label']}")
        print(f"   -> Best day: {report['best_day']} | Worst day: {report['worst_day']}")

    print("\n2. DAYS REQUIRING ATTENTION (< 80%)")
    bad_days = below_good(records)
    for d in bad_days:
        daily_rate = laying_rate(d["eggs"], d["birds"]) * 100
        print(f"Flock {d['flock']} on {d['date']}: {daily_rate:.1f}%")

    print("\n3. REVENUE PROJECTION")
    egg_totals = totals_by_flock(records, "eggs")
    total_eggs = sum(egg_totals.values()) 
    price = 450 
    
    trays, loose = trays_and_loose(total_eggs)
    total_rev = revenue(total_eggs, price)
    
    print(f"Total Eggs Sold: {total_eggs:,}")
    print(f"Packaging: {trays} full trays, {loose} loose eggs")
    print(f"Total Revenue: {total_rev:,} shillings (at {price}/tray)")
    print("===================================\n")

check()
main()

        