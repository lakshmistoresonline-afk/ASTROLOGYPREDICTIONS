import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class CalculationConfig:
    engine_version: str = "V3.15-PROTECTED"
    zodiac: str = "SIDEREAL"
    ayanamsa: str = "LAHIRI"
    house_system: str = "WHOLE_SIGN"
    node_mode: str = "TRUE"
    ephemeris_mode: str = "SWISS_EPHEMERIS"
    topocentric_mode: bool = False
    time_standard: str = "UTC/UT"
    config_version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def get_canonical_calculation_config() -> CalculationConfig:
    return CalculationConfig()

def generate_chart_fingerprint(birth_instant_utc: str, lat: float, lon: float, timezone: str, config: Optional[CalculationConfig] = None) -> str:
    """
    Generates a stable cryptographic SHA-256 fingerprint for canonical chart inputs and configuration
    with 6 decimal place coordinate precision.
    """
    cfg = config or get_canonical_calculation_config()
    payload = {
        "birth_instant_utc": birth_instant_utc,
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "timezone": timezone,
        "config": cfg.to_dict()
    }
    raw_str = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()

def validate_chart_geometry(chart_data: Dict[str, Any]) -> bool:
    """
    Validates chart geometry and house consistency (Rule 5 & Rule 7).
    """
    if not chart_data:
        raise ValueError("CHART_GEOMETRY_INVALID: Empty chart data")

    planets = chart_data.get("planets", {})
    if not planets:
        raise ValueError("CHART_GEOMETRY_INVALID: Missing planets data")

    for p_name, p_info in planets.items():
        if isinstance(p_info, dict):
            house = p_info.get("house")
            if house is not None and not (1 <= house <= 12):
                raise ValueError(f"CHART_GEOMETRY_INVALID: Invalid house {house} for planet {p_name}")

    return True
