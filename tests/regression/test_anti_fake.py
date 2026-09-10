import pytest
from datetime import datetime
from app.astrology.predictions.v10_synastry import v10_synastry_engine
from app.astrology.predictions.v10_transit_notifier import v10_transit_notifier
from app.astrology.predictions.v8_varshaphal import v8_varshaphal_engine

class MockPlanet:
    def __init__(self, house, is_retrograde=False):
        self.house = house
        self.is_retrograde = is_retrograde

class MockChart:
    def __init__(self, moon_long=45.0, planets=None):
        self.moon_long = moon_long
        self.planets = planets or {}

def test_anti_fake_synastry_changes():
    chart_1 = MockChart(moon_long=30.0)
    chart_2 = MockChart(moon_long=60.0)
    chart_3 = MockChart(moon_long=240.0)

    res_1 = v10_synastry_engine.calculate_compatibility(chart_1, chart_2)
    res_2 = v10_synastry_engine.calculate_compatibility(chart_1, chart_3)

    assert res_1["total_score_out_of_36"] != res_2["total_score_out_of_36"]

def test_anti_fake_transit_notifier():
    chart_a = MockChart(planets={"Jupiter": MockPlanet(10, False)})
    chart_b = MockChart(planets={"Mars": MockPlanet(3, True)})

    alerts_a = v10_transit_notifier.check_transit_triggers(chart_a, datetime(2026, 9, 10))
    alerts_b = v10_transit_notifier.check_transit_triggers(chart_b, datetime(2026, 9, 10))

    assert len(alerts_a) == 1
    assert alerts_a[0]["planet"] == "Jupiter"
    assert len(alerts_b) == 0 # Mars not in monitored slow transits or differs

def test_anti_fake_varshaphal():
    birth = datetime(1986, 9, 28, 16, 30)
    res_2026 = v8_varshaphal_engine.calculate_solar_return(birth, 2026)
    res_2030 = v8_varshaphal_engine.calculate_solar_return(birth, 2030)

    assert res_2026["target_year"] == 2026
    assert res_2030["target_year"] == 2030
    assert res_2026["muntha_house"] != res_2030["muntha_house"]
