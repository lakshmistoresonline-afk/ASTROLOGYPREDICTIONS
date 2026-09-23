import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.services.alert_template_generator import alert_template_generator
from app.services.daily_transit_scanner import daily_transit_scanner
from app.services.astrology_chart_agent import astrology_chart_agent
from app.services.scenario_simulator import scenario_simulator

def test_module12_alert_template_generator():
    alert = alert_template_generator.generate_push_alert(
        domain="Career & Authority",
        event_type="PROMOTION",
        confluence_score=88.5,
        transiting_planet="Jupiter",
        target_house=10
    )

    assert "Career & Authority" in alert["title"]
    assert "Jupiter" in alert["body"]
    assert alert["data"]["confluence_score"] == 88.5

def test_module12_daily_transit_scanner():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    daily_transits = {"Jupiter": 120.0, "Mars": 270.0, "Sun": 160.0}
    alerts = daily_transit_scanner.scan_user_chart_for_daily_alerts("user-123", chart, daily_transits)

    assert isinstance(alerts, list)

def test_module13_astrology_chart_agent():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    query = "When is the best time for my career promotion?"
    predictions = [{"domain": "Career & Authority", "score": 72.4, "timing_window": {"peak": "2026-10-20"}}]

    res = astrology_chart_agent.answer_query(query, chart, predictions)
    assert res["domain"] == "Career & Authority"
    assert "72.4%" in res["response"]
    assert "2026-10-20" in res["response"]
    assert res["grounded_in_ast_data"] is True

def test_module13_scenario_simulator():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    opt_a = datetime(2026, 10, 20)
    opt_b = datetime(2026, 12, 15)

    comp = scenario_simulator.compare_candidate_dates(chart, "Career", opt_a, opt_b)
    assert "option_a" in comp
    assert "option_b" in comp
    assert comp["recommendation"] in ["Option A", "Option B"]
    assert "confluence_score" in comp["option_a"]
