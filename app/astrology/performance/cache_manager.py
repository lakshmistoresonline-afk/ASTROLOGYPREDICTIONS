"""
In-Memory / Redis Ephemeris Cache Manager (Module 4 - Task 4.1).
Caches natal chart calculations indefinitely and dynamic transits on a 24-hour sliding window.
Target execution time: < 50ms for cached evaluations.
"""
from typing import Dict, Any, Optional
import time

_ephemeris_cache = {}

class EphemerisCacheManager:
    """
    Cache Manager for ephemeris longitudes, house cusps, and divisional charts.
    Indexed by (Birth_UT_Timestamp, Lat_Lon_Grid_Precision_2DP).
    """

    @staticmethod
    def get_cache_key(ut_timestamp: float, lat: float, lon: float, mode: str = "NATAL") -> str:
        lat_2dp = round(lat, 2)
        lon_2dp = round(lon, 2)
        return f"{mode}_{ut_timestamp:.1f}_{lat_2dp}_{lon_2dp}"

    @staticmethod
    def get(cache_key: str) -> Optional[Dict[str, Any]]:
        entry = _ephemeris_cache.get(cache_key)
        if not entry:
            return None

        # Check TTL for TRANSIT items (24 hours = 86400 seconds)
        if entry.get("type") == "TRANSIT":
            if time.time() - entry.get("timestamp", 0) > 86400:
                del _ephemeris_cache[cache_key]
                return None

        return entry.get("data")

    @staticmethod
    def set(cache_key: str, data: Dict[str, Any], cache_type: str = "NATAL") -> None:
        _ephemeris_cache[cache_key] = {
            "data": data,
            "type": cache_type,
            "timestamp": time.time()
        }

    @staticmethod
    def clear() -> None:
        _ephemeris_cache.clear()

ephemeris_cache_manager = EphemerisCacheManager()
