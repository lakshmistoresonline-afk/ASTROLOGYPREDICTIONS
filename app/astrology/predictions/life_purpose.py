from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_life_purpose_prediction(chart: CanonicalChart, domain_type: str = "Life Purpose & Dharma", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Soul Path Analysis: Atmakaraka, Lagna, Sun, and Moon."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords
    ak_name = chart.jaimini_karakas.get("Atmakaraka")

    if ak_name:
        ak = planets.get(ak_name)
        if ak:
            factors.append(EvidenceEngine.create_factor(
                "Atmakaraka", "planet", "positive", 20,
                f"{ak_name} is your Atmakaraka (Soul Planet): Your life purpose is centered around its qualities in House {ak.house}."
            ))

    # 1st House Lord
    ll_name = house_lords[1]
    ll = planets[ll_name]
    factors.append(EvidenceEngine.create_factor(
        "Lagna Lord Path", "lord", "positive", 10,
        f"Lagna Lord in House {ll.house} directs your physical and karmic focus in this lifetime."
    ))

    # 9th House Lord (Dharma)
    l9_name = house_lords[9]
    l9 = planets[l9_name]
    factors.append(EvidenceEngine.create_factor(
        "Dharma Theme", "lord", "positive", 10,
        f"9th Lord {l9_name} in House {l9.house} indicates your higher purpose and sense of duty (Dharma)."
    ))

    # Varga Confirmation
    v_conf = False
    if "D9" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Navamsha (D9) analysis confirms the deep alignment of soul purpose and destiny."))

    # 3b. Advanced Soul Path Indicators
    # A. Arudha Lagna (AL) - Path in the World
    al_rashi = chart.arudha_padas.get("AL")
    if al_rashi is not None:
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Social Dharma", "yoga", "positive", 12,
            f"Your Arudha Lagna in {RASHI_NAMES[al_rashi]} defines how your life purpose manifests and is recognized in society."
        ))

    # B. Sudarshana Chakra Resonance for 9th House (Dharma)
    s_chakra = chart.sudarshana_chakra.get(9, {})
    if s_chakra.get("resonance") == "HIGH":
        factors.append(EvidenceEngine.create_factor(
            "Strong Dharma Promise", "house", "positive", 15,
            "The 9th house of Dharma is exceptionally strong from all SUDARSHANA perspectives (Lagna, Moon, Sun)."
        ))

    # Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Dharma Activation", "transit", "positive", 8, "Current cycles are activating key points related to your life purpose and soul path."))

    summary_template = domain_type + " alignment: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
