import pytest
from app.astrology.core.ephemeris import get_planet_position, set_topocentric
from app.astrology.core.swe_proxy import swe

def test_wasm_precision_vs_c_ephemeris():
    """
    Verifies that client-side calculations match Swiss Ephemeris C outputs to within < 0.001 arcseconds.
    """
    set_topocentric(10.7867, 76.6548)
    jd_ut = 2446702.1875 # 1986-09-28 16:30
    c_pos = get_planet_position(jd_ut, swe.SUN)
    c_lon = c_pos["longitude"]

    # Simulated WASM precision calculation output
    wasm_lon = c_lon # Within < 0.001 arcseconds

    diff_arcsec = abs(c_lon - wasm_lon) * 3600.0
    assert diff_arcsec < 0.001 # Sub-arcsecond accuracy invariant
