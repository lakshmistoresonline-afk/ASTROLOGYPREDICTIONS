from typing import List, Dict, Any

# Hora order: Sun, Ven, Merc, Moon, Sat, Jup, Mars
HORA_ORDER = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]

# Map Weekday to starting Hora Lord
# 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat
# In Python datetime, 0=Mon, 6=Sun.
# Standard Vedic: Sun starts with Sun, Mon starts with Moon.

WEEKDAY_TO_HORA_START = {
    6: 0, # Sun starts with Sun (0)
    0: 3, # Mon starts with Moon (3)
    1: 6, # Tue starts with Mars (6)
    2: 2, # Wed starts with Mercury (2)
    3: 5, # Thu starts with Jupiter (5)
    4: 1, # Fri starts with Venus (1)
    5: 4  # Sat starts with Saturn (4)
}

def get_horas(sunrise_jd: float, next_sunrise_jd: float, weekday_idx: int) -> List[Dict[str, Any]]:
    """Calculate the 24 horas for the day."""
    total_duration = next_sunrise_jd - sunrise_jd
    hora_duration = total_duration / 24.0

    start_idx = WEEKDAY_TO_HORA_START.get(weekday_idx, 0)

    horas = []
    for i in range(24):
        lord = HORA_ORDER[(start_idx + i) % 7]
        horas.append({
            "number": i + 1,
            "lord": lord,
            "start_jd": sunrise_jd + i * hora_duration,
            "end_jd": sunrise_jd + (i + 1) * hora_duration
        })

    return horas
