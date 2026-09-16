import pytest
import json
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.temporal_rules import TEMPORAL_EVENT_RULES, TEMPORAL_RULE_REGISTRY_VERSION
from app.astrology.predictions.scoring_registry import SCORING_RULES, SCORING_REGISTRY_VERSION
from app.astrology.predictions.temporal_activation import evaluate_temporal_activation, TemporalActivationResult, ASPECT_RULES
from app.astrology.predictions.evidence import EvidenceNode, EvidenceEdge, EvidenceGraph, validate_evidence_graph, calculate_score_from_graph, calculate_score_from_evidence
from app.astrology.predictions.request import normalize_prediction_request, prediction_request_fingerprint
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r42_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R42"
    assert TEMPORAL_RULE_REGISTRY_VERSION == "P0.3-R42"
    assert SCORING_REGISTRY_VERSION == "P0.3-R42"

def test_p03_r42_evidence_graph_serialization_roundtrip():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    act = evaluate_temporal_activation(chart, datetime(2026, 1, 1, 12, 0), domain="CAREER", event_type="PROMOTION")

    eg_dict = act.evidence_graph
    g = EvidenceGraph(
        nodes=[EvidenceNode(**n) for n in eg_dict["nodes"]],
        edges=[EvidenceEdge(**e) for e in eg_dict["edges"]]
    )
    assert validate_evidence_graph(g)

    score1 = calculate_score_from_graph(g)
    score2 = calculate_score_from_evidence(g)
    assert score1 == score2

def test_p03_r42_multiple_event_requests_temporal():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    target_dt = datetime(2026, 1, 1, 12, 0)

    res = generate_evidence_based_predictions(
        chart,
        selected_date=target_dt,
        event_requests={"Career": "PROMOTION", "Finance": "INCOME_EXPANSION"}
    )
    assert res is not None
    assert "temporal_activation_by_event" in res
    assert "PROMOTION" in res["temporal_activation_by_event"]
    assert "INCOME_EXPANSION" in res["temporal_activation_by_event"]

def test_p03_r42_multi_event_order_invariance():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    target_dt = datetime(2026, 1, 1, 12, 0)

    res1 = generate_evidence_based_predictions(
        chart, selected_date=target_dt,
        event_requests={"Career": "PROMOTION", "Finance": "INCOME_EXPANSION"}
    )
    res2 = generate_evidence_based_predictions(
        chart, selected_date=target_dt,
        event_requests={"Finance": "INCOME_EXPANSION", "Career": "PROMOTION"}
    )
    assert res1["temporal_activation_by_event"] == res2["temporal_activation_by_event"]

def test_p03_r42_true_target_date_variance_master():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    target_a = datetime(2026, 1, 1, 10, 0)
    target_b = datetime(2030, 1, 1, 10, 0)

    res_a = generate_evidence_based_predictions(chart, selected_date=target_a, limit_domains=["Career"], event_requests={"Career": "PROMOTION"})
    res_b = generate_evidence_based_predictions(chart, selected_date=target_b, limit_domains=["Career"], event_requests={"Career": "PROMOTION"})

    assert res_a["temporal_activation"]["target_datetime"] != res_b["temporal_activation"]["target_datetime"]
    assert res_a["temporal_activation"]["transit_positions"] != res_b["temporal_activation"]["transit_positions"]

def test_p03_r42_deterministic_repeated_prediction():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    target_dt = datetime(2026, 1, 1, 12, 0)

    res1 = generate_evidence_based_predictions(chart, selected_date=target_dt, event_requests={"Career": "PROMOTION"})
    res2 = generate_evidence_based_predictions(chart, selected_date=target_dt, event_requests={"Career": "PROMOTION"})

    assert json.dumps(res1, sort_keys=True, separators=(",", ":"), default=str) == \
           json.dumps(res2, sort_keys=True, separators=(",", ":"), default=str)

def test_p03_r42_transit_failure_mutation(monkeypatch):
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    target_dt = datetime(2026, 1, 1, 12, 0)

    def mock_calc_fail(jd, pid):
        raise RuntimeError("Simulated Ephemeris Failure")

    monkeypatch.setattr("app.astrology.core.ephemeris.get_planet_position", mock_calc_fail)

    with pytest.raises(RuntimeError, match="CALCULATION_ENGINE_UNAVAILABLE"):
        evaluate_temporal_activation(chart, target_dt, domain="CAREER", event_type="PROMOTION")
