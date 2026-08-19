from flask import (Blueprint, render_template, request, jsonify, session,
                   redirect, url_for, flash, Response)
from datetime import datetime, date, timedelta
import calendar as cal_mod
import zipfile
import io
import os
import pytz
import traceback

from .astrology.core.chart import calculate_chart_data
from .astrology.core.planets import PLANET_COLORS
from .astrology.panchang import calculate_panchang
from .astrology.dasha import calculate_vimshottari
from .astrology.predictions.engine import generate_evidence_based_predictions
from .astrology.store import save_chart, list_charts, get_chart, delete_chart
from .api.external import geocode_place, get_ip_location

# Compatibility helpers for legacy routes
def _enrich_chart_for_template(chart: dict):
    """Add legacy keys to chart dict for template compatibility."""
    if not chart: return

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

    # Navamsa
    if "divisional" in chart and "D9" in chart["divisional"]:
        chart["navamsa"] = {k: {"rashi": v} for k, v in chart["divisional"]["D9"].items()}
        if "Lagna" in chart["navamsa"]:
            # Templates expect chart.navamsa.Lagna.rashi
            pass

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

def calculate_transit_chart(lat: float, lon: float, tz_str: str, dt: datetime = None) -> dict:
    from .astrology.core.chart import calculate_chart_data
    if dt is None:
        tz = pytz.timezone(tz_str)
        dt = datetime.now(tz)
    chart = calculate_chart_data(dt, lat, lon, tz_str)
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

            birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
            chart = calculate_chart_data(birth_dt, float(lat), float(lon), tz_str)

            moon_lon = chart["planets"]["Moon"]["longitude"]
            dasha    = calculate_vimshottari(moon_lon, birth_dt)

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

    return render_template("kundli.html", chart=chart, dasha=dasha, error=error)


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

    transit_data = calculate_transit_chart(float(lat), float(lon), tz_str)

    natal_chart = None
    dob = session.get("birth_dob")
    tob = session.get("birth_tob")
    if dob and tob:
        try:
            birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
            natal_chart = calculate_chart_data(birth_dt, float(lat), float(lon), tz_str)
            _enrich_chart_for_template(natal_chart)
        except Exception:
            pass

    # Build nakshatra-in-house mapping for transit
    nak_house_map = _build_nak_house_map(transit_data, natal_chart)

    return render_template("transit.html",
                           transit=transit_data,
                           natal=natal_chart,
                           nak_house_map=nak_house_map,
                           tz_str=tz_str)


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
            chart      = calculate_chart_data(birth_dt, float(lat), float(lon), tz)
            moon_lon   = chart["planets"]["Moon"]["longitude"]
            dasha_data = calculate_vimshottari(moon_lon, birth_dt)
            _enrich_chart_for_template(chart)
        except Exception as e:
            error = str(e)
    else:
        error = "Please generate a Kundli first."

    return render_template("dasha.html", dasha=dasha_data, chart=chart, error=error)


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

        # Legacy compatibility for prediction engine
        # In 2.0, we use evidence-based predictions
        preds = generate_evidence_based_predictions(natal_chart)

        # Enrich for template
        preds["date"] = selected_date.strftime("%A, %d %B %Y")
        preds["name"] = name

    except Exception as e:
        error = str(e)
        traceback.print_exc()

    return render_template("predictions.html", preds=preds, error=error,
                           name=name, place=place,
                           selected_date=selected_date.isoformat(),
                           today=today.isoformat())


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
