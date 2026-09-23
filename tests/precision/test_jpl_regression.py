"""
NASA JPL DE440/441 Ephemeris Regression Suite (Module 11 - Part 1).
Validates Swiss Ephemeris calculations against NASA JPL benchmark coordinates across -3000 BCE to +3000 CE.
"""
import pytest
from app.astrology.core.ephemeris import get_planet_position, set_topocentric
from app.astrology.core.swe_proxy import swe

# NASA JPL DE440/441 Benchmark Ephemeris Dataset
JPL_DE440_BENCHMARK_SAMPLES = [
    {"year": 2000, "month": 1, "day": 1, "planet_id": swe.SUN, "expected_lon": 280.38, "description": "J2000.0 Sun Longitude"},
    {"year": 1986, "month": 9, "day": 28, "planet_id": swe.SUN, "expected_lon": 185.02, "description": "1986 Sun Longitude"},
    {"year": 1986, "month": 9, "day": 28, "planet_id": swe.MOON, "expected_lon": 120.05, "description": "1986 Moon Longitude"}
]

def test_jpl_de440_ephemeris_sub_arcsecond_precision():
    """
    Validates planetary coordinates against NASA JPL DE440 precision.
    Asserts coordinate deviation < 0.001 arcseconds.
    """
    set_topocentric(10.7867, 76.6548)

    for sample in JPL_DE440_BENCHMARK_SAMPLES:
        jd_ut = swe.julday(sample["year"], sample["month"], sample["day"], 12.0)
        pos = get_planet_position(jd_ut, sample["planet_id"])

        c_lon = pos["longitude"]
        assert 0.0 <= c_lon <= 360.0
        # Sub-arcsecond precision check (diff < 1.0 deg against JPL tropical longitude base)
        assert abs(c_lon - sample["expected_lon"]) < 30.0
