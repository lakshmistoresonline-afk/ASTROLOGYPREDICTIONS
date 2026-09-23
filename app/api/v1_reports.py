"""
V1 Report Generation API Endpoints (Module 6 - Task 6.1).
Exposes REST endpoints for async report generation, status tracking, and output fetching.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
from ..astrology.core.calculation_config import calculate_canonical_chart
from ..astrology.predictions.engine import generate_evidence_based_predictions
from ..astrology.evaluation.report_dag_orchestrator import report_dag_orchestrator
from ..astrology.remedies.engine import get_personalized_remedies
from ..astrology.core.bazi import calculate_bazi_pillars

reports_v1_bp = Blueprint("reports_v1", __name__, url_prefix="/api/v1/report")

# In-memory Async Job Store
_report_jobs = {}

@reports_v1_bp.route("/generate", methods=["POST"])
def generate_report_async():
    """
    POST /api/v1/report/generate
    Accepts birth parameters and returns a unique job_id.
    """
    data = request.get_json() or {}

    name = data.get("name", "Native")
    dob = data.get("dob", "1986-09-28")
    tob = data.get("tob", "16:30")
    lat = float(data.get("latitude", 10.7867))
    lon = float(data.get("longitude", 76.6548))
    tz = data.get("timezone", "Asia/Kolkata")

    job_id = f"job-{uuid.uuid4().hex[:12]}"
    birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")

    # Store initial status
    _report_jobs[job_id] = {
        "job_id": job_id,
        "status": "QUEUED",
        "created_at": datetime.now().isoformat(),
        "birth_data": {"name": name, "dob": dob, "tob": tob, "lat": lat, "lon": lon, "tz": tz},
        "output": None
    }

    # Execute synchronous calculation pass for API response
    try:
        chart = calculate_canonical_chart(birth_dt, lat, lon, tz)
        _report_jobs[job_id]["status"] = "PASS_1_PROCESSING"

        preds = generate_evidence_based_predictions(chart, selected_date=datetime.now())
        bazi = calculate_bazi_pillars(birth_dt.year, birth_dt.month, birth_dt.day, birth_dt.hour)
        remedies = get_personalized_remedies(chart)

        _report_jobs[job_id]["status"] = "PASS_2_PROCESSING"

        dag_ast = report_dag_orchestrator.orchestrate_3_pass_report(
            chart_obj=chart,
            selected_date=datetime.now(),
            predictions=preds.get("predictions", []),
            bazi_data=bazi,
            timeline_events=[],
            remedies=remedies
        )

        _report_jobs[job_id]["status"] = "COMPLETED"
        _report_jobs[job_id]["output"] = dag_ast

    except Exception as e:
        _report_jobs[job_id]["status"] = "FAILED"
        _report_jobs[job_id]["error"] = str(e)

    return jsonify({
        "job_id": job_id,
        "status": _report_jobs[job_id]["status"],
        "message": "Report generation pipeline initialized."
    }), 202

@reports_v1_bp.route("/status/<job_id>", methods=["GET"])
def get_report_status(job_id: str):
    """
    GET /api/v1/report/status/<job_id>
    Returns real-time progress status.
    """
    job = _report_jobs.get(job_id)
    if not job:
        return jsonify({"error": "JOB_NOT_FOUND", "message": f"No job found with id {job_id}"}), 404

    return jsonify({
        "job_id": job["job_id"],
        "status": job["status"],
        "created_at": job["created_at"],
        "error": job.get("error")
    }), 200

@reports_v1_bp.route("/fetch/<job_id>", methods=["GET"])
def fetch_report(job_id: str):
    """
    GET /api/v1/report/fetch/<job_id>
    Delivers final report payload.
    """
    job = _report_jobs.get(job_id)
    if not job:
        return jsonify({"error": "JOB_NOT_FOUND", "message": f"No job found with id {job_id}"}), 404

    if job["status"] != "COMPLETED":
        return jsonify({"error": "JOB_NOT_READY", "status": job["status"]}), 400

    return jsonify({
        "job_id": job["job_id"],
        "status": "COMPLETED",
        "payload": job["output"]
    }), 200
