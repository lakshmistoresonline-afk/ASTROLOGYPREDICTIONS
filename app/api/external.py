"""
External API integrations:
  - OpenCage Geocoder  → city name → (lat, lon, timezone)
  - TimeZoneDB         → (lat, lon) → IANA timezone string

Strict deterministic handling of birth coordinates and timezones.
Zero tolerance for New Delhi fallback on geocode failure.
"""
import os
import requests
from typing import Optional
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim, OpenCage
import pytz
from functools import lru_cache

OPENCAGE_KEY   = os.getenv("OPENCAGE_API_KEY", "")
TIMEZONEDB_KEY = os.getenv("TIMEZONEDB_API_KEY", "")

_tf = TimezoneFinder()

@lru_cache(maxsize=256)
def geocode_place(place_name: str) -> dict:
    """
    Convert a place name to lat/lon/timezone.
    Priority: Canonical Location Database → OpenCage API → Nominatim
    ZERO TOLERANCE FOR NEW DELHI FALLBACK. Returns error dict on failure.
    """
    if not place_name or not place_name.strip():
        return {"error": "LOCATION_RESOLUTION_FAILED", "message": "Birthplace is mandatory."}

    from ..astrology.core.location_db import search_canonical_locations
    local_results = search_canonical_locations(place_name)
    if local_results:
        loc = local_results[0]
        return {
            "lat": loc["latitude"], "lon": loc["longitude"], "timezone": loc["timezone"],
            "display_name": loc["display_name"], "source": loc["source"], "location_id": loc["location_id"]
        }

    from ..astrology.core.cities import search_offline_city
    legacy_results = search_offline_city(place_name)
    if legacy_results:
        res = legacy_results[0]
        return {
            "lat": res["lat"], "lon": res["lon"], "timezone": res["timezone"],
            "display_name": res["display_name"], "source": "OFFLINE_CITIES"
        }

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

    # ZERO NEW DELHI FALLBACK MANDATE
    return {"error": "LOCATION_RESOLUTION_FAILED", "message": "Birthplace could not be verified. Please select a location from the search results."}

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
                "lat": data.get("latitude", 28.6139),
                "lon": data.get("longitude", 77.2090),
                "city": data.get("cityName", "New Delhi"),
                "timezone": data.get("timeZone", "Asia/Kolkata"),
            }
    except Exception: pass
    return {"lat": 28.6139, "lon": 77.2090, "city": "New Delhi", "timezone": "Asia/Kolkata"}
