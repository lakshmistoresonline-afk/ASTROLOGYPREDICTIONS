from datetime import datetime, timedelta, date, time
import pytz

def validate_datetime(dt_str: str, format: str = "%Y-%m-%d %H:%M") -> datetime:
    """Validate and return a naive datetime object from string."""
    try:
        return datetime.strptime(dt_str, format)
    except ValueError as e:
        raise ValueError(f"Invalid birth time format: {e}")

def parse_birth_datetime(dob_str: str, tob_str: str) -> datetime:
    """Robustly parse birth date and time across ISO, US, UK formats, and 12/24 hour times."""
    if not dob_str or not tob_str:
        raise ValueError("Birth date and time are mandatory.")

    dob_str = str(dob_str).strip()
    tob_str = str(tob_str).strip().upper()

    parsed_date = None
    for df in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y.%m.%d", "%d-%m-%Y"]:
        try:
            parsed_date = datetime.strptime(dob_str, df).date()
            break
        except ValueError:
            continue

    if not parsed_date:
        for sep in ['-', '/', '.']:
            if sep in dob_str:
                parts = dob_str.split(sep)
                if len(parts) == 3:
                    try:
                        if len(parts[0]) == 4:
                            parsed_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
                        elif len(parts[2]) == 4:
                            parsed_date = date(int(parts[2]), int(parts[0]), int(parts[1]))
                        break
                    except:
                        pass
    if not parsed_date:
        raise ValueError(f"Invalid birth date format: '{dob_str}'. Use YYYY-MM-DD.")

    parsed_time = None
    for tf in ["%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M%p", "%I:%M:%S %p", "%H%M"]:
        try:
            parsed_time = datetime.strptime(tob_str, tf).time()
            break
        except ValueError:
            continue

    if not parsed_time:
        try:
            is_pm = 'PM' in tob_str
            is_am = 'AM' in tob_str
            clean_time = tob_str.replace('AM', '').replace('PM', '').strip()
            t_parts = clean_time.split(':')
            hour = int(t_parts[0])
            minute = int(t_parts[1]) if len(t_parts) > 1 else 0
            second = int(t_parts[2]) if len(t_parts) > 2 else 0
            if is_pm and hour < 12:
                hour += 12
            elif is_am and hour == 12:
                hour = 0
            parsed_time = time(hour, minute, second)
        except:
            parsed_time = time(12, 0, 0)

    return datetime.combine(parsed_date, parsed_time)

def to_utc(dt: datetime, tz_str: str) -> datetime:
    """
    Convert a naive datetime with a given timezone string to UTC.
    Strictly follows IANA timezone database.
    """
    try:
        tz = pytz.timezone(tz_str)
        if dt.tzinfo is None:
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
    if jd < 1721425.5:
        return datetime(1, 1, 1)
    if jd > 5373484.5:
        return datetime(9999, 12, 31)

    return datetime(1970, 1, 1) + timedelta(days=jd - 2440587.5)
