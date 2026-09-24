import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.store import save_chart

def verify_all_authenticated_routes():
    print("================================================================================")
    print("🌐 MULTI-PAGE AUTHENTICATED DASHBOARD ROUTE VERIFICATION")
    print("================================================================================")

    app = create_app()
    client = app.test_client()

    # Save a valid chart profile to database
    with app.app_context():
        chart_data = {
            "name": "Subramanian T S",
            "birth_dob": "1986-09-28",
            "birth_tob": "16:30",
            "birth_place": "Palakkad, Kerala, India",
            "latitude": 10.7867,
            "longitude": 76.6548,
            "timezone": "Asia/Kolkata"
        }
        cid = save_chart("uid_tester", chart_data)

    routes_to_test = [
        ("/dashboard", "Dashboard / Executive Briefing"),
        ("/kundli", "Birth Chart / Varga Canvas"),
        ("/predictions", "Forecasts & 16 Confluent Life Domains"),
        ("/timeline", "Life Atlas Milestone Roadmap"),
        ("/cosmic_dna", "Cosmic DNA & BaZi Four Pillars"),
        ("/showcase", "Historical Benchmark Replay Engine"),
        ("/matchmaking", "Ashtakoota Marriage Compatibility"),
        ("/transit", "Real-Time Gochara Transit Radar"),
        ("/prashna", "1-249 KP Seed Horary Engine"),
        ("/panchang", "Panchang & Muhurta Radar"),
        ("/varshaphala", "Tajika Annual Solar Return"),
        ("/history", "Vault & Saved Chart Profiles"),
        ("/dasha", "5-Level Vimshottari Hierarchy"),
        ("/ashtakavarga", "337 Parashari Points & Shodhya Pinda"),
        ("/yogas", "50+ Classical Yogas & Raja Yoga Detector"),
        ("/admin/accuracy", "Validation & Accuracy Calibration"),
        ("/commercial/pricing", "Subscription Plans & Pricing Tier Hub")
    ]

    passed_routes = 0
    for route, label in routes_to_test:
        with client.session_transaction() as sess:
            sess["firebase_id_token"] = "mock_token_admin"
            sess["firebase_uid"] = "uid_tester"
            sess["birth_name"] = "Subramanian T S"
            sess["is_admin"] = True
            sess["active_chart_id"] = cid

        response = client.get(route, follow_redirects=True)
        if response.status_code == 200:
            html = response.get_data(as_text=True)

            # Assert Dark Celestial App Shell is present
            has_app_shell = ("app-sidebar" in html) or ("app-header" in html) or ("ASTRO PREDICTIONS" in html)
            has_no_developer_bypass = "Sign in as Standard Tester" not in html

            if has_app_shell and has_no_developer_bypass:
                print(f"   ✅ [200 OK] {route} ({label}) — Dark Celestial Shell Active")
                passed_routes += 1
            else:
                print(f"   ⚠️ [200 OK] {route} ({label}) — Shell verification warning")
        else:
            print(f"   ❌ [{response.status_code}] {route} ({label})")

    total_routes = len(routes_to_test)
    print("================================================================================")
    print(f"🎯 AUTHENTICATED DASHBOARD ROUTE SUMMARY: {passed_routes}/{total_routes} ROUTES VERIFIED ({passed_routes/total_routes*100:.0f}%)")
    print("================================================================================")
    return passed_routes == total_routes

if __name__ == "__main__":
    verify_all_authenticated_routes()
