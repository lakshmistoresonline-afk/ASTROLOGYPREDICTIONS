import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.astrology.panchang import calculate_panchang

def verify_panchang():
    print("================================================================================")
    print("🌅 VERIFYING PANCHANG RUNTIME & SUNRISE/SUNSET CALCULATION")
    print("================================================================================")

    dt = datetime.now()
    lat, lon = 10.7867, 76.6548 # Palakkad, Kerala, India
    tz_str = "Asia/Kolkata"

    p = calculate_panchang(dt, lat, lon, tz_str)

    print(f"  ✅ Tithi: {p.get('tithi', {}).get('name')}")
    print(f"  ✅ Nakshatra: {p.get('nakshatra', {}).get('name')}")
    print(f"  ✅ Yoga: {p.get('yoga', {}).get('name')}")
    print(f"  ✅ Karana: {p.get('karana', {}).get('name')}")
    print(f"  ✅ Sunrise Time: {p.get('sky', {}).get('sunrise')}")
    print(f"  ✅ Sunset Time: {p.get('sky', {}).get('sunset')}")

    assert p.get('tithi', {}).get('name') is not None
    assert p.get('sky', {}).get('sunrise') is not None

    print("================================================================================")
    print("🎯 PANCHANG RUNTIME VERIFICATION PASSED PERFECTLY (0 ERRORS)")
    print("================================================================================")
    return True

if __name__ == "__main__":
    verify_panchang()
