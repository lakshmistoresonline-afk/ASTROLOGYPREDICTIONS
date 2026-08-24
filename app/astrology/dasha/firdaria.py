from datetime import datetime, timedelta
from typing import List, Dict, Any

# Firdaria Periods (Persian system)
# Day Birth: Sun (10), Venus (8), Mercury (13), Moon (9), Saturn (11), Jupiter (12), Mars (7), Nodes (3 each)
# Night Birth: Moon (9), Saturn (11), Jupiter (12), Mars (7), Sun (10), Venus (8), Mercury (13), Nodes (3 each)

DAY_ORDER = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars", "North Node", "South Node"]
NIGHT_ORDER = ["Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "North Node", "South Node"]

YEARS = {
    "Sun": 10, "Venus": 8, "Mercury": 13, "Moon": 9,
    "Saturn": 11, "Jupiter": 12, "Mars": 7, "North Node": 3, "South Node": 3
}

def calculate_firdaria(birth_dt: datetime, is_day: bool) -> List[Dict[str, Any]]:
    order = DAY_ORDER if is_day else NIGHT_ORDER
    periods = []
    curr_start = birth_dt

    for planet in order:
        y = YEARS[planet]
        curr_end = curr_start + timedelta(days=y * 365.2425)

        # Sub-periods (7 sub-periods for major planets, none for nodes usually)
        subs = []
        if planet not in ["North Node", "South Node"]:
            sub_y = y / 7
            s_start = curr_start
            p_idx = order.index(planet)
            for i in range(7):
                s_lord = order[(p_idx + i) % 7]
                s_end = s_start + timedelta(days=sub_y * 365.2425)
                subs.append({"lord": s_lord, "start": s_start, "end": s_end})
                s_start = s_end

        periods.append({
            "lord": planet,
            "start": curr_start,
            "end": curr_end,
            "sub_periods": subs
        })
        curr_start = curr_end

    return periods
