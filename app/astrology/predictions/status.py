from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_status_prediction(chart: CanonicalChart, domain_type: str = "Social Status", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Social Status & Public Reputation Analysis."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 10th House (Status)
    l10_name = house_lords[10]
    l10 = planets[l10_name]
    factors.append(EvidenceEngine.create_factor("Status Lord", "lord", "positive" if l10.house not in [6, 8, 12] else "negative", 15, f"10th Lord {l10_name} in House {l10.house} defines your public reputation."))

    # 2. Sun (Karaka for Status)
    sun = planets["Sun"]
    if "Exalted" in sun.dignity:
        factors.append(EvidenceEngine.create_factor("Sun Strength", "planet", "positive", 12, "Exalted Sun brings high social standing and recognition."))

    # Varga Confirmation
    v_conf = False
    if "D10" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Dashamsha (D10) analysis confirms high social and public standing."))

    # 2b. Advanced Reputation Indicators
    # A. Arudha Lagna (AL) - Exterior Status
    al_rashi = chart.arudha_padas.get("AL")
    if al_rashi is not None:
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Social Perception", "yoga", "positive", 15,
            f"Arudha Lagna in {RASHI_NAMES[al_rashi]} defines how society views your accomplishments and power."
        ))

    # B. Amatyakaraka (AmK)
    amk_name = chart.jaimini_karakas.get("Amatyakaraka (AmK) - Career/Mind")
    if amk_name:
        amk = planets[amk_name]
        factors.append(EvidenceEngine.create_factor(
            "Command Potential", "planet", "positive" if amk.house in [1, 4, 7, 10] else "neutral", 10,
            f"{amk_name} (Amatyakaraka) strength defines your ability to influence others and maintain status."
        ))

    # 3. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Visibility Period", "transit", "positive", 8, "Current cycles enhance your public visibility and social standing."))

    summary_template = "Public reputation and social status strength: {score}%. Confidence: {confidence}."
    return analyze_domain("Social Status", factors, summary_template, varga_data={"confirmed": v_conf}, transit_data={"confirmed": t_conf}, chart=chart)
