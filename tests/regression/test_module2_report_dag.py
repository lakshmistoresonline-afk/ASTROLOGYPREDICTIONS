import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.evaluation.hydration_guard import hydration_guard, FORBIDDEN_TOKENS
from app.astrology.evaluation.report_dag_orchestrator import report_dag_orchestrator
from app.astrology.core.bazi import calculate_bazi_pillars

def test_module2_hydration_guard_token_scan():
    raw_text = "- **RATIONALE**: \nMonitor peak triggers for alignment.\n- **RATIONALE**: Planetary positions support this."
    violations = hydration_guard.scan_for_forbidden_tokens(raw_text)
    assert len(violations) >= 1

    hydrated = hydration_guard.sanitize_and_hydrate(raw_text)
    assert "Monitor peak triggers for alignment." not in hydrated
    assert "- **RATIONALE**: \n" not in hydrated
    assert "Planetary positions" in hydrated

def test_module2_confidence_gating_classification():
    predictions = [
        {"domain": "Career", "score": 68.23, "quality_score": 56.2},  # Primary
        {"domain": "Marriage", "score": 63.49, "quality_score": 52.1}, # Primary
        {"domain": "Personality", "score": 1.50, "quality_score": 2.0} # Background (<15% & <30 quality)
    ]

    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    ast = report_dag_orchestrator.run_pass_1_data_prep(chart, dt, predictions)

    assert ast["total_primary_count"] == 2
    assert ast["total_background_count"] == 1
    assert ast["background_domains"][0]["domain"] == "Personality"

def test_module2_bazi_frame_separation():
    dt = datetime(1986, 9, 28, 16, 30)
    bazi = calculate_bazi_pillars(1986, 9, 28, 16, target_year=2026)

    ast_json = {}
    ast_json = report_dag_orchestrator.run_pass_2_core_narratives(ast_json, bazi)

    assert "natal_bazi" in ast_json
    assert "active_transit_bazi" in ast_json
    assert ast_json["natal_bazi"]["day_master"] == "Ding (Yin Fire)"
    assert "annual_pillar" in ast_json["active_transit_bazi"]
    assert "luck_decade_pillar" in ast_json["active_transit_bazi"]
