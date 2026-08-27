from flask import (Blueprint, render_template, request, jsonify, session,
                   redirect, url_for, flash, Response, send_from_directory)
from datetime import datetime, date, timedelta
import calendar as cal_mod
import zipfile
import io
import os
import json
import pytz
import traceback

from .astrology.core.chart import calculate_chart_data
from .astrology.core.planets import PLANET_COLORS
from .astrology.predictions.data import HOUSE_INTERPRETATIONS
from .astrology.panchang import calculate_panchang
from .astrology.dasha import calculate_vimshottari
from .astrology.predictions.engine import generate_evidence_based_predictions
from .astrology.remedies.engine import get_remedies
from .translations import translate
from .astrology.store import save_chart, list_charts, get_chart, delete_chart
from .api.external import geocode_place, get_ip_location

def _enrich_chart_for_template(chart: dict):
    """Add legacy keys to chart dict for template compatibility."""
    if not chart: return

    from .astrology.core.planets import NAKSHATRA_NAMES, NAKSHATRA_LORDS, NAK_SPAN, PLANET_COLORS

    # 1. Dates
    if hasattr(chart, "birth_datetime") and isinstance(chart.birth_datetime, datetime):
        chart.birth_datetime = chart.birth_datetime.isoformat()
    elif isinstance(chart.get("birth_datetime"), datetime):
        chart["birth_datetime"] = chart["birth_datetime"].isoformat()

    # 2. Basic Metadata
    R_NAMES = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya",
               "Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]

    asc_lon = chart.get("ascendant", 0)
    asc_rashi = int(asc_lon // 30)
    deg = asc_lon % 30
    chart["lagna"] = {
        "rashi": asc_rashi,
        "rashi_name": R_NAMES[asc_rashi],
        "dms": f"{int(deg)}°{int((deg%1)*60)}'",
        "nakshatra": {"name": NAKSHATRA_NAMES[int(asc_lon / NAK_SPAN) % 27]}
    }

    # 3. Planet Sync & House Occupants
    chart["house_occupants"] = {i: [] for i in range(1, 13)}

    for p, data in chart["planets"].items():
        # Ensure model compatibility
        data["name"] = p
        data["retrograde"] = data.get("is_retrograde", False)
        data["color"] = PLANET_COLORS.get(p, "#fff")
        data["rashi_name"] = R_NAMES[data["rashi"]]

        # DMS
        p_lon = data.get("longitude", 0)
        p_deg = p_lon % 30
        data["dms"] = f"{int(p_deg)}°{int((p_deg%1)*60)}'"

        # House (Sync from engine or recalculate)
        h = data.get("house")
        if not h:
            h = (data["rashi"] - asc_rashi + 12) % 12 + 1
            data["house"] = h

        chart["house_occupants"][h].append(p)

    # 4. Divisional Occupants
    divs = chart.get("divisional_charts", {})
    chart["varga_occupants"] = {}
    for v_name, v_data in divs.items():
        v_lagna = v_data.get("Lagna", 0)
        chart["varga_occupants"][f"{v_name}_Lagna"] = v_lagna
        v_occ = {i: [] for i in range(1, 13)}
        for pname, rashi in v_data.items():
            if pname == "Lagna": continue
            hv = (rashi - v_lagna + 12) % 12 + 1
            v_occ[hv].append(pname)
        chart["varga_occupants"][v_name] = v_occ

    # Jaimini Keys normalization
    jk = chart.get("jaimini_karakas", {})
    chart["jaimini_karakas"] = { k.split(' ')[0]: v for k,v in jk.items() }

    # Ensure Atmakaraka key specifically
    if "Atmakaraka" not in chart["jaimini_karakas"]:
        for k, v in jk.items():
            if "Atmakaraka" in k:
                chart["jaimini_karakas"]["Atmakaraka"] = v

    # 5. Additional fields
    chart["chalit_occupants"] = chart.get("bhava_chalit", chart["house_occupants"])
    chart["houses_list"] = [{"house": i, "rashi": (asc_rashi+i-1)%12, "rashi_name": R_NAMES[(asc_rashi+i-1)%12]} for i in range(1,13)]

def _enrich_predictions_with_extras(preds: dict, natal_chart, panchang: dict):
    """Add all missing fields required by predictions.html."""
    from .astrology.core.planets import PLANET_COLORS

    # Ensure natal_chart is a dict for easy access
    if hasattr(natal_chart, "model_dump"):
        natal_chart = natal_chart.model_dump()

    # 1. Day Info (Enemies/Friends)
    day_lord = panchang["vara"]["lord"]
    preds["day_info"] = {
        "vara_lord": day_lord,
        "color": PLANET_COLORS.get(day_lord, "#fff"),
        "favorable_color": "Yellow" if day_lord == "Jupiter" else "Red" if day_lord == "Mars" else "White",
        "lucky_number": 3 if day_lord == "Jupiter" else 9 if day_lord == "Mars" else 1,
        "enemies": ["Rahu", "Ketu"],
        "friends": ["Jupiter", "Venus"],
        "mantra": f"Om Sham {day_lord}aya Namah"
    }
    if day_lord in ["Saturn", "Mars"]:
        preds["day_info"]["enemies"].append(day_lord)

    # 2. Dasha Info
    from .astrology.dasha import calculate_vimshottari
    moon_lon = natal_chart["planets"]["Moon"]["longitude"]
    # Handle both string and datetime
    b_dt = natal_chart["birth_datetime"]
    if isinstance(b_dt, str):
        b_dt = datetime.fromisoformat(b_dt)

    dasha_data = calculate_vimshottari(moon_lon, b_dt)

    cm = dasha_data.get("current_maha")
    ca = dasha_data.get("current_antar")
    cp = dasha_data.get("current_pratyantar")

    preds["maha_lord"] = cm["lord"] if cm else "N/A"
    preds["maha_color"] = cm["color"] if cm else "#fff"
    preds["maha_end"] = cm["end"] if cm else "N/A"

    preds["antar_lord"] = ca["lord"] if ca else "N/A"
    preds["antar_color"] = ca["color"] if ca else "#fff"
    preds["antar_end"] = ca["end"] if ca else "N/A"

    preds["prat_lord"] = cp["lord"] if cp else "N/A"
    preds["prat_color"] = cp["color"] if cp else "#fff"

    preds["dasha_text"] = f"Currently in {preds['maha_lord']} - {preds['antar_lord']} period."

    # 3. Emotional / Moon state
    from .astrology.predictions.data import NAKSHATRA_MEANINGS
    m_nak = panchang["nakshatra"]
    m_nak_name = m_nak["name"]
    m_nak_lord = m_nak["lord"]
    preds["moon_nak"] = m_nak_name
    preds["moon_nak_lord"] = m_nak_lord
    preds["moon_nak_lord_color"] = PLANET_COLORS.get(m_nak_lord, "#fff")
    preds["moon_nak_meaning"] = NAKSHATRA_MEANINGS.get(m_nak_name, "")
    preds["emo_label"] = "Reflective" if panchang["tithi"]["paksha"] == "Krishna" else "Expressive"
    preds["emo_detail"] = f"Mind is influenced by {m_nak_name} nakshatra today."
    preds["moon_phase"] = f"{panchang['tithi']['paksha']} {panchang['tithi']['name']}"
    preds["moon_phase_mood"] = "Stable"
    preds["antar_text"] = f"Influence of {preds['antar_lord']} is prominent today."

    # Moon house from natal moon
    natal_moon_rashi = natal_chart["planets"]["Moon"]["rashi"]
    transit_moon_rashi = panchang["moon_rashi"]["name"]
    from .astrology.panchang import RASHI_NAMES
    try:
        t_m_r_idx = RASHI_NAMES.index(transit_moon_rashi)
        house_from_natal = (t_m_r_idx - natal_moon_rashi + 12) % 12 + 1
        preds["moon_house_from_natal"] = house_from_natal
    except Exception:
        preds["moon_house_from_natal"] = 1

    # 4. Domain Mapping for UI
    marriage_domain = next((d for d in preds["domains"] if "Marriage" in d["domain"]), {})
    career_domain = next((d for d in preds["domains"] if "Career" in d["domain"]), {})

    preds["love_severity"] = "positive" if marriage_domain.get("score", 50) >= 65 else "warning" if marriage_domain.get("score", 50) < 45 else "neutral"
    preds["love_overall"] = marriage_domain.get("summary", "Stable day for relationships.")
    preds["love_texts"] = [{"planet": "Venus", "house": natal_chart["planets"]["Venus"]["house"], "severity": preds["love_severity"], "text": marriage_domain.get("summary")}] if marriage_domain else []

    preds["career_severity"] = "positive" if career_domain.get("score", 50) >= 65 else "warning" if career_domain.get("score", 50) < 45 else "neutral"
    preds["dasha_career"] = career_domain.get("summary", "Steady progress in career.")

    # 5. Sade Sati / Kantaka Alerts
    from .astrology.transit.shani import get_shani_status
    shani = get_shani_status(natal_moon_rashi, natal_chart["asc_rashi"])
    preds["sade_sati"] = {"phase": shani["sade_sati"], "message": f"Saturn is currently in its {shani['sade_sati']} phase."} if shani["sade_sati"] else None
    preds["kantaka_shani"] = {"message": shani["kantaka"]} if shani["kantaka"] else None

    # 6. Planet Forecasts
    preds["planet_forecasts"] = []
    from .astrology.core.nakshatra_sutras import get_nakshatra_sutra
    for p, data in natal_chart["planets"].items():
        p_color = PLANET_COLORS.get(p, "#fff")
        preds["planet_forecasts"].append({
            "planet": p,
            "symbol": "",
            "color": p_color,
            "dms": data["degree"], # Simplified
            "rashi": RASHI_NAMES[data["rashi"]],
            "nakshatra": data["nakshatra"]["name"],
            "nak_sutra": get_nakshatra_sutra(data["nakshatra"]["name"]),
            "nak_lord": data["nakshatra"]["lord"],
            "nak_lord_color": PLANET_COLORS.get(data["nakshatra"]["lord"], "#fff"),
            "natal_house": data["house"],
            "conjoined_natal": []
        })

def calculate_transit_chart(lat: float, lon: float, tz_str: str, dt: datetime = None) -> dict:
    from .astrology.core.chart import calculate_chart_data
    if dt is None:
        tz = pytz.timezone(tz_str)
        dt = datetime.now(tz)
    chart_obj = calculate_chart_data(dt, lat, lon, tz_str)
    chart = chart_obj.model_dump()
    _enrich_chart_for_template(chart)
    return chart

def get_sunrise_sunset_moonrise(target_date: date, lat: float, lon: float, tz_str: str) -> dict:
    from .astrology.panchang.sky import (get_sunrise, get_sunset, get_moonrise, get_moonset,
                                         get_rahu_kaal, get_gulika_kaal, get_yamaghanta)
    from .astrology.core.datetime import datetime_to_jd
    from .astrology.core.swe_proxy import swe

    tz = pytz.timezone(tz_str)
    # Use midnight UTC for the given date as a stable base for sky events
    base_dt = datetime.combine(target_date, datetime.min.time())
    jd_ut = datetime_to_jd(base_dt, "UTC")

    sr_jd = get_sunrise(jd_ut, lat, lon)
    ss_jd = get_sunset(jd_ut, lat, lon)
    mr_jd = get_moonrise(jd_ut, lat, lon)
    ms_jd = get_moonset(jd_ut, lat, lon)

    def jd_to_str(jd):
        if not jd or jd < 0: return "—"
        y, m, d, h = swe.revjul(jd)
        hh = int(h)
        mm = int((h - hh) * 60)
        dt_utc = datetime(y, m, d, hh, mm, second=0, tzinfo=pytz.utc)
        return dt_utc.astimezone(tz).strftime("%I:%M %p")

    # Convert Python weekday (0=Mon, 6=Sun) to Vedic index (0=Sun, 1=Mon...)
    v_weekday = (target_date.weekday() + 1) % 7

    return {
        "sunrise": jd_to_str(sr_jd),
        "sunset": jd_to_str(ss_jd),
        "moonrise": jd_to_str(mr_jd),
        "moonset": jd_to_str(ms_jd),
        "rahu_kaal": get_rahu_kaal(v_weekday, sr_jd, ss_jd, tz_str),
        "gulika_kaal": get_gulika_kaal(v_weekday, sr_jd, ss_jd, tz_str),
        "yamaghanta": get_yamaghanta(v_weekday, sr_jd, ss_jd, tz_str)
    }

main = Blueprint("main", __name__)

@main.app_context_processor
def inject_translate():
    lang = session.get("lang", "en")
    return {"_": lambda k: translate(k, lang), "current_lang": lang}

@main.route("/settings/lang", methods=["POST"])
def set_lang_pref():
    lang = request.form.get("lang")
    if lang in ["en", "hi"]:
        session["lang"] = lang
    return redirect(request.referrer or url_for("main.index"))

@main.route("/settings/ayanamsa", methods=["POST"])
def set_ayanamsa_pref():
    mode = request.form.get("ayanamsa")
    if mode in ["Lahiri", "Raman", "KP"]:
        session["ayanamsa"] = mode
    return redirect(request.referrer or url_for("main.index"))

@main.route("/api/transit/heatmap")
def api_transit_heatmap():
    lat = float(request.args.get("lat", 28.6139))
    lon = float(request.args.get("lon", 77.2090))
    tz_str = request.args.get("tz", "Asia/Kolkata")

    results = []
    today = date.today()
    for i in range(12):
        target_date = today + timedelta(days=i*30)
        chart = calculate_transit_chart(lat, lon, tz_str, datetime.combine(target_date, datetime.min.time()))
        score = 50
        for p_name, p in chart["planets"].items():
            if p_name in ["Jupiter", "Venus"]:
                if p["house"] in [1, 4, 7, 10, 5, 9]: score += 10
            if p_name in ["Saturn", "Mars"]:
                if p["house"] in [6, 8, 12]: score -= 10
        results.append({
            "month": target_date.strftime("%b %Y"),
            "score": max(0, min(100, score)),
            "date": target_date.isoformat()
        })
    return jsonify(results)


# ─────────────────────────────────────────────
#  Home — birth-data input + saved charts
# ─────────────────────────────────────────────
@main.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static', 'img'),
                               'icon.svg', mimetype='image/svg+xml')

@main.route("/")
def index():
    try:
        # Stop the redirect loop. Let users see the Home page even if they have a session.
        # They can click "Dashboard" in the sidebar if they want.

        ip_loc   = get_ip_location()
        saved    = list_charts()
        return render_template("index.html", ip_loc=ip_loc, saved_charts=saved)
    except Exception as e:
        traceback.print_exc()
        return f"Internal Server Error: {str(e)}", 500


def _load_active_chart():
    """Helper to load chart from session or most recent in vault."""
    try:
        dob = session.get("birth_dob")
        tob = session.get("birth_tob")

        if dob and tob:
            lat    = session.get("birth_lat", 28.6139)
            lon    = session.get("birth_lon", 77.2090)
            tz_str = session.get("birth_tz", "Asia/Kolkata")
            name   = session.get("birth_name", "Native")
            place  = session.get("birth_place", "")

            try:
                birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
                chart_obj = calculate_chart_data(birth_dt, float(lat), float(lon), tz_str)
                chart = chart_obj.model_dump()
                chart.update({
                    "name": name, "place": place, "birth_dob": dob, "birth_tob": tob,
                    "latitude": float(lat), "longitude_coord": float(lon),
                    "timezone": tz_str, "birth_datetime": birth_dt.isoformat()
                })
                _enrich_chart_for_template(chart)
                return chart, chart_obj
            except Exception as e:
                print(f"ERROR: Failed to calculate chart from session: {e}")
                # Don't return yet, try fallback

        # Fallback to Vault (latest saved chart)
        latest = list_charts()
        if latest:
            chart = latest[0]
            _enrich_chart_for_template(chart)

            # Sync session so subsequent pages don't need to query vault
            session["birth_lat"]   = chart.get("latitude", 28.6139)
            session["birth_lon"]   = chart.get("longitude_coord", 77.2090)
            session["birth_tz"]    = chart.get("timezone", "Asia/Kolkata")
            session["birth_name"]  = chart.get("name", "")
            session["birth_place"] = chart.get("place", "")
            bd = chart.get("birth_datetime", "")[:16]
            if "T" in bd:
                session["birth_dob"] = bd[:10]
                session["birth_tob"] = bd[11:16]

            try:
                birth_dt = datetime.fromisoformat(chart["birth_datetime"])
                chart_obj = calculate_chart_data(birth_dt, float(session["birth_lat"]), float(session["birth_lon"]), session["birth_tz"])
                return chart, chart_obj
            except Exception as e:
                print(f"ERROR: Failed to calculate chart from vault: {e}")

    except Exception as e:
        print(f"CRITICAL: _load_active_chart failed: {e}")

    return None, None


# ─────────────────────────────────────────────
#  Kundli (birth chart)
# ─────────────────────────────────────────────
@main.route("/kundli", methods=["GET", "POST"])
def kundli():
    error = None
    chart = None
    dasha = None
    remedies = None

    if request.method == "GET":
        chart, chart_obj = _load_active_chart()
        if chart_obj:
            try:
                remedies = get_remedies(chart_obj)
                birth_dt = datetime.fromisoformat(chart["birth_datetime"])
                moon_lon = chart["planets"]["Moon"]["longitude"]
                dasha    = calculate_vimshottari(moon_lon, birth_dt)
            except Exception: pass

    if request.method == "POST":
        try:
            name   = request.form.get("name", "").strip()
            dob    = request.form.get("dob", "")
            tob    = request.form.get("tob", "")
            place  = request.form.get("place", "").strip()
            lat    = request.form.get("lat", "")
            lon    = request.form.get("lon", "")
            tz_str = request.form.get("timezone", "Asia/Kolkata")

            if not dob or not tob:
                raise ValueError("Date and time of birth are required.")

            if not lat or not lon:
                geo = geocode_place(place or "New Delhi")
                lat, lon, tz_str = geo["lat"], geo["lon"], geo["timezone"]
                place = geo.get("display_name", place)

            # Persist in session
            session["birth_lat"]   = float(lat)
            session["birth_lon"]   = float(lon)
            session["birth_tz"]    = tz_str
            session["birth_name"]  = name
            session["birth_place"] = place
            session["birth_dob"]   = dob
            session["birth_tob"]   = tob

            birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
            chart_obj = calculate_chart_data(birth_dt, float(lat), float(lon), tz_str)
            chart = chart_obj.model_dump()
            chart.update({
                "name": name, "place": place, "birth_dob": dob, "birth_tob": tob,
                "latitude": float(lat), "longitude_coord": float(lon),
                "timezone": tz_str, "birth_datetime": birth_dt.isoformat()
            })

            _enrich_chart_for_template(chart)
            save_chart(chart)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"ok": True, "redirect": url_for("main.dashboard")})
            return redirect(url_for("main.dashboard"))

        except Exception as e:
            error = str(e)
            traceback.print_exc()

    return render_template("kundli.html", chart=chart, dasha=dasha, remedies=remedies, error=error)


# ─────────────────────────────────────────────
#  Save chart
# ─────────────────────────────────────────────
@main.route("/kundli/save", methods=["POST"])
def save_kundli():
    data = request.get_json(silent=True) or {}
    chart_data = data.get("chart")
    if not chart_data:
        return jsonify({"error": "No chart data"}), 400
    cid = save_chart(chart_data)
    return jsonify({"id": cid, "message": "Chart saved successfully"})


# ─────────────────────────────────────────────
#  Load saved chart
# ─────────────────────────────────────────────
@main.route("/kundli/load/<cid>")
def load_kundli(cid):
    chart = get_chart(cid)
    if not chart:
        flash("Chart not found.", "danger")
        return redirect(url_for("main.index"))

    _enrich_chart_for_template(chart)

    # Reconstitute session from saved chart
    session["birth_lat"]   = chart.get("latitude", 28.6139)
    session["birth_lon"]   = chart.get("longitude_coord", 77.2090)
    session["birth_tz"]    = chart.get("timezone", "Asia/Kolkata")
    session["birth_name"]  = chart.get("name", "")
    session["birth_place"] = chart.get("place", "")
    bd = chart.get("birth_datetime", "")[:16]
    if "T" in bd:
        session["birth_dob"] = bd[:10]
        session["birth_tob"] = bd[11:16]

    # ?next= lets callers redirect straight to predictions/transit/dasha
    next_page = request.args.get("next", "")
    allowed   = {"predictions", "transit", "dasha", "panchang", "kundli"}
    if next_page in allowed:
        return redirect(url_for(f"main.{next_page}"))

    # Default: render full kundli chart
    dasha = None
    try:
        if "planets" in chart and "Moon" in chart["planets"]:
            moon_lon = chart["planets"]["Moon"]["longitude"]
            birth_dt = datetime.fromisoformat(chart["birth_datetime"])
            dasha = calculate_vimshottari(moon_lon, birth_dt)
    except Exception as de:
        print(f"ERROR: Dasha calculation failed: {de}")

    return render_template("kundli.html", chart=chart, dasha=dasha, error=None)


# ─────────────────────────────────────────────
#  Delete saved chart
# ─────────────────────────────────────────────
@main.route("/kundli/delete/<cid>", methods=["POST"])
def delete_kundli(cid):
    delete_chart(cid)
    return jsonify({"ok": True})


# ─────────────────────────────────────────────
#  User Dashboard (Redesigned)
# ─────────────────────────────────────────────
# Simple Global Cache for Dashboard Performance
DASHBOARD_CACHE = {}

@main.route("/dashboard")
def dashboard():
    chart, chart_obj = _load_active_chart()

    if not chart_obj:
        flash("Please generate a Kundli first to view your dashboard.", "warning")
        return redirect(url_for("main.index"))

    # 1. Check Cache (valid for 15 minutes)
    cache_key = f"{session.get('active_chart_id')}_{datetime.now().strftime('%Y%m%d%H%M')[:11]}" # 10m resolution
    if cache_key in DASHBOARD_CACHE:
        age = (datetime.now() - DASHBOARD_CACHE[cache_key]['ts']).total_seconds()
        if age < 900: # 15 minutes
             return render_template("dashboard.html", **DASHBOARD_CACHE[cache_key]['data'])

    try:
        # ... (rest of implementation)
        name = session.get("birth_name", "Native")
        lat = session.get("birth_lat")
        lon = session.get("birth_lon")
        tz = session.get("birth_tz")

        # Generate full insight engine results
        from .astrology.predictions.engine import generate_evidence_based_predictions
        from .astrology.panchang import calculate_panchang

        preds = generate_evidence_based_predictions(chart_obj)
        panchang = calculate_panchang(datetime.now().date(), float(lat), float(lon), tz, chart_obj.planets["Moon"].nakshatra.index)

        # Add sky data directly
        sky = get_sunrise_sunset_moonrise(datetime.now().date(), float(lat), float(lon), tz)

        # Add panchang and sky to preds for Resonance Center
        preds["panchang"] = panchang
        preds["sky"] = sky
        preds["name"] = name

        # 0.4. Add Panchapakshi details
        from .astrology.core.panchapakshi import get_panchapakshi_info, get_current_activity
        moon_nak_idx = chart_obj.planets["Moon"].nakshatra.index
        is_shukla = panchang["tithi"]["number"] <= 15
        bird = get_panchapakshi_info(moon_nak_idx + 1, is_shukla)

        # Calculate Segment (Simplified for dashboard)
        weekday = datetime.now().weekday()
        # Segment 2 is typically afternoon
        activity = get_current_activity(bird, (weekday + 1) % 7, 2)
        preds["panchapakshi"] = {"bird": bird, "activity": activity}

        # 0.5. Add Muhurta Highlights
        from .astrology.panchang.muhurta import check_muhurta_suitability
        events = ["Financial Investment", "Travel", "New Job Joining", "Business Opening"]
        preds["muhurta_highlights"] = []
        for ev in events:
            suit = check_muhurta_suitability(ev, panchang)
            if suit["status"] == "Auspicious":
                preds["muhurta_highlights"].append({"name": ev, "status": suit["status"], "score": suit["score"]})

        # 0.6. Add Active Remedy Quests
        from .astrology.remedies.engine import get_remedies
        remedies = get_remedies(chart_obj)
        preds["active_quests"] = [r for r in remedies if r.get("quest")][:2]

        # 0.7. Add Retrograde (Karmic) Alerts
        preds["karmic_alerts"] = []
        for p, info in chart_obj.planets.items():
            if info.is_retrograde:
                preds["karmic_alerts"].append({
                    "planet": p,
                    "interpretation": f"{p} is Retrograde, indicating deep karmic review in House {info.house} themes."
                })

        # Map fields for template compatibility
        preds["score"] = round(preds["overall_score"] / 10, 1)
        preds["score_label"] = preds["overall_label"]
        preds["score_color"] = "#16a34a" if preds["overall_score"] >= 65 else "#fbbf24" if preds["overall_score"] >= 45 else "#dc2626"
        preds["score_color"] = (
            "#16a34a" if preds["overall_score"] >= 80 else
            "#65a30d" if preds["overall_score"] >= 65 else
            "#d97706" if preds["overall_score"] >= 45 else
            "#dc2626"
        )

        template_data = {"preds": preds, "chart": chart}
        DASHBOARD_CACHE[cache_key] = {"ts": datetime.now(), "data": template_data}

        return render_template("dashboard.html", **template_data)
    except Exception as e:
        traceback.print_exc()
        return f"Error loading dashboard: {str(e)}", 500


# ─────────────────────────────────────────────
#  Cosmic DNA (Multiversal Profile)
# ─────────────────────────────────────────────
@main.route("/cosmic-dna")
def cosmic_dna():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to unlock your Cosmic DNA profile.", "info")
        return redirect(url_for("main.index"))

    try:
        dna = {
            "vedic": {
                "lagna": chart["lagna"]["rashi_name"],
                "moon": chart["planets"]["Moon"]["rashi_name"],
                "atmakaraka": chart["jaimini_karakas"].get('Atmakaraka (AK) - Soul'),
                "yogi": chart["yogi_details"].get('Yogi'),
            },
            "bazi": {
                "day_master": chart_obj.bazi_pillars.get("DayMaster"),
                "self_element": chart_obj.bazi_pillars.get("Element"),
                "structure": chart_obj.bazi_pillars.get("Structure")
            },
            "human_design": chart_obj.human_design,
            "maya": {
                "seal": chart_obj.maya_tzolkin.get("name"),
                "tone": chart_obj.maya_tzolkin.get("number"),
                "kin_number": (chart_obj.maya_tzolkin.get("number", 1) - 1) * 20 + 1 # Placeholder Kin
            },
            "tibetan": {"mewa": chart_obj.tibetan_data.get('mewa'), "parkha": chart_obj.tibetan_data.get('parkha')},
            "celtic": chart_obj.celtic_tree,
            "native_american": chart_obj.native_american,
            "numerology": chart_obj.numerology,
            "iching": chart_obj.mundane_indicators.get('iching_hexagram'),
            "kabbalah": chart_obj.kabbalah
        }
        return render_template("cosmic_dna.html", dna=dna, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error decoding DNA: {str(e)}", 500


# ─────────────────────────────────────────────
#  Lexicon (Metaphysical Guide)
# ─────────────────────────────────────────────
@main.route("/lexicon")
def lexicon():
    from .astrology.core.lexicon import VEDIC_LEXICON
    return render_template("lexicon.html", terms=VEDIC_LEXICON)


# ─────────────────────────────────────────────
#  Cosmic Weather (Mundane)
# ─────────────────────────────────────────────
@main.route("/weather")
def cosmic_weather():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to see the local cosmic weather.", "info")
        return redirect(url_for("main.index"))

    try:
        weather = chart_obj.weather_indicators
        mundane = chart_obj.mundane_indicators
        return render_template("weather.html", weather=weather, mundane=mundane, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in weather engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Numerology (Lo Shu)
# ─────────────────────────────────────────────
@main.route("/numerology")
def numerology():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to unlock your Numerical Blueprint.", "info")
        return redirect(url_for("main.index"))

    try:
        from .astrology.core.numerology import get_numerology_data, get_lo_shu_grid
        dob = chart.get("birth_dob")
        num = get_numerology_data(dob)
        grid = get_lo_shu_grid(dob)
        return render_template("numerology.html", num=num, grid=grid, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in numerology engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Cosmic Markets (Financial Astrology)
# ─────────────────────────────────────────────
@main.route("/markets")
def cosmic_markets():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to unlock the Cosmic Markets pulse.", "info")
        return redirect(url_for("main.index"))

    try:
        from .astrology.predictions.financial import get_financial_market_indicators
        from .astrology.predictions.crypto import get_crypto_market_analysis

        financial = get_financial_market_indicators(chart_obj)
        crypto = get_crypto_market_analysis(chart_obj)

        return render_template("markets.html", financial=financial, crypto=crypto, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in market engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Yoga Gallery (Celestial Combinations)
# ─────────────────────────────────────────────
@main.route("/yogas")
def yoga_gallery():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to view your yoga gallery.", "info")
        return redirect(url_for("main.index"))

    try:
        # All detected yogas in user's chart
        user_yogas = chart_obj.yogas

        # Build a master list of possible yogas for the gallery
        from .astrology.yogas.detector import check_pancha_mahapurusha
        # Mocking a full planets dict to see all possible yogas (simplified)
        master_yogas = [
            {"name": "Gaja Kesari Yoga", "theme": "Success & Wisdom", "desc": "Jupiter in a Kendra from Moon."},
            {"name": "Budha Aditya Yoga", "theme": "Intelligence", "desc": "Sun and Mercury conjunction."},
            {"name": "Lakshmi Yoga", "theme": "Wealth", "desc": "Strong 9th and 1st lords association."},
            {"name": "Ruchaka Yoga", "theme": "Courage", "desc": "Strong Mars in Kendra."},
            {"name": "Hamsa Yoga", "theme": "Prosperity", "desc": "Strong Jupiter in Kendra."},
            {"name": "Malavya Yoga", "theme": "Art & Luxury", "desc": "Strong Venus in Kendra."},
            {"name": "Shasha Yoga", "theme": "Persistence", "desc": "Strong Saturn in Kendra."},
            {"name": "Bhadra Yoga", "theme": "Analytical", "desc": "Strong Mercury in Kendra."},
            {"name": "Adhi Yoga", "theme": "Leadership", "desc": "Benefics in 6, 7, 8 from Moon."},
            {"name": "Saraswati Yoga", "theme": "Learning", "desc": "Jupiter, Venus, Mercury in specific houses."},
            {"name": "Vipareeta Raja Yoga", "theme": "Sudden Success", "desc": "Dusthana lords in other Dusthanas."},
            {"name": "Kala Sarpa Yoga", "theme": "Karmic Struggle", "desc": "Planets hemmed between nodes."},
            {"name": "Kemadruma Yoga", "theme": "Isolation", "desc": "No planets adjacent to Moon."}
        ]

        present_names = [y["name"] for y in user_yogas]
        for y in master_yogas:
            y["is_present"] = any(name in y["name"] for name in present_names)

        return render_template("yogas.html", master_yogas=master_yogas, user_yogas=user_yogas, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error building yoga gallery: {str(e)}", 500


# ─────────────────────────────────────────────
#  Ashtakavarga Matrix
# ─────────────────────────────────────────────
@main.route("/ashtakavarga")
def ashtakavarga():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to view the Ashtakavarga matrix.", "info")
        return redirect(url_for("main.index"))

    try:
        av = chart_obj.ashtakavarga
        # BAV = Benefic Points for each planet (Dict[Planet, List[int]])
        # SAV = Sarvashtakavarga (Sum of all BAVs)
        return render_template("ashtakavarga.html", av=av, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error building ashtakavarga matrix: {str(e)}", 500


# ─────────────────────────────────────────────
#  Nakshatra Symphony (Lunar Mansions)
# ─────────────────────────────────────────────
@main.route("/nakshatras")
def nakshatra_symphony():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to view your Nakshatra Symphony.", "info")
        return redirect(url_for("main.index"))

    try:
        from .astrology.core.nakshatra_data import NAKSHATRA_DEITIES, NAKSHATRA_SYMBOLS
        from .astrology.core.planets import NAKSHATRA_NAMES

        nak_data = []
        for i in range(27):
            planets_in = [p for p, info in chart_obj.planets.items() if info.nakshatra.index == i]
            nak_data.append({
                "index": i + 1,
                "name": NAKSHATRA_NAMES[i],
                "deity": NAKSHATRA_DEITIES[i],
                "symbol": NAKSHATRA_SYMBOLS[i],
                "planets": planets_in
            })

        return render_template("nakshatras.html", nak_data=nak_data, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error building symphony: {str(e)}", 500


# ─────────────────────────────────────────────
#  Esoteric Audit (Supreme Precision)
# ─────────────────────────────────────────────
@main.route("/esoteric")
def esoteric_audit():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to unlock the Esoteric Audit.", "info")
        return redirect(url_for("main.index"))

    try:
        # Vaisheshikamsha Audit
        vaisheshika = {}
        for p_name, p_info in chart_obj.planets.items():
            if p_info.vaisheshikamsha and p_info.vaisheshikamsha != "None":
                v_count = 0
                if p_info.shadbala_details:
                    v_count = getattr(p_info.shadbala_details, "naisargika_bala", 0)

                vaisheshika[p_name] = {
                    "level": p_info.vaisheshikamsha,
                    "count": v_count
                }

        metrics = {
            "special_lagnas": chart_obj.special_lagnas,
            "arudha_padas": chart_obj.arudha_padas,
            "nadi_signatures": chart_obj.nadi_signatures,
            "harmonic_resonances": chart_obj.harmonic_resonances,
            "bazi_pillars": chart_obj.bazi_pillars,
            "kp_4_steps": chart_obj.kp_4_steps,
            "vaisheshikamsha": vaisheshika
        }
        return render_template("esoteric.html", metrics=metrics, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in esoteric engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Galactic Audit (Cosmic Connections)
# ─────────────────────────────────────────────
@main.route("/galactic")
def galactic_audit():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to view your Galactic Audit.", "info")
        return redirect(url_for("main.index"))

    try:
        from .astrology.core.galactic import analyze_galactic_aspects
        from .astrology.core.fixed_stars import analyze_fixed_star_conjunctions

        galactic = analyze_galactic_aspects(chart_obj.planets)
        stars = analyze_fixed_star_conjunctions(chart_obj.planets, chart_obj.ayanamsa)

        return render_template("galactic.html", galactic=galactic, stars=stars, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in galactic engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Chakra Alignment (Energy Centers)
# ─────────────────────────────────────────────
@main.route("/chakras")
def chakra_alignment():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to view your Chakra Alignment.", "info")
        return redirect(url_for("main.index"))

    try:
        # Chakra to Planet Mapping
        # Muladhara: Saturn
        # Svadhisthana: Jupiter
        # Manipura: Mars
        # Anahata: Venus
        # Vishuddha: Mercury
        # Ajna: Moon (and Sun)
        # Sahasrara: Guru (Higher Jupiter)

        chakra_data = [
            {"name": "Muladhara (Root)", "planet": "Saturn", "color": "#ef4444", "theme": "Survival & Stability"},
            {"name": "Svadhisthana (Sacral)", "planet": "Jupiter", "color": "#f97316", "theme": "Creativity & Joy"},
            {"name": "Manipura (Solar Plexus)", "planet": "Mars", "color": "#eab308", "theme": "Will & Power"},
            {"name": "Anahata (Heart)", "planet": "Venus", "color": "#22c55e", "theme": "Love & Harmony"},
            {"name": "Vishuddha (Throat)", "planet": "Mercury", "color": "#3b82f6", "theme": "Communication & Truth"},
            {"name": "Ajna (Third Eye)", "planet": "Moon", "color": "#6366f1", "theme": "Intuition & Vision"},
            {"name": "Sahasrara (Crown)", "planet": "Sun", "color": "#a855f7", "theme": "Higher Consciousness"}
        ]

        for c in chakra_data:
            p_info = chart_obj.planets.get(c["planet"])
            if p_info:
                c["strength"] = p_info.shadbala_score or 50
                c["dignity"] = p_info.dignity
                c["house"] = p_info.house

        return render_template("chakras.html", chakras=chakra_data, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in chakra engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Eclipse Watch (Karmic Triggers)
# ─────────────────────────────────────────────
@main.route("/eclipses")
def eclipse_watch():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to view your Eclipse Watch.", "info")
        return redirect(url_for("main.index"))

    try:
        eclipses = chart_obj.upcoming_eclipses
        impacts = chart_obj.eclipse_impacts
        return render_template("eclipses.html", eclipses=eclipses, impacts=impacts, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in eclipse engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Friendship Matrix (Panchadha Maitri)
# ─────────────────────────────────────────────
@main.route("/friendship")
def friendship_matrix():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to view your Friendship Matrix.", "info")
        return redirect(url_for("main.index"))

    try:
        from .astrology.strength.friendship import get_compound_friendship
        planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

        matrix = {}
        for p1 in planets:
            matrix[p1] = {}
            for p2 in planets:
                if p1 == p2:
                    matrix[p1][p2] = "Self"
                else:
                    matrix[p1][p2] = get_compound_friendship(p1, p2, chart_obj.planets[p1].house, chart_obj.planets[p2].house)

        return render_template("friendship.html", matrix=matrix, planets=planets, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in friendship engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Life Calendar (Timing Synthesis)
# ─────────────────────────────────────────────
@main.route("/calendar")
def life_calendar():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to unlock your Life Calendar.", "info")
        return redirect(url_for("main.index"))

    try:
        from .astrology.core.biorhythms import calculate_biorhythms
        from .astrology.panchang import calculate_panchang

        # Current month focus
        today = datetime.now()
        bio = calculate_biorhythms(chart_obj.birth_datetime, today)

        # Weekly flow
        week_flow = []
        for i in range(7):
            d = today + timedelta(days=i)
            pan = calculate_panchang(d.date(), chart_obj.latitude, chart_obj.longitude, chart_obj.timezone, chart_obj.planets["Moon"].nakshatra.index)
            # Simple day quality score
            score = 50
            if pan["tithi"]["nature"] == "Auspicious": score += 10
            if pan["nakshatra"]["nature"] == "Auspicious": score += 10
            if pan["yoga"]["nature"] == "Auspicious": score += 10

            week_flow.append({
                "date": d.strftime("%d %b"),
                "day": d.strftime("%a"),
                "score": score,
                "tithi": pan["tithi"]["name"],
                "nakshatra": pan["nakshatra"]["name"]
            })

        return render_template("calendar.html", bio=bio, week_flow=week_flow, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error building calendar: {str(e)}", 500


# ─────────────────────────────────────────────
#  Astro-Locality (Relocation)
# ─────────────────────────────────────────────
@main.route("/relocation")
def relocation():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to see your global power lines.", "info")
        return redirect(url_for("main.index"))

    try:
        from .astrology.core.relocation import get_angular_points
        from .astrology.core.datetime import datetime_to_jd

        jd_ut = datetime_to_jd(chart_obj.birth_datetime, "UTC")
        lines = get_angular_points(jd_ut)

        # Add some major cities for comparison
        try:
            from .astrology.core.cities import MAJOR_CITIES
        except ImportError:
            MAJOR_CITIES = [
                {"name": "New Delhi", "lat": 28.6, "lon": 77.2},
                {"name": "London", "lat": 51.5, "lon": -0.1},
                {"name": "New York", "lat": 40.7, "lon": -74.0}
            ]

        city_scores = []

        for city in MAJOR_CITIES[:20]:
            # Simple score based on proximity to angular lines
            # This is a placeholder for more complex logic
            score = 50
            for p, data in lines.items():
                if abs(city["lon"] - data["MC_Longitude"]) < 5: score += 10
                if abs(city["lon"] - data["IC_Longitude"]) < 5: score += 5

            city_scores.append({
                "name": city["name"],
                "score": min(100, score),
                "lat": city["lat"],
                "lon": city["lon"]
            })

        city_scores.sort(key=lambda x: x["score"], reverse=True)

        return render_template("relocation.html", lines=lines, city_scores=city_scores, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in relocation engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Transit chart
# ─────────────────────────────────────────────
@main.route("/transit")
def transit():
    tz_str = session.get("birth_tz", "Asia/Kolkata")
    lat    = session.get("birth_lat", 28.6139)
    lon    = session.get("birth_lon", 77.2090)
    name   = session.get("birth_name", "Transit")
    place  = session.get("birth_place", "")

    # Optional date override for Time Machine
    date_str      = request.args.get("date", "")
    selected_date = datetime.now(pytz.timezone(tz_str))
    if date_str:
        try:
            parsed = datetime.strptime(date_str, "%Y-%m-%d")
            # Maintain current HH:MM:SS but at the target date
            selected_date = selected_date.replace(year=parsed.year, month=parsed.month, day=parsed.day)
        except ValueError:
            pass

    transit_data = calculate_transit_chart(float(lat), float(lon), tz_str, selected_date)

    natal_chart = None
    dob = session.get("birth_dob")
    tob = session.get("birth_tob")
    if dob and tob:
        try:
            birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
            natal_chart_obj = calculate_chart_data(birth_dt, float(lat), float(lon), tz_str)
            natal_chart = natal_chart_obj.model_dump()
            _enrich_chart_for_template(natal_chart)
        except Exception:
            pass

    # Build nakshatra-in-house mapping for transit
    nak_house_map = []
    if transit_data and "planets" in transit_data:
        nak_house_map = _build_nak_house_map(transit_data, natal_chart)

    # 3. Vedha Analysis
    vedha_alerts = []
    if natal_chart and "planets" in natal_chart and "Moon" in natal_chart["planets"]:
        from .astrology.transit.vedha import check_vedha
        n_moon_rashi = natal_chart["planets"]["Moon"]["rashi"]

        # ... (rest of vedha logic)

        # Prepare transit data relative to moon
        t_for_vedha = {}
        for p, data in transit_data["planets"].items():
            t_rashi = data["rashi"]
            t_house_from_moon = (t_rashi - n_moon_rashi + 12) % 12 + 1
            t_for_vedha[p] = {"house_from_moon": t_house_from_moon}

        # Prepare natal positions relative to moon
        n_for_vedha = {h: [] for h in range(1, 13)}
        for p, data in natal_chart["planets"].items():
            n_rashi = data["rashi"]
            n_house_from_moon = (n_rashi - n_moon_rashi + 12) % 12 + 1
            n_for_vedha[n_house_from_moon].append(p)

        vedha_alerts = check_vedha(t_for_vedha, n_for_vedha)

    return render_template("transit.html",
                           transit=transit_data,
                           natal=natal_chart,
                           nak_house_map=nak_house_map,
                           vedha_alerts=vedha_alerts,
                           tz_str=tz_str,
                           selected_date=selected_date.strftime("%Y-%m-%d"))


# ─────────────────────────────────────────────
#  Dasha
# ─────────────────────────────────────────────
@main.route("/dasha")
def dasha():
    dob = session.get("birth_dob")
    tob = session.get("birth_tob")
    lat = session.get("birth_lat", 28.6139)
    lon = session.get("birth_lon", 77.2090)
    tz  = session.get("birth_tz", "Asia/Kolkata")

    dasha_data = None
    chart      = None
    error      = None

    if dob and tob:
        try:
            birth_dt   = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
            chart_obj  = calculate_chart_data(birth_dt, float(lat), float(lon), tz)
            chart      = chart_obj.model_dump()
            moon_lon   = chart["planets"]["Moon"]["longitude"]
            moon_nak_idx = chart["planets"]["Moon"]["nakshatra"]["index"]

            dasha_data = calculate_vimshottari(moon_lon, birth_dt)

            from .astrology.dasha.yogini import calculate_yogini_dasha
            yogini_data = calculate_yogini_dasha(moon_nak_idx, birth_dt)
            for m in yogini_data["mahadashas"]:
                m["start_str"] = m["start"].strftime("%d %b %Y")
                m["end_str"] = m["end"].strftime("%d %b %Y")

            _enrich_chart_for_template(chart)

            # 3. Enhanced Dasha Activation logic
            from .astrology.core.houses import get_house_lord
            current_maha = dasha_data.get("current_maha", {}).get("lord")
            current_antar = dasha_data.get("current_antar", {}).get("lord")

            # Find houses ruled by current lords
            activated_houses = []
            for h in range(1, 13):
                lord = chart_obj.house_lords[h]
                if lord in [current_maha, current_antar]:
                    activated_houses.append({"house": h, "lord": lord, "theme": HOUSE_INTERPRETATIONS.get(h)})

            dasha_data["activated_houses"] = activated_houses

        except Exception as e:
            error = str(e)
            traceback.print_exc()
    else:
        error = "Please generate a Kundli first."

    return render_template("dasha.html", dasha=dasha_data, yogini=yogini_data, chart=chart, error=error)


# ─────────────────────────────────────────────
#  Predictions
# ─────────────────────────────────────────────
@main.route("/predictions")
def predictions():
    dob   = session.get("birth_dob")
    tob   = session.get("birth_tob")

    # Auto-load latest if session is empty
    if not (dob and tob):
        latest = list_charts()
        if latest:
            c = latest[0]
            session["birth_lat"]   = c.get("latitude", 28.6139)
            session["birth_lon"]   = c.get("longitude_coord", 77.2090)
            session["birth_tz"]    = c.get("timezone", "Asia/Kolkata")
            session["birth_name"]  = c.get("name", "")
            session["birth_place"] = c.get("place", "")
            bd = c.get("birth_datetime", "")[:16]
            if "T" in bd:
                session["birth_dob"] = bd[:10]
                session["birth_tob"] = bd[11:16]
            dob, tob = session["birth_dob"], session["birth_tob"]

    lat   = session.get("birth_lat", 28.6139)
    lon   = session.get("birth_lon", 77.2090)
    tz    = session.get("birth_tz", "Asia/Kolkata")
    name  = session.get("birth_name", "Native")
    place = session.get("birth_place", "")

    # Optional date override (for calendar navigation)
    date_str      = request.args.get("date", "")
    today         = date.today()
    selected_date = today
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            pass

    preds  = None
    error  = None

    if not (dob and tob):
        error = "Please generate a Kundli first to see predictions."
        return render_template("predictions.html", preds=None, error=error,
                               selected_date=selected_date.isoformat(),
                               today=today.isoformat())

    try:
        birth_dt    = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        natal_chart = calculate_chart_data(birth_dt, float(lat), float(lon), tz)

        # 1. Get Panchang for the selected date
        from .astrology.panchang import calculate_panchang
        # We need the natal moon nakshatra for Tarabala
        moon_nak_idx = natal_chart.planets["Moon"].nakshatra.index
        # Get yesterday for next_sr calculation
        yest = selected_date - timedelta(days=1)
        panchang = calculate_panchang(selected_date, float(lat), float(lon), tz, moon_nak_idx)

        # 2. Generate evidence-based predictions
        # Convert selected_date (date object) to datetime for the engine
        dt_for_engine = datetime.combine(selected_date, datetime.min.time())
        preds = generate_evidence_based_predictions(natal_chart, selected_date=dt_for_engine)

        # 3. Merge for template compatibility
        preds["date"] = selected_date.strftime("%A, %d %B %Y")
        preds["name"] = name
        preds["panchang"] = panchang

        # Map fields for template
        preds["score"] = round(preds["overall_score"] / 10, 1)
        preds["score_label"] = preds["overall_label"]
        preds["score_color"] = (
            "#16a34a" if preds["overall_score"] >= 80 else
            "#65a30d" if preds["overall_score"] >= 65 else
            "#d97706" if preds["overall_score"] >= 45 else
            "#dc2626"
        )

        preds["tithi_name"] = panchang["tithi"]["name"]
        preds["yoga_name"] = panchang["yoga"]["name"]
        preds["panchang_ok"] = panchang["is_auspicious"]

        # 4. Fill extras for template compatibility
        _enrich_predictions_with_extras(preds, natal_chart, panchang)

        # 4b. Lal Kitab Remedies
        from .astrology.remedies.engine import get_lal_kitab_remedies
        preds["lalkitab_remedies"] = get_lal_kitab_remedies(natal_chart)

        # 4c. AI Insight (optional)
        if os.getenv("LLM_MODEL"):
             preds["ai_note"] = _llm_day_note(panchang, {"score": preds["score"], "label": preds["score_label"]}, selected_date.isoformat())

        # 5. Personalized Day Score Adjustment
        if "tarabala" in panchang:
            if panchang["tarabala"]["quality"] == "Inauspicious":
                preds["score"] = max(1.0, preds["score"] - 1.5)
                preds["panchang_ok"] = False
            elif "Auspicious" in panchang["tarabala"]["quality"]:
                preds["score"] = min(10.0, preds["score"] + 1.0)

        # 6. House Activation for Day
        transit_moon_house = preds.get("moon_house_from_natal", 1)
        preds["activated_house_theme"] = HOUSE_INTERPRETATIONS.get(transit_moon_house, "General themes.")

        # 7. Hora Awareness
        preds["hora_status"] = "Neutral"
        if panchang.get("current_hora") == natal_chart.house_lords[1]:
            preds["hora_status"] = "Peak Performance: Current hour lord aligns with your Lagna Lord."

    except Exception as e:
        error = str(e)
        traceback.print_exc()

    return render_template("predictions.html", preds=preds, error=error,
                           name=name, place=place,
                           selected_date=selected_date.isoformat(),
                           today=today.isoformat())

# ─────────────────────────────────────────────
#  Shani (Saturn) Engine
# ─────────────────────────────────────────────
@main.route("/shani")
def shani_report():
    dob = session.get("birth_dob")
    tob = session.get("birth_tob")
    lat = session.get("birth_lat", 28.6139)
    lon = session.get("birth_lon", 77.2090)
    tz  = session.get("birth_tz", "Asia/Kolkata")

    if not (dob and tob):
        return redirect(url_for("main.index"))

    try:
        from .astrology.transit.shani import calculate_sade_sati, get_shani_status
        birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        chart = calculate_chart_data(birth_dt, float(lat), float(lon), tz)

        moon_rashi = chart.planets["Moon"].rashi
        asc_rashi = chart.asc_rashi

        status = get_shani_status(moon_rashi, asc_rashi)
        timeline = calculate_sade_sati(moon_rashi)

        from .astrology.panchang import RASHI_NAMES
        return render_template("shani.html",
                               status=status,
                               timeline=timeline,
                               rashi_names=RASHI_NAMES,
                               name=session.get("birth_name", "Native"))
    except Exception as e:
        traceback.print_exc()
        return str(e), 500

# ─────────────────────────────────────────────
#  Varshaphala (Yearly Chart)
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
#  Varshaphala (Yearly Progress)
# ─────────────────────────────────────────────
@main.route("/varshaphala")
def varshaphala():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        flash("Generate a Kundli first to view your Yearly Solar Return.", "info")
        return redirect(url_for("main.index"))

    try:
        lat, lon, tz = chart_obj.latitude, chart_obj.longitude, chart_obj.timezone

        # Current/Next solar return year
        target_year = date.today().year

        from .astrology.core.varshaphala import get_solar_return_jd, get_varshaphala_data
        from .astrology.core.datetime import datetime_to_jd

        natal_jd = datetime_to_jd(chart_obj.birth_datetime, tz)
        sr_jd = get_solar_return_jd(natal_jd, target_year)

        # Calculate chart for that exact moment
        from .astrology.core.swe_proxy import swe as swe_mod
        y, m, d, h = swe_mod.revjul(sr_jd)
        sr_dt_utc = datetime(y, m, d, int(h), int((h%1)*60))

        # Create the yearly chart
        from .astrology.core.chart import calculate_chart_data
        yearly_chart_obj = calculate_chart_data(sr_dt_utc, float(lat), float(lon), "UTC")
        yearly_chart = yearly_chart_obj.model_dump()

        # Natal lagna for Muntha
        extra = get_varshaphala_data(chart_obj.birth_datetime, chart_obj.asc_rashi, target_year)

        yearly_chart["name"] = f"Solar Return {target_year}"
        yearly_chart["age"] = extra["age"]
        yearly_chart["muntha_rashi"] = extra["muntha_rashi"]
        yearly_chart["muntha_house"] = extra["muntha_house"]
        yearly_chart["varsheshwar"] = yearly_chart_obj.varsheshwar

        # Mudda Dasha
        from .astrology.dasha.mudda import calculate_mudda_dasha
        try:
            mudda = calculate_mudda_dasha(yearly_chart["planets"]["Moon"]["longitude"], sr_dt_utc)
        except Exception as me:
            print(f"ERROR: Mudda calculation failed: {me}")
            mudda = {"mahadashas": []}

        _enrich_chart_for_template(yearly_chart)

        return render_template("varshaphala.html", yearly=yearly_chart, mudda=mudda, chart=chart)
    except Exception as e:
        traceback.print_exc()
        return f"Error in Varshaphala engine: {str(e)}", 500


# ─────────────────────────────────────────────
#  Prashna (Horary)
# ─────────────────────────────────────────────
@main.route("/prashna", methods=["GET", "POST"])
def prashna():
    chart, chart_obj = _load_active_chart()
    if not chart_obj:
        # For Prashna, we only need the user's current location, which we get from session
        lat = session.get("birth_lat", 28.6139)
        lon = session.get("birth_lon", 77.2090)
        tz  = session.get("birth_tz", "Asia/Kolkata")
    else:
        lat, lon, tz = chart_obj.latitude, chart_obj.longitude, chart_obj.timezone

    now = datetime.now(pytz.timezone(tz))
    result = None
    prashna_chart = None

    if request.method == "POST":
        q_type = request.form.get("question_type", "Career")

        from .astrology.prashna.engine import calculate_prashna_chart, analyze_prashna
        from .astrology.panchang import calculate_panchang

        prashna_chart_obj = calculate_prashna_chart(now, float(lat), float(lon), tz)
        panchang = calculate_panchang(now.date(), float(lat), float(lon), tz)

        result = analyze_prashna(prashna_chart_obj, q_type, panchang=panchang)
        prashna_chart = prashna_chart_obj.model_dump()
        _enrich_chart_for_template(prashna_chart)

    return render_template("prashna.html", result=result, chart=prashna_chart, now=now)


# ─────────────────────────────────────────────
#  Matchmaking (Guna Milan)
# ─────────────────────────────────────────────
@main.route("/matchmaking", methods=["GET", "POST"])
def matchmaking():
    result = None
    error = None
    boy_info = {}
    girl_info = {}

    if request.method == "POST":
        try:
            # Boy details
            b_name = request.form.get("b_name", "Boy")
            b_dob = request.form.get("b_dob")
            b_tob = request.form.get("b_tob")
            b_place = request.form.get("b_place")

            # Girl details
            g_name = request.form.get("g_name", "Girl")
            g_dob = request.form.get("g_dob")
            g_tob = request.form.get("g_tob")
            g_place = request.form.get("g_place")

            if not all([b_dob, b_tob, b_place, g_dob, g_tob, g_place]):
                raise ValueError("All fields are required for both Boy and Girl.")

            from .astrology.core.chart import calculate_chart_data
            from .astrology.matchmaking.engine import get_matchmaking_score

            # Process Boy
            b_geo = geocode_place(b_place)
            if "error" in b_geo: raise ValueError(f"Boy's location: {b_geo['error']}")

            b_dt = datetime.strptime(f"{b_dob} {b_tob}", "%Y-%m-%d %H:%M")
            b_chart = calculate_chart_data(b_dt, b_geo["lat"], b_geo["lon"], b_geo["timezone"])
            b_moon = b_chart.planets["Moon"]

            # Process Girl
            g_geo = geocode_place(g_place)
            if "error" in g_geo: raise ValueError(f"Girl's location: {g_geo['error']}")

            g_dt = datetime.strptime(f"{g_dob} {g_tob}", "%Y-%m-%d %H:%M")
            g_chart = calculate_chart_data(g_dt, g_geo["lat"], g_geo["lon"], g_geo["timezone"])
            g_moon = g_chart.planets["Moon"]

            result = get_matchmaking_score(b_chart, g_chart)

            boy_info = {"name": b_name, "nak": b_moon.nakshatra.name, "rashi": b_moon.rashi}
            girl_info = {"name": g_name, "nak": g_moon.nakshatra.name, "rashi": g_moon.rashi}

        except Exception as e:
            error = str(e)
            traceback.print_exc()

    return render_template("matchmaking.html", result=result, error=error,
                           boy=boy_info, girl=girl_info)


# ─────────────────────────────────────────────
#  PDF Report
# ─────────────────────────────────────────────
@main.route("/kundli/pdf")
def kundli_pdf():
    from fpdf import FPDF
    from datetime import datetime

    dob   = session.get("birth_dob")
    tob   = session.get("birth_tob")
    lat   = session.get("birth_lat", 28.6139)
    lon   = session.get("birth_lon", 77.2090)
    tz    = session.get("birth_tz", "Asia/Kolkata")
    name  = session.get("birth_name", "Native")
    place = session.get("birth_place", "")

    if not (dob and tob):
        return "Please generate a Kundli first.", 400

    try:
        birth_dt    = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        chart = calculate_chart_data(birth_dt, float(lat), float(lon), tz)
        preds = generate_evidence_based_predictions(chart)

        pdf = FPDF()
        pdf.add_page()

        # Background Aesthetic
        pdf.set_fill_color(10, 10, 15) # Dark Space
        pdf.rect(0, 0, 210, 297, "F")

        # Header Box
        pdf.set_fill_color(251, 191, 36) # Gold
        pdf.rect(10, 10, 190, 40, "F")

        pdf.set_font("helvetica", "B", 24)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 30, "CELESTIAL BLUEPRINT", ln=True, align="C")
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, -10, f"Birth Record for: {name}", ln=True, align="C")
        pdf.ln(25)

        # Content Background
        pdf.set_text_color(241, 245, 249) # White-ish

        # Section 1: Vital Stats
        pdf.set_font("helvetica", "B", 14)
        pdf.set_draw_color(139, 92, 246) # Accent
        pdf.cell(0, 10, "1. NATAL COORDINATES", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        pdf.set_font("helvetica", "", 11)
        pdf.cell(95, 8, f"Date: {dob}", ln=0)
        pdf.cell(95, 8, f"Time: {tob} ({tz})", ln=True)
        pdf.cell(95, 8, f"Location: {place}", ln=0)
        pdf.cell(95, 8, f"Geo: {lat}N, {lon}E", ln=True)
        pdf.cell(95, 8, f"Ayanamsa: {round(chart.ayanamsa, 4)} (Lahiri)", ln=1)
        pdf.ln(10)

        # Section 2: Planetary Alignment
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "2. COSMIC ALIGNMENT (GRAHA STHITI)", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        pdf.set_fill_color(20, 20, 30)
        pdf.set_text_color(251, 191, 36)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(30, 10, " Planet", border=0, fill=True)
        pdf.cell(30, 10, " Sign", border=0, fill=True)
        pdf.cell(35, 10, " Degree", border=0, fill=True)
        pdf.cell(20, 10, " House", border=0, fill=True)
        pdf.cell(45, 10, " Dignity", border=0, fill=True)
        pdf.cell(30, 10, " Status", border=0, fill=True, ln=True)

        pdf.set_text_color(241, 245, 249)
        pdf.set_font("helvetica", "", 10)
        for p_name, p in chart.planets.items():
            pdf.cell(30, 9, f" {p_name}", border=0)
            pdf.cell(30, 9, f" {p.rashi_name}", border=0)
            pdf.cell(35, 9, f" {p.dms}", border=0)
            pdf.cell(20, 9, f" {p.house}", border=0)
            pdf.cell(45, 9, f" {p.dignity}", border=0)
            status = "Direct" if not p.is_retrograde else "Retrograde"
            if p.is_combust: status += " (C)"
            pdf.cell(30, 9, f" {status}", border=0, ln=True)
        pdf.ln(10)

        # Section 3: Yogas
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "3. FORMED YOGAS (CELESTIAL COMBINATIONS)", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        for yoga in chart.yogas:
            pdf.set_font("helvetica", "B", 11)
            pdf.set_text_color(251, 191, 36)
            pdf.cell(0, 8, yoga["name"], ln=True)
            pdf.set_font("helvetica", "I", 10)
            pdf.set_text_color(161, 161, 170)
            pdf.multi_cell(0, 6, yoga["interpretation"])
            pdf.ln(2)
        pdf.ln(10)

        # Section 4: Domain Predictions
        pdf.add_page()
        pdf.set_fill_color(10, 10, 15); pdf.rect(0, 0, 210, 297, "F")
        pdf.set_text_color(241, 245, 249)

        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 15, "4. KARMIC INDICATORS & LIFE AREAS", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(8)

        for domain in preds["domains"]:
            # Domain Card Start
            start_y = pdf.get_y()
            if start_y > 240: pdf.add_page(); pdf.set_fill_color(10, 10, 15); pdf.rect(0, 0, 210, 297, "F"); start_y = 20

            pdf.set_font("helvetica", "B", 13)
            pdf.set_text_color(251, 191, 36)
            pdf.cell(0, 10, f"{domain['domain'].upper()} — {int(domain['score'])}% Intensity", ln=True)

            pdf.set_font("helvetica", "", 10)
            pdf.set_text_color(241, 245, 249)
            pdf.multi_cell(0, 6, domain["summary"])
            pdf.ln(2)

            pdf.set_font("helvetica", "I", 9)
            pdf.set_text_color(148, 163, 184)
            for ev in domain["evidence"]:
                pdf.cell(5)
                pdf.multi_cell(0, 5, f"> {ev}")

            pdf.ln(5)

        # Section 5: Life Timeline
        pdf.add_page()
        pdf.set_fill_color(10, 10, 15); pdf.rect(0, 0, 210, 297, "F")
        pdf.set_text_color(241, 245, 249)
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 15, "5. LIFE TIMELINE (VIMSHOTTARI FORECAST)", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)

        for item in preds["timeline"]:
            pdf.set_font("helvetica", "B", 12)
            pdf.set_text_color(251, 191, 36)
            pdf.cell(60, 8, f"{item['period']}", ln=0)
            pdf.set_font("helvetica", "", 10)
            pdf.set_text_color(148, 163, 184)
            pdf.cell(60, 8, f"({item['start']} - {item['end']})", ln=0)
            pdf.set_font("helvetica", "B", 10)
            pdf.set_text_color(241, 245, 249)
            pdf.cell(0, 8, f" {item['theme']}", ln=True)
            pdf.ln(2)

        # Footer
        pdf.set_y(280)
        pdf.set_font("helvetica", "I", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 10, "Generated by Jyotish Celestial OS. All data computed locally using Swiss Ephemeris.", align="C")

        from flask import Response
        return Response(
            pdf.output(),
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment;filename=jyotish_report_{name.replace(' ','_')}.pdf"}
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error generating PDF: {str(e)}", 500

# ─────────────────────────────────────────────
#  Data Sovereignty: Export All Profiles
# ─────────────────────────────────────────────
@main.route("/data/export")
def export_all_data():
    from .astrology.store import list_charts
    charts = list_charts()
    return Response(
        json.dumps(charts, indent=2),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=jyotish_dashboard_backup.json"}
    )

@main.route("/data/import", methods=["POST"])
def import_all_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        data = json.load(file)
        from .astrology.store import save_chart
        count = 0
        for item in data:
            # item is a dict with chart data
            save_chart(item)
            count += 1
        flash(f"Successfully imported {count} profiles!", "success")
    except Exception as e:
        flash(f"Import failed: {str(e)}", "danger")

    return redirect(url_for("main.index"))

@main.route("/api/lexicon")
def api_lexicon():
    q = request.args.get("q", "")
    from .astrology.core.lexicon import search_lexicon
    return jsonify(search_lexicon(q))


# ─────────────────────────────────────────────
#  API: Month day-quality scores for calendar
# ─────────────────────────────────────────────
@main.route("/api/month-scores")
def month_scores():
    year   = int(request.args.get("year",  date.today().year))
    month  = int(request.args.get("month", date.today().month))
    lat    = float(request.args.get("lat",  session.get("birth_lat", 28.6139)))
    lon    = float(request.args.get("lon",  session.get("birth_lon", 77.2090)))
    tz_str = request.args.get("tz", session.get("birth_tz", "Asia/Kolkata"))

    num_days = cal_mod.monthrange(year, month)[1]
    scores   = {}

    for day in range(1, num_days + 1):
        d = date(year, month, day)
        try:
            pan        = calculate_panchang(d, lat, lon, tz_str, None)
            scores[day] = _quick_day_score(pan, d)
        except Exception:
            scores[day] = {"score": 5, "color": "#9ca3af", "label": "Neutral",
                           "tithi": "", "nakshatra": "", "vara": ""}

    return jsonify(scores)


def _quick_day_score(pan: dict, d: date) -> dict:
    score = 5
    vara_scores = {
        "Sun": 7, "Moon": 8, "Mars": 4, "Mercury": 7,
        "Jupiter": 9, "Venus": 8, "Saturn": 3,
    }
    vara_lord = pan.get("vara", {}).get("lord", "")
    score += vara_scores.get(vara_lord, 0) - 5

    tithi_num = pan.get("tithi", {}).get("number", 5)
    good_tithis = {1, 2, 3, 5, 7, 10, 11, 13, 15}
    bad_tithis  = {4, 6, 8, 9, 12, 14, 30}
    if tithi_num in good_tithis:
        score += 1
    elif tithi_num in bad_tithis:
        score -= 1

    yoga_name = pan.get("yoga", {}).get("name", "")
    good_yogas = {"Siddhi", "Amriti", "Shubha", "Labha", "Sukla", "Brahma", "Indra"}
    bad_yogas  = {"Vyatipata", "Ganda", "Shoola", "Atiganda", "Vajra", "Vyaghata"}
    if yoga_name in good_yogas:
        score += 1
    elif yoga_name in bad_yogas:
        score -= 1

    score = max(1, min(10, score))

    if score >= 8:
        color, label = "#16a34a", "Excellent"
    elif score >= 6:
        color, label = "#65a30d", "Good"
    elif score >= 5:
        color, label = "#d97706", "Moderate"
    elif score >= 3:
        color, label = "#ea580c", "Caution"
    else:
        color, label = "#dc2626", "Difficult"

    return {
        "score":     score,
        "color":     color,
        "label":     label,
        "tithi":     pan.get("tithi", {}).get("name", ""),
        "nakshatra": pan.get("nakshatra", {}).get("name", ""),
        "vara":      vara_lord,
    }


# ─────────────────────────────────────────────
#  API: Deep day detail for calendar panel
# ─────────────────────────────────────────────
@main.route("/api/day-detail")
def day_detail():
    date_str = request.args.get("date", date.today().isoformat())
    lat      = float(request.args.get("lat",  session.get("birth_lat", 28.6139)))
    lon      = float(request.args.get("lon",  session.get("birth_lon", 77.2090)))
    tz_str   = request.args.get("tz", session.get("birth_tz", "Asia/Kolkata"))

    try:
        d    = datetime.strptime(date_str, "%Y-%m-%d").date()
        pan  = calculate_panchang(d, lat, lon, tz_str, None)
        sky  = get_sunrise_sunset_moonrise(d, lat, lon, tz_str)
        q    = _quick_day_score(pan, d)

        # Per-element quality for breakdown display
        tithi_num  = pan.get("tithi", {}).get("number", 5)
        yoga_name  = pan.get("yoga",  {}).get("name", "")
        vara_lord  = pan.get("vara",  {}).get("lord", "")
        nak_name   = pan.get("nakshatra", {}).get("name", "")

        _vara_scores  = {"Sun":7,"Moon":8,"Mars":4,"Mercury":7,"Jupiter":9,"Venus":8,"Saturn":3}
        _good_tithis  = {1,2,3,5,7,10,11,13,15}
        _bad_tithis   = {4,6,8,9,12,14,30}
        _good_yogas   = {"Siddhi","Amriti","Shubha","Labha","Sukla","Brahma","Indra","Siddha",
                         "Sadhya","Priti","Ayushman","Saubhagya","Shobhana","Sukarma",
                         "Dhriti","Vriddhi","Dhruva","Harshana","Variyan","Shiva"}
        _bad_yogas    = {"Vyatipata","Ganda","Shoola","Atiganda","Vajra","Vyaghata",
                         "Vishkamba","Parigha","Vaidhriti"}

        vara_q  = "positive" if _vara_scores.get(vara_lord, 5) >= 7 else (
                  "negative" if _vara_scores.get(vara_lord, 5) <= 4 else "neutral")
        tithi_q = "positive" if tithi_num in _good_tithis else (
                  "negative" if tithi_num in _bad_tithis   else "neutral")
        yoga_q  = "positive" if yoga_name in _good_yogas else (
                  "negative" if yoga_name in _bad_yogas    else "neutral")

        # Nakshatra nature from panchang result
        nak_nature = pan.get("nakshatra", {}).get("nature", "Mixed")
        nak_q = "positive" if nak_nature == "Auspicious" else (
                "negative" if nak_nature == "Inauspicious" else "neutral")

        breakdown = [
            {"limb":"Vara",      "name":pan.get("vara",{}).get("name",""),
             "detail":f"Lord: {vara_lord}", "quality": vara_q},
            {"limb":"Tithi",     "name":pan.get("tithi",{}).get("name",""),
             "detail":pan.get("tithi",{}).get("paksha",""), "quality": tithi_q},
            {"limb":"Nakshatra", "name":nak_name,
             "detail":f"Lord: {pan.get('nakshatra',{}).get('lord','')}", "quality": nak_q},
            {"limb":"Yoga",      "name":yoga_name,
             "detail":pan.get("yoga",{}).get("nature",""), "quality": yoga_q},
            {"limb":"Karana",    "name":pan.get("karana",{}).get("name",""),
             "detail":pan.get("karana",{}).get("nature",""), "quality":"neutral"},
        ]

        # Inauspicious windows from sky data
        inauspicious = [
            {"name":"Rahu Kaal",   "time": sky.get("rahu_kaal","—"),   "color":"#7c3aed"},
            {"name":"Gulika Kaal", "time": sky.get("gulika_kaal","—"), "color":"#6b7280"},
            {"name":"Yamaghanta",  "time": sky.get("yamaghanta","—"),  "color":"#ef4444"},
        ]

        return jsonify({
            "date":         date_str,
            "weekday":      d.strftime("%A"),
            "score":        q,
            "panchang":     pan,
            "breakdown":    breakdown,
            "sunrise":      sky.get("sunrise","—"),
            "sunset":       sky.get("sunset","—"),
            "moonrise":     sky.get("moonrise","—"),
            "moonset":      sky.get("moonset","—"),
            "solar_noon":   sky.get("solar_noon","—"),
            "day_length":   sky.get("day_length","—"),
            "moon_phase":   sky.get("moon_phase_name","—"),
            "moon_phase_pct": sky.get("moon_phase_pct", 0),
            "abhijit":      pan.get("abhijit_muhurta","—"),
            "tarabala":     pan.get("tarabala",{}),
            "chandra_bala": pan.get("chandra_bala",{}),
            "inauspicious": inauspicious,
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────
#  Export: iCal (.ics) — Google/Apple/Outlook
# ─────────────────────────────────────────────
@main.route("/export/ics")
def export_ics():
    year   = int(request.args.get("year",  date.today().year))
    month  = int(request.args.get("month", date.today().month))
    lat    = float(request.args.get("lat",  session.get("birth_lat", 28.6139)))
    lon    = float(request.args.get("lon",  session.get("birth_lon", 77.2090)))
    tz_str = request.args.get("tz", session.get("birth_tz", "Asia/Kolkata"))
    name   = session.get("birth_name", "Vedic")

    num_days = cal_mod.monthrange(year, month)[1]
    lines    = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:-//Jyotish Dashboard//jyotish-{year}-{month:02d}//EN",
        f"X-WR-CALNAME:Vedic Panchang {cal_mod.month_name[month]} {year}",
        "X-WR-CALDESC:Daily panchang quality from Jyotish Dashboard",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]

    QUALITY_EMOJI = {
        "Excellent": "🟢", "Good": "🟡", "Moderate": "🟠",
        "Caution": "🔴", "Difficult": "❌",
    }

    for day in range(1, num_days + 1):
        d = date(year, month, day)
        try:
            pan = calculate_panchang(d, lat, lon, tz_str, None)
            sky = get_sunrise_sunset_moonrise(d, lat, lon, tz_str)
            q   = _quick_day_score(pan, d)
            # Try AI note if API key available
            ai_note = _llm_day_note(pan, q, d.isoformat())

            tithi     = pan.get("tithi",     {}).get("name", "")
            nakshatra = pan.get("nakshatra", {}).get("name", "")
            yoga      = pan.get("yoga",      {}).get("name", "")
            vara      = pan.get("vara",      {}).get("lord", "")
            rahu      = sky.get("rahu_kaal", "")
            abhijit   = pan.get("abhijit_muhurta", "")

            emoji     = QUALITY_EMOJI.get(q["label"], "⚪")
            summary   = f"{emoji} {q['label']} Day · {tithi} · {nakshatra}"
            if name and name != "Vedic":
                summary = f"{emoji} {q['label']} ({name}) · {tithi} · {nakshatra}"

            desc_parts = [
                f"Day Quality: {q['label']} ({q['score']}/10)",
                f"Vara: {vara}  |  Tithi: {tithi}  |  Nakshatra: {nakshatra}",
                f"Yoga: {yoga}",
                f"Sunrise: {sky.get('sunrise','')}  |  Sunset: {sky.get('sunset','')}",
                f"Rahu Kaal: {rahu}",
                f"Abhijit Muhurta: {abhijit}",
            ]
            if ai_note:
                desc_parts.append(f"\n{ai_note}")

            desc = "\\n".join(desc_parts)
            dt_start = d.strftime("%Y%m%d")
            dt_end   = (d + timedelta(days=1)).strftime("%Y%m%d")
            uid      = f"jyotish-{d.isoformat()}@dashboard"

            lines += [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTART;VALUE=DATE:{dt_start}",
                f"DTEND;VALUE=DATE:{dt_end}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{desc}",
                f"CATEGORIES:{q['label']},Panchang",
                "STATUS:CONFIRMED",
                "END:VEVENT",
            ]
        except Exception:
            pass

    lines.append("END:VCALENDAR")
    ics_content = "\r\n".join(lines) + "\r\n"
    filename    = f"vedic-panchang-{year}-{month:02d}.ics"
    return Response(
        ics_content,
        mimetype="text/calendar",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ─────────────────────────────────────────────
#  Export: Obsidian vault ZIP
# ─────────────────────────────────────────────
@main.route("/export/obsidian")
def export_obsidian():
    year   = int(request.args.get("year",  date.today().year))
    month  = int(request.args.get("month", date.today().month))
    lat    = float(request.args.get("lat",  session.get("birth_lat", 28.6139)))
    lon    = float(request.args.get("lon",  session.get("birth_lon", 77.2090)))
    tz_str = request.args.get("tz", session.get("birth_tz", "Asia/Kolkata"))
    name   = session.get("birth_name", "")

    num_days = cal_mod.monthrange(year, month)[1]
    buf      = io.BytesIO()

    QUALITY_EMOJI = {
        "Excellent": "🟢", "Good": "🟡", "Moderate": "🟠",
        "Caution": "🔴", "Difficult": "❌",
    }

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for day in range(1, num_days + 1):
            d = date(year, month, day)
            try:
                pan = calculate_panchang(d, lat, lon, tz_str, None)
                sky = get_sunrise_sunset_moonrise(d, lat, lon, tz_str)
                q   = _quick_day_score(pan, d)
                ai_note = _llm_day_note(pan, q, d.isoformat())

                tithi     = pan.get("tithi",     {})
                nakshatra = pan.get("nakshatra", {})
                yoga      = pan.get("yoga",      {})
                karana    = pan.get("karana",    {})
                vara      = pan.get("vara",      {})
                tarabala  = pan.get("tarabala",  {})
                cbala     = pan.get("chandra_bala", {})

                q_icon = QUALITY_EMOJI.get(q["label"], "⚪")
                weekday = d.strftime("%A")

                lines = [
                    "---",
                    f'date: "{d.isoformat()}"',
                    f'weekday: "{weekday}"',
                    f'tithi: "{tithi.get("name","")}"',
                    f'nakshatra: "{nakshatra.get("name","")}"',
                    f'yoga: "{yoga.get("name","")}"',
                    f'vara: "{vara.get("lord","")}"',
                    f'quality: "{q["label"]}"',
                    f'score: {q["score"]}',
                    f'tags: [panchang, vedic, {q["label"].lower()}]',
                    "---",
                    "",
                    f"# {q_icon} {d.strftime('%-d %B %Y')} — {q['label']} Day",
                    "",
                ]

                if ai_note:
                    lines += ["> [!note] Vedic Insight", f"> {ai_note}", ""]

                lines += [
                    "## Panchang",
                    "",
                    "| Limb | Value | Quality |",
                    "|---|---|---|",
                    f"| **Vara** | {weekday} (Lord: {vara.get('lord','')}) | {'✅' if vara.get('lord') in ['Moon','Jupiter','Venus','Mercury'] else '⚠️'} |",
                    f"| **Tithi** | {tithi.get('name','')} ({tithi.get('paksha','')}) | {'✅' if tithi.get('quality','') == 'Auspicious' else '⚠️'} |",
                    f"| **Nakshatra** | {nakshatra.get('name','')} (Lord: {nakshatra.get('lord','')}) | {'✅' if nakshatra.get('nature','') == 'Auspicious' else '⚠️'} |",
                    f"| **Yoga** | {yoga.get('name','')} | {'✅' if yoga.get('nature','') == 'Auspicious' else '⚠️'} |",
                    f"| **Karana** | {karana.get('name','')} | — |",
                    "",
                    "## Sky",
                    "",
                    "| | Time |",
                    "|---|---|",
                    f"| 🌅 Sunrise | {sky.get('sunrise','—')} |",
                    f"| 🌇 Sunset | {sky.get('sunset','—')} |",
                    f"| ☀️ Solar Noon | {sky.get('solar_noon','—')} |",
                    f"| 🌙 Moonrise | {sky.get('moonrise','—')} |",
                    f"| 🌑 Moonset | {sky.get('moonset','—')} |",
                    f"| ⏱ Day Length | {sky.get('day_length','—')} |",
                    "",
                    "## Auspicious",
                    "",
                    f"- ✅ **Abhijit Muhurta**: {pan.get('abhijit_muhurta','—')}",
                    "",
                ]

                if tarabala:
                    lines.append(f"- ⭐ **Tarabala**: {tarabala.get('name','—')} — {tarabala.get('quality','—')}")
                if cbala:
                    lines.append(f"- 🌙 **Chandra Bala**: {cbala.get('quality','—')}")
                lines.append("")

                lines += [
                    "## Inauspicious Periods",
                    "",
                    f"- ⚠️ **Rahu Kaal**: {sky.get('rahu_kaal','—')}",
                    f"- ⚠️ **Gulika Kaal**: {sky.get('gulika_kaal','—')}",
                    f"- ⚠️ **Yamaghanta**: {sky.get('yamaghanta','—')}",
                    "",
                    "---",
                    f"*Generated by [Jyotish Dashboard](https://github.com/Aerofarmer/jyotish-dashboard)*",
                ]

                md_content = "\n".join(lines)
                fname = f"{d.isoformat()}.md"
                zf.writestr(f"Panchang/{year}-{month:02d}/{fname}", md_content)

            except Exception:
                pass

        # Index file
        index_lines = [
            f"# Vedic Panchang — {cal_mod.month_name[month]} {year}",
            "",
            f"{'Name: ' + name if name else ''}",
            "",
            "| Date | Day | Quality | Score | Tithi | Nakshatra |",
            "|---|---|---|---|---|---|",
        ]
        # rebuild quick for index
        for day in range(1, num_days + 1):
            d = date(year, month, day)
            try:
                pan = calculate_panchang(d, lat, lon, tz_str, None)
                q   = _quick_day_score(pan, d)
                emoji = QUALITY_EMOJI.get(q["label"], "⚪")
                index_lines.append(
                    f"| [[{d.isoformat()}]] | {d.strftime('%A')} | {emoji} {q['label']} | {q['score']}/10 | {pan.get('tithi',{}).get('name','')} | {pan.get('nakshatra',{}).get('name','')} |"
                )
            except Exception:
                pass
        zf.writestr(f"Panchang/{year}-{month:02d}/INDEX.md", "\n".join(index_lines))

    buf.seek(0)
    filename = f"vedic-panchang-obsidian-{year}-{month:02d}.zip"
    return Response(
        buf.getvalue(),
        mimetype="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ─────────────────────────────────────────────
#  Open-LLM day note (optional enrichment)
# ─────────────────────────────────────────────
_JYOTISHI_SYSTEM = (
    "You are Jyotishi, a traditional Vedic astrologer with mastery of Jyotish shastra, "
    "panchang limbs, nakshatras, and daily muhurtas. "
    "Respond in exactly 2 sentences. "
    "First sentence: describe the cosmic energy of the day using Sanskrit terms naturally. "
    "Second sentence: give one concrete, practical guidance the native can act on today. "
    "Never use bullet points, headers, or markdown. Be concise and mystical."
)

def _llm_day_note(pan: dict, score: dict, date_str: str) -> str | None:
    base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    api_key  = os.getenv("LLM_API_KEY",  "ollama")   # 'ollama' works for local Ollama
    model    = os.getenv("LLM_MODEL",    "llama3.2")
    try:
        from openai import OpenAI
        tithi     = pan.get("tithi",     {}).get("name", "")
        nakshatra = pan.get("nakshatra", {}).get("name", "")
        yoga      = pan.get("yoga",      {}).get("name", "")
        vara      = pan.get("vara",      {}).get("lord", "")
        user_msg  = (
            f"Date: {date_str}\n"
            f"Tithi: {tithi} | Nakshatra: {nakshatra} | Yoga: {yoga} | Vara lord: {vara}\n"
            f"Day quality: {score.get('label','')} ({score.get('score',5)}/10)\n"
            "Write the 2-sentence Vedic insight now."
        )
        client = OpenAI(base_url=base_url, api_key=api_key)
        resp   = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _JYOTISHI_SYSTEM},
                {"role": "user",   "content": user_msg},
            ],
            max_tokens=130,
            temperature=0.72,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None

# ─────────────────────────────────────────────
#  AstroChat: AI Consultation
# ─────────────────────────────────────────────
@main.route("/api/chat", methods=["POST"])
def api_astro_chat():
    from openai import OpenAI

    data = request.json or {}
    user_msg = data.get("message")

    # Get current chart context
    dob   = session.get("birth_dob")
    tob   = session.get("birth_tob")
    lat   = session.get("birth_lat", 28.6139)
    lon   = session.get("birth_lon", 77.2090)
    tz    = session.get("birth_tz", "Asia/Kolkata")

    if not (dob and tob):
        return jsonify({"response": "I need your birth chart first. Please generate a Kundli so I can analyze your specific placements."})

    try:
        birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        chart = calculate_chart_data(birth_dt, float(lat), float(lon), tz)
        preds = generate_evidence_based_predictions(chart)

        # Build concise context for LLM
        chart_summary = {
            "lagna": chart.asc_nakshatra.name,
            "rashi": chart.asc_rashi,
            "planets": {n: {"house": p.house, "rashi": p.rashi, "dignity": p.dignity} for n, p in chart.planets.items()},
            "yogas": [y["name"] for y in chart.yogas],
            "current_periods": preds.get("dasha_text")
        }

        base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
        api_key  = os.getenv("LLM_API_KEY",  "ollama")
        model    = os.getenv("LLM_MODEL",    "llama3.2")

        if not model:
            return jsonify({"response": "AstroChat is currently disabled. Please set LLM_MODEL in your .env file to enable local AI consultation."})

        system_prompt = (
            "You are an expert Vedic Astrologer (Jyotishi). Use the following birth chart data to answer the user's question. "
            f"Birth Data: {json.dumps(chart_summary)}. "
            "Be empathetic, traditional yet practical, and always refer to specific placements in their chart. "
            "Keep answers concise (max 3-4 sentences)."
        )

        client = OpenAI(base_url=base_url, api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=250,
            temperature=0.7
        )

        return jsonify({"response": resp.choices[0].message.content.strip()})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"response": f"I encountered an error connecting to my cosmic intuition: {str(e)}"}), 500


# ─────────────────────────────────────────────
#  Panchang
# ─────────────────────────────────────────────
@main.route("/panchang", methods=["GET", "POST"])
def panchang():
    error         = None
    panchang_data = None
    sky_data      = None

    today  = date.today()
    lat    = session.get("birth_lat", 28.6139)
    lon    = session.get("birth_lon", 77.2090)
    tz_str = session.get("birth_tz", "Asia/Kolkata")
    place  = session.get("birth_place", "New Delhi")

    birth_nak_idx = None
    dob = session.get("birth_dob")
    tob = session.get("birth_tob")
    if dob and tob:
        try:
            birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
            from .astrology.core.swe_proxy import swe as swe_mod
            from .astrology.core.datetime import datetime_to_jd
            from .astrology.core.ephemeris import get_planet_position
            jd = datetime_to_jd(birth_dt, tz_str)
            moon_pos = get_planet_position(jd, swe_mod.MOON)
            from .astrology.core.planets import NAK_SPAN
            birth_nak_idx = int(moon_pos["longitude"] / NAK_SPAN)
        except Exception:
            pass

    if request.method == "POST":
        try:
            date_str = request.form.get("date", today.isoformat())
            place_q  = request.form.get("place", "").strip()
            lat_f    = request.form.get("lat", "")
            lon_f    = request.form.get("lon", "")
            tz_str_f = request.form.get("timezone", tz_str)

            if lat_f and lon_f:
                lat    = float(lat_f)
                lon    = float(lon_f)
                tz_str = tz_str_f
            elif place_q:
                geo = geocode_place(place_q)
                if "error" not in geo:
                    lat    = geo["lat"]
                    lon    = geo["lon"]
                    tz_str = geo["timezone"]
                    place  = geo.get("display_name", place_q)

            target_date   = date.fromisoformat(date_str)
            panchang_data = calculate_panchang(target_date, float(lat), float(lon),
                                               tz_str, birth_nak_idx)
            sky_data = panchang_data["sky"]

            # Check suitability for common events
            from .astrology.panchang.muhurta import check_muhurta_suitability
            panchang_data["event_suitability"] = {
                "Marriage": check_muhurta_suitability("Marriage", panchang_data),
                "Business Opening": check_muhurta_suitability("Business Opening", panchang_data),
                "Property Purchase": check_muhurta_suitability("Property Purchase", panchang_data),
                "Vehicle Purchase": check_muhurta_suitability("Vehicle Purchase", panchang_data)
            }
        except Exception as e:
            error = str(e)
            traceback.print_exc()
    else:
        try:
            panchang_data = calculate_panchang(today, float(lat), float(lon),
                                               tz_str, birth_nak_idx)
            sky_data = panchang_data["sky"]

            from .astrology.panchang.muhurta import check_muhurta_suitability
            panchang_data["event_suitability"] = {
                "Marriage": check_muhurta_suitability("Marriage", panchang_data),
                "Business Opening": check_muhurta_suitability("Business Opening", panchang_data),
                "Property Purchase": check_muhurta_suitability("Property Purchase", panchang_data),
                "Vehicle Purchase": check_muhurta_suitability("Vehicle Purchase", panchang_data)
            }
        except Exception as e:
            error = str(e)

    return render_template("panchang.html",
                           panchang=panchang_data, sky=sky_data,
                           place=place, today=today.isoformat(), error=error)


# ─────────────────────────────────────────────
#  JSON API
# ─────────────────────────────────────────────
@main.route("/api/geocode")
def api_geocode():
    q = request.args.get("q", "")
    if not q:
        return jsonify({"error": "No query"}), 400
    return jsonify(geocode_place(q))


@main.route("/api/sky")
def api_sky():
    try:
        lat    = float(request.args.get("lat", 28.6139))
        lon    = float(request.args.get("lon", 77.2090))
        tz_str = request.args.get("tz", "Asia/Kolkata")
        date_s = request.args.get("date", date.today().isoformat())
        d      = date.fromisoformat(date_s)
        data   = get_sunrise_sunset_moonrise(d, lat, lon, tz_str)
        return jsonify(data)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400


@main.route("/api/panchang")
def api_panchang():
    try:
        lat    = float(request.args.get("lat", 28.6139))
        lon    = float(request.args.get("lon", 77.2090))
        tz_str = request.args.get("tz", "Asia/Kolkata")
        date_s = request.args.get("date", date.today().isoformat())
        d      = date.fromisoformat(date_s)
        data   = calculate_panchang(d, lat, lon, tz_str)
        return jsonify(data)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400


@main.route("/api/transit")
def api_transit():
    try:
        lat    = float(request.args.get("lat", session.get("birth_lat", 28.6139)))
        lon    = float(request.args.get("lon", session.get("birth_lon", 77.2090)))
        tz_str = request.args.get("tz", session.get("birth_tz", "Asia/Kolkata"))
        data   = calculate_transit_chart(lat, lon, tz_str)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route("/api/saved-charts")
def api_saved_charts():
    return jsonify(list_charts())


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def _build_nak_house_map(transit_data: dict, natal_chart: dict | None) -> list:
    """
    For each transit planet: which natal house it occupies,
    which nakshatra it's in, and warning level.
    """
    from .astrology.core.planets import NAKSHATRA_NAMES, NAKSHATRA_LORDS, NAK_SPAN
    from .astrology.predictions.data import TRANSIT_NAKSHATRA_WARNINGS, NAKSHATRA_MEANINGS

    if not natal_chart:
        return []

    # Map rashi to natal house index
    asc_rashi = natal_chart.get("asc_rashi")
    if asc_rashi is None:
        # Fallback to calculating from ascendant longitude
        asc_rashi = int(natal_chart.get("ascendant", 0) // 30)

    lagna_house_map = {}
    for i in range(12):
        rashi = (asc_rashi + i) % 12
        lagna_house_map[rashi] = i + 1

    result = []

    for p_name, p_data in transit_data["planets"].items():
        t_rashi     = p_data["rashi"]
        natal_house = lagna_house_map.get(t_rashi)
        nak_idx     = int(p_data["longitude"] / NAK_SPAN)
        nak_name    = NAKSHATRA_NAMES[nak_idx]
        nak_lord    = NAKSHATRA_LORDS[nak_idx]
        nak_meaning = NAKSHATRA_MEANINGS.get(nak_name, "")
        nak_warning = TRANSIT_NAKSHATRA_WARNINGS.get(nak_name)

        # Natal planet in same house?
        natal_house_occupants = []
        if natal_house:
            # JSON keys are strings, but natal_house is int
            occ = natal_chart.get("house_occupants", {})
            natal_house_occupants = occ.get(str(natal_house)) or occ.get(natal_house) or []

        result.append({
            "planet":      p_name,
            "symbol":      p_data.get("symbol", ""),
            "color":       PLANET_COLORS.get(p_name, "#fff"),
            "rashi":       p_data["rashi_name"],
            "longitude":   round(p_data["longitude"], 2),
            "dms":         p_data["dms"],
            "retrograde":  p_data.get("retrograde", False),
            "natal_house": natal_house,
            "natal_occupants": natal_house_occupants,
            "nakshatra":   nak_name,
            "nak_pada":    int((p_data["longitude"] % (360/27)) / (360/108)) + 1,
            "nak_lord":    nak_lord,
            "nak_meaning": nak_meaning,
            "nak_warning": nak_warning,
            "warning_level": (
                nak_warning[0] if nak_warning else
                "warning" if p_name in ("Saturn","Rahu","Ketu") else
                "positive" if p_name in ("Jupiter","Venus") else "neutral"
            ),
        })

    return result
