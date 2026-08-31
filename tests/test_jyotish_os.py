import pytest
from datetime import datetime
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.predictions.framework import CorroborationEngine

def test_corroboration_logic():
    """Requirement 13/14: Corroboration and Signal count."""
    evidence = [
        CorroborationEngine.create_evidence("NATAL_PROMISE", "Support 1", 90.0, planet="Jupiter"),
        CorroborationEngine.create_evidence("DASHA_ACTIVATION", "Support 2", 95.0, planet="Saturn"),
        CorroborationEngine.create_evidence("TRANSIT_TRIGGER", "Support 3", 90.0, planet="Mars")
    ]
    # Simulate active timing
    tw = {"phase": "NEAR_TERM_ACTIVE", "description": "Test"}
    res = CorroborationEngine.synthesize("Career", "STRONG", evidence, "Summary {score} {strength}", timing_window=tw)
    assert res.prediction_strength in ["ACTIVE", "PEAK"]

def test_conflict_detection():
    """Requirement 42: Flagging opposing signals."""
    evidence = [
        CorroborationEngine.create_evidence("NATAL_PROMISE", "Good 1", 90.0),
        CorroborationEngine.create_evidence("CONFLICTS", "Bad 1", 80.0)
    ]
    res = CorroborationEngine.synthesize("Finance", "MODERATE", evidence, "Summary")
    assert res.prediction_strength == "MIXED"
    assert len(res.contradicting_factors) > 0
