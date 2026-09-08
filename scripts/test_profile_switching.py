import requests
import re
import sys

s = requests.Session()
BASE_URL = "http://127.0.0.1:5001"

def get_dash_info():
    r = s.get(f"{BASE_URL}/dashboard")
    if r.status_code != 200:
        return f"Error: {r.status_code}"

    html = r.text
    name = re.search(r'Active Profile:</span>\s*<span[^>]*>([^<]+)</span>', html)
    score = re.search(r'score-hero[^>]*>(\d+)</span>', html)

    return {
        "name": name.group(1).strip() if name else "None",
        "score": score.group(1) if score else "None"
    }

def load_profile(pid):
    print(f"Loading profile {pid}...")
    r = s.get(f"{BASE_URL}/kundli/load/{pid}?next=dashboard", allow_redirects=True)
    print(f"Final URL: {r.url}")

print("Initial Dashboard Info:")
print(get_dash_info())

print("\n--- SWITCHING TO SUBRAMANIAN (de9427a1) ---")
load_profile('de9427a1')
info_a = get_dash_info()
print(f"Dashboard A: {info_a}")

print("\n--- SWITCHING TO GATEV323 (913637d9) ---")
load_profile('913637d9')
info_b = get_dash_info()
print(f"Dashboard B: {info_b}")

if info_a['name'] != info_b['name']:
    print("\n✅ PASS: Profile switching works.")
else:
    print("\n❌ FAIL: Profile switching failed.")
