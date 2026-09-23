import pytest
from app.astrology.timing.kakshya import kakshya_evaluator, KAKSHYA_LORDS
from app.astrology.timing.nadi import nadi_transit_grid

def test_module7_kakshya_subzone_divisions():
    # Test 0.0 deg (Aries Kakshya 0 -> Saturn)
    k0 = kakshya_evaluator.get_kakshya_info(0.0)
    assert k0["rashi"] == 0
    assert k0["kakshya_index"] == 0
    assert k0["kakshya_lord"] == "Saturn"

    # Test 3.8 deg (Aries Kakshya 1 -> Jupiter)
    k1 = kakshya_evaluator.get_kakshya_info(3.8)
    assert k1["rashi"] == 0
    assert k1["kakshya_index"] == 1
    assert k1["kakshya_lord"] == "Jupiter"

    # Test 29.5 deg (Aries Kakshya 7 -> Lagna)
    k7 = kakshya_evaluator.get_kakshya_info(29.5)
    assert k7["rashi"] == 0
    assert k7["kakshya_index"] == 7
    assert k7["kakshya_lord"] == "Lagna"

def test_module7_kakshya_bav_evaluation():
    bav_matrix = {"Jupiter": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]}
    natal_rashis = {"Saturn": 0, "Jupiter": 1, "Mars": 2}

    # Transit Jupiter in Aries at 1.0 deg (Kakshya 0 -> Saturn)
    # BAV for Aries (index 0) = 1 (High Activation)
    res_high = kakshya_evaluator.evaluate_transit_kakshya("Jupiter", 1.0, bav_matrix, natal_rashis)
    assert res_high["activation_status"] == "HIGH_ACTIVATION"
    assert res_high["has_bav_bindu"] is True

def test_module7_nadi_directional_trines():
    # Natal Sun at 10.0 deg Leo (Fire Element)
    # Transit Jupiter at 11.5 deg Aries (Fire Element, 1st/5th/9th directional trine)
    # Diff = 11.5 - 10.0 = 1.5 deg (within +/- 2.5 deg orb tolerance)
    transit_planets = {"Jupiter": 11.5}
    natal_planets = {"Sun": 130.0} # 130 deg = 10.0 deg Leo (Fire sign)

    triggers = nadi_transit_grid.evaluate_nadi_aspects(transit_planets, natal_planets, orb_tolerance=2.5)
    assert len(triggers) == 1
    assert triggers[0]["transiting_planet"] == "Jupiter"
    assert triggers[0]["natal_planet"] == "Sun"
    assert triggers[0]["nadi_element"] == "FIRE"
    assert triggers[0]["orb_error"] == 1.5
