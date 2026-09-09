import pytest
from app.astrology.outcomes.historical_adapter import load_historical_cases_dataset

def test_historical_cases_adapter_import():
    res = load_historical_cases_dataset()
    assert res["success"] is True
    assert res["record_count"] > 0
    assert res["meta"]["accepted_count"] == res["record_count"]
