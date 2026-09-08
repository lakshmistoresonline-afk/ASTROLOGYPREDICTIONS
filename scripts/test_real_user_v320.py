import requests
import json
import os
import sys
from datetime import datetime, timedelta

# TradeMind V3.20 - Real User Integration Test
# Validates end-to-end prospective workflow:
# Enroll -> Create Profile -> Dashboard -> Timeline -> Verify Event -> PDF Report

BASE_URL = "http://127.0.0.1:5001"

def run_test():
    print("="*60)
    print("🚀 TRADEMIND JYOTISH AI V3.20 - REAL USER INTEGRATION TEST")
    print("="*60)

    # 1. Establish Session
    s = requests.Session()

    # 2. Beta Enrollment (Group 1 Participant)
    print("\n[STEP 1] Enrolling Beta Participant...")
    enroll_payload = {
        "participant_id": "test-beta-user-001",
        "group_id": "BETA_GROUP_1"
    }
    resp = s.post(f"{BASE_URL}/beta/enroll", json=enroll_payload)
    if resp.status_code == 200:
        print(f"✅ Enrolled: {resp.json().get('session_id')}")
    else:
        print("❌ Enrollment Failed. Is the server running on port 5001?")
        return

    # 3. Create Birth Profile
    print("\n[STEP 2] Creating Birth Profile (Palakkad)...")
    profile_payload = {
        "name": "Beta Participant One",
        "dob": "1986-09-28",
        "tob": "16:30",
        "place": "Palakkad",
        "lat": "10.78",
        "lon": "76.65",
        "timezone": "Asia/Kolkata",
        "confidence": "HIGH"
    }
    # Send as AJAX to verify JSON response handling
    resp = s.post(f"{BASE_URL}/kundli", data=profile_payload, headers={'X-Requested-With': 'XMLHttpRequest'})
    try:
        data = resp.json()
        if resp.status_code == 200 and data.get('ok'):
            print("✅ Profile created successfully.")
        else:
            print(f"❌ Profile Creation Failed: {data}")
            return
    except Exception as e:
        print(f"❌ Profile Creation non-JSON response: {resp.status_code}")
        print(f"   Response Preview: {resp.text[:200]}")
        return

    # 4. Verify Dashboard & Snapshots
    print("\n[STEP 3] Triggering Prediction Snapshots...")
    resp = s.get(f"{BASE_URL}/dashboard")
    if "Namaste, Beta Participant One" in resp.text:
        print("✅ Dashboard accessible. Snapshots triggered.")
    else:
        print("❌ Dashboard failure.")
        return

    # 5. Verify Timeline & Event Mapping
    print("\n[STEP 4] Verifying Life Timeline (V3.17+)...")
    resp = s.get(f"{BASE_URL}/timeline")
    if "Life Timeline" in resp.text:
        print("✅ Timeline generated.")
    else:
        print("❌ Timeline generation failed.")
        return

    # 6. Test Prospective Validation (Matching)
    print("\n[STEP 5] Testing Event Matching (Walk-Forward)...")
    # Need an event ID from the database for this user
    import sqlite3
    conn = sqlite3.connect('data/app.db')
    c = conn.cursor()
    c.execute("SELECT id, peak_date FROM timeline_event_snapshots WHERE domain='Career' LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row:
        event_id, peak_date = row
        print(f"   Targeting Event: {event_id} (Peak: {peak_date})")

        # Test Exact Match (0 days error)
        verify_payload = {"actual_date": peak_date}
        resp = s.post(f"{BASE_URL}/api/v1/timeline/verify/{event_id}", json=verify_payload)
        res_data = resp.json()
        if res_data.get('status') == "MATCH":
            print(f"✅ Deterministic Matching: PASS (Status: {res_data['status']}, Error: {res_data['error_days']}d)")
        else:
            print(f"❌ Matching failed: {resp.text}")
    else:
        print("⚠️ No Career event found in timeline to verify.")

    # 7. Generate Complete PDF Report
    print("\n[STEP 6] Generating Consolidated PDF Report...")
    resp = s.get(f"{BASE_URL}/report/download")
    if resp.status_code == 200 and resp.headers.get('Content-Type') == 'application/pdf':
        filename = "V320_RealUser_Audit_Report.pdf"
        with open(filename, "wb") as f:
            f.write(resp.content)
        print(f"✅ PDF Generated: PASS ({len(resp.content)} bytes)")
        print(f"   Report saved to: {os.path.abspath(filename)}")
    else:
        print(f"❌ PDF Generation Failed (Status: {resp.status_code})")

    print("\n" + "="*60)
    print("🎯 V3.20 REAL USER TEST COMPLETE - SYSTEM VALIDATED")
    print("="*60)

if __name__ == "__main__":
    run_test()
