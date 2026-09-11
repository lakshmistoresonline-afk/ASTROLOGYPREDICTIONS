import hashlib
import json
from typing import Dict, Any

CANONICAL_CALCULATION_CONFIG = {
    "engine_version": "V3.15-PROTECTED",
    "zodiac": "SIDEREAL",
    "ayanamsa": "LAHIRI",
    "house_system": "WHOLE_SIGN",
    "node_mode": "TRUE",
    "ephemeris_mode": "SWISS_EPHEMERIS",
    "topocentric_mode": False,
    "time_standard": "UTC/UT",
    "config_version": "1.0.0"
}

def generate_chart_fingerprint(birth_instant_utc: str, lat: float, lon: float, timezone: str, config: Dict[str, Any] = None) -> str:
    """
    Generates a stable cryptographic SHA-256 fingerprint for canonical chart inputs and configuration.
    """
    cfg = config or CANONICAL_CALCULATION_CONFIG
    payload = {
        "birth_instant_utc": birth_instant_utc,
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "timezone": timezone,
        "config": cfg
    }
    raw_str = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
