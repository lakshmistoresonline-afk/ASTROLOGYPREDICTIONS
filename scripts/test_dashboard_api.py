import requests
import sys

s = requests.Session()
BASE_URL = "http://127.0.0.1:5001"

def get_info(pid):
    print(f"\nLoading profile {pid}...")
    s.get(f'{BASE_URL}/kundli/load/{pid}?next=dashboard')
    r = s.get(f'{BASE_URL}/api/v1/debug/dashboard-data')
    return r.json()

if __name__ == "__main__":
    sectors = ["Personality & Essence", "Finance & Wealth", "Career & Authority", "Marriage & Relationships"]

    print("Testing Profile A (de9427a1 - Subramanian)...")
    try:
        d1 = get_info('de9427a1')
        print(f"Name: {d1.get('profile_name')}")
        print(f"Top: {d1.get('top_signal', {}).get('domain')} -> {d1.get('top_signal', {}).get('score')}")
    except Exception as e:
        print(f"Error testing server: {e}")
