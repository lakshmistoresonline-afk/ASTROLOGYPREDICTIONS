import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.matchmaking.engine import get_matchmaking_score, is_manglik
from app.astrology.core.tajika_varshaphala import calculate_varshaphala, calculate_sahams
from app.astrology.remedies.engine import get_personalized_remedies
from app.astrology.predictions.temporal_activation import evaluate_temporal_activation

def test_sprint1_matchmaking_guna_milan():
    # Boy: Aug 24, 1985 10:30 AM Delhi
    dt1 = datetime(1985, 8, 24, 10, 30)
    chart1 = calculate_canonical_chart(dt1, 28.6139, 77.2090, "Asia/Kolkata")

    # Girl: Sep 28, 1986 16:30 Palakkad
    dt2 = datetime(1986, 9, 28, 16, 30)
    chart2 = calculate_canonical_chart(dt2, 10.7867, 76.6548, "Asia/Kolkata")

    match_res = get_matchmaking_score(chart1, chart2)

    assert "total_score" in match_res
    assert match_res["max_score"] == 36.0
    assert "verdict" in match_res
    assert len(match_res["kutas"]) == 8
    assert "manglik_analysis" in match_res
    assert "deep_comparison" in match_res

def test_sprint1_manglik_dosha_cancellation():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    m_res = is_manglik(chart)
    assert "is_manglik" in m_res
    assert "house" in m_res

def test_sprint1_tajika_varshaphala_annual_chart():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    # Solar return for 2026 (Age 40)
    varsha = calculate_varshaphala(chart, 2026)

    assert varsha["target_year"] == 2026
    assert varsha["age"] == 40
    assert "muntha_house" in varsha
    assert "varsheshwara" in varsha
    assert "sahams" in varsha
    assert "Punya Saham (Fortuna & Prosperity)" in varsha["sahams"]
    assert "Karma Saham (Action & Authority)" in varsha["sahams"]

def test_sprint1_personalized_remedies_diagnostics():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    remedies = get_personalized_remedies(chart)
    assert isinstance(remedies, list)
    assert len(remedies) >= 1
    for r in remedies:
        assert "planet" in r
        assert "approach" in r
        assert "why" in r
        assert "how" in r

def test_sprint1_temporal_activation_ashtakavarga_confluence():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    t_res = evaluate_temporal_activation(chart, datetime(2026, 10, 20), domain="Career & Authority", event_type="PROMOTION")
    assert t_res is not None
    assert t_res.activation_score > 0.0
    assert "evidence_graph" in t_res.to_dict()
