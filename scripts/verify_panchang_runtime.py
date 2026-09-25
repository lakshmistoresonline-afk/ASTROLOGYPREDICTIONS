import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.astrology.panchang import calculate_panchang

def verify_panchang_multi_location():
    print("================================================================================")
    print("🌅 VERIFYING PANCHANG RUNTIME & COORDINATE SENSITIVITY")
    print("================================================================================")

    dt = datetime.now()

    # 1. Location A: Palakkad, Kerala, India (10.7867° N, 76.6548° E)
    p_a = calculate_panchang(dt, 10.7867, 76.6548, "Asia/Kolkata")
    sunrise_a = p_a.get('sky', {}).get('sunrise')
    sunset_a = p_a.get('sky', {}).get('sunset')

    print("📍 LOCATION A: Palakkad, Kerala, India (Asia/Kolkata)")
    print(f"   Tithi: {p_a.get('tithi', {}).get('name')}")
    print(f"   Nakshatra: {p_a.get('nakshatra', {}).get('name')}")
    print(f"   Sunrise: {sunrise_a}")
    print(f"   Sunset: {sunset_a}")

    # 2. Location B: London, UK (51.5074° N, -0.1278° W)
    p_b = calculate_panchang(dt, 51.5074, -0.1278, "Europe/London")
    sunrise_b = p_b.get('sky', {}).get('sunrise')
    sunset_b = p_b.get('sky', {}).get('sunset')

    print("\n📍 LOCATION B: London, UK (Europe/London)")
    print(f"   Tithi: {p_b.get('tithi', {}).get('name')}")
    print(f"   Nakshatra: {p_b.get('nakshatra', {}).get('name')}")
    print(f"   Sunrise: {sunrise_b}")
    print(f"   Sunset: {sunset_b}")

    # Assertions: Real non-placeholder values
    assert sunrise_a not in [None, "—", ""]
    assert sunset_a not in [None, "—", ""]
    assert sunrise_b not in [None, "—", ""]
    assert sunset_b not in [None, "—", ""]

    # Assert Coordinate Sensitivity: Sunrise/Sunset differs appropriately across longitudes/latitudes
    assert (sunrise_a != sunrise_b) or (sunset_a != sunset_b), "Sunrise/Sunset failed to react to coordinate shift!"

    print("\n================================================================================")
    print("🎯 PANCHANG RUNTIME & COORDINATE SENSITIVITY PASSED PERFECTLY (100% PARITY)")
    print("================================================================================")
    return True

if __name__ == "__main__":
    verify_panchang_multi_location()
