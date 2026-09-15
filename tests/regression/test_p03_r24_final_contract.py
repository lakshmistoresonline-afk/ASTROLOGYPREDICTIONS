import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import (
    evaluate_natal_promise,
    calculate_score_from_evidence,
    EVENT_RULES
)
from app.astrology.predictions.request import (
    normalize_prediction_request,
    prediction_request_fingerprint
)
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r24_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R30"

def test_p03_r24_request_normalization_determinism():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    req1 = normalize_prediction_request(chart, selected_date=dt, limit_domains=["Career"], event_requests={"Career": "PROMOTION"})
    req2 = normalize_prediction_request(chart, selected_date=dt, event_requests={"Career": "PROMOTION"}, limit_domains=["Career"])

    assert prediction_request_fingerprint(req1) == prediction_request_fingerprint(req2)

def test_p03_r24_target_date_invariance():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    res_a = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    res_b = evaluate_natal_promise(chart, "CAREER", "PROMOTION")

    assert res_a["promise_score"] == res_b["promise_score"]
    assert res_a["evidence_items"] == res_b["evidence_items"]

def test_p03_r24_missing_provenance_fails_closed():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    chart.chart_fingerprint = None
    with pytest.raises(ValueError, match="MISSING_CHART_PROVENANCE"):
        generate_evidence_based_predictions(chart, selected_date=dt)
