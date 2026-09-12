import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import evaluate_natal_promise

def test_p03_event_specific_natal_promise_differentiation():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    promo = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    job_change = evaluate_natal_promise(chart, "CAREER", "JOB_CHANGE")
    divorce = evaluate_natal_promise(chart, "MARRIAGE", "SEPARATION_OR_DIVORCE")

    assert promo["event_type"] == "PROMOTION"
    assert job_change["event_type"] == "JOB_CHANGE"
    assert divorce["event_type"] == "SEPARATION_OR_DIVORCE"

    assert promo["relevant_houses"] != job_change["relevant_houses"]

def test_p03_unknown_event_insufficient_evidence():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    res = evaluate_natal_promise(chart, "UNKNOWN_DOMAIN", "UNKNOWN_EVENT")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"
