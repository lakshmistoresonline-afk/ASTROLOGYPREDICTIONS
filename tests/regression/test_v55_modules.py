import pytest
from datetime import datetime
from app.astrology.backtesting.v55_historical_replay import V55HistoricalReplayEngine
from app.astrology.evaluation.v55_event_metrics import calculate_event_level_metrics
from app.astrology.calibration.v55_calibration import evaluate_v55_calibration
from app.astrology.backtesting.v55_sample_governance import govern_sample_size

def test_historical_replay_cutoff():
    engine = V55HistoricalReplayEngine("ds1", datetime(1980, 1, 1))
    res = engine.replay_case({"name": "Jobs"}, {"date": "1980-12-12", "domain": "Career & Authority"})
    assert res["leakage_prevented"] is True

def test_event_metrics_insufficient():
    res = calculate_event_level_metrics([], [])
    assert res["status"] == "INSUFFICIENT_SAMPLE"

def test_calibration_insufficient():
    res = evaluate_v55_calibration([])
    assert res["calibration_status"] == "INSUFFICIENT_SAMPLE"

def test_sample_governance():
    res = govern_sample_size(5, 39)
    assert res["governance_status"] == "INSUFFICIENT_SAMPLE"
