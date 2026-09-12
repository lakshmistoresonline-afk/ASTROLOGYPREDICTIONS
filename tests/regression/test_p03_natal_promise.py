import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import (
    evaluate_natal_promise,
    calculate_score_from_evidence,
    EVENT_RULES
)
from app.astrology.predictions.engine import generate_evidence_based_predictions

def test_p03_registry_completeness():
    assert len(EVENT_RULES) >= 14
    for ev, rule in EVENT_RULES.items():
        assert "domain" in rule
        assert "primary_houses" in rule
        assert "karakas" in rule
        assert "required_min_score" in rule

def test_p03_domain_mismatch_rejection():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    res = evaluate_natal_promise(chart, "FINANCE", "MARRIAGE")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"
    assert any("event_domain_mismatch" in err for err in res["negative_evidence"])

def test_p03_unknown_event_rejection():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    res = evaluate_natal_promise(chart, "CAREER", "TOTALLY_UNKNOWN_EVENT")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"
    assert any("unsupported_event" in err for err in res["negative_evidence"])

def test_p03_event_differentiation():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    promo = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    job_change = evaluate_natal_promise(chart, "CAREER", "JOB_CHANGE")
    leadership = evaluate_natal_promise(chart, "CAREER", "LEADERSHIP_APPOINTMENT")
    marriage = evaluate_natal_promise(chart, "MARRIAGE", "MARRIAGE")
    divorce = evaluate_natal_promise(chart, "MARRIAGE", "SEPARATION_OR_DIVORCE")
    income = evaluate_natal_promise(chart, "FINANCE", "INCOME_EXPANSION")
    pressure = evaluate_natal_promise(chart, "FINANCE", "FINANCIAL_PRESSURE")
    prop_buy = evaluate_natal_promise(chart, "PROPERTY", "PROPERTY_PURCHASE")
    prop_sale = evaluate_natal_promise(chart, "PROPERTY", "PROPERTY_SALE")

    assert promo["event_type"] == "PROMOTION"
    assert job_change["event_type"] == "JOB_CHANGE"
    assert leadership["event_type"] == "LEADERSHIP_APPOINTMENT"
    assert promo["relevant_houses"] != job_change["relevant_houses"]

    assert marriage["event_type"] == "MARRIAGE"
    assert divorce["event_type"] == "SEPARATION_OR_DIVORCE"
    assert income["event_type"] == "INCOME_EXPANSION"
    assert pressure["event_type"] == "FINANCIAL_PRESSURE"
    assert prop_buy["event_type"] == "PROPERTY_PURCHASE"
    assert prop_sale["event_type"] == "PROPERTY_SALE"

def test_p03_score_reconstruction_from_evidence():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "PROMOTION")

    items = res["evidence_items"]
    recomputed = calculate_score_from_evidence(items)
    assert recomputed == res["promise_score"]

def test_p03_anti_double_counting_capping():
    items = [
        {"evidence_group": "SIGNIFICATOR_STRENGTH", "magnitude": 0.3},
        {"evidence_group": "SIGNIFICATOR_STRENGTH", "magnitude": 0.3},
        {"evidence_group": "SIGNIFICATOR_STRENGTH", "magnitude": 0.3}
    ]
    score = calculate_score_from_evidence(items)
    assert score <= 0.35

def test_p03_determinism():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    res1 = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    res2 = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    assert res1["promise_score"] == res2["promise_score"]
    assert res1["promise_level"] == res2["promise_level"]
    assert len(res1["evidence_items"]) == len(res2["evidence_items"])

def test_p03_no_future_leakage():
    dt = datetime(1990, 9, 10, 14, 30)
    chart1 = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res1 = evaluate_natal_promise(chart1, "CAREER", "PROMOTION")

    dt_future = datetime(2050, 1, 1, 12, 0)
    chart2 = calculate_canonical_chart(dt_future, 10.5276, 76.2144, "Asia/Kolkata")
    res2 = evaluate_natal_promise(chart2, "CAREER", "PROMOTION")

    assert res1["promise_score"] == res2["promise_score"]
    assert res1["promise_level"] == res2["promise_level"]

def test_p03_multi_chart_coverage():
    dt1 = datetime(1980, 5, 15, 6, 0)
    chart1 = calculate_canonical_chart(dt1, 28.6139, 77.2090, "Asia/Kolkata")
    res1 = evaluate_natal_promise(chart1, "PROPERTY", "PROPERTY_PURCHASE")
    assert res1["domain"] == "PROPERTY"

    dt2 = datetime(2000, 12, 1, 18, 45)
    chart2 = calculate_canonical_chart(dt2, 51.5074, -0.1278, "Europe/London")
    res2 = evaluate_natal_promise(chart2, "EDUCATION", "ACADEMIC_ENROLLMENT")
    assert res2["domain"] == "EDUCATION"

def test_p03_master_engine_integration():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    preds = generate_evidence_based_predictions(chart)
    assert preds is not None
    assert "predictions" in preds
    assert len(preds["predictions"]) >= 1
    # Verify career domain prediction contains evidence
    career_p = next((p for p in preds["predictions"] if p["domain"] == "Career & Authority"), None)
    assert career_p is not None
    assert len(career_p["evidence_chain"]) >= 1
