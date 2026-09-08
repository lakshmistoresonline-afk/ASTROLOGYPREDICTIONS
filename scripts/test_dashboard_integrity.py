import requests
import re
import sys

# Test script for V3.22 Dashboard Data-Binding Integrity
# Profiles:
# A: de9427a1 (Subramanian T S)
# B: 913637d9 (GateV323)

BASE_URL = "http://127.0.0.1:5001"

def get_dashboard_info(session, pid):
    print(f"\n--- TESTING PROFILE {pid} ---")
    # 1. Load profile
    load_url = f"{BASE_URL}/kundli/load/{pid}?next=dashboard"
    r = session.get(load_url, allow_redirects=True)
    if r.status_code != 200:
        return f"Error loading profile: {r.status_code}"

    html = r.text

    # 2. Extract key fields
    name_match = re.search(r'Active Profile:</span>\s*<span[^>]*>([^<]+)</span>', html)
    score_match = re.search(r'score-hero[^>]*>(\d+)</span>', html)
    hero_match = re.search(r'display-hero[^>]*>([^<]+)</h1>', html)

    info = {
        "name": name_match.group(1).strip() if name_match else "NOT_FOUND",
        "score": score_match.group(1) if score_match else "NOT_FOUND",
        "hero": hero_match.group(1).strip() if hero_match else "NOT_FOUND"
    }

    print(f"Detected Name: {info['name']}")
    print(f"Detected Score: {info['score']}")
    print(f"Detected Hero: {info['hero']}")

    return info

def run_test():
    s = requests.Session()

    print("STAGING TEST: V3.22 DATA BINDING")

    # Test Profile A
    info_a = get_dashboard_info(s, 'de9427a1')

    # Test Profile B
    info_b = get_dashboard_info(s, '913637d9')

    print("\n" + "="*40)
    print("FINAL INTEGRITY RESULT")
    print("="*40)

    if info_a['name'] == info_b['name']:
        print("❌ FAIL: Profile name did not change.")
    elif info_a['score'] == info_b['score'] and info_a['hero'] == info_b['hero']:
        print("⚠️  WARNING: Intelligence values are identical. Check if engine is dynamic.")
    else:
        print("✅ PASS: Dashboard data is dynamic and profile-dependent.")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"Test Execution Failed: {e}")
        sys.exit(1)
