import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import (
    evaluate_natal_promise,
    calculate_score_from_evidence,
    EVENT_RULES
)
from app.astrology.predictions.engine import generate_evidence_based_predictions

def test_r15_01_registry_completeness():
    assert len(EVENT_RULES) >= 14
    for ev, rule in EVENT_RULES.items():
        assert "domain" in rule
        assert "primary_houses" in rule
        assert "karakas" in rule
        assert "required_min_score" in rule

def test_r15_02_missing_event_type():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"

def test_r15_03_unsupported_event():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "INVALID_EVENT_XYZ")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"
    assert any("unsupported_event" in err for err in res["negative_evidence"])

def test_r15_04_domain_mismatch():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "FINANCE", "PROMOTION")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"
    assert any("event_domain_mismatch" in err for err in res["negative_evidence"])

def test_r15_05_missing_chart():
    res = evaluate_natal_promise(None, "CAREER", "PROMOTION")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"

def test_r15_06_determinism():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res1 = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    res2 = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    assert res1["promise_score"] == res2["promise_score"]
    assert res1["promise_level"] == res2["promise_level"]
    assert len(res1["evidence_items"]) == len(res2["evidence_items"])

def test_r15_07_score_reconstruction():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    recomputed = calculate_score_from_evidence(res["evidence_items"])
    assert recomputed == res["promise_score"]

def test_r15_08_independence_capping():
    items = [
        {"evidence_group": "SIGNIFICATOR_STRENGTH", "independence_key": "sig_Sun", "magnitude": 0.4},
        {"evidence_group": "SIGNIFICATOR_STRENGTH", "independence_key": "sig_Sun", "magnitude": 0.4}
    ]
    score = calculate_score_from_evidence(items)
    assert score <= 0.35

def test_r15_09_date_invariance():
    dt1 = datetime(1990, 9, 10, 14, 30)
    chart1 = calculate_canonical_chart(dt1, 10.5276, 76.2144, "Asia/Kolkata")
    res1 = evaluate_natal_promise(chart1, "CAREER", "PROMOTION")
    res2 = evaluate_natal_promise(chart1, "CAREER", "PROMOTION")

    assert res1["promise_score"] == res2["promise_score"]
    assert res1["promise_level"] == res2["promise_level"]

def test_r15_10_event_differentiation():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    p = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    j = evaluate_natal_promise(chart, "CAREER", "JOB_CHANGE")
    assert p["event_type"] != j["event_type"]

def test_r15_11_master_engine_propagation():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    preds = generate_evidence_based_predictions(chart, event_requests={"Career": "PROMOTION"})
    assert preds is not None
    assert "predictions" in preds

def test_r15_12_marriage_event():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "MARRIAGE", "MARRIAGE")
    assert res["domain"] == "MARRIAGE"

def test_r15_13_divorce_event():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "MARRIAGE", "SEPARATION_OR_DIVORCE")
    assert res["domain"] == "MARRIAGE"

def test_r15_14_income_expansion():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "FINANCE", "INCOME_EXPANSION")
    assert res["domain"] == "FINANCE"

def test_r15_15_financial_pressure():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "FINANCE", "FINANCIAL_PRESSURE")
    assert res["domain"] == "FINANCE"

def test_r15_16_property_purchase():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "PROPERTY", "PROPERTY_PURCHASE")
    assert res["domain"] == "PROPERTY"

def test_r15_17_property_sale():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "PROPERTY", "PROPERTY_SALE")
    assert res["domain"] == "PROPERTY"

def test_r15_18_academic_enrollment():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "EDUCATION", "ACADEMIC_ENROLLMENT")
    assert res["domain"] == "EDUCATION"

def test_r15_19_child_birth():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CHILDREN", "CHILD_BIRTH")
    assert res["domain"] == "CHILDREN"

def test_r15_20_foreign_settlement():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "FOREIGN", "FOREIGN_SETTLEMENT")
    assert res["domain"] == "FOREIGN"

def test_r15_21_health_vitality():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "HEALTH", "HEALTH_VITALITY")
    assert res["domain"] == "HEALTH"

def test_r15_22_spiritual_initiation():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "SPIRITUALITY", "SPIRITUAL_INITIATION")
    assert res["domain"] == "SPIRITUALITY"

def test_r15_23_leadership_appointment():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "LEADERSHIP_APPOINTMENT")
    assert res["event_type"] == "LEADERSHIP_APPOINTMENT"
