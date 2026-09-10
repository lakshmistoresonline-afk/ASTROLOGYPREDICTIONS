import pytest
from datetime import datetime
from app.astrology.predictions.v10_transit_notifier import v10_transit_notifier
from app.astrology.predictions.v10_synastry import v10_synastry_engine

class MockChart:
    def __init__(self):
        self.planets = {}

def test_v10_transit_notifications():
    chart = MockChart()
    alerts = v10_transit_notifier.check_transit_triggers(chart, datetime(2026, 9, 10))
    assert len(alerts) > 0
    assert alerts[0]["planet"] == "Jupiter"

def test_v10_synastry_compatibility():
    chart_a = MockChart()
    chart_b = MockChart()
    res = v10_synastry_engine.calculate_compatibility(chart_a, chart_b)
    assert res["total_score_out_of_36"] == 28
    assert res["compatibility_rating"] == "HIGHLY_FAVORABLE"
