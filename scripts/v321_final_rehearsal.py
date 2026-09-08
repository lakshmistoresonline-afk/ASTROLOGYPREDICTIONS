import requests
import json
import os
from datetime import datetime

# V3.21 Final Release Rehearsal
BASE_URL = "http://127.0.0.1:5001"

def rehearse():
    print("🚀 V3.21 RELEASE REHEARSAL")
    s = requests.Session()

    # 1. Onboarding
    print("\n[1] Creating Profile...")
    payload = {
        "name": "V321 Rehearsal Native",
        "dob": "1990-01-01", "tob": "12:00",
        "place": "Palakkad", "lat": 10.78, "lon": 76.65,
        "timezone": "Asia/Kolkata", "confidence": "HIGH"
    }
    s.post(f"{BASE_URL}/kundli", data=payload)

    # 2. Dashboard UX
    print("[2] Checking Dashboard UX (Clustering & Priority)...")
    resp = s.get(f"{BASE_URL}/dashboard")
    if "Personal Life Intelligence" in resp.text and "Signal Strength" in resp.text:
        print("✅ Dashboard: PASS")
    else:
        print("❌ Dashboard: FAIL (Unexpected content)")

    # 3. Specificity Check
    print("[3] Checking Prediction Specificity (Event Type)...")
    resp = s.get(f"{BASE_URL}/predictions")
    if "Trends" in resp.text or "ACTIVE" in resp.text:
        print("✅ Specificity: PASS")

    # 4. Timeline Clustering
    print("[4] Checking Lifetime Timeline & Clusters...")
    resp = s.get(f"{BASE_URL}/timeline")
    if "CONFLUENCE CLUSTERS" in resp.text:
        print("✅ Clustering: PASS")
    else:
        print("❌ Clustering: FAIL")

    # 5. Consolidated PDF
    print("[5] Generating V3.21 Premium PDF...")
    resp = s.get(f"{BASE_URL}/report/download")
    if resp.status_code == 200:
        print(f"✅ PDF Generation: PASS ({len(resp.content)} bytes)")
    else:
        print(f"❌ PDF Generation: FAIL ({resp.status_code})")

    print("\n🎯 V3.21 REHEARSAL COMPLETE")

if __name__ == "__main__":
    rehearse()
