from datetime import date, datetime
from .tithi import get_tithi_info, get_tithi_end_time
from .nakshatra import get_nakshatra_info, get_nakshatra_end_time
from .yoga import get_yoga_info, get_yoga_end_time
from .karana import get_karana_info, get_karana_end_time
from .sky import get_sunrise, get_sunset
from ..core.datetime import datetime_to_jd
from ..core.ephemeris import get_ayanamsa
import pytz

def calculate_panchang_2_0(target_date: date, lat: float, lon: float, tz_str: str) -> dict:
    """High-precision Panchang solver."""
    tz = pytz.timezone(tz_str)
    # Use local noon for limb calculation
    noon_dt = datetime.combine(target_date, datetime.min.time()).replace(hour=12)
    jd_ut = datetime_to_jd(noon_dt, tz_str)

    tithi = get_tithi_info(jd_ut)
    nak = get_nakshatra_info(jd_ut)
    yoga = get_yoga_info(jd_ut)
    karana = get_karana_info(jd_ut)

    # End times (in JD)
    tithi_end_jd = get_tithi_end_time(jd_ut)
    nak_end_jd = get_nakshatra_end_time(jd_ut)

    def jd_to_local_str(jd):
        if jd < 0: return "—"
        # Convert JD back to UTC datetime, then to local
        import swisseph as swe
        y, m, d, h = swe.revjul(jd)
        # fractional h to h, m, s
        hh = int(h)
        mm = int((h - hh) * 60)
        ss = int(((h - hh) * 60 - mm) * 60)
        dt_utc = datetime(y, m, d, hh, mm, ss, tzinfo=pytz.utc)
        return dt_utc.astimezone(tz).strftime("%I:%M %p")

    return {
        "tithi": {
            "number": tithi["number"],
            "end_time": jd_to_local_str(tithi_end_jd)
        },
        "nakshatra": {
            "number": nak["number"],
            "end_time": jd_to_local_str(nak_end_jd),
            "pada": nak["pada"]
        },
        "yoga": {
            "number": yoga["number"]
        },
        "karana": {
            "number": karana["number"]
        },
        "ayanamsa": round(get_ayanamsa(jd_ut), 4)
    }
