from typing import Dict, Any, List, Optional
from .calc_client import calc_client
from .datetime import datetime_to_jd
from .houses import get_house_from_longitude, get_house_lord, RASHI_LORDS
from .planets import NAKSHATRA_NAMES, NAKSHATRA_LORDS, NAK_SPAN
from .nakshatra_data import NAKSHATRA_DEITIES, NAKSHATRA_SYMBOLS
from ..strength.dignity import get_dignity
from ..strength.functional import get_functional_status
from ..charts.divisional import get_varga_chart
from ..strength.shadbala import calculate_shadbala
from ..charts.ashtakavarga import calculate_ashtakavarga
from ..yogas.detector import detect_yogas
from .models import CanonicalChart, PlanetInfo, NakshatraInfo
from .jaimini import calculate_charakarakas, get_karakamsha_swamsha
from .advanced import (
    calculate_arudha_padas, get_jaimini_aspects, calculate_yogi_avayogi,
    calculate_special_lagnas, calculate_shree_lagna, calculate_varnada_lagna
)
from ..panchang.sky import get_sunrise, get_sunset
from ..dasha.kalachakra import calculate_kalachakra_dasha
from ..dasha.chara import calculate_chara_dasha
from ..dasha.shattrimsha import calculate_shattrimsha_dasha
from ..strength.avasthas import calculate_baladi_avastha, calculate_deeptadi_avastha
from ..strength.longevity_calculation import calculate_pindayu
from datetime import datetime
import traceback
from functools import lru_cache

from ..matchmaking.data import NAKSHATRA_GANA, NAKSHATRA_YONI, NAKSHATRA_NADI

def _get_nakshatra_info(longitude: float) -> NakshatraInfo:
    """Calculate detailed Nakshatra info for a given longitude."""
    idx = int(longitude / NAK_SPAN) % 27
    deg = longitude % NAK_SPAN
    pada = int(deg / (NAK_SPAN / 4)) + 1

    return NakshatraInfo(
        name=NAKSHATRA_NAMES[idx],
        index=idx,
        pada=pada,
        lord=NAKSHATRA_LORDS[idx],
        deity=NAKSHATRA_DEITIES[idx] if idx < len(NAKSHATRA_DEITIES) else None,
        symbol=NAKSHATRA_SYMBOLS[idx] if idx < len(NAKSHATRA_SYMBOLS) else None,
        gana=NAKSHATRA_GANA[idx] if idx < len(NAKSHATRA_GANA) else None,
        yoni=NAKSHATRA_YONI[idx] if idx < len(NAKSHATRA_YONI) else None,
        nadi=NAKSHATRA_NADI[idx] if idx < len(NAKSHATRA_NADI) else None,
        degree_range=(idx * NAK_SPAN, (idx + 1) * NAK_SPAN)
    )

@lru_cache(maxsize=128)
def calculate_chart_data(birth_dt: datetime, lat: float, lon: float, tz_str: str, birth_time_conf: str = "HIGH") -> CanonicalChart:
    """Master Engine: Returns a complete CanonicalChart using isolated Calculation Service."""
    try:
        # 1. Fetch Astronomical Facts from Isolated Service
        # We pass decimal hour in UT for julday
        hour_utc = birth_dt.hour + birth_dt.minute/60.0 + birth_dt.second/3600.0
        # Actually, the service expects Year, Month, Day, Hour
        # But we need to ensure it's UT. The client currently just passes what we give it.
        # Let's adjust client or handle it here.

        # Better: use datetime_to_jd to get UT, but service wants Y/M/D/H.
        # Let's assume service handles local to UT if we tell it the timezone,
        # or we just pass UT. Let's pass UT components.
        from .datetime import to_utc
        dt_utc = to_utc(birth_dt, tz_str)
        h_utc = dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0

        facts = calc_client.get_natal_chart(
            dt_utc.year, dt_utc.month, dt_utc.day, h_utc, lat, lon
        )

        jd_ut = facts["jd_ut"]
        ayanamsa = facts["ayanamsa"]
        ascendant = facts["ascendant"]
        asc_rashi = int(ascendant // 30)
        asc_nak = _get_nakshatra_info(ascendant)

        raw_planets = facts["planets"]
        planets_lon = {n: p["longitude"] for n, p in raw_planets.items()}

        # 2. Derived Vedic Data (Calculated locally from facts)
        sr_jd = get_sunrise(jd_ut, lat, lon) or jd_ut - 0.25
        ss_jd = get_sunset(jd_ut, lat, lon) or jd_ut + 0.25
        next_sr = get_sunrise(jd_ut + 1.0, lat, lon) or jd_ut + 0.75

        # Vedic Weekday
        python_weekday = birth_dt.weekday()
        if jd_ut < sr_jd:
            python_weekday = (python_weekday - 1 + 7) % 7
        v_weekday = (python_weekday + 1) % 7 # 0=Sun

        # Upagrahas
        from .upagrahas import get_upagraha_longitudes
        planets_lon.update(get_upagraha_longitudes(jd_ut, sr_jd, ss_jd, next_sr, v_weekday, lat, lon))

        # Divisional Charts
        divisions = [1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]
        divs = { f"D{d}": get_varga_chart(planets_lon, ascendant, d) for d in divisions }

        # Strength Engine (Local)
        from ..panchang.hora import WEEKDAY_TO_HORA_START, HORA_ORDER
        from ..panchang.tithi import get_tithi_info
        is_day = sr_jd < jd_ut < ss_jd
        t_data = get_tithi_info(jd_ut)
        t_num = t_data.get("number", 1)

        h_start = WEEKDAY_TO_HORA_START.get(v_weekday, 0)
        diff_h = (jd_ut - sr_jd) * 24.0
        hora_lord = HORA_ORDER[(h_start + int(diff_h)) % 7]
        WEEKDAY_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

        temp_shad = {
            "planets": { n: {"longitude": l, "rashi": int(l//30), "house": get_house_from_longitude(l, ascendant), "is_retrograde": raw_planets.get(n,{}).get("is_retrograde", False), "speed_long": raw_planets.get(n,{}).get("speed", 1.0)} for n,l in planets_lon.items() if n in WEEKDAY_LORDS},
            "divisional_charts": divs
        }
        shad_map = calculate_shadbala(temp_shad, is_day, t_num <= 15, WEEKDAY_LORDS[v_weekday], hora_lord)

        planets = {}
        func_map = get_functional_status(asc_rashi)

        for name, lon_p in planets_lon.items():
            rashi = int(lon_p // 30)
            deg = lon_p % 30
            house = get_house_from_longitude(lon_p, ascendant)
            dignity = get_dignity(name, rashi, deg)

            planets[name] = PlanetInfo(
                name=name, longitude=lon_p,
                latitude=raw_planets.get(name, {}).get("latitude", 0.0),
                speed=raw_planets.get(name, {}).get("speed", 1.0),
                is_retrograde=raw_planets.get(name, {}).get("is_retrograde", False),
                is_combust=False,
                rashi=rashi, degree=deg, house=house, dignity=dignity,
                nakshatra=_get_nakshatra_info(lon_p),
                dispositor=RASHI_LORDS[rashi],
                functional_status=func_map.get(name, "Neutral"),
                shadbala_score=shad_map.get(name, {}).get("total_shadbala", 0.0),
                baladi_avastha=calculate_baladi_avastha(rashi, deg),
                deeptadi_avastha=calculate_deeptadi_avastha(name, dignity),
                navamsa_rashi=divs["D9"].get(name, rashi)
            )

        # 3. Final canonical object
        planets_rashi_map = {n: int(l//30) for n, l in planets_lon.items()}
        final_chart = CanonicalChart(
            birth_datetime=birth_dt, timezone=tz_str, latitude=lat, longitude=lon,
            birth_time_confidence=birth_time_conf,
            ayanamsa=ayanamsa, ascendant=ascendant, asc_rashi=asc_rashi,
            asc_nakshatra=asc_nak, planets=planets, houses=facts["houses"],
            house_lords={h: get_house_lord(h, asc_rashi) for h in range(1, 13)},
            divisional_charts=divs, ashtakavarga=calculate_ashtakavarga(planets_rashi_map, asc_rashi),
            yogas=[], jaimini_karakas=calculate_charakarakas(planets_lon),
            special_lagnas=calculate_special_lagnas(jd_ut, sr_jd, planets_lon["Sun"]),
            arudha_padas=calculate_arudha_padas(asc_rashi, {h: get_house_lord(h, asc_rashi) for h in range(1, 13)}, planets),
            yogi_details=calculate_yogi_avayogi(planets_lon["Sun"], planets_lon["Moon"]),
            rashi_drishti={r: get_jaimini_aspects(r) for r in range(12)},
            karakamsha_swamsha=get_karakamsha_swamsha(planets, divs["D9"].get("Lagna", 0)),
            chara_dasha=calculate_chara_dasha(asc_rashi, {n: p.rashi for n, p in planets.items()}, birth_dt),
            kalachakra_dasha=calculate_kalachakra_dasha(planets_lon["Moon"], birth_dt),
            shattrimsha_dasha=calculate_shattrimsha_dasha(asc_nak.index, birth_dt),
            pindayu=calculate_pindayu(planets, asc_rashi)
        )

        final_chart.yogas = detect_yogas(planets, final_chart.house_lords, chart=final_chart)
        return final_chart

    except Exception as e:
        # Critical failures are raised to be caught by the route handler
        raise
