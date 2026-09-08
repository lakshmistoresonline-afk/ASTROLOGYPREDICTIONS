import requests
import sys

s = requests.Session()
BASE_URL = "http://127.0.0.1:5001"

def get_info(pid):
    print(f"\nLoading profile {pid}...")
    s.get(f'{BASE_URL}/kundli/load/{pid}?next=dashboard')
    r = s.get(f'{BASE_URL}/api/v1/debug/dashboard-data')
    return r.json()

sectors = ["Personality & Essence", "Finance & Wealth", "Career & Authority", "Marriage & Relationships"]

print("Testing Profile A (de9427a1 - Subramanian)...")
d1 = get_info('de9427a1')
print(f"Name: {d1.get('profile_name')}")
print(f"Top: {d1.get('top_signal', {}).get('domain')} -> {d1.get('top_signal', {}).get('score')}")
print("Sectors:")
for d in sectors:
    print(f"  {d}: {d1.get('domain_scores', {}).get(d)}%")

print("\nTesting Profile B (913637d9 - GateV323)...")
d2 = get_info('913637d9')
print(f"Name: {d2.get('profile_name')}")
print(f"Top: {d2.get('top_signal', {}).get('domain')} -> {d2.get('top_signal', {}).get('score')}")
print("Sectors:")
for d in sectors:
    print(f"  {d}: {d2.get('domain_scores', {}).get(d)}%")

if d1.get('profile_name') != d2.get('profile_name'):
    print("\n✅ PASS: Profile name changed dynamically.")
else:
    print("\n❌ FAIL: Profile name is stuck.")

if d1.get('top_signal', {}).get('score') != d2.get('top_signal', {}).get('score'):
    print("✅ PASS: Intelligence score changed dynamically.")
else:
    print("⚠️  INFO: Intelligence score is identical.")
