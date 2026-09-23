import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.synthesis.jaimini_engine import jaimini_engine
from app.astrology.synthesis.multisystem_synthesizer import multisystem_synthesizer
from app.astrology.dasha.sookshma_prana import deep_dasha_engine
from app.astrology.predictions.probability_matrix import probability_matrix_generator

def test_module8_jaimini_karakas_ranking():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    karakas = jaimini_engine.calculate_chara_karakas(chart.planets)
    assert "Atmakaraka" in karakas
    assert "Amatyakaraka" in karakas
    assert "Darakaraka" in karakas
    assert karakas["Atmakaraka"] == "Mercury" # Mercury has highest degree in sign (28.1 deg)

def test_module8_multisystem_confluence_index():
    res = multisystem_synthesizer.calculate_confluence_index(
        vedic_score=0.85,
        jaimini_score=0.80,
        tajika_score=0.75,
        bazi_score=0.70
    )

    assert res["confluence_index_score"] == 79.5
    assert res["confluence_tier"] == "STRONG_CONFLUENCE"
    assert "vedic_kakshya_contribution" in res["weighted_breakdown"]

def test_module9_deep_dasha_sookshma_prana():
    start_dt = datetime(2026, 1, 1, 0, 0)
    target_dt = datetime(2026, 2, 15, 14, 30)

    res = deep_dasha_engine.calculate_sookshma_prana_dasha(
        pratyantar_lord="Rahu",
        pratyantar_start=start_dt,
        pratyantar_duration_days=180.0,
        target_datetime=target_dt
    )

    assert "sookshma_dasha" in res
    assert "prana_dasha" in res
    assert "lord" in res["sookshma_dasha"]
    assert "lord" in res["prana_dasha"]

def test_module9_365day_rolling_probability_matrix():
    start_dt = datetime(2026, 1, 1)
    chart = None

    dataset = probability_matrix_generator.generate_12month_probability_matrix(chart, start_dt)
    assert len(dataset) == 365
    assert dataset[0]["date"] == "2026-01-01"
    assert dataset[364]["date"] == "2026-12-31"
    assert 0.0 <= dataset[0]["career_momentum"] <= 1.0
    assert 0.0 <= dataset[0]["financial_liquidity"] <= 1.0
