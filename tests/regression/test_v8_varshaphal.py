import pytest
from datetime import datetime
from app.astrology.predictions.v8_varshaphal import v8_varshaphal_engine

def test_v8_solar_return_calculation():
    birth_dt = datetime(1986, 9, 28, 16, 30)
    res = v8_varshaphal_engine.calculate_solar_return(birth_dt, 2026)
    assert res["target_year"] == 2026
    assert res["varshesha"] == "Sun"
    assert res["engine_version"] == "V8.0-PROD"
