import requests
import sys

s = requests.Session()
BASE_URL = "http://127.0.0.1:5001"

try:
    print("Loading chart...")
    r1 = s.get(f"{BASE_URL}/kundli/load/de9427a1?next=dashboard", timeout=60)
    print(f"Load Status: {r1.status_code}")
    print(f"Redirects: {[res.url for res in r1.history]}")

    print("\nGetting Dashboard...")
    r2 = s.get(f"{BASE_URL}/dashboard", timeout=60)
    print(f"Dash Status: {r2.status_code}")
    print(f"Content Length: {len(r2.text)}")

    if "DASHBOARD_REPRESENTATION_ERROR" in r2.text:
        print("\n❌ FOUND ERROR PAGE IN CONTENT")
    else:
        print("\n✅ DASHBOARD CONTENT SEEMS VALID")
        print(f"Snippet: {r2.text[:200]}")

except Exception as e:
    print(f"Request failed: {e}")
