from datetime import datetime
import pytz
from .ephemeris import get_julian_day

def validate_datetime(dt_str: str, format: str = "%Y-%m-%d %H:%M") -> datetime:
    """Validate and return a naive datetime object from string."""
    return datetime.strptime(dt_str, format)

def to_utc(dt: datetime, tz_str: str) -> datetime:
    """Convert a naive datetime with a given timezone string to UTC."""
    tz = pytz.timezone(tz_str)
    if dt.tzinfo is None:
        dt = tz.localize(dt)
    return dt.astimezone(pytz.utc)

def datetime_to_jd(dt: datetime, tz_str: str = "UTC") -> float:
    """Convert local datetime to Julian Day (UT)."""
    dt_utc = to_utc(dt, tz_str)
    hour_utc = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    return get_julian_day(dt_utc.year, dt_utc.month, dt_utc.day, hour_utc)
