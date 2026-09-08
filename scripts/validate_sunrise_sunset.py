import os
import sys
from datetime import datetime, date
import pytz

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.astrology.panchang.sky import get_sunrise, get_sunset
from app.astrology.core.datetime import datetime_to_jd, jd_to_datetime

def validate(location_name, lat, lon, tz_name):
    tz = pytz.timezone(tz_name)
    # Test for today: Sep 4, 2026
    target_date = date(2026, 9, 4)
    midnight_local = tz.localize(datetime.combine(target_date, datetime.min.time()))
    jd_ut = datetime_to_jd(midnight_local.replace(tzinfo=None), tz_name)

    sr_jd = get_sunrise(jd_ut, lat, lon)
    ss_jd = get_sunset(jd_ut, lat, lon)

    sr_dt = pytz.utc.localize(jd_to_datetime(sr_jd)).astimezone(tz) if sr_jd else None
    ss_dt = pytz.utc.localize(jd_to_datetime(ss_jd)).astimezone(tz) if ss_jd else None

    print(f"Location: {location_name:15} | Sunrise: {sr_dt.strftime('%H:%M') if sr_dt else 'N/A'} | Sunset: {ss_dt.strftime('%H:%M') if ss_dt else 'N/A'}")

def main():
    test_cases = [
        ("Thrissur", 10.5276, 76.2144, "Asia/Kolkata"),
        ("Coimbatore", 11.0168, 76.9558, "Asia/Kolkata"),
        ("New Delhi", 28.6139, 77.2090, "Asia/Kolkata"),
        ("London", 51.5074, -0.1278, "Europe/London"),
        ("New York", 40.7128, -74.0060, "America/New_York"),
        ("Sydney", -33.8688, 151.2093, "Australia/Sydney")
    ]

    print("--- Sunrise/Sunset Validation (Sep 4, 2026) ---")
    for name, lat, lon, tz in test_cases:
        validate(name, lat, lon, tz)

if __name__ == "__main__":
    main()
