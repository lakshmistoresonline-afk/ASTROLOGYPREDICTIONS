from typing import Dict, List, Any

# Tatva sequence (90 mins cycle):
# Prithvi (6 mins), Jala (12 mins), Agni (18 mins), Vayu (24 mins), Akash (30 mins)
TATVA_SEQUENCE = [
    ("Prithvi", 6), ("Jala", 12), ("Agni", 18), ("Vayu", 24), ("Akash", 30)
]

def get_current_tatva(sunrise_jd: float, target_jd: float) -> Dict[str, Any]:
    """Calculate the active Tatva based on time from sunrise."""
    if not sunrise_jd or target_jd < sunrise_jd:
        return {"name": "Unknown", "quality": "Neutral"}

    # Time elapsed in minutes
    diff_min = (target_jd - sunrise_jd) * 1440.0

    # 90 minute cycle
    cycle_min = diff_min % 90.0

    accumulated = 0.0
    for name, duration in TATVA_SEQUENCE:
        if accumulated <= cycle_min < (accumulated + duration):
            quality = "Auspicious" if name in ["Prithvi", "Jala"] else "Mixed" if name == "Akash" else "Inauspicious"
            return {"name": name, "quality": quality, "minutes_into": round(cycle_min - accumulated, 1)}
        accumulated += duration

    return {"name": "Akash", "quality": "Mixed"}
