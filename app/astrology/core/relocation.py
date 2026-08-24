from .swe_proxy import swe
from typing import Dict, List, Any
from .datetime import datetime_to_jd

def get_angular_points(jd_ut: float) -> Dict[str, Dict[str, float]]:
    """
    Calculate where planets are conjunct angles globally.
    MC (Zenith), IC (Nadir), AS (Rising), DS (Setting).
    """
    results = {}
    p_names = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE
    }

    # Get RAMC for the given JD_UT
    # Simplified: JD_UT already accounts for time. RAMC is derived from it.
    # In SwissEph, we need local sidereal time to find angles.
    # For global lines, we solve: Planet_RA = RAMC_at_Longitude

    for name, pid in p_names.items():
        # Get Planet RA and Dec
        res = swe.calc_ut(jd_ut, pid, swe.FLG_EQUATORIAL)
        ra = res[0] if not isinstance(res[0], list) else res[0][0] # Planet Right Ascension in degrees

        # MC Longitude: Longitude where Planet RA = RAMC
        # RAMC = GST + Longitude
        # Longitude = Planet_RA - GST

        gst = swe.sidtime(jd_ut) * 15.0 # GST in degrees
        mc_lon = (ra - gst + 180) % 360 - 180

        results[name] = {
            "MC_Longitude": round(mc_lon, 2),
            "IC_Longitude": round((mc_lon + 180 + 180) % 360 - 180, 2),
            "interpretation": f"Planetary power is maximized at {round(mc_lon, 2)} longitude for {name} MC line."
        }
    return results

def calculate_relocated_lagna(jd_ut: float, new_lat: float, new_lon: float) -> float:
    """Calculate the Ascendant for a different location at the same birth moment."""
    from .houses import get_houses
    h_data = get_houses(jd_ut, new_lat, new_lon)
    return h_data["ascendant"]
