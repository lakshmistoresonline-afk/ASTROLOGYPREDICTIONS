import requests
import json
import sqlite3
import os
import sys

BASE = 'http://127.0.0.1:5001'

def check():
    print("--- V3.22 RUNTIME GATE CHECK ---")
    s = requests.Session()

    # 1. Onboarding
    print("[1] Onboarding Dashboard...")
    payload = {"name": "V322Tester", "dob": "1990-01-01", "tob": "12:00", "place": "Palakkad", "lat": 10.78, "lon": 76.65, "timezone": "Asia/Kolkata"}
    s.post(f"{BASE}/kundli", data=payload)
    r = s.get(f"{BASE}/dashboard")
    if "Priority Insight" in r.text and "V3.22 Engine Active" in r.text:
        print("✅ Dashboard: PASS (Hero signal & Spec active)")
    else:
        print("❌ Dashboard: FAIL")

    # 2. Timeline & Clusters
    print("[2] Timeline & Clustering...")
    r = s.get(f"{BASE}/timeline")
    if "CONFLUENCE CLUSTERS" in r.text:
        print("✅ Clustering: PASS")
    else:
        print("❌ Clustering: FAIL")

    # 3. PDF Redesign
    print("[3] PDF Redesign...")
    r_pdf = s.get(f"{BASE}/report/download")
    if r_pdf.status_code == 200 and len(r_pdf.content) > 10000:
        print(f"✅ PDF: PASS ({len(r_pdf.content)} bytes)")
    else:
        print(f"❌ PDF: FAIL")

    # 4. Prospective Verification
    print("[4] Prospective Rejection...")
    import sqlite3
    conn = sqlite3.connect('D:/ASTROLOGYPREDICTIONS/data/app.db')
    c = conn.cursor()
    c.execute("SELECT id FROM prediction_outcomes WHERE source_type='REAL_WORLD' ORDER BY created_at DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        eid = row[0]
        r_verify = s.post(f"{BASE}/api/v1/outcome/update", json={"id": eid, "actual_date": "1980-01-01", "status": "OCCURRED"})
        if r_verify.status_code == 400:
            print("✅ Prospective Enforcement: PASS (Rejected retrospective)")
        else:
            print(f"❌ Prospective Enforcement: FAIL ({r_verify.status_code})")

    # 5. Regression
    print("[5] Regression Baseline...")
    import subprocess
    reg_proc = subprocess.run([sys.executable, "scripts/v314_validation.py"], capture_output=True, text=True)
    if '"precision": 0.6071428571428571' in reg_proc.stdout:
        print("✅ V3.15 Regression: PASS")
    else:
        print("❌ V3.15 Regression: FAIL")

if __name__ == "__main__":
    check()
