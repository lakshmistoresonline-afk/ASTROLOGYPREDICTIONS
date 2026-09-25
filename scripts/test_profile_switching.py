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

if __name__ == "__main__":
    try:
        print("Initial Dashboard Info:")
        print(get_dash_info())
    except Exception as e:
        print(f"Live server test skipped: {e}")
