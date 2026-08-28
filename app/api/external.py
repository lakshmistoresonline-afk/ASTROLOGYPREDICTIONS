"""
External API integrations:
  - OpenCage Geocoder  → city name → (lat, lon, timezone)
  - TimeZoneDB         → (lat, lon) → IANA timezone string

Strict deterministic handling of birth coordinates and timezones.
"""
import os
import requests
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim, OpenCage
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pytz
from functools import lru_cache

OPENCAGE_KEY   = os.getenv("OPENCAGE_API_KEY", "")
TIMEZONEDB_KEY = os.getenv("TIMEZONEDB_API_KEY", "")

_tf = TimezoneFinder()

@lru_cache(maxsize=256)
def geocode_place(place_name: str) -> dict:
    """
    Convert a place name to lat/lon/timezone.
    Priority: Local Offline Database → OpenCage API → Nominatim
    """
    from ..astrology.core.cities import search_offline_city
    local_results = search_offline_city(place_name)
    if local_results:
        return local_results[0]

    if OPENCAGE_KEY:
        try:
            gc = OpenCage(OPENCAGE_KEY, timeout=5)
            results = gc.geocode(place_name, exactly_one=True)
            if results:
                lat, lon = results.latitude, results.longitude
                tz = _tz_from_coords(lat, lon)
                if tz:
                    return {
                        "lat": lat, "lon": lon, "timezone": tz,
                        "display_name": results.address, "source": "OpenCage",
                    }
        except Exception: pass

    try:
        gc = Nominatim(user_agent="jyotish-os/1.0", timeout=5)
        results = gc.geocode(place_name, exactly_one=True, language="en")
        if results:
            lat, lon = results.latitude, results.longitude
            tz = _tz_from_coords(lat, lon)
            if tz:
                return {
                    "lat": lat, "lon": lon, "timezone": tz,
                    "display_name": results.address, "source": "Nominatim",
                }
    except Exception: pass

    return {"error": f"Could not determine deterministic location for '{place_name}'"}

def _tz_from_coords(lat: float, lon: float) -> Optional[str]:
    """
    Get IANA timezone string from coordinates.
    Strictly deterministic. No guessing.
    """
    tz = _tf.timezone_at(lat=lat, lng=lon)
    if tz:
        return tz

    if TIMEZONEDB_KEY:
        try:
            url = "https://api.timezonedb.com/v2.1/get-time-zone"
            params = {"key": TIMEZONEDB_KEY, "format": "json", "by": "position", "lat": lat, "lng": lon}
            resp = requests.get(url, params=params, timeout=5)
            data = resp.json()
            if data.get("status") == "OK":
                return data.get("zoneName")
        except Exception: pass

    return None

def get_ip_location() -> dict:
    """Approximate location for initial dashboard context."""
    try:
        resp = requests.get("https://freeipapi.com/api/json", timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "lat": data.get("latitude", 20.5937),
                "lon": data.get("longitude", 78.9629),
                "city": data.get("cityName", "India"),
                "timezone": data.get("timeZone", "Asia/Kolkata"),
            }
    except Exception: pass
    return {"lat": 20.5937, "lon": 78.9629, "city": "Delhi", "timezone": "Asia/Kolkata"}
