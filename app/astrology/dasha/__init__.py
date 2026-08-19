from .vimshottari import get_vimshottari_periods
from datetime import datetime

def calculate_vimshottari(moon_longitude: float, birth_dt: datetime) -> dict:
    """Legacy compatibility for Dasha."""
    periods = get_vimshottari_periods(moon_longitude, birth_dt)

    # Format to look like legacy structure
    mahadashas = []
    for p in periods:
        mahadashas.append({
            "lord": p["lord"],
            "start": p["start"].strftime("%d %b %Y"),
            "end": p["end"].strftime("%d %b %Y"),
            "color": "#fff", # Placeholder
            "is_current": p["start"] <= datetime.now() < p["end"]
        })

    current_maha = next((m for m in mahadashas if m["is_current"]), None)

    return {
        "mahadashas": mahadashas,
        "current_maha": current_maha
    }

def dasha_summary(moon_longitude: float, birth_dt: datetime) -> dict:
    data = calculate_vimshottari(moon_longitude, birth_dt)
    cm = data["current_maha"]
    return {
        "mahadasha": cm["lord"] if cm else "N/A",
        "maha_end": cm["end"] if cm else "N/A",
        "maha_color": "#fff"
    }
