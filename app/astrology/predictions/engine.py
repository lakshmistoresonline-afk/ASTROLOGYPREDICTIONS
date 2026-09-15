from typing import Dict, Any, List
from datetime import datetime
import hashlib
from ..core.models import CanonicalChart, DomainPrediction
from .engines.career import CareerPredictionEngine
from .engines.finance import FinancePredictionEngine
from .engines.marriage import MarriagePredictionEngine
from .engines.health import HealthPredictionEngine
from .engines.travel import TravelPredictionEngine
from .engines.education import EducationPredictionEngine
from .engines.personality import PersonalityPredictionEngine
from .engines.property import PropertyPredictionEngine
from .engines.business import BusinessPredictionEngine
from .engines.children import ChildrenPredictionEngine
from .engines.spirituality import SpiritualityPredictionEngine
from .engines.foreign import ForeignSettlementEngine
from .engines.family import FamilyPredictionEngine
from .engines.vehicles import VehiclesPredictionEngine
from .engines.legal import LegalPredictionEngine
from .engines.fame import FamePredictionEngine
from .v5_natal_promise import EVENT_RULES
from .request import normalize_prediction_request, prediction_request_fingerprint

from concurrent.futures import ThreadPoolExecutor

_prediction_cache = {}

PREDICTION_ENGINE_VERSION = "P0.3-R30"

def generate_evidence_based_predictions(chart: CanonicalChart, selected_date: datetime = None, limit_domains: List[str] = None, event_requests: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Master Engine (V3.24): Orchestrates specialized domain engines using hierarchical confluence.
    Enforces strict event validation, fail-closed caching via SHA-256 request fingerprinting,
    structured timeline/domain errors, and explicit target date contract.
    """
    if selected_date is None:
        raise ValueError("INVALID_REQUEST: selected_date is required. Implicit datetime.now() fallback is prohibited.")

    if event_requests is None:
        event_requests = {}

    # Centralized Event Request Validation
    for dom, ev in event_requests.items():
        ev_key = ev.upper().replace(" ", "_")
        if ev_key not in EVENT_RULES:
            raise ValueError(f"UNSUPPORTED_EVENT: '{ev}' is not registered in canonical EVENT_RULES.")
        rule = EVENT_RULES[ev_key]
        if dom.upper() != rule["domain"]:
            raise ValueError(f"DOMAIN_MISMATCH: Event '{ev}' belongs to domain '{rule['domain']}', not requested domain '{dom.upper()}'.")

    # 0. Cache Check via Canonical Request Fingerprint (Fail-closed provenance verification)
    try:
        req_model = normalize_prediction_request(
            chart=chart,
            selected_date=selected_date,
            limit_domains=limit_domains,
            event_requests=event_requests,
            engine_version=PREDICTION_ENGINE_VERSION
        )
    except Exception as e:
        raise ValueError(f"CACHE_FAIL_CLOSED: Failed to normalize prediction request provenance: {e}")

    cache_key = prediction_request_fingerprint(req_model)
    if cache_key in _prediction_cache:
        return _prediction_cache[cache_key]

    domain_tasks = {
        "Career": CareerPredictionEngine.get_prediction,
        "Finance": FinancePredictionEngine.get_prediction,
        "Marriage": MarriagePredictionEngine.get_prediction,
        "Health": HealthPredictionEngine.get_prediction,
        "Travel": TravelPredictionEngine.get_prediction,
        "Education": EducationPredictionEngine.get_prediction,
        "Personality": PersonalityPredictionEngine.get_prediction,
        "Property": PropertyPredictionEngine.get_prediction,
        "Business": BusinessPredictionEngine.get_prediction,
        "Children": ChildrenPredictionEngine.get_prediction,
        "Spirituality": SpiritualityPredictionEngine.get_prediction,
        "Foreign Settlement": ForeignSettlementEngine.get_prediction,
        "Family": FamilyPredictionEngine.get_prediction,
        "Vehicles": VehiclesPredictionEngine.get_prediction,
        "Legal": LegalPredictionEngine.get_prediction,
        "Fame": FamePredictionEngine.get_prediction
    }

    # Optimization: Only process requested domains if limit_domains is provided
    if limit_domains:
        domain_tasks = {k: v for k, v in domain_tasks.items() if any(k.lower() in ld.lower() for ld in limit_domains)}

    results = []

    cat_map = {
        "Career": "material",
        "Finance": "material",
        "Marriage": "social",
        "Health": "survival",
        "Travel": "survival",
        "Education": "essence",
        "Personality": "essence",
        "Property": "material",
        "Business": "material",
        "Children": "social",
        "Spirituality": "essence",
        "Foreign Settlement": "survival",
        "Family": "social",
        "Vehicles": "material",
        "Legal": "survival",
        "Fame": "material"
    }

    def process_domain(name, engine_func):
        try:
            ev_type = event_requests.get(name)
            if ev_type:
                prediction = engine_func(chart, selected_date, event_type=ev_type)
            else:
                prediction = engine_func(chart, selected_date)

            p_dict = prediction.model_dump()
            p_dict["category"] = cat_map.get(name, "essence")
            p_dict["headline"] = prediction.headline
            p_dict["status"] = "SUCCESS"
            return p_dict
        except Exception as e:
            return {
                "domain": name,
                "status": "ERROR",
                "error_code": "DOMAIN_EXECUTION_FAILURE",
                "message": str(e),
                "engine_version": PREDICTION_ENGINE_VERSION
            }

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_domain = {executor.submit(process_domain, name, func): name for name, func in domain_tasks.items()}
        for future in future_to_domain:
            res = future.result()
            if res:
                results.append(res)

    results_sorted = sorted(results, key=lambda x: (x.get("domain", ""), x.get("score", 0)), reverse=False)
    categorized = {
        "material": [p for p in results_sorted if p.get("category") == "material"],
        "social": [p for p in results_sorted if p.get("category") == "social"],
        "survival": [p for p in results_sorted if p.get("category") == "survival"],
        "essence": [p for p in results_sorted if p.get("category") == "essence"]
    }

    from .v322_timeline import lifetime_timeline_engine_v22
    timeline_sorted = []
    clusters = []
    if not limit_domains:
        try:
            h_digest = hashlib.sha256(cache_key.encode('utf-8')).hexdigest()[:16]
            dummy_id = f"chart-{h_digest}"
            tl_obj = lifetime_timeline_engine_v22.generate_lifetime_timeline(chart, dummy_id)
            timeline_sorted = [e.model_dump() if hasattr(e, 'model_dump') else e for e in tl_obj.events]
        except Exception as tle:
            timeline_sorted = [{
                "status": "ERROR",
                "error_code": "TIMELINE_EXECUTION_FAILURE",
                "message": str(tle),
                "engine_version": PREDICTION_ENGINE_VERSION
            }]

    today_str = selected_date.strftime('%Y-%m-%d')
    upcoming_roadmap = [e for e in timeline_sorted if isinstance(e, dict) and (e.get('peak') or '0000') >= today_str]

    res_payload = {
        "overall_status": f"V3.24 Authoritative Intelligence Report Generated ({PREDICTION_ENGINE_VERSION})",
        "predictions": results_sorted,
        "categorized_domains": categorized,
        "timeline": timeline_sorted,
        "upcoming_roadmap": upcoming_roadmap,
        "clusters": clusters,
        "calculation_confidence": "HIGH (Swiss Ephemeris)",
        "evidence_strength": "HIERARCHICAL",
        "timing_confidence": "TRANSIT_VERIFIED",
        "historical_match_rate": None,
        "generated_at": datetime.now().isoformat()
    }

    if not limit_domains or len(limit_domains) > 0:
        _prediction_cache[cache_key] = res_payload

    return res_payload
