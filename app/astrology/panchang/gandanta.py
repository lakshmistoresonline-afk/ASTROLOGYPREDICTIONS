from typing import Dict, List, Any

# Gandanta: Dangerous junction points (last/first 3° of specific signs)
# Fire signs (0, 4, 8): Aries, Leo, Sag (Start)
# Water signs (3, 7, 11): Cancer, Scorpio, Pisces (End)

def check_gandanta(planets: Dict[str, Any], asc_lon: float) -> List[Dict[str, Any]]:
    results = []

    # 1. Rashi Gandanta
    # 0-1, 119-121, 239-241 (approx)
    G_RANGES = [
        (357, 3),   # Meena-Mesha
        (117, 123), # Karka-Simha
        (237, 243)  # Vrishchika-Dhanu
    ]

    def is_in_g(lon):
        for start, end in G_RANGES:
            if start > end: # wrap
                if lon >= start or lon <= end: return True
            else:
                if start <= lon <= end: return True
        return False

    # Check Lagna
    if is_in_g(asc_lon):
        results.append({"target": "Ascendant", "type": "Lagna Gandanta", "impact": "High intensity at birth; strong soul-purpose but initial challenges."})

    # Check Moon
    moon_lon = planets["Moon"].longitude
    if is_in_g(moon_lon):
        results.append({"target": "Moon", "type": "Tithi Gandanta", "impact": "Emotional sensitivity and karmic transitions."})

    return results

def get_nakshatra_tyajya(nak_idx: int, duration_hours: float) -> str:
    """
    Tyajya (Forbidden time): Specific 4-ghatika (96 min) window in each nakshatra.
    """
    # Tyajya start points (in percent of nakshatra duration)
    TYAJYA_POINTS = {
         0: 0.50, 1: 0.24, 2: 0.30, 3: 0.40, 4: 0.14, 5: 0.21, 6: 0.30, 7: 0.20, 8: 0.32,
         # ... 27 nakshatras
    }
    start_pct = TYAJYA_POINTS.get(nak_idx, 0.25)
    start_h = duration_hours * start_pct
    end_h = start_h + 1.6 # 4 ghatikas = 1.6 hours

    return f"From {round(start_h, 1)}h to {round(end_h, 1)}h into the Nakshatra."
