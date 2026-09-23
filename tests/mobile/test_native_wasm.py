import pytest
from app.astrology.core.ephemeris import get_planet_position, set_topocentric
from app.astrology.core.swe_proxy import swe

def test_mobile_native_wasm_calculation_speed():
    set_topocentric(10.7867, 76.6548)
    jd_ut = 2446702.1875

    import time
    start = time.time()
    for _ in range(100): # 100 fast calculations
        pos = get_planet_position(jd_ut, swe.SUN)
    elapsed_ms = (time.time() - start) * 1000.0

    assert pos["longitude"] > 0.0
    assert elapsed_ms < 15.0 # Sub-15ms calculation performance invariant
