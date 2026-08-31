from flask import Blueprint, request, jsonify, session
from ..database.models import db, PredictionOutcome, RemedyTask
from datetime import datetime

tracking_bp = Blueprint("tracking", __name__)

# --- PRODUCTION CALIBRATION V1.0.0 ---

@tracking_bp.route("/api/v1/tracking/snapshot", methods=["POST"])
def save_prediction_snapshot():
    """
    Saves an immutable snapshot of a generated prediction (Phase 5).
    Enables reproducibility by storing all engine versions.
    """
    data = request.json
    chart_id = session.get("active_chart_id")
    if not chart_id: return jsonify({"success": False, "error": "NO_CHART"}), 400

    snapshot = PredictionOutcome(
        chart_id=chart_id,
        calculation_version=data.get("calc_v", "CALC-SWE-2.10.3"),
        dasha_version=data.get("dasha_v", "DASHA-VIM-365.2425"),
        transit_version=data.get("transit_v", "TRANSIT-PEAK-ORB1.0"),
        evidence_version=data.get("evidence_v", "EVIDENCE-HIERARCHY-7L"),
        remedy_version=data.get("remedy_v", "REMEDY-CONTEXT-V2"),
        domain=data.get("domain"),
        prediction_strength=data.get("strength"),
        prediction_text=data.get("summary"),
        historical_prediction_date=datetime.now(), # Default to now for live
        start_date=data.get("start"),
        peak_date=data.get("peak"),
        end_date=data.get("end"),
        status="PENDING"
    )
    db.session.add(snapshot)
    db.session.commit()
    return jsonify({"success": True, "snapshot_id": snapshot.id})

@tracking_bp.route("/api/v1/tracking/outcome/<int:snapshot_id>", methods=["POST"])
def report_snapshot_outcome(snapshot_id):
    """Updates a snapshot with real-world results (Phase 5)."""
    data = request.json
    snapshot = PredictionOutcome.query.get_or_404(snapshot_id)

    snapshot.status = data.get("status") # OCCURRED, PARTIALLY_OCCURRED, etc.
    snapshot.actual_event_date = data.get("event_date")
    snapshot.event_description = data.get("description")
    snapshot.user_reported_confidence = data.get("confidence", 3)
    snapshot.user_notes = data.get("notes")
    snapshot.reported_at = datetime.utcnow()

    # Post-process timing quality if event date provided
    if snapshot.actual_event_date and snapshot.peak_date:
        try:
            actual = datetime.strptime(snapshot.actual_event_date, "%Y-%m-%d")
            peak = datetime.strptime(snapshot.peak_date, "%Y-%m-%d")
            diff = abs((actual - peak).days)

            if diff <= 15: snapshot.timing_quality = "TIMING_MATCH_15"
            elif diff <= 30: snapshot.timing_quality = "TIMING_MATCH_30"
            elif diff <= 90: snapshot.timing_quality = "TIMING_MATCH_90"
            else: snapshot.timing_quality = "BROAD_MATCH"
        except:
            snapshot.timing_quality = "UNKNOWN"

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
