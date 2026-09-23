import pytest
from app.astrology.core.kp import kp_engine, KPEngine, KPSubLordResult

def test_kp_sub_lord_favorable_promise():
    planet_data = {
        "name": "Jupiter",
        "star_lord": "Sun",
        "sub_lord": "Venus",
        "significators": [1, 5, 9, 10, 11],
        "sub_lord_significators": [2, 7, 11] # Favorable houses
    }

    res = kp_engine.evaluate_promise(planet_data, target_house=10)

    assert isinstance(res, KPSubLordResult)
    assert res.planet == "Jupiter"
    assert res.star_lord == "Sun"
    assert res.sub_lord == "Venus"
    assert res.favorable is True
    assert res.significators == [1, 5, 9, 10, 11]

def test_kp_sub_lord_unfavorable_promise():
    planet_data = {
        "name": "Saturn",
        "star_lord": "Mars",
        "sub_lord": "Rahu",
        "significators": [6, 8, 12],
        "sub_lord_significators": [6, 8, 12] # Detrimental houses
    }

    res = kp_engine.evaluate_promise(planet_data, target_house=10)

    assert isinstance(res, KPSubLordResult)
    assert res.planet == "Saturn"
    assert res.favorable is False
