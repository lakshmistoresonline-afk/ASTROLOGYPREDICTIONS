from flask import Blueprint, jsonify, session
from datetime import datetime
from ..routes import _load_active_chart
from ..astrology.predictions.engine import generate_evidence_based_predictions
from ..astrology.predictions.daily import get_daily_forecast

v6_bp = Blueprint('v6_api', __name__, url_prefix='/api/v6')

@v6_bp.route('/summary')
def v6_summary():
    """
    V6.0 World-Class Intelligence API Endpoint.
    Consolidates home summary, strongest event, lifecycle phase, and forecast data.
    """
    try:
        chart, chart_obj = _load_active_chart()
        if not chart_obj:
            return jsonify({"status": "NO_ACTIVE_PROFILE"}), 404

        preds = generate_evidence_based_predictions(chart_obj)
        daily = get_daily_forecast(chart_obj, datetime.now())

        top_pred = preds['predictions'][0] if preds.get('predictions') else None

        return jsonify({
            "status": "SUCCESS",
            "profile_name": session.get("birth_name", "Native"),
            "current_phase": daily.get("current_dasha", "Active Dasha Phase"),
            "strongest_event": top_pred,
            "predictions_count": len(preds.get('predictions', [])),
            "engine_version": "V6.0-PROD"
        })
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
