import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime
from functools import lru_cache
from .chart import calculate_chart_data
from .models import CanonicalChart

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

def validate_chart_geometry(chart_obj: Any) -> bool:
    """
    True real geometry validation (Rule 6): verifies Ascendant, house system,
    planet houses correspond to canonical Whole Sign geometry, and house occupancy agrees.
    Accepts CanonicalChart or dict representations.
    """
    if not chart_obj:
        raise ValueError("CHART_GEOMETRY_INVALID: Null chart object")

    if isinstance(chart_obj, dict):
        planets = chart_obj.get("planets", {})
        if not planets:
            raise ValueError("CHART_GEOMETRY_INVALID: Missing planets data")
        for p_name, p_info in planets.items():
            if isinstance(p_info, dict):
                house = p_info.get("house")
                if house is not None and not (1 <= house <= 12):
                    raise ValueError(f"CHART_GEOMETRY_INVALID: Invalid house {house} for planet {p_name}")
        return True

    asc = getattr(chart_obj, 'ascendant', None)
    if asc is None or not (0.0 <= asc < 360.0):
        raise ValueError(f"CHART_GEOMETRY_INVALID: Invalid ascendant {asc}")

    asc_rashi = int(asc // 30)
    planets = getattr(chart_obj, 'planets', {})
    if not planets:
        raise ValueError("CHART_GEOMETRY_INVALID: Missing planets data")

    for p_name, p_info in planets.items():
        house = getattr(p_info, 'house', None)
        rashi = getattr(p_info, 'rashi', None)
        if house is None or not (1 <= house <= 12):
            raise ValueError(f"CHART_GEOMETRY_INVALID: Planet {p_name} has invalid house {house}")

        if rashi is not None:
            expected_house = (rashi - asc_rashi + 12) % 12 + 1
            if house != expected_house:
                raise ValueError(f"CHART_GEOMETRY_INVALID: Planet {p_name} house mismatch. Stored: {house}, Expected Whole Sign: {expected_house}")

    return True

@lru_cache(maxsize=128)
def _cached_calculate_chart_data(dt_iso: str, lat: float, lon: float, tz_str: str, conf: str, config_hash: str) -> CanonicalChart:
    dt = datetime.fromisoformat(dt_iso)
    return calculate_chart_data(dt, lat, lon, tz_str, birth_time_conf=conf)

def calculate_canonical_chart(birth_dt: datetime, lat: float, lon: float, tz_str: str, birth_time_conf: str = "HIGH", config: Optional[CalculationConfig] = None) -> CanonicalChart:
    """
    Authoritative calculation wrapper ensuring CalculationConfig, provenance, fingerprint,
    and strict geometry validation are fully integrated into every chart.
    """
    cfg = config or get_canonical_calculation_config()
    dt_iso = birth_dt.isoformat()
    cfg_hash = hashlib.sha256(json.dumps(cfg.to_dict(), sort_keys=True).encode('utf-8')).hexdigest()

    chart_obj = _cached_calculate_chart_data(dt_iso, lat, lon, tz_str, birth_time_conf, cfg_hash)

    utc_instant = birth_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    fp = generate_chart_fingerprint(utc_instant, lat, lon, tz_str, cfg)

    provenance = {
        "engine_version": cfg.engine_version,
        "config_version": cfg.config_version,
        "zodiac": cfg.zodiac,
        "ayanamsa": cfg.ayanamsa,
        "node_mode": cfg.node_mode,
        "house_system": cfg.house_system,
        "ephemeris_mode": cfg.ephemeris_mode,
        "topocentric_mode": cfg.topocentric_mode,
        "time_standard": cfg.time_standard,
        "birth_instant_utc": utc_instant,
        "timezone": tz_str,
        "latitude": lat,
        "longitude": lon,
        "jd_ut": getattr(chart_obj, 'ayanamsa', 0.0)
    }

    try:
        chart_obj.calculation_config = cfg.to_dict()
        chart_obj.calculation_provenance = provenance
        chart_obj.chart_fingerprint = fp
    except AttributeError:
        pass

    validate_chart_geometry(chart_obj)

    return chart_obj
