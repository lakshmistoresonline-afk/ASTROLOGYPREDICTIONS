from ..core.swe_proxy import swe
from typing import Optional
from datetime import datetime

def get_sky_event(jd_ut: float, lat: float, lon: float, planet_id: int, event_type: int) -> Optional[float]:
    """
    Get JD for a sky event (sunrise, sunset, etc).
    event_type: 1 = RISE, 2 = SET (simplified for fallback)
    """
    # Standard atmospheric pressure and temperature for refraction
    atpress = 1013.25
    attemp = 15.0

    # 1. Try Swiss Ephemeris first
    try:
        res = swe.rise_trans(jd_ut, planet_id, lon, lat, 0, atpress, attemp, event_type)
        # res should be (status, [tret1, ...])
        if res and isinstance(res, tuple) and len(res) > 1:
            tret = res[1]
            if tret and tret[0] > 1000000:
                return tret[0]
    except Exception as e:
        print(f"DEBUG: SWE rise_trans failed: {e}")

    # 2. Fallback to Ephem library for basic sky events if SWE is missing/mocked
    try:
        import ephem
        obs = ephem.Observer()
        obs.lat = str(lat)
        obs.lon = str(lon)
        obs.elev = 0
        obs.pressure = 1013.25
        obs.temp = 15.0

        # Convert JD to datetime for ephem
        from ..core.datetime import jd_to_datetime
        dt = jd_to_datetime(jd_ut)
        obs.date = dt

        body = ephem.Sun() if planet_id == 0 else ephem.Moon()

        if event_type == 1: # CALC_RISE
            e_dt = obs.next_rising(body).datetime()
        elif event_type == 2: # CALC_SET
            e_dt = obs.next_setting(body).datetime()
        else:
            return None

        # Convert back to JD
        from ..core.datetime import datetime_to_jd
        return datetime_to_jd(e_dt, "UTC")
    except Exception:
        pass

    # 3. Simple Mathematical Fallback (Sunrise Equation)
    # Sufficient for UI visualization if all libraries fail
    try:
        import math
        from ..core.datetime import jd_to_datetime
        dt = jd_to_datetime(jd_ut)

        # Day of year
        n = dt.timetuple().tm_yday

        # calculate solar declination
        decl = -23.44 * math.cos(math.radians(360/365.24 * (n + 10)))

        # calculate hour angle
        lat_rad = math.radians(lat)
        decl_rad = math.radians(decl)

        cos_h = (math.sin(math.radians(-0.83)) - math.sin(lat_rad) * math.sin(decl_rad)) / (math.cos(lat_rad) * math.cos(decl_rad))

        if cos_h > 1: return None # Polar night
        if cos_h < -1: return None # Polar day

        h = math.degrees(math.acos(cos_h))

        # mean solar noon in UTC decimal hours (rough approximation)
        solar_noon = 12.0 - lon / 15.0

        if event_type == 1: # Rise
            event_utc_hour = (solar_noon - h / 15.0) % 24
        else: # Set
            event_utc_hour = (solar_noon + h / 15.0) % 24

        from ..core.datetime import datetime_to_jd
        target_dt = datetime(dt.year, dt.month, dt.day, int(event_utc_hour), int((event_utc_hour % 1) * 60))
        return datetime_to_jd(target_dt, "UTC")
    except Exception:
        return None

def get_sunrise(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, 0, 1) # 0=SUN, 1=RISE

def get_sunset(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, 0, 2) # 0=SUN, 2=SET

def get_moonrise(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, 1, 1) # 1=MOON, 1=RISE

def get_moonset(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, 1, 2) # 1=MOON, 2=SET

def get_kaal_window(part: int, sunrise_jd: float, sunset_jd: float) -> str:
    """Calculate a specific day-segment time window string."""
    if not sunrise_jd or not sunset_jd or sunrise_jd <= 0 or sunset_jd <= 0:
        return "—"

    total_days = sunset_jd - sunrise_jd
    if total_days <= 0: return "—"

    segment = total_days / 8.0
    start_jd = sunrise_jd + (part - 1) * segment
    end_jd = sunrise_jd + part * segment

    def jd_to_str(jd):
        try:
            from ..core.swe_proxy import swe
            y, m, d, h = swe.revjul(jd)
            hh = int(h)
            mm = int((h - hh) * 60)
            return f"{hh:02d}:{mm:02d}"
        except Exception:
            return "—"

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
