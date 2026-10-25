from datetime import timedelta
from collections import defaultdict
import logging

log = logging.getLogger(__name__)

def missing_days(rows):
    if not rows:
        return []

    dates = [r.date for r in rows]
    min_date = min(dates)
    max_date = max(dates)
    
    flocks = sorted(list(set(r.flock for r in rows)))
    existing = set((r.flock, r.date) for r in rows)
    
    missing = []
    current = min_date
    while current <= max_date:
        for flock in flocks:
            pair = (flock, current)
            if pair not in existing:
                weekday = current.strftime("%A")
                missing.append((flock, current))
                log.warning(f"Missing record for Flock {flock} on {current} ({weekday})")
        current += timedelta(days=1)
        
    return missing

def totals_by_flock(rows, metric="eggs"):
    totals = defaultdict(int)
    for r in rows:
        totals[r.flock] += getattr(r, metric)
    return totals