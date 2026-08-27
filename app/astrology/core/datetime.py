from datetime import datetime, timedelta
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
    """Convert local datetime to Julian Day (UT). Robust version."""
    dt_utc = to_utc(dt, tz_str).replace(tzinfo=None)
    # 2440587.5 is the JD for 1970-01-01 00:00:00 UTC
    diff = dt_utc - datetime(1970, 1, 1)
    return 2440587.5 + diff.total_seconds() / 86400.0

def jd_to_datetime(jd: float) -> datetime:
    """Convert Julian Day to naive UTC datetime. Robust version with range safety."""
    try:
        # JD 0.0 is 4713 BC, far outside datetime range.
        # Year 1 starts around JD 1721425.5
        if jd < 1721425.5:
             return datetime(1, 1, 1)
        if jd > 5373484.5: # Far future (Year 9999)
             return datetime(9999, 12, 31)

        # 2440587.5 is the JD for 1970-01-01 00:00:00 UTC
        return datetime(1970, 1, 1) + timedelta(days=jd - 2440587.5)
    except Exception:
        return datetime.now()
