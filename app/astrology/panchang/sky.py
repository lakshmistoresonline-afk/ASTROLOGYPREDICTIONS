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
    # For actual sunrise (visible), we might need to adjust flags.
    # Official Swiss Ephemeris suggests:

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

def get_kaal_window(part: int, sunrise_jd: float, sunset_jd: float) -> str:
    """Calculate a specific day-segment time window string."""
    from datetime import datetime, timedelta, timezone

    total_days = sunset_jd - sunrise_jd
    segment = total_days / 8.0
    start_jd = sunrise_jd + (part - 1) * segment
    end_jd = sunrise_jd + part * segment

    def jd_to_str(jd):
        y, m, d, h = swe.revjul(jd)
        hh = int(h)
        mm = int((h - hh) * 60)
        return f"{hh:02d}:{mm:02d}" # Simple HH:MM for now

    return f"{jd_to_str(start_jd)} – {jd_to_str(end_jd)}"

def get_rahu_kaal(weekday: int, sunrise_jd: float, sunset_jd: float) -> str:
    order = {0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3, 6: 8}
    return get_kaal_window(order.get(weekday, 1), sunrise_jd, sunset_jd)

def get_gulika_kaal(weekday: int, sunrise_jd: float, sunset_jd: float) -> str:
    order = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1, 5: 7, 6: 6}
    return get_kaal_window(order.get(weekday, 1), sunrise_jd, sunset_jd)

def get_yamaghanta(weekday: int, sunrise_jd: float, sunset_jd: float) -> str:
    order = {0: 4, 1: 3, 2: 2, 3: 1, 4: 7, 5: 6, 6: 5}
    return get_kaal_window(order.get(weekday, 1), sunrise_jd, sunset_jd)
