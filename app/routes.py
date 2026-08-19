from flask import (Blueprint, render_template, request, jsonify, session,
                   redirect, url_for, flash, Response)
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

    # Ensure birth_datetime is string for templates
    if hasattr(chart, "birth_datetime") and isinstance(chart.birth_datetime, datetime):
        chart.birth_datetime = chart.birth_datetime.isoformat()
    elif isinstance(chart.get("birth_datetime"), datetime):
        chart["birth_datetime"] = chart["birth_datetime"].isoformat()

    # House occupants
    chart["house_occupants"] = {h: [] for h in range(1, 13)}
    for p, data in chart["planets"].items():
        chart["house_occupants"][data["house"]] = chart["house_occupants"].get(data["house"], [])
        chart["house_occupants"][data["house"]].append(p)

    # Lagna
    rashi_names = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya",
                   "Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]

    asc_rashi = chart.get("asc_rashi", 0)
    asc_lon = chart.get("ascendant", 0)
    deg = asc_lon % 30
    d = int(deg)
    m = int((deg - d) * 60)

    from .astrology.core.planets import NAKSHATRA_NAMES
    nak_idx = int(asc_lon / (360/27))
    nak_name = NAKSHATRA_NAMES[nak_idx]

    chart["lagna"] = {
        "rashi": asc_rashi,
        "rashi_name": rashi_names[asc_rashi],
        "rashi_english": ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"][asc_rashi],
        "dms": f"{d}°{m}'",
        "nakshatra": {"name": nak_name}
    }

    # Navamsa & Dashamsha
    chart["navamsa"] = {}
    chart["dashamsha"] = {}
    divs = chart.get("divisional_charts", {})
    if "D9" in divs:
        chart["navamsa"] = {k: {"rashi": v} for k, v in divs["D9"].items()}
    if "D10" in divs:
        chart["dashamsha"] = {k: {"rashi": v} for k, v in divs["D10"].items()}

    # Houses (Whole Sign)
    chart["houses"] = []
    for i in range(1, 13):
        r_idx = (asc_rashi + i - 1) % 12
        chart["houses"].append({
            "house": i,
            "rashi": r_idx,
            "rashi_name": rashi_names[r_idx]
        })

    # planets cleanup for legacy templates
    from .astrology.core.planets import NAKSHATRA_NAMES, NAKSHATRA_LORDS, NAK_SPAN
    for p, data in chart["planets"].items():
        data["retrograde"] = data.get("is_retrograde", False)
        # Add color if missing
        if "color" not in data:
            data["color"] = PLANET_COLORS.get(p, "#fff")
        # Add dms if missing
        lon = data.get("longitude", 0)
        if "dms" not in data:
            p_deg = lon % 30
            pd = int(p_deg)
            pm = int((p_deg - pd) * 60)
            data["dms"] = f"{pd}°{pm}'"
        if "rashi_name" not in data:
            data["rashi_name"] = rashi_names[data["rashi"]]

        # Add nakshatra info
        if "nakshatra" not in data:
            nak_idx = int(lon / NAK_SPAN)
            nak_deg = lon % NAK_SPAN
            data["nakshatra"] = {
                "name": NAKSHATRA_NAMES[nak_idx],
                "pada": int(nak_deg / (NAK_SPAN / 4)) + 1,
                "lord": NAKSHATRA_LORDS[nak_idx]
            }

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
    import swisseph as swe

    tz = pytz.timezone(tz_str)
    noon_dt = datetime.combine(target_date, datetime.min.time()).replace(hour=12)
    jd_ut = datetime_to_jd(noon_dt, tz_str)

    sr_jd = get_sunrise(jd_ut, lat, lon) or 0
    ss_jd = get_sunset(jd_ut, lat, lon) or 0
    mr_jd = get_moonrise(jd_ut, lat, lon)
    ms_jd = get_moonset(jd_ut, lat, lon)

    def jd_to_str(jd):
        if not jd or jd < 0: return "—"
        y, m, d, h = swe.revjul(jd)
        hh = int(h)
        mm = int((h - hh) * 60)
        dt_utc = datetime(y, m, d, hh, mm, second=0, tzinfo=pytz.utc)
        return dt_utc.astimezone(tz).strftime("%I:%M %p")

    weekday = target_date.weekday()

    return {
        "sunrise": jd_to_str(sr_jd),
        "sunset": jd_to_str(ss_jd),
        "moonrise": jd_to_str(mr_jd),
        "moonset": jd_to_str(ms_jd),
        "rahu_kaal": get_rahu_kaal(weekday, sr_jd, ss_jd),
        "gulika_kaal": get_gulika_kaal(weekday, sr_jd, ss_jd),
        "yamaghanta": get_yamaghanta(weekday, sr_jd, ss_jd)
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
@main.route("/")
def index():
    try:
        ip_loc   = get_ip_location()
        saved    = list_charts()
        return render_template("index.html", ip_loc=ip_loc, saved_charts=saved)
    except Exception as e:
        traceback.print_exc()
        return f"Internal Server Error: {str(e)}", 500


# ─────────────────────────────────────────────
#  Kundli (birth chart)
# ─────────────────────────────────────────────
@main.route("/kundli", methods=["GET", "POST"])
def kundli():
    error = None
    chart = None
    dasha = None
    remedies = None

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
                if not place:
                    raise ValueError("Enter a place or coordinates.")
                geo = geocode_place(place)
                if "error" in geo:
                    raise ValueError(geo["error"])
                lat    = geo["lat"]
                lon    = geo["lon"]
                tz_str = geo["timezone"]
                place  = geo.get("display_name", place)
            else:
                lat = float(lat)
                lon = float(lon)

            # 0. Apply Ayanamsa Preference
            from .astrology.core.ephemeris import set_ayanamsa_mode
            import swisseph as swe_lib
            ayanamsa_map = {"Lahiri": swe_lib.SIDM_LAHIRI, "Raman": swe_lib.SIDM_RAMAN, "KP": swe_lib.SIDM_KRISHNAMURTI}
            pref = session.get("ayanamsa", "Lahiri")
            set_ayanamsa_mode(ayanamsa_map.get(pref, swe_lib.SIDM_LAHIRI))

            birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")

            # 1. Apply Rectification (Nudge birth time)
            rect = request.form.get("rectify") or request.args.get("rectify")
            if rect:
                try: birth_dt += timedelta(minutes=int(rect))
                except Exception: pass

            chart_obj = calculate_chart_data(birth_dt, float(lat), float(lon), tz_str)
            chart = chart_obj.model_dump()

            moon_lon = chart["planets"]["Moon"]["longitude"]
            dasha    = calculate_vimshottari(moon_lon, birth_dt)

            print(f"DEBUG: Kundli Dasha keys: {list(dasha.keys()) if dasha else 'None'}")
            if dasha:
                print(f"DEBUG: balance_years = {dasha.get('balance_years')}")

            # Enrich chart with metadata for UI
            chart["name"] = name
            chart["place"] = place
            chart["birth_dob"] = dob
            chart["birth_tob"] = tob
            chart["latitude"] = float(lat)
            chart["longitude_coord"] = float(lon)
            chart["timezone"] = tz_str
            chart["birth_datetime"] = birth_dt.isoformat()

            _enrich_chart_for_template(chart)
            remedies = get_remedies(chart_obj)

            # Persist in session for transit/dasha/predictions
            session["birth_lat"]   = float(lat)
            session["birth_lon"]   = float(lon)
            session["birth_tz"]    = tz_str
            session["birth_name"]  = name
            session["birth_place"] = place
            session["birth_dob"]   = dob
            session["birth_tob"]   = tob

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
        moon_lon = chart["planets"]["Moon"]["longitude"]
        birth_dt = datetime.fromisoformat(chart["birth_datetime"])
        dasha = calculate_vimshottari(moon_lon, birth_dt)
    except Exception:
        pass

    return render_template("kundli.html", chart=chart, dasha=dasha, error=None)


# ─────────────────────────────────────────────
#  Delete saved chart
# ─────────────────────────────────────────────
@main.route("/kundli/delete/<cid>", methods=["POST"])
def delete_kundli(cid):
    delete_chart(cid)
    return jsonify({"ok": True})


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
    nak_house_map = _build_nak_house_map(transit_data, natal_chart)

    # 3. Vedha Analysis
    vedha_alerts = []
    if natal_chart:
        from .astrology.transit.vedha import check_vedha
        # We need house occupants relative to natal moon
        # For simplicity, we'll use the natal moon rashi to determine houses
        n_moon_rashi = natal_chart["planets"]["Moon"]["rashi"]

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
        panchang = calculate_panchang(selected_date, float(lat), float(lon), tz, moon_nak_idx)

        # 2. Generate evidence-based predictions
        preds = generate_evidence_based_predictions(natal_chart)

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

        # 5. Personalized Day Score Adjustment
        if "tarabala" in panchang:
            if panchang["tarabala"]["quality"] == "Inauspicious":
                preds["score"] = max(1.0, preds["score"] - 1.5)
                preds["panchang_ok"] = False
            elif "Auspicious" in panchang["tarabala"]["quality"]:
                preds["score"] = min(10.0, preds["score"] + 1.0)

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
@main.route("/varshaphala")
def varshaphala():
    dob = session.get("birth_dob")
    tob = session.get("birth_tob")
    lat = session.get("birth_lat", 28.6139)
    lon = session.get("birth_lon", 77.2090)
    tz  = session.get("birth_tz", "Asia/Kolkata")

    if not (dob and tob):
        return redirect(url_for("main.index"))

    # Current/Next solar return year
    target_year = date.today().year

    from .astrology.core.varshaphala import get_solar_return_jd, get_varshaphala_data
    from .astrology.core.datetime import datetime_to_jd

    birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
    natal_jd = datetime_to_jd(birth_dt, tz)

    # Use cached or direct calc
    sr_jd = get_solar_return_jd(natal_jd, target_year)

    # Calculate chart for that exact moment
    # We convert JD back to a datetime for calculate_chart_data
    import swisseph as swe_mod
    y, m, d, h = swe_mod.revjul(sr_jd)
    # revjul h is decimal hour in UTC
    sr_dt_utc = datetime(y, m, d, int(h), int((h%1)*60), int(((h%1)*60%1)*60))

    # Create the yearly chart
    from .astrology.core.chart import calculate_chart_data
    yearly_chart = calculate_chart_data(sr_dt_utc, float(lat), float(lon), "UTC")
    chart = yearly_chart.model_dump()

    # Natal lagna for Muntha
    natal_chart = calculate_chart_data(birth_dt, float(lat), float(lon), tz)
    extra = get_varshaphala_data(birth_dt, natal_chart.asc_rashi, target_year)

    chart["name"] = f"Yearly Chart ({target_year})"
    chart["place"] = session.get("birth_place", "New Delhi")
    chart["age"] = extra["age"]
    chart["muntha_rashi"] = extra["muntha_rashi"]
    chart["muntha_house"] = extra["muntha_house"]

    _enrich_chart_for_template(chart)

    return render_template("kundli.html", chart=chart, is_yearly=True)

# ─────────────────────────────────────────────
#  Prashna (Horary)
# ─────────────────────────────────────────────
@main.route("/prashna")
def prashna():
    lat    = session.get("birth_lat", 28.6139)
    lon    = session.get("birth_lon", 77.2090)
    tz_str = session.get("birth_tz", "Asia/Kolkata")
    place  = session.get("birth_place", "New Delhi")

    now = datetime.now(pytz.timezone(tz_str))

    chart_obj = calculate_chart_data(now, float(lat), float(lon), tz_str)
    chart = chart_obj.model_dump()

    # Enrichment
    chart["name"] = "Prashna Chart"
    chart["place"] = f"Calculated for: {place}"
    chart["birth_dob"] = now.strftime("%Y-%m-%d")
    chart["birth_tob"] = now.strftime("%H:%M")
    chart["latitude"] = float(lat)
    chart["longitude_coord"] = float(lon)
    chart["timezone"] = tz_str
    chart["birth_datetime"] = now.isoformat()

    _enrich_chart_for_template(chart)

    moon_lon = chart["planets"]["Moon"]["longitude"]
    dasha    = calculate_vimshottari(moon_lon, now)

    return render_template("kundli.html", chart=chart, dasha=dasha, is_prashna=True)

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
            b_dt = datetime.strptime(f"{b_dob} {b_tob}", "%Y-%m-%d %H:%M")
            b_chart = calculate_chart_data(b_dt, b_geo["lat"], b_geo["lon"], b_geo["timezone"])
            b_moon = b_chart.planets["Moon"]

            # Process Girl
            g_geo = geocode_place(g_place)
            g_dt = datetime.strptime(f"{g_dob} {g_tob}", "%Y-%m-%d %H:%M")
            g_chart = calculate_chart_data(g_dt, g_geo["lat"], g_geo["lon"], g_geo["timezone"])
            g_moon = g_chart.planets["Moon"]

            result = get_matchmaking_score(
                {"rashi": b_moon.rashi, "nakshatra_idx": b_moon.nakshatra.index},
                {"rashi": g_moon.rashi, "nakshatra_idx": g_moon.nakshatra.index}
            )

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
        pdf.set_font("helvetica", "B", 20)
        pdf.cell(0, 10, "Jyotish Vedic Dashboard - Birth Report", ln=True, align="C")
        pdf.ln(5)

        # Native Info
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, f"Native: {name}", ln=True)
        pdf.set_font("helvetica", "", 12)
        pdf.cell(0, 8, f"Birth: {dob} {tob}", ln=True)
        pdf.cell(0, 8, f"Place: {place} ({lat}, {lon})", ln=True)
        pdf.ln(5)

        # Lagna Info
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "Birth Details", ln=True)
        pdf.set_font("helvetica", "", 12)
        pdf.cell(0, 8, f"Ascendant (Lagna): {chart.asc_rashi} - {chart.asc_nakshatra.name}", ln=True)
        pdf.cell(0, 8, f"Ayanamsa: {round(chart.ayanamsa, 4)}", ln=True)
        pdf.ln(5)

        # Planets
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "Planetary Positions", ln=True)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(30, 8, "Planet", border=1)
        pdf.cell(30, 8, "Rashi", border=1)
        pdf.cell(40, 8, "Degree", border=1)
        pdf.cell(20, 8, "House", border=1)
        pdf.cell(50, 8, "Dignity", border=1, ln=True)

        pdf.set_font("helvetica", "", 10)
        for p_name, p in chart.planets.items():
            pdf.cell(30, 8, p_name, border=1)
            pdf.cell(30, 8, str(p.rashi), border=1)
            pdf.cell(40, 8, f"{round(p.degree, 2)}", border=1)
            pdf.cell(20, 8, str(p.house), border=1)
            pdf.cell(50, 8, p.dignity, border=1, ln=True)
        pdf.ln(5)

        # Predictions
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "Domain Analysis & Predictions", ln=True)
        pdf.ln(5)

        for domain in preds["domains"]:
            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, f"{domain['domain']} - {domain['score']}%", ln=True)
            pdf.set_font("helvetica", "I", 10)
            pdf.multi_cell(0, 8, domain["summary"])
            pdf.set_font("helvetica", "", 10)
            for ev in domain["evidence"]:
                pdf.cell(10) # indent
                pdf.multi_cell(0, 6, f"- {ev}")
            pdf.ln(5)

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
            import swisseph as swe_mod
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
        except Exception as e:
            error = str(e)
            traceback.print_exc()
    else:
        try:
            panchang_data = calculate_panchang(today, float(lat), float(lon),
                                               tz_str, birth_nak_idx)
            sky_data = panchang_data["sky"]
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

    lagna_house_map = {h["rashi"]: h["house"] for h in natal_chart["houses"]}
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
            natal_house_occupants = natal_chart["house_occupants"].get(natal_house, [])

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
