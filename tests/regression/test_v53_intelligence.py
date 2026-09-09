import pytest
from app.astrology.predictions.v53_hypothesis_engine import V53PredictionIntelligenceEngine

def test_hypothesis_engine_ranking():
    engine = V53PredictionIntelligenceEngine("CAREER")
    engine.add_candidate("promotion", 0.85, 0.1, ["Vimshottari", "Chara", "Transit"])
    engine.add_candidate("job_change", 0.50, 0.3, ["Vimshottari"])

    res = engine.evaluate_exclusivity_and_ranking()
    assert res["status"] == "CONFIRMED"
    assert res["primary_event"] == "promotion"
    assert res["clock_status"] == "DISAGREEMENT" # 3 different clocks

def test_hypothesis_engine_withheld():
    engine = V53PredictionIntelligenceEngine("FINANCE")
    engine.add_candidate("windfall", 0.2, 0.4, ["Vimshottari"])

    res = engine.evaluate_exclusivity_and_ranking()
    assert res["status"] == "WITHHELD_OR_UNCALIBRATED"
    assert res["primary_event"] is None
