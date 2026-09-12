import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import evaluate_natal_promise

def test_p03_event_specific_natal_promise():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    career_promise = evaluate_natal_promise(chart, "CAREER", "promotion")
    marriage_promise = evaluate_natal_promise(chart, "MARRIAGE", "wedding")

    assert career_promise["domain"] == "CAREER"
    assert career_promise["promise_level"] in ["STRONG_PROMISE", "MODERATE_PROMISE", "CONDITIONAL_PROMISE", "WEAK_PROMISE", "WITHHELD"]
    assert "positive_evidence" in career_promise
    assert "negative_evidence" in career_promise

    assert marriage_promise["domain"] == "MARRIAGE"
    assert marriage_promise["promise_level"] in ["STRONG_PROMISE", "MODERATE_PROMISE", "CONDITIONAL_PROMISE", "WEAK_PROMISE", "WITHHELD"]

def test_p03_insufficient_evidence():
    res = evaluate_natal_promise(None, "CAREER", "promotion")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"
