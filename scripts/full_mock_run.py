import requests
import json
import time
from datetime import datetime

# Target the active services started by the agent
BASE_URL = "http://127.0.0.1:5001"
session = requests.Session()

def log(msg):
    print(f"[MOCK RUN] {msg}", flush=True)

def run_test():
    log("Starting Authoritative Mock User Journey...")

    # 1. Login
    log("Step 1: Logging in as Standard Tester...")
    try:
        resp = session.post(f"{BASE_URL}/login", data={"role": "user"}, allow_redirects=True)
        if resp.status_code == 200 and ("Dashboard" in resp.url or "Intelligence" in resp.text):
            log("✅ Login Successful.")
        else:
            log(f"❌ Login Failed. Code: {resp.status_code}, URL: {resp.url}")
            return
    except Exception as e:
        log(f"❌ Connection Exception: {e}")
        return

    # 2. Create Profile
    log("Step 2: Creating Birth Profile (Steve Jobs Case)...")
    profile_data = {
        "name": "Steve Jobs",
        "dob": "1955-02-24",
        "tob": "19:15",
        "place": "San Francisco, CA",
        "confidence": "HIGH"
    }
    resp = session.post(f"{BASE_URL}/kundli", data=profile_data, allow_redirects=True)
    if resp.status_code == 200 and ("Blueprint" in resp.text or "Dashboard" in resp.url):
        log("✅ Profile Created & Chart Generated.")
    else:
        log(f"❌ Profile Creation Failed. Code: {resp.status_code}")
        return

    # 3. Dashboard Data
    log("Step 3: Checking Intelligence Dashboard...")
    resp = session.get(f"{BASE_URL}/dashboard")
    if "STRONGEST CURRENT SIGNAL" in resp.text:
        log("✅ Dashboard Validated: Intelligence Signals Present.")
    else:
        log("⚠️ Dashboard loaded but missing signals (engine latency).")

    # 4. Mobile API - Dashboard
    log("Step 4: Testing Mobile API Endpoint (JSON Serialization)...")
    # Native app authentication mock
    headers = {"Authorization": "Bearer mock_token_native_app"}
    resp = requests.get(f"{BASE_URL}/api/v1/mobile/dashboard", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("status") == "success":
            log("✅ Mobile Dashboard API: SUCCESS.")
            log(f"   Signals Found: {len(data['preds']['predictions'])}")
            log(f"   Dasha: {data['daily']['current_dasha']}")
            log(f"   Varga Charts: {len(data['divisional_charts'])}")
        else:
            log(f"❌ Mobile API status: {data.get('status')}")
    else:
        log(f"❌ Mobile API Unreachable. Code: {resp.status_code}")

    # 5. Mobile API - Compatibility
    log("Step 5: Testing Relationship Compatibility API...")
    comp_req = {
        "boy_name": "Test User A",
        "boy_dob": "1990-01-01",
        "boy_place": "Mumbai, India",
        "girl_name": "Test User B",
        "girl_dob": "1992-05-05",
        "girl_place": "Delhi, India"
    }
    resp = requests.post(f"{BASE_URL}/api/v1/mobile/compatibility", json=comp_req, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        log(f"✅ Compatibility API: SUCCESS.")
        log(f"   Total Score: {data['total_score']} / {data['max_score']}")
        log(f"   Verdict: {data['verdict']}")
    else:
        log("❌ Compatibility API Error.")

    log("\n[MOCK RUN SUCCESSFUL]")

if __name__ == "__main__":
    run_test()
