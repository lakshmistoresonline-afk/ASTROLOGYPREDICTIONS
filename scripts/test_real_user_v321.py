import requests
import json
import os
import sys
from datetime import datetime, timedelta

# TradeMind V3.21 - Validation Integrity Test
# Validates: simulated data isolation and version consistency

BASE_URL = "http://127.0.0.1:5001"

def run_test():
    print("="*60)
    print("🧪 TRADEMIND JYOTISH AI V3.21 - VALIDATION INTEGRITY TEST")
    print("="*60)

    s = requests.Session()

    # 1. Check Accuracy Dashboard
    print("\n[STEP 1] Checking Accuracy Isolation...")
    resp = s.get(f"{BASE_URL}/admin/accuracy")
    if "Prospective Precision" in resp.text and "Simulated Precision" in resp.text:
        print("✅ Dashboard: PASS (Separated view found)")
    else:
        print("❌ Dashboard: FAIL (Missing separated labels)")

    # 2. Check Database for V3.21
    print("\n[STEP 2] Verifying V3.21 Snapshot Creation...")
    payload = {
        "name": "Integrity Tester",
        "dob": "1990-01-01",
        "tob": "12:00",
        "place": "London",
        "lat": 51.5,
        "lon": -0.1,
        "timezone": "Europe/London",
        "confidence": "HIGH"
    }
    s.post(f"{BASE_URL}/kundli", data=payload)
    # Trigger snapshot
    s.get(f"{BASE_URL}/dashboard")

    import sqlite3
    conn = sqlite3.connect('data/app.db')
    c = conn.cursor()
    c.execute("SELECT engine_version FROM prediction_outcomes WHERE prediction_text LIKE '%Integrity Tester%' OR chart_id IN (SELECT id FROM charts WHERE name='Integrity Tester') LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row and row[0] == "V3.21":
        print("✅ Versioning: PASS (V3.21 stored)")
    else:
        print(f"❌ Versioning: FAIL (Got {row[0] if row else 'None'})")

    print("\n" + "="*60)
    print("🎯 V3.21 INTEGRITY TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_test()
