import pytest
from datetime import datetime
from app.astrology.predictions.v10_transit_notifier import v10_transit_notifier
from app.astrology.predictions.v10_synastry import v10_synastry_engine

class MockPlanet:
    def __init__(self, house, is_retrograde=False):
        self.house = house
        self.is_retrograde = is_retrograde

class MockChart:
    def __init__(self, moon_long=45.0, planets=None):
        self.moon_long = moon_long
        self.planets = planets or {"Jupiter": MockPlanet(10, False)}

def test_v10_transit_notifications():
    chart = MockChart()
    alerts = v10_transit_notifier.check_transit_triggers(chart, datetime(2026, 9, 10))
    assert len(alerts) > 0
    assert alerts[0]["planet"] == "Jupiter"

def test_v10_synastry_compatibility():
    chart_a = MockChart(moon_long=45.0)
    chart_b = MockChart(moon_long=50.0)
    res = v10_synastry_engine.calculate_compatibility(chart_a, chart_b)
    assert res["total_score_out_of_36"] > 25.0
    assert res["compatibility_rating"] in ["GOOD", "EXCELLENT", "FAVORABLE"]
