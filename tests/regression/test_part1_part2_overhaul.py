import pytest
import os
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.adapters.ui_component_adapter import ui_component_adapter
from app.astrology.synthesis.language_localizer import language_localizer

def test_part1_natal_wheel_double_ring_spec():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    spec = ui_component_adapter.format_interactive_natal_wheel_spec(chart)
    assert spec["component"] == "InteractiveNatalWheel"
    assert "ascendant_longitude" in spec
    assert len(spec["house_cusps"]) == 12
    assert len(spec["planet_glyphs"]) >= 7

def test_part1_score_dial_formatting():
    prob_dataset = [
        {"date": "2026-10-20", "career_momentum": 0.88, "financial_liquidity": 0.75}
    ]
    trend_spec = ui_component_adapter.format_probability_trend_spec(prob_dataset)
    assert trend_spec["component"] == "ProbabilityTrendChart"
    assert trend_spec["total_days"] == 1

def test_part2_directory_layout_architecture_check():
    required_dirs = [
        "app/api",
        "app/astrology",
        "app/astrology/synthesis",
        "app/utils",
        "app/workers",
        "frontend/components/astrology",
        "frontend/hooks",
        "frontend/lib/ephemeris",
        "tests",
        "wasm"
    ]

    for d in required_dirs:
        full_p = os.path.abspath(d)
        assert os.path.exists(full_p), f"Required directory {d} missing!"
