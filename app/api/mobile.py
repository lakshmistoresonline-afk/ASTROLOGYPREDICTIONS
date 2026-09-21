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
    from ..routes import _load_active_chart
    from ..astrology.predictions.engine import generate_evidence_based_predictions
    from ..astrology.predictions.daily import get_daily_forecast
    from ..astrology.remedies.engine import get_personalized_remedies
    from datetime import datetime
    from ..astrology.core.calculation_config import calculate_canonical_chart
    from ..astrology.core.datetime import parse_birth_datetime

    chart, chart_obj = None, None
    try:
        chart, chart_obj = _load_active_chart()
    except Exception:
        pass

    if not chart_obj:
        charts = list_charts(uid)
        if charts:
            latest_chart = charts[0]
            cid = latest_chart.get("id")
            chart_data = get_chart(uid, cid)
            if chart_data:
                try:
                    dob = chart_data.get('birth_dob') or chart_data.get('dob')
                    tob = chart_data.get('birth_tob') or chart_data.get('tob')
                    lat = float(chart_data.get('latitude') or chart_data.get('lat', 0))
                    lon = float(chart_data.get('longitude_coord') or chart_data.get('lon', 0))
                    tz = chart_data.get('timezone') or chart_data.get('tz', 'Asia/Kolkata')
                    birth_dt = parse_birth_datetime(dob, tob)
                    chart_obj = calculate_canonical_chart(birth_dt, lat, lon, tz)
                except Exception:
                    pass

    if not chart_obj:
        return jsonify({
            "status": "success",
            "preds": {"predictions": []},
            "daily": {"strongest_theme": "No birth profile loaded.", "current_dasha": "None", "opportunities": []},
            "remedies": []
        })

    try:
        preds = generate_evidence_based_predictions(chart_obj, selected_date=datetime.now())
    except Exception:
        preds = {"predictions": []}

    try:
        daily = get_daily_forecast(chart_obj, datetime.now())
    except Exception:
        daily = {"strongest_theme": "Theme Focus", "current_dasha": "Active Phase", "opportunities": []}

    try:
        raw_remedies = get_personalized_remedies(chart_obj)
        remedies = []
        for r in raw_remedies:
            remedies.append({
                "planet": r.get("planet", ""),
                "action": r.get("how", ""),
                "type": r.get("problem", ""),
                "approach": r.get("approach", ""),
                "priority": r.get("priority", ""),
                "why": r.get("why", "")
            })
    except Exception:
        remedies = []

    predictions_list = []
    for p in preds.get("predictions", []):
        tw = p.get("timing_window", {})
        predictions_list.append({
            "domain": p.get("domain", ""),
            "score": float(p.get("score", 0.0)),
            "prediction_strength": p.get("prediction_strength", ""),
            "summary": p.get("summary", ""),
            "supporting_signals": p.get("supporting_signals", []),
            "conflicting_signals": p.get("conflicting_signals", []),
            "timing_window": {
                "start": tw.get("start"),
                "peak": tw.get("peak"),
                "end": tw.get("end"),
                "description": tw.get("description", "")
            }
        })

    planets_list = []
    if chart_obj and hasattr(chart_obj, "planets"):
        from ..astrology.strength.detailed import strength_engine
        from ..astrology.core.fixed_stars import analyze_fixed_star_conjunctions
        from ..astrology.panchang.sky import get_sunrise, get_sunset
        from ..astrology.panchang.hora import WEEKDAY_TO_HORA_START, HORA_ORDER
        from ..astrology.panchang.tithi import get_tithi_info

        # Strength Context Resolve
        from ..astrology.core.datetime import datetime_to_jd
        jd = datetime_to_jd(datetime.now(), chart_obj.timezone)
        sr = get_sunrise(jd, chart_obj.latitude, chart_obj.longitude)
        ss = get_sunset(jd, chart_obj.latitude, chart_obj.longitude)
        is_day = sr < jd < ss
        t_data = get_tithi_info(jd)
        is_shukla = t_data.get("number", 1) <= 15

        python_weekday = datetime.now().weekday()
        v_weekday = (python_weekday + 1) % 7
        h_start = WEEKDAY_TO_HORA_START.get(v_weekday, 0)
        diff_h = (jd - sr) * 24.0
        hora_lord = HORA_ORDER[(h_start + int(diff_h)) % 7]
        WEEKDAY_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        wd_lord = WEEKDAY_LORDS[v_weekday]

        s_report = strength_engine.get_strength_report(chart_obj.model_dump(), is_day, is_shukla, wd_lord, hora_lord)
        f_stars = analyze_fixed_star_conjunctions(chart_obj.planets, chart_obj.ayanamsa)

        for name, info in chart_obj.planets.items():
            s_data = s_report.get(name, {})
            star_conj = next((s for s in f_stars if s["planet"] == name), None)

            planets_list.append({
                "name": name,
                "rashi": int(info.rashi),
                "house": int(info.house),
                "is_retrograde": bool(info.is_retrograde),
                "is_combust": bool(info.is_combust),
                "dignity": str(info.dignity),
                "strength_rupas": float(s_data.get("score", 0.0)),
                "strength_factors": s_data.get("transparent_factors", []),
                "fixed_star_label": star_conj["star"] if star_conj else None
            })

    vargas_dict = {}
    if chart_obj and hasattr(chart_obj, "divisional_charts"):
        for v_name, v_pos in chart_obj.divisional_charts.items():
            vargas_dict[v_name] = v_pos

    # Multi-Dasha and Cross-System Synthesis Generation
    chara_list = []
    if chart_obj and hasattr(chart_obj, "chara_dasha") and isinstance(chart_obj.chara_dasha, dict):
        for k, v in chart_obj.chara_dasha.items():
            if isinstance(v, dict):
                chara_list.append(f"Chara {k}: {v.get('lord', 'Active')}")
            else:
                chara_list.append(f"Chara {k}: {str(v)}")

    # 3rd Level Dasha (Pratyantar) and Bhava Bala (Phase 6)
    pratyantars = []
    bhava_bala_map = {}
    if chart_obj:
        from ..astrology.dasha import calculate_vimshottari
        from ..astrology.strength.bhava_bala import calculate_bhava_bala

        # Pratyantar
        moon_lon = chart_obj.planets["Moon"].longitude
        dasha_full = calculate_vimshottari(moon_lon, chart_obj.birth_datetime)
        curr_antar = dasha_full.get("current_antar")
        if curr_antar and "pratyantardashas" in curr_antar:
            for p in curr_antar["pratyantardashas"]:
                pratyantars.append({
                    "lord": p["lord"],
                    "start": p["start"],
                    "end": p["end"],
                    "level": 3
                })

        # Bhava Bala
        # Derive house occupants first
        house_occupants = {i: [] for i in range(1, 13)}
        for p_name, p_info in chart_obj.planets.items():
            house_occupants[p_info.house].append(p_name)

        bb_input = {
            "planets": chart_obj.planets,
            "house_lords": chart_obj.house_lords,
            "house_occupants": house_occupants
        }
        bhava_bala_raw = calculate_bhava_bala(bb_input)
        bhava_bala_map = {str(k): float(v) for k, v in bhava_bala_raw.items()}

    # Cross System synthesis mocks (BaZi, Hellenistic, Gene Keys)
    bazi_pillars = ["Jia Zi (Wood Rat)", "Bing Yin (Fire Tiger)", "Geng Wu (Metal Horse)", "Xin Chou (Metal Ox)"]
    hellenistic_releasing = "Zodiacal Releasing: Level 1 Gemini (Peak Active Potential), Level 2 Libra"
    gene_keys_profile = "Life's Work: 25.2 (Innocence), Evolution: 46.2, Radiance: 51.5"

    ashtakavarga_data = {}
    if chart_obj and hasattr(chart_obj, "ashtakavarga"):
        ashtakavarga_data = chart_obj.ashtakavarga

    return jsonify({
        "status": "success",
        "preds": {"predictions": predictions_list},
        "daily": {
            "strongest_theme": daily.get("strongest_theme", ""),
            "current_dasha": daily.get("current_dasha", ""),
            "opportunities": daily.get("opportunities", [])
        },
        "remedies": remedies,
        "planets": planets_list,
        "divisional_charts": vargas_dict,
        "chara_dasha": chara_list[:6],
        "bazi_pillars": bazi_pillars,
        "hellenistic_releasing": hellenistic_releasing,
        "gene_keys_profile": gene_keys_profile,
        "ashtakavarga": ashtakavarga_data,
        "pratyantar_dasha": pratyantars,
        "bhava_bala": bhava_bala_map
    })

@mobile_bp.route("/compatibility", methods=["POST"])
@login_required
def mobile_compatibility():
    from ..astrology.matchmaking.engine import get_matchmaking_score
    from ..astrology.core.calculation_config import calculate_canonical_chart
    from ..astrology.core.datetime import parse_birth_datetime
    from .external import geocode_place

    data = request.json or {}
    b_name = data.get("boy_name", "Boy")
    b_dob = data.get("boy_dob")
    b_tob = data.get("boy_tob", "12:00")
    b_place = data.get("boy_place")

    g_name = data.get("girl_name", "Girl")
    g_dob = data.get("girl_dob")
    g_tob = data.get("girl_tob", "12:00")
    g_place = data.get("girl_place")

    if not b_dob or not b_place or not g_dob or not g_place:
        return jsonify({"status": "error", "message": "Missing birth date or birthplace parameters."}), 400

    try:
        geo_b = geocode_place(b_place)
        if "error" in geo_b: return jsonify({"status": "error", "message": f"Boy location error: {geo_b['error']}"}), 400
        dt_b = parse_birth_datetime(b_dob, b_tob)
        chart_b = calculate_canonical_chart(dt_b, float(geo_b["lat"]), float(geo_b["lon"]), str(geo_b["timezone"]))

        geo_g = geocode_place(g_place)
        if "error" in geo_g: return jsonify({"status": "error", "message": f"Girl location error: {geo_g['error']}"}), 400
        dt_g = parse_birth_datetime(g_dob, g_tob)
        chart_g = calculate_canonical_chart(dt_g, float(geo_g["lat"]), float(geo_g["lon"]), str(geo_g["timezone"]))

        res = get_matchmaking_score(chart_b, chart_g)
        return jsonify({
            "status": "success",
            "total_score": float(res.get("total_score", 0.0)),
            "max_score": float(res.get("max_score", 36.0)),
            "verdict": str(res.get("verdict", "Average")),
            "kutas": res.get("kutas", []),
            "deep_comparison": res.get("deep_comparison", {})
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

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

    if not dob or not tob:
        return jsonify({"status": "error", "message": "Missing required birth date or time."}), 400

    if lat is None or lon is None or not tz:
        if not place:
            return jsonify({"status": "error", "message": "Birthplace or coordinates required."}), 400
        from .external import geocode_place
        geo = geocode_place(place)
        if isinstance(geo, dict) and geo.get("error"):
            return jsonify({"status": "error", "message": geo.get("message", "Birthplace could not be verified.")}), 400
        lat, lon, tz = geo["lat"], geo["lon"], geo["timezone"]

    try:
        from flask import session
        dt = parse_birth_datetime(dob, tob)
        chart_obj = calculate_canonical_chart(dt, float(lat), float(lon), str(tz))
        chart_dict = chart_obj.model_dump()
        chart_dict["name"] = name
        cid = save_chart(uid, chart_dict)
        session["active_chart_id"] = cid
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

@mobile_bp.route("/muhurta", methods=["GET"])
@login_required
def mobile_muhurta():
    from ..astrology.panchang.sky import get_sunrise, get_sunset
    from ..astrology.panchang.muhurta import get_choghadiya, get_brahma_muhurta, get_abhijit_muhurta
    from ..astrology.core.datetime import datetime_to_jd, jd_to_datetime
    from datetime import datetime, timedelta
    import pytz

    lat = float(request.args.get("lat", 28.61))
    lon = float(request.args.get("lon", 77.23))
    tz_str = request.args.get("tz", "Asia/Kolkata")

    now = datetime.now()
    jd = datetime_to_jd(now, tz_str)

    sr = get_sunrise(jd, lat, lon)
    ss = get_sunset(jd, lat, lon)
    nsr = get_sunrise(jd + 1.0, lat, lon)

    weekday = now.weekday()
    v_weekday = (weekday + 1) % 7

    choghadiyas = get_choghadiya(sr, ss, nsr, v_weekday)
    brahma = get_brahma_muhurta(sr, ss)
    abhijit = get_abhijit_muhurta(sr, ss)

    tz = pytz.timezone(tz_str)
    def format_jd(j):
        dt = jd_to_datetime(j)
        return pytz.utc.localize(dt).astimezone(tz).strftime("%H:%M")

    res_chog = []
    for c in choghadiyas:
        res_chog.append({
            "name": c["name"],
            "start": format_jd(c["start_jd"]),
            "end": format_jd(c["end_jd"]),
            "is_auspicious": c["name"] in ["Amrit", "Shubh", "Labh", "Chara"]
        })

    return jsonify({
        "status": "success",
        "choghadiya": res_chog,
        "brahma_muhurta": {"start": format_jd(brahma[0]), "end": format_jd(brahma[1])},
        "abhijit_muhurta": {"start": format_jd(abhijit[0]), "end": format_jd(abhijit[1])}
    })
