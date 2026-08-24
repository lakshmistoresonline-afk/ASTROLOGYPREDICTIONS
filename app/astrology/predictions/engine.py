from typing import Dict, Any, List
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .personality import get_personality_prediction
from .education import get_education_prediction
from .career import get_career_prediction
from .business import get_business_prediction
from .finance import get_finance_prediction
from .marriage import get_marriage_prediction
from .health import get_health_prediction
from .travel import get_travel_prediction
from .legal import get_legal_prediction
from .spirituality import get_spirituality_prediction
from .fame import get_fame_prediction
from .life_purpose import get_life_purpose_prediction
from .life_themes import get_life_themes_prediction
from .children import get_children_prediction
from .family import get_family_prediction
from .property import get_property_prediction
from .foreign import get_foreign_prediction
from .longevity import get_longevity_prediction
from .wealth import get_wealth_prediction
from .leadership import get_leadership_prediction
from .parents import get_parents_prediction
from .siblings import get_siblings_prediction
from .vehicles import get_vehicles_prediction
from .relationships import get_relationships_prediction
from .status import get_status_prediction
from .government import get_government_prediction
from .yearly import get_yearly_prediction
from .monthly import get_monthly_prediction
from .speculation import get_speculation_prediction
from .scoring import get_label_from_score
from ..timing.engine import get_timing_score

def generate_evidence_based_predictions(chart: CanonicalChart, selected_date: datetime = None) -> Dict[str, Any]:
    """Aggregate all domain predictions with evidence, scoring, and timing context."""

    if selected_date is None:
        selected_date = datetime.now()

    # Define which planets/houses are relevant for each domain for timing
    domain_configs = {
        "Personality": (get_personality_prediction, [chart.house_lords[1], "Sun", "Moon"], [1]),
        "Education": (get_education_prediction, ["Mercury", "Jupiter", chart.house_lords[5]], [2, 4, 5, 9]),
        "Career": (get_career_prediction, [chart.house_lords[10], "Saturn", "Sun"], [10, 6, 11]),
        "Business": (get_business_prediction, ["Mercury", chart.house_lords[7], chart.house_lords[10]], [7, 10, 11]),
        "Finance": (get_finance_prediction, ["Jupiter", "Venus", chart.house_lords[2]], [2, 11]),
        "Wealth": (get_wealth_prediction, ["Jupiter", chart.house_lords[2]], [2]),
        "Marriage": (get_marriage_prediction, ["Venus", "Jupiter", chart.house_lords[7]], [7]),
        "Relationships": (get_relationships_prediction, ["Venus", chart.house_lords[11]], [7, 11]),
        "Children": (get_children_prediction, ["Jupiter", chart.house_lords[5]], [5]),
        "Family": (get_family_prediction, ["Moon", chart.house_lords[2], chart.house_lords[4]], [2, 4, 9]),
        "Parents": (get_parents_prediction, ["Sun", "Moon", chart.house_lords[4], chart.house_lords[9]], [4, 9]),
        "Siblings": (get_siblings_prediction, ["Mars", chart.house_lords[3]], [3, 11]),
        "Health": (get_health_prediction, ["Sun", "Moon", chart.house_lords[1]], [1, 6, 8, 12]),
        "Property": (get_property_prediction, ["Mars", "Venus", chart.house_lords[4]], [4]),
        "Vehicles": (get_vehicles_prediction, ["Venus", chart.house_lords[4]], [4]),
        "Travel": (get_travel_prediction, ["Moon", "Rahu", chart.house_lords[9]], [3, 7, 9, 12]),
        "Foreign Travel": (get_foreign_prediction, ["Rahu", chart.house_lords[12], chart.house_lords[9]], [9, 12]),
        "Foreign Settlement": (get_foreign_prediction, ["Rahu", chart.house_lords[12]], [12]),
        "Legal": (get_legal_prediction, ["Jupiter", "Mars", chart.house_lords[6]], [6, 7, 8]),
        "Spirituality": (get_spirituality_prediction, ["Jupiter", "Ketu", chart.house_lords[12]], [9, 12]),
        "Fame": (get_fame_prediction, ["Sun", chart.house_lords[10], chart.house_lords[5]], [1, 5, 10, 11]),
        "Leadership": (get_leadership_prediction, ["Sun", "Mars", chart.house_lords[10]], [1, 10]),
        "Longevity": (get_longevity_prediction, ["Saturn", chart.house_lords[8]], [1, 8]),
        "Life Purpose": (get_life_purpose_prediction, ["Sun", "Moon"], [1, 5, 9, 10]),
        "Life Themes": (get_life_themes_prediction, ["Sun", "Moon"], [1, 10]),
        "Social Status": (get_status_prediction, ["Sun", chart.house_lords[10]], [10]),
        "Dharma": (get_life_purpose_prediction, [chart.house_lords[9]], [9]),
        "Creativity": (get_children_prediction, ["Venus", chart.house_lords[5]], [5]),
        "Risk Tolerance": (get_leadership_prediction, ["Mars", "Rahu"], [1, 3, 8]),
        "Decision Style": (get_personality_prediction, ["Mercury", "Jupiter"], [1, 5]),
        "Communication": (get_personality_prediction, ["Mercury", chart.house_lords[2], chart.house_lords[3]], [2, 3]),
        "Learning Style": (get_education_prediction, ["Mercury", "Jupiter"], [2, 4, 5]),
        "Foreign Employment": (get_foreign_prediction, [chart.house_lords[10], "Rahu", chart.house_lords[12]], [10, 12]),
        "Government Authority": (get_government_prediction, ["Sun", "Mars", chart.house_lords[10]], [1, 10]),
        "Debt & Legal": (get_legal_prediction, ["Mars", "Saturn", chart.house_lords[6]], [6, 8, 12]),
        "Inheritance": (get_wealth_prediction, ["Saturn", chart.house_lords[8]], [2, 8]),
        "Social Service": (get_life_purpose_prediction, ["Saturn", chart.house_lords[6]], [6, 10]),
        "Mental Stability": (get_health_prediction, ["Moon", "Mercury", chart.house_lords[4]], [1, 4, 5]),
        "Speculation": (get_speculation_prediction, ["Mercury", "Rahu", chart.house_lords[5]], [5, 8, 11]),
        "Yearly Forecast": (lambda c, date=selected_date: get_yearly_prediction(c, date.year), ["Sun", chart.house_lords[1]], [1, 9, 10])
    }

    results = []
    total_score = 0.0

    # Categorization mapping
    CATEGORIES = {
        "Essence": ["Personality", "Life Purpose", "Life Themes", "Dharma", "Creativity", "Decision Style", "Communication", "Mental Stability"],
        "Material": ["Career", "Business", "Finance", "Wealth", "Property", "Vehicles", "Inheritance", "Foreign Employment", "Government Authority", "Speculation"],
        "Social": ["Marriage", "Relationships", "Children", "Family", "Parents", "Siblings", "Social Service", "Social Status", "Fame", "Leadership"],
        "Survival": ["Health", "Longevity", "Travel", "Foreign Travel", "Foreign Settlement", "Legal", "Debt & Legal", "Risk Tolerance", "Learning Style", "Yearly Forecast"]
    }

    categorized_results = {cat: [] for cat in CATEGORIES}

    for domain_name, (engine_func, planets, houses) in domain_configs.items():
        # 1. Calculate Timing First
        timing_ctx = get_timing_score(chart, planets, houses, selected_date)

        # 2. Call Engine with Timing Context if supported
        import inspect
        sig = inspect.signature(engine_func)
        kwargs = {}
        if "domain_type" in sig.parameters:
            kwargs["domain_type"] = domain_name
        if "timing_data" in sig.parameters:
            kwargs["timing_data"] = timing_ctx

        domain_res = engine_func(chart, **kwargs)

        # 3. Finalize Timing display
        domain_res.timing = [
            {"period": "Current Support", "impact": timing_ctx["label"], "score": timing_ctx["total_timing_score"]}
        ]

        res_dict = domain_res.model_dump()
        results.append(res_dict)
        total_score += domain_res.score

        # Categorize
        found_cat = False
        for cat, domains in CATEGORIES.items():
            if domain_name in domains:
                categorized_results[cat].append(res_dict)
                found_cat = True
                break
        if not found_cat:
            if "Miscellaneous" not in categorized_results: categorized_results["Miscellaneous"] = []
            categorized_results["Miscellaneous"].append(res_dict)

    avg_score = total_score / len(domain_configs)

    # 2. Add Timeline (Dasha-based)
    from .timeline import get_life_timeline, get_current_micro_timing
    from .financial import get_financial_market_indicators
    from .crypto import get_crypto_market_analysis
    from .bhava_analysis import get_detailed_bhava_analysis
    from ..core.panchapakshi import get_panchapakshi_info

    micro_timing = get_current_micro_timing(chart)

    # 3. Add Panchapakshi & BCP Summary
    moon_nak = chart.planets["Moon"].nakshatra.index + 1
    from ..panchang.tithi import get_tithi
    from ..panchang.sky import get_sunrise, get_sunset
    from ..core.swe_proxy import swe
    from ..core.datetime import datetime_to_jd

    jd = datetime_to_jd(selected_date, chart.timezone)
    sr_jd = get_sunrise(jd, chart.latitude, chart.longitude)
    ss_jd = get_sunset(jd, chart.latitude, chart.longitude)

    t_data = get_tithi(jd)
    bird = get_panchapakshi_info(moon_nak, t_data["number"] <= 15)

    # Calculate Segment (1-5)
    segment = 0
    if sr_jd and ss_jd:
        if sr_jd <= jd <= ss_jd:
            # Day
            duration = ss_jd - sr_jd
            segment = int(((jd - sr_jd) / duration) * 5)
        else:
            # Night (rough)
            segment = 2 # Placeholder for night segment

    if segment > 4: segment = 4

    from ..core.panchapakshi import get_current_activity
    # weekday from selected_date
    wd = (selected_date.weekday() + 1) % 7 # 0=Sun
    activity = get_current_activity(bird, wd, segment)

    bcp_data = chart.bcp_activation
    f_indicators = get_financial_market_indicators(chart)
    crypto_data = get_crypto_market_analysis(chart)

    return {
        "overall_score": round(avg_score, 2),
        "overall_label": get_label_from_score(avg_score),
        "domains": results,
        "categorized_domains": categorized_results,
        "timeline": get_life_timeline(chart),
        "micro_timing": micro_timing,
        "bhava_analysis": get_detailed_bhava_analysis(chart),
        "monthly_forecast": get_monthly_prediction(chart, selected_date),
        "selected_date": selected_date.isoformat(),
        "panchapakshi": {"bird": bird, "activity": activity, "segment": segment + 1},
        "bcp_summary": bcp_data,
        "financial_outlook": f_indicators,
        "crypto_market": crypto_data,
        "advanced_metrics": {
            "kp_4_steps": chart.kp_4_steps,
            "nadi_signatures": chart.nadi_signatures,
            "transit_vedha": chart.transit_vedha,
            "jaimini_aspects": chart.jaimini_aspects,
            "western_aspects": chart.western_aspects,
            "special_points": chart.special_points,
            "mundane": chart.mundane_indicators,
            "weather": chart.weather_indicators,
            "astrocartography": chart.astrocartography,
            "bhrigu_bindu": chart.bhrigu_bindu,
            "bhrigu_insights": chart.bhrigu_insights,
            "shodhya_pinda": chart.ashtakavarga.get("ShodhyaPinda"),
            "heliocentric": chart.heliocentric_positions,
            "harmonic_resonances": chart.harmonic_resonances,
            "bazi_pillars": chart.bazi_pillars,
            "uranian_tnps": chart.uranian_tnps,
            "maya_tzolkin": chart.maya_tzolkin,
            "mahabote": chart.mahabote,
            "tibetan": chart.tibetan_data,
            "celtic": chart.celtic_tree,
            "firdaria": chart.firdaria,
            "native_american": chart.native_american,
            "kabbalah": chart.kabbalah,
            "human_design": chart.human_design,
            "galactic_aspects": chart.galactic_aspects,
            "zi_wei_dou_shu": chart.zi_wei_dou_shu,
            "lilith": chart.lilith,
            "geomancy": chart.geomancy,
            "hellenistic": {
                "lots": chart.hellenistic_lots,
                "annual_profection": chart.annual_profection,
                "egyptian_bounds": chart.egyptian_bounds,
                "zodiacal_releasing": chart.zodiacal_releasing
            },
            "uranian_formulas": chart.uranian_formulas,
            "gene_keys": chart.gene_keys,
            "global_context": {
                "numerology": chart.numerology,
                "biorhythms": chart.biorhythms,
                "asteroids": chart.asteroids,
                "sabian": chart.sabian_symbols,
                "eclipses": chart.upcoming_eclipses,
                "eclipse_impacts": chart.eclipse_impacts,
                "extended_sahams": chart.extended_sahams,
                "western_timing": {
                    "secondary_progressions": chart.secondary_progressions,
                    "solar_arc_directions": chart.solar_arc_directions
                },
                "draconic": chart.draconic_chart,
                "lal_kitab_yearly": chart.lal_kitab_year_data
            }
        }
    }
