from datetime import datetime, date, timedelta
import sys
import os

# Add parent dir to sys.path to import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from app.astrology.calculator import _rahu_kaal, _gulika_kaal, _yamaghanta

def test_kaal():
    # Mock sunrise/sunset (12 hour day)
    sunrise = datetime(2023, 10, 23, 6, 0) # A Monday
    sunset  = datetime(2023, 10, 23, 18, 0)

    # Monday is Python 0
    weekday = 0

    print(f"Testing for Monday (12h day, 06:00-18:00):")
    print(f"Rahu Kaal (Expected 2nd part, 07:30-09:00):  {_rahu_kaal(weekday, sunrise, sunset)}")
    print(f"Gulika Kaal (Expected 5th part, 12:00-13:30): {_gulika_kaal(weekday, sunrise, sunset)}")
    print(f"Yamaghanta (Expected 4th part, 10:30-12:00):  {_yamaghanta(weekday, sunrise, sunset)}")

    # Wednesday (Python 2)
    # Rahu: 5th part (12:00-13:30)
    # Gulika: 3rd part (09:00-10:30)
    # Yamaghanta: 2nd part (07:30-09:00)
    weekday = 2
    print(f"\nTesting for Wednesday:")
    print(f"Rahu Kaal (Expected 5th part, 12:00-13:30):  {_rahu_kaal(weekday, sunrise, sunset)}")
    print(f"Gulika Kaal (Expected 3rd part, 09:00-10:30): {_gulika_kaal(weekday, sunrise, sunset)}")
    print(f"Yamaghanta (Expected 2nd part, 07:30-09:00):  {_yamaghanta(weekday, sunrise, sunset)}")

if __name__ == "__main__":
    test_kaal()
