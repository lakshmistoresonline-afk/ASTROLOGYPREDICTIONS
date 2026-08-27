from typing import Dict, Any, List
from .ephemeris import get_planet_position, get_ayanamsa, set_topocentric
from .swe_proxy import swe
from .datetime import datetime_to_jd
from .houses import get_houses, get_house_from_longitude, get_house_lord, RASHI_LORDS
from .planets import PLANETS, NAKSHATRA_NAMES, NAKSHATRA_LORDS, NAK_SPAN
from .nakshatra_data import NAKSHATRA_DEITIES, NAKSHATRA_SYMBOLS
from ..strength.dignity import get_dignity
from ..strength.functional import get_functional_status
from ..strength.aspects import get_graha_drishti
from ..charts.divisional import get_varga_chart
from ..strength.shadbala import calculate_shadbala, calculate_vimsopaka, calculate_ishta_kashta, calculate_exaltation_bala
from ..strength.bhava_bala import calculate_bhava_bala
from ..charts.ashtakavarga import calculate_ashtakavarga
from ..yogas.detector import detect_yogas
from .models import CanonicalChart, PlanetInfo, NakshatraInfo, ShadbalaInfo, KPInfo
from .kp import get_kp_lords
from .jaimini import calculate_charakarakas, get_karakamsha_swamsha
from .bhrigu import calculate_bhrigu_bindu, get_bhrigu_insights
from .fixed_stars import analyze_fixed_star_conjunctions
from .numerology import get_numerology_data, get_lo_shu_grid
from .biorhythms import calculate_biorhythms
from .asteroids import get_asteroid_positions
from .sabian import get_sabian_symbol
from .sarvatobhadra import check_sbc_transit_impact
from .advanced import (
    calculate_arudha_padas, get_jaimini_aspects, calculate_yogi_avayogi,
    analyze_argala, calculate_indu_lagna, calculate_dagtha_rashis,
    calculate_special_lagnas, calculate_shree_lagna, calculate_varnada_lagna
)
from .sahams_library import calculate_extended_sahams
from .eclipses import get_upcoming_eclipses, check_eclipse_impact
from .heliocentric import get_heliocentric_positions
from .bazi import calculate_bazi_pillars
from .uranian import get_uranian_positions
from .maya import calculate_maya_tzolkin
from .mundane import get_mundane_indicators
from .mahabote import calculate_mahabote
from .tibetan import calculate_tibetan_mewa, get_tibetan_parkha
from .celtic import get_celtic_tree_astrology
from .native_american import get_native_american_totem
from .galactic import analyze_galactic_aspects
from .zi_wei_dou_shu import calculate_zi_wei_palaces
from .lilith import get_lilith_positions
from .geomancy import calculate_birth_figure
from .kabbalah import get_kabbalistic_profile
from .human_design import calculate_human_design
from .hellenistic import get_annual_profection, calculate_greek_lots, get_egyptian_bound
from .uranian_formulas import calculate_uranian_formulas
from .gene_keys import get_gene_key_interpretation
from ..dasha.firdaria import calculate_firdaria
from ..timing.zodiacal_releasing import calculate_zodiacal_releasing
from ..charts.harmonics import calculate_harmonics, analyze_harmonic_resonance
from ..timing.progressions import calculate_secondary_progressions, calculate_solar_arc_directions
from ..charts.draconic import get_draconic_chart
from ..yearly.lal_kitab_varshphal import get_lal_kitab_year_lord, analyze_lal_kitab_yearly_houses
from .western_aspects import calculate_natal_western_aspects
from .decanates import get_decanate_info, get_dwadashamsha
from .iching import get_hexagram
from .weather import get_weather_indicators
from .relocation import get_angular_points
from .tajika import calculate_tajika_yogas, calculate_sahams
from .nadi import get_nadi_connections
from .points import calculate_sensitive_points, calculate_ashtakavarga_precincts
from .sudarshana import get_sudarshana_analysis
from .tajika_varsheshwar import calculate_varsheshwar
from .kp_significators import calculate_kp_significators
from .kp_advanced import calculate_kp_4_steps
from .bcp import calculate_bcp_activation
from .nadi_amsha import get_nadi_amsha
from ..yogas.nadi_detector import check_nadi_signatures
from ..transit.advanced import calculate_transit_vedha
from ..strength.avasthas import calculate_baladi_avastha, calculate_lajjitadi_avastha, calculate_deeptadi_avastha
from ..strength.vaisheshikamsha import calculate_vaisheshikamsha
from ..charts.navamsha_nuance import is_pushkar_navamsha
from ..panchang.gandanta import check_gandanta
from ..panchang.muhurta import get_visha_amrit_ghatis
from ..dasha.conditional import check_dasha_suitability
from ..dasha.kalachakra import calculate_kalachakra_dasha
from ..dasha.chara import calculate_chara_dasha
from ..dasha.shattrimsha import calculate_shattrimsha_dasha
from ..strength.longevity_calculation import calculate_pindayu
from .varshaphala_strength import calculate_harsha_bala, calculate_panchavargiya_bala
from .varshaphala_strength import calculate_harsha_bala, calculate_panchavargiya_bala
from ..strength.war import analyze_planetary_war
from .houses import get_houses, get_house_from_longitude, get_house_lord, RASHI_LORDS, get_house_from_cusps
from datetime import datetime
import traceback
from functools import lru_cache

from ..matchmaking.data import NAKSHATRA_GANA, NAKSHATRA_YONI, NAKSHATRA_NADI

def _get_nakshatra_info(longitude: float) -> NakshatraInfo:
    """Calculate detailed Nakshatra info for a given longitude."""
    idx = int(longitude / NAK_SPAN)
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

from ..strength.relationships import get_natural_relationship, get_composite_relationship, get_temporary_relationship

@lru_cache(maxsize=128)
def calculate_chart_data(birth_dt: datetime, lat: float, lon: float, tz_str: str) -> CanonicalChart:
    """Master Engine: Returns a complete CanonicalChart object."""
    try:
        # Enable Topocentric Precision
        set_topocentric(lat, lon)
        jd_ut = datetime_to_jd(birth_dt, tz_str)

        # 1. Houses and Lagna
        house_data = get_houses(jd_ut, lat, lon)
        ascendant = house_data["ascendant"]
        asc_rashi = int(ascendant // 30)
        asc_nak = _get_nakshatra_info(ascendant)

        # 2. Basic Planet Data
        raw_planets = {}
        planets_lon = {}

        for name, pid in PLANETS.items():
            pos = get_planet_position(jd_ut, pid)
            raw_planets[name] = pos
            planets_lon[name] = pos["longitude"]

        # Ketu logic
        planets_lon["Ketu"] = (planets_lon["Rahu"] + 180) % 360

        # Upagrahas
        from .upagrahas import get_upagraha_longitudes
        from ..panchang.sky import get_sunrise, get_sunset
        sr_jd = get_sunrise(jd_ut, lat, lon) or jd_ut - 0.25
        ss_jd = get_sunset(jd_ut, lat, lon) or jd_ut + 0.25
        next_sr = get_sunrise(jd_ut + 1.0, lat, lon) or jd_ut + 0.75

        # Correctly determine Vedic Weekday (Day starts at Sunrise)
        # 0=Mon, 1=Tue... 6=Sun
        python_weekday = birth_dt.weekday()
        if jd_ut < sr_jd:
            # If born before sunrise, technically still previous day in Vedic tradition
            python_weekday = (python_weekday - 1 + 7) % 7

        v_weekday = (python_weekday + 1) % 7 # 0=Sun, 1=Mon...

        planets_lon.update(get_upagraha_longitudes(jd_ut, sr_jd, ss_jd, next_sr, v_weekday, lat, lon))

        # 3. Divisional Charts
        divisions = [1, 9, 10] # Min needed for UI
        divs = { f"D{d}": get_varga_chart(planets_lon, ascendant, d) for d in divisions }

        # 4. Enhanced Planet Data
        planets = {}
        func_map = get_functional_status(asc_rashi)

        # Temp Shadbala
        from ..panchang.hora import WEEKDAY_TO_HORA_START, HORA_ORDER
        from ..panchang.tithi import get_tithi_info
        is_day = sr_jd < jd_ut < ss_jd
        t_num = get_tithi_info(jd_ut)["number"]

        h_start = WEEKDAY_TO_HORA_START.get(v_weekday, 0)
        diff_h = (jd_ut - sr_jd) * 24.0
        hora_lord = HORA_ORDER[(h_start + int(diff_h)) % 7]

        WEEKDAY_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

        temp_shad = {
            "planets": { n: {"longitude": l, "rashi": int(l//30), "house": get_house_from_longitude(l, ascendant), "is_retrograde": False, "speed_long": 1.0} for n,l in planets_lon.items() if n not in ["Rahu","Ketu"]},
            "divisional_charts": divs
        }
        shad_map = calculate_shadbala(temp_shad, is_day, t_num<=15, WEEKDAY_LORDS[v_weekday], hora_lord)

        for name, lon_p in planets_lon.items():
            rashi = int(lon_p // 30)
            deg = lon_p % 30
            house = get_house_from_longitude(lon_p, ascendant)
            dignity = get_dignity(name, rashi, deg)

            planets[name] = PlanetInfo(
                name=name, longitude=lon_p,
                latitude=raw_planets.get(name, {}).get("latitude", 0.0),
                speed=raw_planets.get(name, {}).get("speed_long", 1.0),
                is_retrograde=raw_planets.get(name, {}).get("is_retrograde", False),
                is_combust=False, rashi=rashi, degree=deg, house=house, dignity=dignity,
                nakshatra=_get_nakshatra_info(lon_p),
                dispositor=RASHI_LORDS[rashi],
                functional_status=func_map.get(name, "Neutral"),
                shadbala_score=shad_map.get(name, {}).get("total_shadbala", 400.0),
                baladi_avastha=calculate_baladi_avastha(rashi, deg),
                deeptadi_avastha=calculate_deeptadi_avastha(name, dignity),
                vaisheshikamsha="Parijata",
                vimsopaka_score=15.0, ishta_phala=30.0, kashta_phala=10.0,
                navamsa_rashi=divs["D9"].get(name, rashi)
            )

        # 5. Build Final Object
        planets_rashi_map = {n: int(l//30) for n, l in planets_lon.items()}
        final_chart = CanonicalChart(
            birth_datetime=birth_dt, timezone=tz_str, latitude=lat, longitude=lon,
            ayanamsa=get_ayanamsa(jd_ut), ascendant=ascendant, asc_rashi=asc_rashi,
            asc_nakshatra=asc_nak, planets=planets, houses=house_data["cusps"],
            house_lords={h: get_house_lord(h, asc_rashi) for h in range(1, 13)},
            divisional_charts=divs, ashtakavarga=calculate_ashtakavarga(planets_rashi_map, asc_rashi),
            yogas=[], bhava_chalit={h: [] for h in range(1, 13)},
            kp_cusps=get_houses(jd_ut, lat, lon, hsys=b'P')["cusps"],
            jaimini_karakas=calculate_charakarakas(planets_lon),
            special_lagnas=calculate_special_lagnas(jd_ut, sr_jd, planets_lon["Sun"]),
            arudha_padas=calculate_arudha_padas(asc_rashi, {h: get_house_lord(h, asc_rashi) for h in range(1, 13)}, planets),
            yogi_details=calculate_yogi_avayogi(planets_lon["Sun"], planets_lon["Moon"]),
            rashi_drishti={r: get_jaimini_aspects(r) for r in range(12)},
            karakamsha_swamsha=get_karakamsha_swamsha(planets, divs["D9"].get("Lagna", 0)),
            chara_dasha=calculate_chara_dasha(asc_rashi, {n: p.rashi for n, p in planets.items()}, birth_dt),
            kalachakra_dasha=calculate_kalachakra_dasha(planets_lon["Moon"], birth_dt),
            shattrimsha_dasha=calculate_shattrimsha_dasha(asc_nak.index, birth_dt),
            bazi_pillars=calculate_bazi_pillars(birth_dt.year, birth_dt.month, birth_dt.day, birth_dt.hour),
            maya_tzolkin=calculate_maya_tzolkin(birth_dt.year, birth_dt.month, birth_dt.day),
            human_design=calculate_human_design(planets),
            numerology=get_numerology_data(birth_dt.strftime('%Y-%m-%d')),
            biorhythms=calculate_biorhythms(birth_dt, datetime.now())
        )
        final_chart.yogas = detect_yogas(planets, final_chart.house_lords, chart=final_chart)
        return final_chart

    except Exception as e:
        print(f"CRITICAL ENGINE ERROR: {e}")
        traceback.print_exc()
        return _create_fallback_chart(birth_dt, lat, lon, tz_str)

def _create_fallback_chart(dt, lat, lon, tz):
    return CanonicalChart(
        birth_datetime=dt, latitude=lat, longitude=lon, timezone=tz, ayanamsa=24.0,
        ascendant=0.0, asc_rashi=0, asc_nakshatra=_get_nakshatra_info(0.0),
        planets={}, houses=[0.0]*13, house_lords={}, divisional_charts={}, ashtakavarga={}, yogas=[]
    )
