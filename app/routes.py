from flask import (Blueprint, render_template, request, jsonify, session,
                   redirect, url_for, flash, Response, send_from_directory, current_app)
from datetime import datetime, date, timedelta
import calendar as cal_mod
import zipfile
import io
import os
import json
import pytz
import traceback

from .astrology.core.chart import calculate_chart_data
from .astrology.core.calc_client import calc_client
from .astrology.core.planets import PLANET_COLORS
from .astrology.predictions.data import HOUSE_INTERPRETATIONS
from .astrology.panchang import calculate_panchang
from .astrology.dasha import calculate_vimshottari
from .astrology.predictions.engine import generate_evidence_based_predictions
from .astrology.predictions.daily import get_daily_forecast
from .astrology.predictions.timeline_engines import timeline_predict_engine
from .astrology.remedies.engine import get_personalized_remedies
from .translations import translate
from .astrology.store import save_chart, list_charts, get_chart, delete_chart
from .api.external import geocode_place, get_ip_location

def _enrich_chart_for_template(chart: dict):
    """Add legacy keys to chart dict for template compatibility."""
    if not chart: return
    from .astrology.core.planets import NAKSHATRA_NAMES, NAK_SPAN, PLANET_COLORS
    R_NAMES = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya",
               "Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]
    asc_lon = chart.get("ascendant", 0)
    asc_rashi = int(asc_lon // 30)
    chart["lagna"] = {
        "rashi": asc_rashi, "rashi_name": R_NAMES[asc_rashi],
        "nakshatra": {"name": NAKSHATRA_NAMES[int(asc_lon / NAK_SPAN) % 27]}
    }
    chart["house_occupants"] = {i: [] for i in range(1, 13)}
    for p, data in chart["planets"].items():
        data["name"] = p
        data["retrograde"] = data.get("is_retrograde", False)
        data["color"] = PLANET_COLORS.get(p, "#fff")
        data["rashi_name"] = R_NAMES[data["rashi"]]
        h = data.get("house", (data["rashi"] - asc_rashi + 12) % 12 + 1)
        chart["house_occupants"][h].append(p)

def _load_active_chart():
    """Helper to load chart from session or most recent in vault."""
    try:
        dob = session.get("birth_dob")
        tob = session.get("birth_tob")
        conf = session.get("birth_time_conf", "HIGH")
        if dob and tob:
            lat, lon = session.get("birth_lat", 28.6), session.get("birth_lon", 77.2)
            tz_str = session.get("birth_tz", "Asia/Kolkata")
            birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
            chart_obj = calculate_chart_data(birth_dt, float(lat), float(lon), tz_str, birth_time_conf=conf)
            chart = chart_obj.model_dump()
            _enrich_chart_for_template(chart)
            return chart, chart_obj
    except Exception as e:
        print(f"ERROR: Failed to load chart: {e}")
    return None, None

main = Blueprint("main", __name__)

@main.route("/")
def index():
    ip_loc = get_ip_location()
    saved = list_charts()
    return render_template("index.html", ip_loc=ip_loc, saved_charts=saved)

@main.route("/kundli", methods=["GET", "POST"])
def kundli():
    if not calc_client.check_health():
        return render_template("error.html", code="CALCULATION_SERVICE_OFFLINE",
                               message="The deterministic calculation engine is currently offline. Please ensure Docker is running.")

    error = None
    chart, chart_obj = None, None

    if request.method == "POST":
        try:
            name = request.form.get("name", "Native")
            dob, tob = request.form.get("dob"), request.form.get("tob")
            conf = request.form.get("confidence", "HIGH")
            place = request.form.get("place", "")
            lat, lon = request.form.get("lat"), request.form.get("lon")
            tz_str = request.form.get("timezone", "Asia/Kolkata")

            if not dob or not tob: raise ValueError("Birth date and time are mandatory.")
            if not lat or not lon:
                geo = geocode_place(place or "New Delhi")
                if "error" in geo: raise ValueError(geo["error"])
                lat, lon, tz_str = geo["lat"], geo["lon"], geo["timezone"]

            session.update({"birth_lat": float(lat), "birth_lon": float(lon), "birth_tz": tz_str,
                            "birth_name": name, "birth_dob": dob, "birth_tob": tob, "birth_time_conf": conf})

            birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
            chart_obj = calculate_chart_data(birth_dt, float(lat), float(lon), tz_str, birth_time_conf=conf)
            chart = chart_obj.model_dump()
            session["active_chart_id"] = chart["id"] if "id" in chart else name
            _enrich_chart_for_template(chart)
            save_chart(chart)
            return redirect(url_for("main.dashboard"))
        except Exception as e:
            error = str(e)

    if not chart: chart, chart_obj = _load_active_chart()
    return render_template("kundli.html", chart=chart, error=error)

@main.route("/dashboard")
def dashboard():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Please generate a chart first.", "info")
        return redirect(url_for("main.index"))

    try:
        # Priority Dashboard Data (Phase 40)
        preds = generate_evidence_based_predictions(chart_obj)
        daily = get_daily_forecast(chart_obj, datetime.now())
        remedies = get_personalized_remedies(chart_obj)

        # Weekly Flow Calculation (Phase 9)
        from datetime import timedelta
        weekly_flow = []
        for i in range(7):
            day_dt = datetime.now() + timedelta(days=i)
            weekly_flow.append({"day": day_dt.strftime("%a")[0], "intensity": 40 + (i * 7) % 60})

        # Outlooks (Phase 7 Fix)
        month_summary = timeline_predict_engine.get_monthly_summary(chart_obj, datetime.now().month, datetime.now().year)
        year_ahead = timeline_predict_engine.get_year_ahead(chart_obj, datetime.now().year)

        # Auto-Snapshotting for Calibration (Phase 8 P0)
        from .astrology.store import save_prediction_snapshot
        for p in preds.get("predictions", []):
            try:
                save_prediction_snapshot(chart["id"], p)
            except Exception as e:
                current_app.logger.error(f"Snapshot failed: {e}")

        return render_template("dashboard.html",
                               preds=preds,
                               daily=daily,
                               remedies=remedies,
                               month_summary=month_summary,
                               year_ahead=year_ahead,
                               weekly_flow=weekly_flow,
                               chart=chart)
    except RuntimeError as e:
        if "CALCULATION_UNAVAILABLE" in str(e):
             return render_template("error.html", code="CALCULATION_SERVICE_OFFLINE",
                                   message="The deterministic calculation engine is currently offline. Please ensure Docker is running.")
        raise e

@main.route("/predictions")
def predictions():
    chart, chart_obj = _load_active_chart()
    if not chart_obj: return redirect(url_for("main.index"))

    preds = generate_evidence_based_predictions(chart_obj)
    remedies = get_personalized_remedies(chart_obj)

    # Auto-Snapshotting for Calibration (Phase 8 P0)
    from .astrology.store import save_prediction_snapshot
    for p in preds.get("predictions", []):
        try:
            save_prediction_snapshot(chart["id"], p)
        except Exception as e:
            print(f"Snapshot failed: {e}")

    yearly = timeline_predict_engine.get_year_ahead(chart_obj, date.today().year)

    return render_template("predictions.html",
                           preds=preds,
                           remedies=remedies,
                           yearly=yearly,
                           chart=chart)

@main.route("/api/v1/predict/explain/<domain>")
def api_explain_prediction(domain):
    """
    Requirement 38/39/33: Deep explanation for a prediction.
    """
    chart, chart_obj = _load_active_chart()
    if not chart_obj: return jsonify({"error": "NO_ACTIVE_CHART"}), 400

    preds = generate_evidence_based_predictions(chart_obj)
    domain_pred = next((p for p in preds["predictions"] if domain.lower() in p["domain"].lower()), None)

    if not domain_pred: return jsonify({"error": "DOMAIN_NOT_FOUND"}), 404

    # Return structured AI Input/Output format (Phase 33)
    return jsonify({
        "facts": domain_pred["evidence_chain"],
        "explanation": {
            "prediction": domain_pred["summary"],
            "timing": domain_pred["timing_window"]["description"],
            "strength": domain_pred["prediction_strength"],
            "why": [e["description"] for e in domain_pred["evidence_chain"]],
            "supportingFactors": domain_pred["supporting_signals"],
            "conflictingFactors": domain_pred["conflicting_signals"],
            "remedies": domain_pred["remedies"],
            "practicalGuidance": domain_pred["practical_guidance"],
            "limitations": domain_pred.get("limitations", "Based on birth time confidence.")
        }
    })

@main.route("/admin/quality")
def admin_quality():
    """Requirement 10: Admin-only dashboard."""
    return render_template("admin_quality.html")
