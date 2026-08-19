import json
import os
import pytest
from datetime import datetime
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.astrology.calculator import calculate_full_chart
from app.astrology.panchang import calculate_panchang

BASELINE_DIR = os.path.join(os.path.dirname(__file__), "baselines")

def get_baselines():
    files = [f for f in os.listdir(BASELINE_DIR) if f.endswith(".json")]
    cases = []
    for f in files:
        with open(os.path.join(BASELINE_DIR, f), "r") as fb:
            cases.append(json.load(fb))
    return cases

@pytest.mark.parametrize("baseline", get_baselines())
def test_baseline_consistency(baseline):
    tc = baseline["test_case"]
    print(f"Testing consistency for {tc['id']}...")

    birth_dt = datetime.strptime(f"{tc['dob']} {tc['tob']}", "%Y-%m-%d %H:%M")

    new_chart = calculate_full_chart(
        birth_dt, tc['lat'], tc['lon'], tc['tz'],
        name=tc['name'], place=tc['place']
    )

    new_panchang = calculate_panchang(
        birth_dt.date(), tc['lat'], tc['lon'], tc['tz']
    )

    # Compare chart (critical fields)
    old_chart = baseline["chart"]

    # Check Lagna
    assert new_chart["lagna"]["longitude"] == pytest.approx(old_chart["lagna"]["longitude"], abs=1e-4)

    # Check Planets
    for p_name in old_chart["planets"]:
        assert new_chart["planets"][p_name]["longitude"] == pytest.approx(old_chart["planets"][p_name]["longitude"], abs=1e-4)
        assert new_chart["planets"][p_name]["rashi"] == old_chart["planets"][p_name]["rashi"]

    # Compare Panchang
    old_pan = baseline["panchang"]
    assert new_panchang["tithi"]["number"] == old_pan["tithi"]["number"]
    assert new_panchang["nakshatra"]["name"] == old_pan["nakshatra"]["name"]
    assert new_panchang["yoga"]["name"] == old_pan["yoga"]["name"]
    assert new_panchang["karana"]["name"] == old_pan["karana"]["name"]
