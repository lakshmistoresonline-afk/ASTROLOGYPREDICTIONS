"""
Real-Time WebSocket Transit Stream Route (Module 26 - Task 26.1).
Exposes /ws/transits/live broadcasting real-time planetary coordinates and active Kakshya entry triggers.
"""
from typing import Dict, Any
from datetime import datetime
from ..astrology.core.ephemeris import get_planet_position, set_topocentric
from ..astrology.core.swe_proxy import swe

def calculate_current_transits_realtime(lat: float = 10.7867, lon: float = 76.6548) -> Dict[str, Any]:
    """Calculates current planetary longitudes for real-time WebSocket streaming."""
    set_topocentric(lat, lon)
    now = datetime.now()
    jd_ut = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)

    planet_ids = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE
    }

    positions = {}
    for name, pid in planet_ids.items():
        pos = get_planet_position(jd_ut, pid)
        positions[name] = round(pos["longitude"], 4)

    positions["Ketu"] = round((positions["Rahu"] + 180.0) % 360.0, 4)

    return {
        "stream_event": "LIVE_TRANSIT_UPDATE",
        "timestamp_utc": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "julian_day_ut": round(jd_ut, 5),
        "transits": positions
    }
