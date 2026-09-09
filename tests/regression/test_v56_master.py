import pytest
from app.astrology.predictions.v56_engine import V56MasterIntelligenceEngine

def test_v56_master_engine_competition():
    engine = V56MasterIntelligenceEngine("CAREER")
    engine.add_candidate("promotion", 0.9, 0.1, ["Vimshottari", "Transit"], 0.95)
    engine.add_candidate("job_change", 0.6, 0.3, ["Vimshottari"], 0.70)

    res = engine.run_competition()
    assert res["status"] == "CONFIRMED"
    assert res["primary"]["event_type"] == "promotion"
    assert res["primary"]["status"] == "PRIMARY"

def test_v56_negative_evidence_suppression():
    engine = V56MasterIntelligenceEngine("PROPERTY")
    # High contradiction and low stability should suppress candidate
    engine.add_candidate("property_purchase", 0.7, 0.6, ["Transit"], 0.40)

    res = engine.run_competition()
    assert res["status"] == "WITHHELD"
    assert res["primary"] is None
