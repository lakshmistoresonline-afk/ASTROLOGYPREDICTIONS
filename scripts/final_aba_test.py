import requests
import re
import sys
import html

s = requests.Session()
BASE_URL = "http://127.0.0.1:5001"

def capture_dash(pid):
    print(f"\n--- TESTING PROFILE {pid} ---")
    try:
        # Load profile
        load_r = s.get(f"{BASE_URL}/kundli/load/{pid}?next=dashboard", timeout=120)
        # Get dashboard
        r = s.get(f"{BASE_URL}/dashboard", timeout=120)

        text = html.unescape(r.text)

        name_m = re.search(r'Active Profile:</span>\s*<span[^>]*>([^<]+)</span>', text)
        score_m = re.search(r'score-hero[^>]*>(\d+)</span>', text)
        hero_m = re.search(r'display-hero[^>]*>([^<]+)</h1>', text)
        dasha_m = re.search(r'Current Life Phase</div>\s*<div[^>]*>([^<]+)</div>', text)

        name = name_m.group(1).strip() if name_m else "None"
        score = score_m.group(1) if score_m else "None"
        hero = hero_m.group(1).strip() if hero_m else "None"
        dasha = dasha_m.group(1).strip() if dasha_m else "None"

        print(f"Name: {name}")
        print(f"Score: {score}")
        print(f"Hero: {hero}")
        print(f"Dasha: {dasha}")

        return {'name': name, 'score': score, 'hero': hero}
    except Exception as e:
        print(f"Error: {e}")
        return None

def run_test():
    print("ABA TEST START")
    res_a1 = capture_dash('de9427a1')
    res_b = capture_dash('913637d9')
    res_a2 = capture_dash('de9427a1')

    print("\n" + "="*40)
    if res_a1 and res_b and res_a2:
        # Success criteria
        name_match = (res_a1['name'] == 'Subramanian T S' and res_b['name'] == 'GateV323' and res_a2['name'] == 'Subramanian T S')
        score_diff = (res_a1['score'] != res_b['score'])
        hero_diff = (res_a1['hero'] != res_b['hero'])

        if name_match:
            print("✅ PASS: Profile switching verified.")
        else:
            print("❌ FAIL: Profile switching failed.")

        if score_diff:
            print(f"✅ PASS: Data is profile-dependent (Scores: {res_a1['score']} vs {res_b['score']}).")
        else:
            print(f"⚠️  WARNING: Scores are identical ({res_a1['score']}).")

        if hero_diff:
            print(f"✅ PASS: Hero is profile-dependent (Hero: {res_a1['hero']} vs {res_b['hero']}).")
        else:
            print(f"⚠️  WARNING: Heroes are identical ({res_a1['hero']}).")

        if name_match and score_diff and hero_diff:
            print("\n🌟 V3.22 DATA BINDING INTEGRITY: PASSED")
        else:
            print("\n❌ V3.22 DATA BINDING INTEGRITY: FAILED")
    else:
        print("❌ FAIL: Test execution incomplete due to errors.")

if __name__ == "__main__":
    run_test()
