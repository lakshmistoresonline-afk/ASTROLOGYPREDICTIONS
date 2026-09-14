import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime

@dataclass(frozen=True)
class PredictionRequestModel:
    birth_datetime: str
    timezone: str
    latitude: float
    longitude: float
    chart_fingerprint: str
    calculation_config_fingerprint: str
    selected_date: str
    limit_domains: Optional[List[str]] = None
    event_requests: Optional[Dict[str, str]] = None
    prediction_engine_version: str = "P0.3-R23"
    schema_version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if d["limit_domains"]:
            d["limit_domains"] = sorted([str(dom).strip() for dom in d["limit_domains"]])
        if d["event_requests"]:
            d["event_requests"] = {str(k).strip().title(): str(v).strip().upper() for k, v in sorted(d["event_requests"].items())}
        return d

def normalize_prediction_request(
    chart: Any,
    selected_date: datetime,
    limit_domains: Optional[List[str]] = None,
    event_requests: Optional[Dict[str, str]] = None,
    engine_version: str = "P0.3-R23"
) -> PredictionRequestModel:
    if selected_date is None:
        raise ValueError("INVALID_REQUEST: selected_date is required.")

    chart_fp = getattr(chart, 'chart_fingerprint', None)
    if not chart_fp:
        raise ValueError("CACHE_FAIL_CLOSED: Missing chart_fingerprint on CanonicalChart.")

    cfg_fp = getattr(chart, 'calculation_config_fingerprint', None)
    if not cfg_fp:
        raise ValueError("CACHE_FAIL_CLOSED: Missing calculation_config_fingerprint on CanonicalChart.")

    birth_dt_str = getattr(chart, 'birth_datetime', datetime.now()).isoformat()
    tz_str = getattr(chart, 'timezone', 'UTC')
    lat = float(getattr(chart, 'latitude', 0.0))
    lon = float(getattr(chart, 'longitude', 0.0))

    return PredictionRequestModel(
        birth_datetime=birth_dt_str,
        timezone=tz_str,
        latitude=round(lat, 6),
        longitude=round(lon, 6),
        chart_fingerprint=chart_fp,
        calculation_config_fingerprint=cfg_fp,
        selected_date=selected_date.isoformat(),
        limit_domains=limit_domains,
        event_requests=event_requests,
        prediction_engine_version=engine_version
    )

def canonical_prediction_request_json(req: PredictionRequestModel) -> str:
    return json.dumps(req.to_dict(), sort_keys=True, default=str)

def prediction_request_fingerprint(req: PredictionRequestModel) -> str:
    raw = canonical_prediction_request_json(req)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()
