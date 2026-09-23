import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.core.houses import RASHI_NAMES
from app.astrology.dasha import calculate_vimshottari

app = create_app()
with app.app_context():
    birth_dt = datetime(1869, 10, 2, 8, 36)
    lat = 21.6417
    lon = 69.6293
    tz_str = "Asia/Kolkata"

    chart = calculate_chart_data(birth_dt, lat, lon, tz_str)

    out = {
        "ascendant": {
            "rashi": RASHI_NAMES[chart.asc_rashi],
            "degree": round(chart.ascendant % 30, 2),
            "nakshatra": chart.asc_nakshatra.name,
            "pada": chart.asc_nakshatra.pada,
            "lord": chart.asc_nakshatra.lord
        },
        "moon": {
            "rashi": RASHI_NAMES[chart.planets['Moon'].rashi],
            "degree": round(chart.planets['Moon'].degree, 2),
            "nakshatra": chart.planets['Moon'].nakshatra.name,
            "pada": chart.planets['Moon'].nakshatra.pada,
            "lord": chart.planets['Moon'].nakshatra.lord
        },
        "sun": {
            "rashi": RASHI_NAMES[chart.planets['Sun'].rashi],
            "degree": round(chart.planets['Sun'].degree, 2),
            "nakshatra": chart.planets['Sun'].nakshatra.name
        },
        "planets": {
            p_name: {
                "longitude": round(p.longitude, 2),
                "rashi": RASHI_NAMES[p.rashi],
                "house": p.house,
                "dignity": p.dignity,
                "shadbala": round(p.shadbala_score, 1),
                "retrograde": p.is_retrograde
            } for p_name, p in chart.planets.items()
        },
        "ashtakavarga": chart.ashtakavarga.get("SAV", []),
        "chart_fingerprint": chart.chart_fingerprint
    }

    print("GANDHI_CALCULATION_JSON_START")
    print(json.dumps(out, indent=2))
    print("GANDHI_CALCULATION_JSON_END")
