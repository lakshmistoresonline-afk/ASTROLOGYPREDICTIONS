from flask import Blueprint, jsonify, request, g
from ..services.auth import login_required
from ..astrology.store import list_charts, save_chart, get_chart
from ..database.models import ReportRecord, PredictionOutcome
from ..astrology.core.calculation_config import calculate_canonical_chart
from ..astrology.core.datetime import parse_birth_datetime

mobile_bp = Blueprint("mobile", __name__, url_prefix="/api/v1/mobile")

@mobile_bp.route("/dashboard", methods=["GET"])
@login_required
def mobile_dashboard():
    uid = g.firebase_uid
    charts = list_charts(uid)
    return jsonify({
        "status": "success",
        "firebase_uid": uid,
        "charts_count": len(charts),
        "recent_charts": charts[:5]
    })

@mobile_bp.route("/charts", methods=["GET", "POST"])
@login_required
def mobile_charts():
    uid = g.firebase_uid
    if request.method == "GET":
        charts = list_charts(uid)
        return jsonify({"status": "success", "charts": charts})

    data = request.json or {}
    name = data.get("name", "Native")
    dob = data.get("dob")
    tob = data.get("tob")
    place = data.get("place")
    lat = data.get("lat")
    lon = data.get("lon")
    tz = data.get("tz")

    if not dob or not tob or not place or lat is None or lon is None or not tz:
        return jsonify({"status": "error", "message": "Missing required birth parameters or coordinates."}), 400

    try:
        dt = parse_birth_datetime(dob, tob)
        chart_obj = calculate_canonical_chart(dt, float(lat), float(lon), str(tz))
        chart_dict = chart_obj.model_dump()
        chart_dict["name"] = name
        cid = save_chart(uid, chart_dict)
        return jsonify({"status": "success", "chart_id": cid})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@mobile_bp.route("/reports", methods=["GET"])
@login_required
def mobile_reports():
    uid = g.firebase_uid
    reports = ReportRecord.query.filter_by(owner_uid=uid).all()
    res = [{"report_id": r.report_id, "report_type": r.report_type, "title": r.title, "created_at": r.created_at.isoformat()} for r in reports]
    return jsonify({"status": "success", "reports": res})

@mobile_bp.route("/profile", methods=["GET"])
@login_required
def mobile_profile():
    user = g.current_user
    return jsonify({
        "status": "success",
        "firebase_uid": user.firebase_uid,
        "email": user.email,
        "display_name": user.display_name,
        "role": user.role
    })
