import json
import os
import pytest
from datetime import datetime
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.astrology.core.chart import calculate_chart_data
from app.astrology.panchang import calculate_panchang_2_0

BASELINE_DIR = os.path.join(os.path.dirname(__file__), "baselines")

def get_baselines():
    if not os.path.exists(BASELINE_DIR):
        return []
    files = [f for f in os.listdir(BASELINE_DIR) if f.endswith(".json")]
    cases = []
    for f in files:
        with open(os.path.join(BASELINE_DIR, f), "r") as fb:
            cases.append(json.load(fb))
    return cases

@pytest.mark.parametrize("baseline", get_baselines())
def test_baseline_consistency(baseline):
    tc = baseline["test_case"]

    birth_dt = datetime.strptime(f"{tc['dob']} {tc['tob']}", "%Y-%m-%d %H:%M")

    new_chart = calculate_chart_data(
        birth_dt, tc['lat'], tc['lon'], tc['tz']
    )

    new_panchang = calculate_panchang_2_0(
        birth_dt.date(), tc['lat'], tc['lon'], tc['tz']
    )

    # Compare chart (critical fields)
    old_chart = baseline["chart"]

    # Check Lagna
    assert new_chart["ascendant"] == pytest.approx(old_chart["ascendant"], abs=1e-4)

    # Check Planets
    for p_name in old_chart["planets"]:
        assert new_chart["planets"][p_name]["longitude"] == pytest.approx(old_chart["planets"][p_name]["longitude"], abs=1e-4)
        assert new_chart["planets"][p_name]["rashi"] == old_chart["planets"][p_name]["rashi"]

    # Compare Panchang
    old_pan = baseline["panchang"]
    assert new_panchang["tithi"]["number"] == old_pan["tithi"]["number"]
    assert new_panchang["nakshatra"]["number"] == old_pan["nakshatra"]["number"]
    assert new_panchang["yoga"]["number"] == old_pan["yoga"]["number"]
    assert new_panchang["karana"]["number"] == old_pan["karana"]["number"]
