import requests

s = requests.Session()
BASE_URL = "http://127.0.0.1:5001"

pid = 'de9427a1'
s.get(f"{BASE_URL}/kundli/load/{pid}?next=dashboard")
r = s.get(f"{BASE_URL}/dashboard")
print(r.text[:2000])
