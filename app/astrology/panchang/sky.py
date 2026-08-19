import swisseph as swe
from typing import Optional

def get_sky_event(jd_ut: float, lat: float, lon: float, planet_id: int, event_type: int) -> Optional[float]:
    """
    Get JD for a sky event (sunrise, sunset, etc).
    event_type: swe.CALC_RISE, swe.CALC_SET, etc.
    """
    # Standard atmospheric pressure and temperature for refraction
    atpress = 1013.25
    attemp = 15.0

    # event_type is a combination of flags
    # We want topocentric rise/set
    flags = swe.BIT_DISC_CENTER # Standard for many astro calcs, but for sunrise usually top edge
    # For actual sunrise (visible), we might need to adjust flags.
    # Official Swiss Ephemeris suggests:
    flags = 0 # Default is center.

    try:
        res = swe.rise_trans(jd_ut, planet_id, lon, lat, 0, atpress, attemp, event_type)
        return res[0] # The JD of the event
    except Exception:
        return None

def get_sunrise(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    # Search for rise after midnight of the day
    return get_sky_event(jd_ut, lat, lon, swe.SUN, swe.CALC_RISE | swe.BIT_HINDSIGHT)

def get_sunset(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, swe.SUN, swe.CALC_SET | swe.BIT_HINDSIGHT)

def get_moonrise(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, swe.MOON, swe.CALC_RISE | swe.BIT_HINDSIGHT)

def get_moonset(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, swe.MOON, swe.CALC_SET | swe.BIT_HINDSIGHT)
