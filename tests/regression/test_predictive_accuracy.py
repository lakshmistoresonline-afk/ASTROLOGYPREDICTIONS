import pytest
from datetime import datetime, timedelta
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.bnn_engine import bnn_engine
from app.astrology.dasha_engine import conditional_dasha_engine
from app.astrology.varga_engine import shodashavarga_engine
from app.synthesis.confluence_matrix import predictive_confluence_matrix

def test_phase7_bnn_linkages_and_progressions():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    linkages = bnn_engine.calculate_bnn_linkages(chart.planets)
    assert isinstance(linkages, list)
    assert len(linkages) >= 1

    progs = bnn_engine.calculate_bnn_progressions(age=40)
    assert progs["jupiter_progression_sign_shift"] == 3 # 40 // 12 = 3 signs
    assert progs["saturn_progression_sign_shift"] == 1  # 40 // 30 = 1 sign

def test_phase7_twin_birth_d60_differentiation():
    """
    Twin Birth Differentiation Test:
    Verifies that twin births born 180 seconds (3 minutes) apart yield distinct D60 Shashtiamsha divisions.
    """
    # Twin 1: 16:30:00
    dt_twin1 = datetime(1986, 9, 28, 16, 30, 0)
    chart1 = calculate_canonical_chart(dt_twin1, 10.7867, 76.6548, "Asia/Kolkata")

    # Twin 2: 16:33:00 (180 seconds later)
    dt_twin2 = datetime(1986, 9, 28, 16, 33, 0)
    chart2 = calculate_canonical_chart(dt_twin2, 10.7867, 76.6548, "Asia/Kolkata")

    # Fast-moving Moon longitude change in 3 minutes (~0.025 deg = 1.5 arcmin)
    m1_lon = chart1.planets["Moon"].longitude
    m2_lon = chart2.planets["Moon"].longitude

    d60_m1 = shodashavarga_engine.calculate_d60_shashtiamsha(m1_lon)
    d60_m2 = shodashavarga_engine.calculate_d60_shashtiamsha(m2_lon)

    # Ascendant cusp longitude shift in 3 minutes (~0.75 deg)
    d60_asc1 = shodashavarga_engine.calculate_d60_shashtiamsha(chart1.ascendant)
    d60_asc2 = shodashavarga_engine.calculate_d60_shashtiamsha(chart2.ascendant)

    assert chart1.chart_fingerprint != chart2.chart_fingerprint
    assert d60_asc1 != d60_asc2 # D60 Ascendant sign differs due to 3-min shift!

def test_phase7_multi_engine_pcs_confluence_scoring():
    # Case 1: High Confluence Favorable Event
    pcs1 = predictive_confluence_matrix.calculate_pcs_score(
        s_kp=0.90, s_parashari=0.85, s_bnn=0.88, s_jaimini=0.82, s_prashna=0.80, kp_promise_favorable=True
    )

    assert pcs1["predictive_confluence_score_pcs"] >= 78.0
    assert pcs1["event_status"] == "HIGH PROBABILITY / VERIFIED"
    assert pcs1["kp_hard_lock_active"] is False

    # Case 2: KP Hard Lock Negation Override
    pcs2 = predictive_confluence_matrix.calculate_pcs_score(
        s_kp=0.30, s_parashari=0.90, s_bnn=0.85, s_jaimini=0.80, s_prashna=0.75, kp_promise_favorable=False
    )

    assert pcs2["event_status"] == "BLOCKED / DELAYED"
    assert pcs2["predictive_confluence_score_pcs"] <= 42.0
    assert pcs2["kp_hard_lock_active"] is True
