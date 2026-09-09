import pytest
from datetime import datetime
from app.astrology.backtesting.pipeline_connector import pipeline_connector
from app.astrology.outcomes.taxonomy import normalize_event_type
from app.astrology.backtesting.leakage_guard import validate_no_leakage

def test_event_normalization():
    assert normalize_event_type("wedding") == "marriage"
    assert normalize_event_type("Promotion") == "promotion"
    assert normalize_event_type("unknown_custom_event") == "other_major_life_event"

def test_pipeline_quality_gates():
    bad_record = {"person_id": None, "event_date": "2020-01-01", "source": "test"}
    res = pipeline_connector.import_and_validate_record(bad_record)
    assert res["accepted"] is False
    assert res["reason"] == "INSUFFICIENT_BIRTH_DATA"

def test_leakage_guard_assertion():
    cutoff = datetime(2020, 1, 1)
    past_timestamp = datetime(2019, 5, 1)
    future_timestamp = datetime(2021, 1, 1)

    assert validate_no_leakage(cutoff, past_timestamp) is True
    assert validate_no_leakage(cutoff, future_timestamp) is False

def test_readiness_state_n_zero():
    report = pipeline_connector.get_readiness_report()
    assert report["real_outcome_count"] == 0
    assert report["status_message"] == "BLOCKED — NO REAL OUTCOME DATA"
