import requests

s = requests.Session()
BASE_URL = "http://127.0.0.1:5001"

def check(pid):
    print(f"--- Loading {pid} ---")
    r = s.get(f"{BASE_URL}/kundli/load/{pid}?next=dashboard", allow_redirects=False)
    print(f"Redirect to: {r.headers.get('Location')}")
    # Cookies should have session updated

    r2 = s.get(f"{BASE_URL}/dashboard")
    import re
    name = re.search(r'Active Profile:</span>\s*<span[^>]*>([^<]+)</span>', r2.text)
    print(f"Name in HTML: {name.group(1).strip() if name else 'None'}")

print("Step 1: Load Subramanian (de9427a1)")
check('de9427a1')

print("\nStep 2: Load GateV323 (913637d9)")
check('913637d9')
