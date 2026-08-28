from datetime import datetime, timedelta
import pytz

def validate_datetime(dt_str: str, format: str = "%Y-%m-%d %H:%M") -> datetime:
    """Validate and return a naive datetime object from string."""
    try:
        return datetime.strptime(dt_str, format)
    except ValueError as e:
        raise ValueError(f"Invalid birth time format: {e}")

def to_utc(dt: datetime, tz_str: str) -> datetime:
    """
    Convert a naive datetime with a given timezone string to UTC.
    Strictly follows IANA timezone database.
    """
    try:
        tz = pytz.timezone(tz_str)
        if dt.tzinfo is None:
            # Handle ambiguous times (DST) by choosing standard time or raising error
            # For birth data, we assume the user provides local time as usually understood.
            dt = tz.localize(dt, is_dst=None)
        return dt.astimezone(pytz.utc)
    except Exception as e:
        raise ValueError(f"Timezone conversion failed for '{tz_str}': {e}")

def datetime_to_jd(dt: datetime, tz_str: str = "UTC") -> float:
    """
    Convert local datetime to Julian Day (UT).
    Accuracy is maintained through high-precision time deltas.
    """
    dt_utc = to_utc(dt, tz_str).replace(tzinfo=None)

    # Julian Date reference for 1970-01-01 00:00:00 UTC
    JD_1970 = 2440587.5

    diff = dt_utc - datetime(1970, 1, 1)
    return JD_1970 + (diff.total_seconds() / 86400.0)

def jd_to_datetime(jd: float) -> datetime:
    """
    Convert Julian Day to naive UTC datetime.
    Range limited to Year 1 - Year 9999 for Python compatibility.
    """
    # JD 1721425.5 is 0001-01-01 00:00:00
    if jd < 1721425.5:
        return datetime(1, 1, 1)
    if jd > 5373484.5:
        return datetime(9999, 12, 31)

    return datetime(1970, 1, 1) + timedelta(days=jd - 2440587.5)
