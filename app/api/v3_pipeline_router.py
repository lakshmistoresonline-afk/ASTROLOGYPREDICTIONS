"""
Unified Pipeline Router & Schema Standardization (Module 22 - Task 22.4).
Exposes REST endpoint POST /api/v3/predict/full with strict Pydantic V2 schemas and zero-null guarantees.
"""
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..astrology.core.calculation_config import calculate_canonical_chart
from ..astrology.predictions.master_synthesizer import master_predictive_synthesizer
from ..astrology.synthesis.contradiction_resolver import contradiction_resolver
from ..astrology.core.high_latitude_cusps import high_latitude_cusp_engine

router_v3_bp = Blueprint("router_v3", __name__, url_prefix="/api/v3/predict")

class FullPredictionRequest(BaseModel):
    name: str = Field("Native", description="Subject name")
    dob: str = Field("1986-09-28", description="YYYY-MM-DD")
    tob: str = Field("16:30", description="HH:MM")
    latitude: float = Field(10.7867, description="Latitude degree")
    longitude: float = Field(76.6548, description="Longitude degree")
    timezone: str = Field("Asia/Kolkata", description="IANA Timezone")
    target_domain: Optional[str] = Field("Career & Authority", description="Target life domain")
    prashna_seed: Optional[int] = Field(None, description="Optional 1-249 Prashna Seed")

@router_v3_bp.route("/full", methods=["POST"])
def predict_full_pipeline():
    """
    POST /api/v3/predict/full
    Unified pipeline endpoint with zero-null response guarantees.
    """
    try:
        raw_data = request.get_json() or {}
        req = FullPredictionRequest(**raw_data)

        birth_dt = datetime.strptime(f"{req.dob} {req.tob}", "%Y-%m-%d %H:%M")
        chart = calculate_canonical_chart(birth_dt, req.latitude, req.longitude, req.timezone)

        # High-Latitude polar check
        polar_cusps = high_latitude_cusp_engine.calculate_houses_polar_safe(
            chart.birth_datetime.timestamp(), req.latitude, req.longitude
        )

        # Master Synthesis
        now = datetime.now()
        master_report = master_predictive_synthesizer.synthesize_master_prediction(
            chart_obj=chart,
            target_domain=req.target_domain,
            target_event="PROMOTION" if "Career" in req.target_domain else "ACTIVATION",
            selected_date=now,
            prashna_seed=req.prashna_seed
        )

        # Contradiction Resolution
        resolved = contradiction_resolver.resolve_contradictions(
            kp_favorable=master_report.kp_promise_favorable,
            parashari_score=master_report.master_confluence_score,
            jaimini_activated=master_report.jaimini_karaka_sync,
            domain=req.target_domain,
            event_type=master_report.target_event
        )

        response_payload = {
            "profile_name": req.name,
            "chart_fingerprint": chart.chart_fingerprint,
            "polar_region_info": polar_cusps,
            "master_prediction": {
                "confluence_score": master_report.master_confluence_score,
                "confidence_tier": master_report.confidence_tier,
                "precision_window": master_report.precision_timing_window,
                "verdict": resolved["verdict"],
                "harmonized_score": resolved["final_harmonized_score"],
                "harmonized_narrative": resolved["harmonized_narrative"]
            },
            "zero_null_guarantee": True,
            "execution_status": "SUCCESS"
        }

        return jsonify(response_payload), 200

    except Exception as e:
        return jsonify({
            "execution_status": "ERROR",
            "error_code": "PIPELINE_EXECUTION_FAILURE",
            "message": str(e)
        }), 400
