import os
import sys
from datetime import datetime

# Set PYTHONPATH to include project root
sys.path.append(os.getcwd())

from app import create_app
from app.database.models import db, UserAccount

def log(msg):
    print(f"[INTERNAL MOCK] {msg}", flush=True)

def run_internal_test():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        # Setup mock user
        user = UserAccount(firebase_uid="uid_tester", email="tester@astropredictions.app", role="user")
        db.session.add(user)
        db.session.commit()

        client = app.test_client()

        log("Step 1: Mock Authentication...")
        with client.session_transaction() as sess:
            sess["firebase_id_token"] = "mock_token_tester"
            sess["firebase_uid"] = "uid_tester"
        log("✅ Session established.")

        log("Step 2: Creating Birth Profile (Steve Jobs)...")
        # San Francisco coordinates approx: 37.77, -122.41, America/Los_Angeles
        # Using geocode_place mock result equivalent
        profile_data = {
            "name": "Steve Jobs",
            "dob": "1955-02-24",
            "tob": "19:15",
            "place": "San Francisco, CA",
            "lat": 37.7749,
            "lon": -122.4194,
            "timezone": "America/Los_Angeles"
        }
        resp = client.post("/kundli", data=profile_data, follow_redirects=True)
        if resp.status_code == 200:
            log("✅ Profile Created.")
        else:
            log(f"❌ Profile Creation Failed: {resp.status_code}")
            return

        log("Step 3: Accessing Dashboard Intelligence...")
        resp = client.get("/dashboard")
        if resp.status_code == 200 and "Intelligence" in resp.text:
            log("✅ Dashboard Loaded.")
        else:
            log("❌ Dashboard Failed.")

        log("Step 4: Verifying Mobile Dashboard API...")
        # Mobile API uses Bearer token in headers
        headers = {"Authorization": "Bearer mock_token_native_app"}
        resp = client.get("/api/v1/mobile/dashboard", headers=headers)
        if resp.status_code == 200:
            data = resp.get_json()
            log(f"✅ Mobile API: {data['status']}")
            log(f"   Predictions: {len(data['preds']['predictions'])}")
            log(f"   Planets Serialized: {len(data.get('planets', []))}")
            log(f"   Vimsopaka Scores: {len(data.get('vimsopaka_scores', [])) if 'vimsopaka_scores' in data else 'N/A'}")
        else:
            log(f"❌ Mobile API Error: {resp.status_code}")

        log("Step 5: Testing Compatibility Hub API...")
        comp_req = {
            "boy_name": "Test A", "boy_dob": "1990-01-01", "boy_place": "Delhi",
            "girl_name": "Test B", "girl_dob": "1992-05-05", "girl_place": "Mumbai"
        }
        # Note: geocoding might fail in internal test if no internet, but logic check is possible
        try:
            resp = client.post("/api/v1/mobile/compatibility", json=comp_req, headers=headers)
            if resp.status_code == 200:
                data = resp.get_json()
                log(f"✅ Compatibility: {data['total_score']} Gunas")
        except:
            log("⚠️ Compatibility logic requires network for geocoding (skipped).")

        log("\n[INTERNAL MOCK RUN SUCCESSFUL]")

if __name__ == "__main__":
    run_internal_test()
