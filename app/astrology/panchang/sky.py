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
        # Check if rise_trans is actually functional
        if hasattr(swe, 'rise_trans'):
            # Corrected signature for pysweph/pyswisseph on Windows
            # Args: tjdut, body, rsmi, geopos=(lon, lat, alt), atpress, attemp, flags
            res = swe.rise_trans(jd_ut, planet_id, event_type, (lon, lat, 0.0), atpress, attemp, swe.FLG_SIDEREAL)
            # res should be (status, tret)
            if res and isinstance(res, (list, tuple)):
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

        event_utc_hour = event_utc_hour % 24

        from ..core.datetime import jd_to_datetime
        # Use timedelta to avoid invalid hour errors
        from datetime import date, timedelta
        target_dt = datetime.combine(dt.date(), datetime.min.time()) + timedelta(hours=event_utc_hour)
        return datetime_to_jd(target_dt, "UTC")
    except Exception as e:
        print(f"DEBUG: Math fallback failed: {e}")
        return None

def get_sunrise(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, 0, 1) # 0=SUN, 1=RISE

def get_sunset(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, 0, 2) # 0=SUN, 2=SET

def get_moonrise(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, 1, 1) # 1=MOON, 1=RISE

def get_moonset(jd_ut: float, lat: float, lon: float) -> Optional[float]:
    return get_sky_event(jd_ut, lat, lon, 1, 2) # 1=MOON, 2=SET

def get_kaal_window(part: int, sunrise_jd: float, sunset_jd: float, tz_str: str = "UTC") -> str:
    """Calculate a specific day-segment time window string."""
    if not sunrise_jd or not sunset_jd or sunrise_jd <= 0 or sunset_jd <= 0:
        return "—"

    total_days = sunset_jd - sunrise_jd
    if total_days <= 0: return "—"

    segment = total_days / 8.0
    start_jd = sunrise_jd + (part - 1) * segment
    end_jd = sunrise_jd + part * segment

    import pytz
    tz = pytz.timezone(tz_str)

    def jd_to_local_str(jd):
        try:
            from ..core.datetime import jd_to_datetime
            dt_utc = jd_to_datetime(jd)
            return pytz.utc.localize(dt_utc).astimezone(tz).strftime("%H:%M")
        except Exception:
            return "—"

    return f"{jd_to_local_str(start_jd)} – {jd_to_local_str(end_jd)}"

def get_rahu_kaal(weekday: int, sunrise_jd: float, sunset_jd: float, tz_str: str = "UTC") -> str:
    # 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat
    order = {1: 2, 2: 7, 3: 5, 4: 6, 5: 4, 6: 3, 0: 8}
    return get_kaal_window(order.get(weekday, 1), sunrise_jd, sunset_jd, tz_str)

def get_gulika_kaal(weekday: int, sunrise_jd: float, sunset_jd: float, tz_str: str = "UTC") -> str:
    # Mon: 6, Tue: 5, Wed: 4, Thu: 3, Fri: 2, Sat: 1, Sun: 7
    order = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 0: 7}
    return get_kaal_window(order.get(weekday, 1), sunrise_jd, sunset_jd, tz_str)

def get_yamaghanta(weekday: int, sunrise_jd: float, sunset_jd: float, tz_str: str = "UTC") -> str:
    # Mon: 4, Tue: 3, Wed: 2, Thu: 1, Fri: 7, Sat: 6, Sun: 5
    order = {1: 4, 2: 3, 3: 2, 4: 1, 5: 7, 6: 6, 0: 5}
    return get_kaal_window(order.get(weekday, 1), sunrise_jd, sunset_jd, tz_str)
