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
from ..strength.bhava_bala import calculate_bhava_bala
from ..charts.ashtakavarga import calculate_ashtakavarga
from ..yogas.detector import detect_yogas
from .models import CanonicalChart, PlanetInfo, NakshatraInfo, ShadbalaInfo, KPInfo
from .kp import get_kp_lords
from .jaimini import calculate_charakarakas
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

    # 2b. Upagrahas (Gulika, Mandi)
    from .upagrahas import get_upagraha_longitudes
    from ..panchang.sky import get_sunrise, get_sunset
    sr_jd = get_sunrise(jd_ut, lat, lon)
    ss_jd = get_sunset(jd_ut, lat, lon)
    next_sr = get_sunrise(jd_ut + 1.0, lat, lon)
    weekday = birth_dt.weekday() # 0=Mon
    # Python weekday (0=Mon) to Vedic (0=Sun)
    vedic_weekday = (weekday + 1) % 7

    upagrahas = get_upagraha_longitudes(jd_ut, sr_jd, ss_jd, next_sr, vedic_weekday, lat, lon)
    planets_lon.update(upagrahas)

    # 3. Divisional Charts (Full set D1-D60) - Needed for Vimsopaka
    divisions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20, 24, 27, 30, 40, 45, 60]
    divisional_charts = {}
    for d in divisions:
        varga = get_varga_chart(planets_lon, ascendant, d)
        divisional_charts[f"D{d}"] = varga

    # 4. Enhanced Planet Data
    planets = {}
    functional_status_map = get_functional_status(asc_rashi)

    # Temporary dict to build Shadbala
    from ..panchang.sky import get_sunrise, get_sunset
    from ..panchang.tithi import get_tithi
    from ..panchang.hora import WEEKDAY_TO_HORA_START, HORA_ORDER

    sunrise_jd = get_sunrise(jd_ut, lat, lon)
    sunset_jd = get_sunset(jd_ut, lat, lon)
    is_day = sunrise_jd < jd_ut < sunset_jd if sunrise_jd and sunset_jd else True

    t_data = get_tithi(jd_ut)
    is_shukla = t_data["number"] <= 15

    weekday_idx = (birth_dt.weekday() + 1) % 7 # 0=Sun
    # Map to Lord
    WD_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    wd_lord = WD_LORDS[weekday_idx]

    # Simple Hora Lord
    h_start = WEEKDAY_TO_HORA_START.get(weekday_idx, 0)
    # diff from sunrise in hours
    diff_h = (jd_ut - sunrise_jd) * 24.0 if sunrise_jd else 0.0
    hora_lord = HORA_ORDER[(h_start + int(diff_h)) % 7]

    temp_chart_for_shadbala = {
        "planets": {
            name: {
                "longitude": lon,
                "house": get_house_from_longitude(lon, ascendant),
                "rashi": int(lon // 30),
                "speed_long": 1.0, # Placeholder
                "is_retrograde": False
            } for name, lon in planets_lon.items() if name not in ["Rahu", "Ketu"]
        },
        "divisional_charts": divisional_charts
    }
    shadbala_map = calculate_shadbala(temp_chart_for_shadbala, is_day=is_day, is_shukla=is_shukla, wd_lord=wd_lord, hora_lord=hora_lord)

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

        # Calculate Vargottama
        d9_rashi = divisional_charts["D9"].get(name)
        is_vargottama = (rashi == d9_rashi)

        # Calculate relationships
        sign_lord = RASHI_LORDS[rashi]
        nak_info = _get_nakshatra_info(lon)
        nak_lord = nak_info.lord

        # We need all planet houses to calculate temporary relationship
        # Since we are in a loop, let's do a second pass for relationships later
        # OR use natural relationships for now and patch later.

        # Calculate planetary war (Mars to Saturn)
        is_in_war = False
        if name in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            for other_name, other_lon in planets_lon.items():
                if other_name != name and other_name in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
                    if abs(lon - other_lon) < 1.0:
                        is_in_war = True
                        break

        # Calculate Moolatrikona
        dignity = get_dignity(name, rashi, deg)
        is_mt = (dignity == "Moolatrikona")

        # Calculate Avasthas
        baladi = calculate_baladi_avastha(rashi, deg)
        deeptadi = calculate_deeptadi_avastha(name, dignity)

        # Lajjitadi (needs house occupants)
        # We'll set this in a second pass since we need occupants

        p_vargas = {v: divisional_charts[v][name] for v in divisional_charts if name in divisional_charts[v]}
        vaisheshika = calculate_vaisheshikamsha(name, p_vargas)

        is_pushkar = is_pushkar_navamsha(rashi, deg)
        nadi_a = get_nadi_amsha(rashi, deg)

        weight = 1.0
        if baladi == "Yuva (Adult)": weight = 1.2
        elif baladi == "Vriddha (Old)": weight = 0.5
        elif baladi == "Mrita (Dead)": weight = 0.1

        if "Deept" in deeptadi: weight += 0.5
        if "Kopita" in deeptadi: weight -= 0.5
        if is_pushkar: weight += 0.5

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
            dignity=dignity,
            nakshatra=nak_info,
            dispositor=sign_lord,
            functional_status=functional_status_map.get(name),
            directional_strength=sb_info.get("dig_bala"),
            is_in_planetary_war=is_in_war,
            is_in_moolatrikona=is_mt,
            shadbala_score=sb_info.get("total_shadbala"),
            baladi_avastha=baladi,
            deeptadi_avastha=deeptadi,
            vaisheshikamsha=vaisheshika["level"],
            pushkar_navamsha=is_pushkar,
            nadi_amsha=nadi_a,
            avastha_weight=weight,
            shadbala_label=f"{sb_info.get('total_rupas')} Rupas" if sb_info else None,
            shadbala_details=ShadbalaInfo(**sb_info) if sb_info else None,
            kp_details=None, # Filled in step 8
            vimsopaka_score=v_score,
            ishta_phala=ishta,
            kashta_phala=kashta,
            is_vargottama=is_vargottama,
            navamsa_rashi=d9_rashi,
            # Relationships set in second pass
            nakshatra_lord_rel=None,
            dispositor_rel=None
        )

    # Second pass for accurate temporary relationships and Lajjitadi
    for name, p_info in planets.items():
        # Lajjitadi
        h_occupants = house_occupants_map.get(p_info.house, [])
        p_info.lajjitadi_avastha = calculate_lajjitadi_avastha(name, p_info.rashi, h_occupants, p_info.house, p_info.dignity)

        if name in ["Rahu", "Ketu"]: continue

        s_lord = p_info.dispositor
        n_lord = p_info.nakshatra.lord

        if s_lord in planets:
            p_info.dispositor_rel = get_composite_relationship(
                name, p_info.house, s_lord, planets[s_lord].house
            )
        else:
            p_info.dispositor_rel = get_natural_relationship(name, s_lord)

        if n_lord in planets:
            p_info.nakshatra_lord_rel = get_composite_relationship(
                name, p_info.house, n_lord, planets[n_lord].house
            )
        else:
            p_info.nakshatra_lord_rel = get_natural_relationship(name, n_lord)

    # 5. House Lords
    house_lords = {h: get_house_lord(h, asc_rashi) for h in range(1, 13)}

    # 6. Ashtakavarga
    planets_rashi = {name: info.rashi for name, info in planets.items()}
    av_data = calculate_ashtakavarga(planets_rashi, asc_rashi)

    # 7. Yogas - (Will re-call with chart object at the end or use partial)
    # Temporary placeholder yogas
    yoga_results = detect_yogas(planets, house_lords)

    # 8. KP Cusps and Bhava Chalit
    kp_data = get_houses(jd_ut, lat, lon, hsys=b'P')
    kp_cusps = kp_data["cusps"]

    bhava_chalit = {h: [] for h in range(1, 13)}
    house_occupants_map = {h: [] for h in range(1, 13)}
    for name, p_info in planets.items():
        # Get KP Sub-Lord and SSL
        from .kp import get_kp_sub_sub_lord
        star, sub, ssl = get_kp_sub_sub_lord(p_info.longitude)

        # 4th Step: Star Lord of Sub Lord
        # (This requires calculating position of Sub Lord or using a proxy)
        # In reality, it needs a more complex recursive lookup.
        p_info.kp_details = KPInfo(star_lord=star, sub_lord=sub, sub_sub_lord=ssl, step4_lord=sub) # Using sub as proxy for now

        # Bhava Chalit mapping
        bc_house = get_house_from_cusps(p_info.longitude, kp_cusps)
        bhava_chalit[bc_house].append(name)
        house_occupants_map[p_info.house].append(name)

    # 8b. Bhava Bala
    bhava_bala = calculate_bhava_bala({
        "planets": planets,
        "house_occupants": house_occupants_map,
        "house_lords": house_lords
    })

    # 9. Jaimini Karakas
    jaimini_data = calculate_charakarakas(planets_lon)
    from .jaimini import get_karakamsha_swamsha
    ks_data = get_karakamsha_swamsha(planets, divisional_charts["D9"].get("Lagna", 0))

    # 10. Aspect Insights
    from ..strength.aspects import get_aspect_analysis
    aspect_insights = get_aspect_analysis(planets, asc_rashi)

    # 11. Advanced Jyotish Calculations
    # A. Special Lagnas
    special_lagnas = calculate_special_lagnas(jd_ut, sunrise_jd, planets_lon["Sun"])
    special_lagnas["Indu Lagna"] = calculate_indu_lagna(planets, house_lords)

    # B. Arudha Padas
    arudhas = calculate_arudha_padas(asc_rashi, house_lords, planets)

    # C. Yogi/Avayogi
    yogi_data = calculate_yogi_avayogi(planets_lon["Sun"], planets_lon["Moon"])

    # Bhrigu Bindu
    b_bindu = calculate_bhrigu_bindu(planets_lon["Moon"], planets_lon["Rahu"])
    b_insights = get_bhrigu_insights(planets)

    # D. Jaimini Aspects
    j_aspects = {r: get_jaimini_aspects(r) for r in range(12)}

    # E. Argala Analysis
    from .argala import calculate_full_argala
    argala = calculate_full_argala(planets, asc_rashi)

    # F. Dagtha Rashis (Burnt Signs)
    from ..panchang.tithi import get_tithi
    tithi_data = get_tithi(jd_ut)
    dagtha = calculate_dagtha_rashis(tithi_data["number"])

    # G. Ishta/Kashta Totals
    ishta_total = sum(p.ishta_phala for p in planets.values() if p.ishta_phala)
    kashta_total = sum(p.kashta_phala for p in planets.values() if p.kashta_phala)

    # H. Planetary War (Graha Yuddha)
    war_results = analyze_planetary_war(planets)

    # I. Harsha Bala (for Varshaphala context)
    harsha_bala = calculate_harsha_bala(planets, asc_rashi)

    # 12. Cosmic Refinements (Tajika, Nadi, Sahams)
    tajika = calculate_tajika_yogas(planets)
    sahams = calculate_sahams(planets, ascendant, is_day)
    ext_sahams = calculate_extended_sahams(planets, ascendant, is_day)
    nadi = get_nadi_connections(planets)

    # Rashi Drishti (Jaimini Aspects)
    rashi_drishti = {r: get_jaimini_aspects(r) for r in range(12)}

    # 13. Esoteric and Conditional Systems
    eclipses = get_upcoming_eclipses(jd_ut)
    ec_impact = check_eclipse_impact(planets, eclipses)

    # We pass the chart data partially to calculate points
    sensitive_pts = calculate_sensitive_points(final_chart if 'final_chart' in locals() else type('obj', (object,), {'planets': planets, 'ascendant': ascendant, 'divisional_charts': divisional_charts, 'house_lords': house_lords}) )
    sudarshana = get_sudarshana_analysis(type('obj', (object,), {'planets': planets, 'asc_rashi': asc_rashi, 'house_lords': house_lords}))
    cond_dashas = check_dasha_suitability(type('obj', (object,), {'planets': planets, 'house_lords': house_lords}))
    khandas = calculate_ashtakavarga_precincts(av_data["SAV"])

    # Yearly & KP Refinements
    from .varshaphala import calculate_muntha
    age_y = datetime.now().year - birth_dt.year
    m_rashi = calculate_muntha(asc_rashi, age_y)
    v_lord = calculate_varsheshwar(planets, asc_rashi, m_rashi, asc_rashi, is_day)
    kp_sigs = calculate_kp_significators(planets, kp_cusps)
    g_alerts = check_gandanta(planets, ascendant)

    # Advanced Timing & Charts
    sec_prog = calculate_secondary_progressions(birth_dt, datetime.now(), lat, lon, tz_str)
    solar_arc = calculate_solar_arc_directions(planets, birth_dt, datetime.now(), tz_str)
    draconic = get_draconic_chart(planets, planets_lon["Rahu"])

    # Heliocentric & Harmonics
    helio = get_heliocentric_positions(jd_ut)
    harmonics = calculate_harmonics(planets_lon, [5, 7, 9, 13])
    h_resonances = analyze_harmonic_resonance(harmonics)

    # Bazi, Uranian, Maya
    bazi = calculate_bazi_pillars(birth_dt.year, birth_dt.month, birth_dt.day, birth_dt.hour)
    uranian = get_uranian_positions(jd_ut)
    maya = calculate_maya_tzolkin(birth_dt.year, birth_dt.month, birth_dt.day)
    mundane = get_mundane_indicators(jd_ut)
    weather = get_weather_indicators(jd_ut)
    astrocart = get_angular_points(jd_ut)

    # Mahabote, Tibetan, Celtic
    mahabote = calculate_mahabote(birth_dt.year, vedic_weekday)
    tibetan = {
        "mewa": calculate_tibetan_mewa(birth_dt.year),
        "parkha": get_tibetan_parkha(birth_dt.year)
    }
    celtic = get_celtic_tree_astrology(birth_dt.month, birth_dt.day)
    native = get_native_american_totem(birth_dt.month, birth_dt.day)
    kabbalah_p = get_kabbalistic_profile(planets)

    # Galactic, Zi Wei, Lilith, Geomancy
    galactic = analyze_galactic_aspects(planets)
    zi_wei = calculate_zi_wei_palaces(birth_dt.month, birth_dt.day, birth_dt.hour // 2)
    lilith = get_lilith_positions(jd_ut)
    geomancy = calculate_birth_figure(birth_dt.year, birth_dt.month, birth_dt.day, birth_dt.hour)

    hd_data = calculate_human_design(planets)

    # Hellenistic & Gene Keys
    g_lots = calculate_greek_lots(planets, ascendant, is_day)
    ann_prof = get_annual_profection(asc_rashi, age_y)
    g_keys = [get_gene_key_interpretation(g) for g in hd_data["active_gates"]]
    e_bounds = {name: get_egyptian_bound(p.rashi, p.degree) for name, p in planets.items()}

    # Zodiacal Releasing
    f_rashi = int(g_lots.get("Lot of Fortune", 0) // 30)
    s_rashi = int(g_lots.get("Lot of Spirit", 0) // 30)
    zr = {
        "Fortune": calculate_zodiacal_releasing(f_rashi, birth_dt),
        "Spirit": calculate_zodiacal_releasing(s_rashi, birth_dt)
    }

    # Uranian Formulas
    u_forms = calculate_uranian_formulas(planets, uranian)

    firdaria = calculate_firdaria(birth_dt, is_day)

    lk_year_lord = get_lal_kitab_year_lord(planets, datetime.now().year, birth_dt.year)
    lk_yearly_h = analyze_lal_kitab_yearly_houses(planets, age_y + 1)

    # Fixed Stars
    ayanamsa = get_ayanamsa(jd_ut)
    f_stars = analyze_fixed_star_conjunctions(planets, ayanamsa)

    # Western Aspects
    w_aspects = calculate_natal_western_aspects(planets)

    # 13a. Global Data Integration (Numerology, Biorhythms, Asteroids)
    num_data = get_numerology_data(birth_dt.strftime('%Y-%m-%d'))
    bio_data = calculate_biorhythms(birth_dt, datetime.now())
    ast_data = get_asteroid_positions(jd_ut)

    # Sabian Symbols for major points
    sabian = {
        "Lagna": get_sabian_symbol(asc_rashi, ascendant % 30),
        "Sun": get_sabian_symbol(planets["Sun"].rashi, planets["Sun"].degree),
        "Moon": get_sabian_symbol(planets["Moon"].rashi, planets["Moon"].degree)
    }

    # Decanates and Dwadashamshas
    for name, p_info in planets.items():
        dec = get_decanate_info(p_info.rashi, p_info.degree)
        dwad = get_dwadashamsha(p_info.rashi, p_info.degree)
        hex_data = get_hexagram(p_info.longitude)

        # We can add these to p_info or store separately.
        # Let's assume p_info has space or we add it to the model.

    # 13b. KP 4-Step and Nadi Signatures
    # Create a partial chart object for functions that need it
    partial_chart = type('obj', (object,), {
        'planets': planets,
        'house_lords': house_lords,
        'ascendant': ascendant,
        'divisional_charts': divisional_charts
    })
    kp_4_steps = calculate_kp_4_steps(partial_chart)
    nadi_sigs = check_nadi_signatures(planets)

    # Current Transit Vedha (using natal moon)
    # This usually needs current time planets, but we can store the logic.
    natal_moon_rashi = planets["Moon"].rashi
    # For now, we simulate with natal positions to show Vedha in natal chart (Natal Vedha)
    vedha = calculate_transit_vedha(natal_moon_rashi, {n: p.longitude for n, p in planets.items()})

    # BCP Activation
    bcp_data = calculate_bcp_activation(asc_rashi, birth_dt.year, datetime.now().year)

    # Supreme Precision Data
    sl_lon = calculate_shree_lagna(planets_lon["Moon"], ascendant)
    hl_rashi = int(special_lagnas["Hora Lagna"] // 30)
    vl_data = calculate_varnada_lagna(asc_rashi, hl_rashi)
    kc_dasha = calculate_kalachakra_dasha(planets_lon["Moon"], birth_dt)

    # Conditional Dashas (Advanced)
    shat_dasha = calculate_shattrimsha_dasha(asc_nak.index, birth_dt)

    # Longevity Contribution
    pindayu = calculate_pindayu(planets)

    planets_rashi_map = {n: p.rashi for n, p in planets.items()}
    chara = calculate_chara_dasha(asc_rashi, planets_rashi_map, birth_dt)

    # 14. Yoga Re-detection (Second pass with full chart context)
    final_chart = CanonicalChart(
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
        jaimini_karakas=jaimini_data,
        bhava_bala=bhava_bala,
        aspect_insights=aspect_insights,
        special_lagnas=special_lagnas,
        arudha_padas=arudhas,
        yogi_details=yogi_data,
        jaimini_aspects=j_aspects,
        argala_analysis=argala,
        dagtha_rashis=dagtha,
        ishta_kashta_totals={"ishta": ishta_total, "kashta": kashta_total},
        tajika_yogas=tajika,
        sahams=sahams,
        nadi_connections=nadi,
        rashi_drishti=rashi_drishti,
        sudarshana_chakra=sudarshana,
        sensitive_points=sensitive_pts,
        conditional_dashas=cond_dashas,
        khanda_analysis=khandas,
        varsheshwar=v_lord,
        kp_significators=kp_sigs,
        kp_4_steps=kp_4_steps,
        gandanta_alerts=g_alerts,
        bcp_activation=bcp_data,
        kalachakra_dasha=kc_dasha,
        shree_lagna=sl_lon,
        varnada_lagna=vl_data,
        karakamsha_swamsha=ks_data,
        chara_dasha=chara,
        pindayu=pindayu,
        shattrimsha_dasha=shat_dasha,
        transit_vedha=vedha,
        nadi_signatures=nadi_sigs,
        bhrigu_bindu=b_bindu,
        bhrigu_insights=b_insights,
        fixed_star_conjunctions=f_stars,
        western_aspects=w_aspects,
        special_points={
            "Vertex": house_data.get("vertex", 0.0),
            "East Point": house_data.get("equatorial_ascendant", 0.0),
            "MC": house_data.get("mc", 0.0)
        },
        numerology=num_data,
        biorhythms=bio_data,
        asteroids=ast_data,
        sabian_symbols=sabian,
        upcoming_eclipses=eclipses,
        eclipse_impacts=ec_impact,
        extended_sahams=ext_sahams,
        secondary_progressions=sec_prog,
        solar_arc_directions=solar_arc,
        draconic_chart=draconic,
        heliocentric_positions=helio,
        harmonic_charts=harmonics,
        harmonic_resonances=h_resonances,
        bazi_pillars=bazi,
        uranian_tnps=uranian,
        maya_tzolkin=maya,
        mundane_indicators=mundane,
        weather_indicators=weather,
        astrocartography=astrocart,
        mahabote=mahabote,
        tibetan_data=tibetan,
        celtic_tree=celtic,
        firdaria=firdaria,
        native_american=native,
        kabbalah=kabbalah_p,
        galactic_aspects=galactic,
        zi_wei_dou_shu=zi_wei,
        lilith=lilith,
        geomancy=geomancy,
        human_design=hd_data,
        hellenistic_lots=g_lots,
        annual_profection=ann_prof,
        gene_keys=g_keys,
        egyptian_bounds=e_bounds,
        zodiacal_releasing=zr,
        uranian_formulas=u_forms,
        lal_kitab_year_data={"lord": lk_year_lord, "houses": lk_yearly_h}
    )

    # Recalculate yogas with full context
    final_chart.yogas = detect_yogas(planets, house_lords, chart=final_chart)

    return final_chart
