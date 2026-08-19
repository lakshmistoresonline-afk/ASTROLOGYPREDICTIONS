from typing import Dict, Any, List
from .ephemeris import get_planet_position, get_ayanamsa, set_topocentric
from .datetime import datetime_to_jd
from .houses import get_houses, get_house_from_longitude, get_house_lord, RASHI_LORDS
from .planets import PLANETS, NAKSHATRA_NAMES, NAKSHATRA_LORDS, NAK_SPAN
from .nakshatra_data import NAKSHATRA_DEITIES, NAKSHATRA_SYMBOLS
from ..strength.dignity import get_dignity
from ..strength.functional import get_functional_status
from ..strength.aspects import get_graha_drishti
from ..charts.divisional import get_varga_chart
from ..strength.shadbala import calculate_shadbala, calculate_vimsopaka, calculate_ishta_kashta, calculate_exaltation_bala
from ..charts.ashtakavarga import calculate_ashtakavarga
from ..yogas.detector import detect_yogas
from .models import CanonicalChart, PlanetInfo, NakshatraInfo, ShadbalaInfo, KPInfo
from .kp import get_kp_lords
from .jaimini import calculate_charakarakas
from .houses import get_houses, get_house_from_longitude, get_house_lord, RASHI_LORDS, get_house_from_cusps
from datetime import datetime
from functools import lru_cache

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
        symbol=NAKSHATRA_SYMBOLS[idx] if idx < len(NAKSHATRA_SYMBOLS) else None
    )

@lru_cache(maxsize=128)
def calculate_chart_data(birth_dt: datetime, lat: float, lon: float, tz_str: str) -> CanonicalChart:
    """Master Engine: Returns a complete CanonicalChart object."""
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

    # First pass: Get longitudes for all planets
    for name, pid in PLANETS.items():
        pos = get_planet_position(jd_ut, pid)
        raw_planets[name] = pos
        planets_lon[name] = pos["longitude"]

    # Ketu logic (Standard: Mean Node + 180)
    rahu_lon = planets_lon["Rahu"]
    ketu_lon = (rahu_lon + 180) % 360
    # For speed, Ketu speed is usually considered opposite of Rahu or similar
    planets_lon["Ketu"] = ketu_lon

    # 3. Divisional Charts (Full set D1-D60) - Needed for Vimsopaka
    divisions = [1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]
    divisional_charts = {}
    for d in divisions:
        varga = get_varga_chart(planets_lon, ascendant, d)
        divisional_charts[f"D{d}"] = varga

    # 4. Enhanced Planet Data
    planets = {}
    functional_status_map = get_functional_status(asc_rashi)

    # Temporary dict to build Shadbala
    temp_chart_for_shadbala = {
        "planets": {
            name: {
                "longitude": lon,
                "house": get_house_from_longitude(lon, ascendant)
            } for name, lon in planets_lon.items() if name != "Ketu"
        }
    }
    shadbala_map = calculate_shadbala(temp_chart_for_shadbala)

    for name, lon in planets_lon.items():
        if name == "Ketu":
            # Synthesize Ketu pos from Rahu if needed, or re-calculate
            # For now, simplistic synthesis
            lat_k = -raw_planets["Rahu"]["latitude"]
            speed_k = raw_planets["Rahu"]["speed_long"] # Nodes are usually retrograde
            is_retro_k = True
        else:
            lat_k = raw_planets[name]["latitude"]
            speed_k = raw_planets[name]["speed_long"]
            is_retro_k = raw_planets[name]["is_retrograde"]

        rashi = int(lon // 30)
        deg = lon % 30
        house = get_house_from_longitude(lon, ascendant)

        # Check combustion (Sun is planet id 0)
        is_combust = False
        if name != "Sun":
            sun_lon = planets_lon["Sun"]
            diff = abs(lon - sun_lon) % 360
            if diff > 180: diff = 360 - diff
            if diff < 8.0: # Simplified combustion limit
                is_combust = True

        sb_info = shadbala_map.get(name, {})

        # Calculate Vimsopaka
        p_vargas = {v: divisional_charts[v][name] for v in divisional_charts if name in divisional_charts[v]}
        v_score = calculate_vimsopaka(name, p_vargas)

        # Calculate Ishta/Kashta (Simplified)
        ucha_b = calculate_exaltation_bala(name, lon)
        ishta, kashta = calculate_ishta_kashta(name, ucha_b, 30.0) # 30 is neutral chesta

        planets[name] = PlanetInfo(
            name=name,
            longitude=lon,
            latitude=lat_k,
            speed=speed_k,
            is_retrograde=is_retro_k,
            is_combust=is_combust,
            rashi=rashi,
            degree=deg,
            house=house,
            dignity=get_dignity(name, rashi, deg),
            nakshatra=_get_nakshatra_info(lon),
            dispositor=RASHI_LORDS[rashi],
            functional_status=functional_status_map.get(name),
            shadbala_score=sb_info.get("total_shadbala"),
            shadbala_label=f"{sb_info.get('total_rupas')} Rupas" if sb_info else None,
            shadbala_details=ShadbalaInfo(**sb_info) if sb_info else None,
            kp_details=None, # Filled in step 8
            vimsopaka_score=v_score,
            ishta_phala=ishta,
            kashta_phala=kashta
        )

    # 5. House Lords
    house_lords = {h: get_house_lord(h, asc_rashi) for h in range(1, 13)}

    # 6. Ashtakavarga
    planets_rashi = {name: info.rashi for name, info in planets.items()}
    av_data = calculate_ashtakavarga(planets_rashi, asc_rashi)

    # 7. Yogas
    yoga_results = detect_yogas(planets, house_lords)

    # 8. KP Cusps and Bhava Chalit
    kp_data = get_houses(jd_ut, lat, lon, hsys=b'P')
    kp_cusps = kp_data["cusps"]

    bhava_chalit = {h: [] for h in range(1, 13)}
    for name, p_info in planets.items():
        # Get KP Sub-Lord
        star, sub = get_kp_lords(p_info.longitude)
        p_info.kp_details = KPInfo(star_lord=star, sub_lord=sub)

        # Bhava Chalit mapping
        bc_house = get_house_from_cusps(p_info.longitude, kp_cusps)
        bhava_chalit[bc_house].append(name)

    # 9. Jaimini Karakas
    jaimini_data = calculate_charakarakas(planets_lon)

    return CanonicalChart(
        birth_datetime=birth_dt,
        timezone=tz_str,
        latitude=lat,
        longitude=lon,
        ayanamsa=get_ayanamsa(jd_ut),
        ascendant=ascendant,
        asc_rashi=asc_rashi,
        asc_nakshatra=asc_nak,
        planets=planets,
        houses=house_data["cusps"],
        house_lords=house_lords,
        divisional_charts=divisional_charts,
        ashtakavarga=av_data,
        yogas=yoga_results,
        bhava_chalit=bhava_chalit,
        kp_cusps=kp_cusps,
        jaimini_karakas=jaimini_data
    )
