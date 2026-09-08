from flask import Blueprint, request, jsonify, session
from ..database.models import db, PredictionOutcome, RemedyTask
from ..astrology.predictions.framework import CorroborationEngine
from datetime import datetime
import json

tracking_bp = Blueprint("tracking", __name__)

# --- CONTROLLED BETA V3.15 ---

@tracking_bp.route("/api/v1/tracking/snapshot", methods=["POST"])
def save_prediction_snapshot():
    """
    Saves an immutable snapshot of a generated prediction (V3.15 Frozen).
    """
    data = request.json
    chart_id = session.get("active_chart_id")
    if not chart_id: return jsonify({"success": False, "error": "NO_CHART"}), 400

    # Ensure engine version is locked to V3.15
    engine_v = CorroborationEngine.ENGINE_VERSION

    # V3.15 Data Governance: Determine provenance
    source_type = data.get("source_type", "UNVERIFIED")
    if source_type == "REAL_WORLD" and not data.get("participant_id"):
        return jsonify({"success": False, "error": "REAL_WORLD_REQUIRES_PARTICIPANT"}), 400

    tw = data.get("timing_window", {})
    if not tw and data.get("peak"): # Handle flattened inputs if any
         tw = {"build": data.get("start"), "peak": data.get("peak"), "decline": data.get("end"), "phase": data.get("phase")}

    snapshot = PredictionOutcome(
        chart_id=chart_id,
        group_id=data.get("group_id", "BETA_GROUP_1"),
        participant_id=data.get("participant_id"),
        session_id=data.get("session_id"),
        engine_version=engine_v,
        calculation_version=data.get("calc_v", "CALC-SWE-2.10.3"),
        dasha_version=data.get("dasha_v", "DASHA-VIM-365.2425"),
        transit_version=data.get("transit_v", "TRANSIT-V3.15"),
        evidence_version=data.get("evidence_v", "EVIDENCE-V3.15"),
        remedy_version=data.get("remedy_v", "REMEDY-V3.15"),
        timing_calibration_version="V3.15",

        domain=data.get("domain"),
        event_type=data.get("event_type"),
        event_magnitude=data.get("magnitude"),
        what_may_develop=data.get("what_may_develop"),
        prediction_strength=data.get("strength"),
        engine_confidence=data.get("confidence_bucket"),
        confluence_score=data.get("score") / 100.0 if data.get("score") else 0.0,
        quality_score=data.get("q_score"),
        prediction_text=data.get("summary"),
        evidence_snapshot=json.dumps(data.get("evidence_chain", [])),

        start_date=tw.get("build") or tw.get("activation"),
        peak_date=tw.get("peak"),
        end_date=tw.get("decline"),
        timing_phase=tw.get("phase"),
        proximity_weight=data.get("weight") or tw.get("proximity_weight"),
        status="PENDING",
        source_type=source_type
    )
    db.session.add(snapshot)
    db.session.commit()
    return jsonify({"success": True, "snapshot_id": snapshot.id})

@tracking_bp.route("/api/v1/tracking/outcome/<int:snapshot_id>", methods=["POST"])
def report_snapshot_outcome(snapshot_id):
    """
    Updates a snapshot with real-world results.
    Strictly prohibits modifying the original prediction fields.
    """
    data = request.json
    snapshot = PredictionOutcome.query.get_or_404(snapshot_id)

    # Outcome Fields Only
    snapshot.status = data.get("status") # OCCURRED, PARTIALLY_OCCURRED, etc.
    snapshot.actual_event_date = data.get("event_date")

    # V3.15 Prospective Enforcement: Reject retrospective dates for REAL_WORLD beta
    if snapshot.source_type == "REAL_WORLD" and snapshot.actual_event_date:
        try:
            actual_date = datetime.strptime(snapshot.actual_event_date, "%Y-%m-%d").date()
            # Safety: Ensure created_at exists (it should due to DB default)
            created_date = (snapshot.created_at or datetime.utcnow()).date()

            if actual_date < created_date:
                return jsonify({
                    "success": False,
                    "error": "RETROSPECTIVE_OUTCOME_PROHIBITED",
                    "message": f"Outcome date ({actual_date}) cannot be earlier than prediction date ({created_date}) for real-world beta."
                }), 400
        except (ValueError, AttributeError):
            pass

    snapshot.actual_event_end_date = data.get("event_end_date")
    snapshot.event_description = data.get("description")
    snapshot.verification_level = data.get("verification", "SELF_REPORTED")
    snapshot.user_reported_confidence = data.get("user_confidence")
    snapshot.user_notes = data.get("notes")
    snapshot.practitioner_feedback = json.dumps(data.get("feedback", {}))
    snapshot.reported_at = datetime.utcnow()

    # Calculate Timing Metrics
    if snapshot.actual_event_date and snapshot.peak_date:
        try:
            actual = datetime.strptime(snapshot.actual_event_date, "%Y-%m-%d")
            peak = datetime.strptime(snapshot.peak_date, "%Y-%m-%d")
            error = (actual - peak).days
            snapshot.timing_error_days = error

            abs_err = abs(error)
            if abs_err <= 3: snapshot.timing_quality = "PEAK_HIT_3"
            elif abs_err <= 7: snapshot.timing_quality = "PEAK_HIT_7"
            elif abs_err <= 15: snapshot.timing_quality = "ACTIVE_WINDOW_HIT"
            elif abs_err <= 30: snapshot.timing_quality = "BROAD_MATCH"
            else: snapshot.timing_quality = "NO_MATCH"

            # Calculate Lead Time
            lead_time = (actual - snapshot.created_at).days
            snapshot.lead_time_days = lead_time
        except:
            snapshot.timing_quality = "CALC_ERROR"

    db.session.commit()
    return jsonify({"success": True})

@tracking_bp.route("/api/tracking/history", methods=["GET"])
def get_outcome_history():
    """Returns a list of recent outcomes for the dashboard."""
    outcomes = PredictionOutcome.query.order_by(PredictionOutcome.created_at.desc()).limit(20).all()
    history = []
    for o in outcomes:
        history.append({
            "category": o.domain,
            "status": o.status,
            "prediction": o.prediction_text[:120],
            "timing_quality": o.timing_quality
        })
    return jsonify({"history": history})

@tracking_bp.route("/api/v1/calibration/dashboard", methods=["GET"])
def get_quality_dashboard():
    """Requirement 6: Internal Quality Dashboard data (V3.2 Enhanced)."""
    domains = [
        "Career & Authority", "Finance & Wealth", "Marriage & Relationships",
        "Health & Vitality", "Business & Enterprise", "Fame & Reputation"
    ]
    stats = []
    for d in domains:
        outcomes = PredictionOutcome.query.filter(PredictionOutcome.domain.ilike(f"%{d}%")).all()
        cases = len(outcomes)
        occurred = len([o for o in outcomes if o.status == "OCCURRED"])

        timing_15 = len([o for o in outcomes if o.status == "OCCURRED" and o.timing_quality == "ACTIVE_WINDOW_HIT"])
        timing_30 = len([o for o in outcomes if o.status == "OCCURRED" and o.timing_quality == "BROAD_MATCH"]) # Mapping old/broad for UI
        timing_90 = len([o for o in outcomes if o.status == "OCCURRED" and o.timing_quality == "BROAD_MATCH"])

        stats.append({
            "domain": d,
            "total": cases,
            "occurred": occurred,
            "timing_15": timing_15,
            "timing_30": timing_30,
            "timing_90": timing_90,
            "match_rate": round(occurred/cases * 100, 2) if cases > 0 else 0
        })
    return jsonify(stats)
