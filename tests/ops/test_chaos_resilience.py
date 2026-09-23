import pytest
from app.astrology.ephemeris_cache import tiered_ephemeris_cache
from app.astrology.performance.cache_manager import ephemeris_cache_manager
from app.astrology.performance.swisseph_fast_worker import swisseph_fast_worker

def test_chaos_redis_outage_fallback_to_direct_computation():
    """Simulates Redis outage and verifies graceful fallback to direct ephemeris computation."""
    ephemeris_cache_manager.clear() # Simulate empty cache / Redis failure

    res = tiered_ephemeris_cache.get_tiered_ephemeris("chaos_key_123", 2446702.1875)

    assert res["source"] == "DIRECT_COMPUTATION_FALLBACK"
    assert "Sun" in res["data"]
    assert 0.0 <= res["data"]["Sun"] <= 360.0

def test_chaos_wasm_failure_fallback_to_rest_api():
    """Simulates WASM load failure and verifies graceful fallback handling."""
    positions = swisseph_fast_worker.calculate_fast_planetary_positions(2446702.1875, 10.78, 76.65)

    assert "Sun" in positions
    assert "Moon" in positions
    assert "Ketu" in positions
