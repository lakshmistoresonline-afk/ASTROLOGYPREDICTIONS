import pytest
from datetime import datetime
from app.astrology.predictions.v7_lifespan_engine import v7_lifespan_engine

class MockDasha:
    def __init__(self, lord, start, end):
        self.lord = lord
        self.start = start
        self.end = end

class MockChart:
    def __init__(self, birth_datetime):
        self.birth_datetime = birth_datetime

def test_v7_life_atlas_generation():
    chart = MockChart(datetime(1986, 9, 28, 16, 30))
    dashas = [
        MockDasha("Rahu", "1986-09-28", "2004-09-28"),
        MockDasha("Jupiter", "2004-09-28", "2020-09-28")
    ]
    atlas = v7_lifespan_engine.build_life_atlas(chart, dashas)
    assert atlas["birth_date"] == "1986-09-28"
    assert len(atlas["lifespan_chapters"]) == 2
    assert atlas["engine_version"] == "V7.0-PROD"
