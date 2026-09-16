import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.evidence import EvidenceNode, EvidenceGraph, calculate_score_from_evidence
from app.astrology.predictions.v5_natal_promise import evaluate_natal_promise, EVENT_RULES
from app.astrology.predictions.request import normalize_prediction_request, prediction_request_fingerprint
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r29_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R41"

def test_p03_r29_true_target_date_invariance():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    target_a = datetime(2026, 1, 1, 10, 0)
    target_b = datetime(2030, 1, 1, 10, 0)

    res_a = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    res_b = evaluate_natal_promise(chart, "CAREER", "PROMOTION")

    assert res_a["promise_score"] == res_b["promise_score"]
    assert res_a["promise_level"] == res_b["promise_level"]
    assert res_a["evidence_graph"] == res_b["evidence_graph"]

    req_a = normalize_prediction_request(chart, selected_date=target_a, event_requests={"Career": "PROMOTION"})
    req_b = normalize_prediction_request(chart, selected_date=target_b, event_requests={"Career": "PROMOTION"})
    assert prediction_request_fingerprint(req_a) != prediction_request_fingerprint(req_b)

def test_p03_r29_missing_selected_date_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="INVALID_REQUEST: selected_date is required"):
        generate_evidence_based_predictions(chart, selected_date=None)

def test_p03_r29_unsupported_event_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="UNSUPPORTED_EVENT"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Career": "BAD_EVENT"})

def test_p03_r29_domain_mismatch_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="DOMAIN_MISMATCH"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Finance": "PROMOTION"})
