import pytest
from datetime import datetime
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.predictions.framework import CorroborationEngine

def test_corroboration_logic():
    """Requirement 13/14: Corroboration and Signal count."""
    evidence = [
        CorroborationEngine.create_evidence("NATAL_PROMISE", "Support 1", 80.0),
        CorroborationEngine.create_evidence("DASHA_ACTIVATION", "Support 2", 85.0),
        CorroborationEngine.create_evidence("TRANSIT_TRIGGER", "Support 3", 90.0)
    ]
    res = CorroborationEngine.synthesize("Career", "STRONG", evidence, "Summary {score} {strength}")
    # (0.8*0.35 + 0.85*0.30 + 0.90*0.15) = 0.28 + 0.255 + 0.135 = 0.67
    assert res.prediction_strength == "STRONG"

def test_conflict_detection():
    """Requirement 42: Flagging opposing signals."""
    evidence = [
        CorroborationEngine.create_evidence("NATAL_PROMISE", "Good 1", 90.0),
        CorroborationEngine.create_evidence("CONFLICTS", "Bad 1", 80.0)
    ]
    res = CorroborationEngine.synthesize("Finance", "MODERATE", evidence, "Summary")
    # total_friction = 0.8 * -0.40 = -0.32 (<= -0.20 triggers MIXED)
    assert res.prediction_strength == "MIXED"
    assert len(res.conflicting_signals) > 0
