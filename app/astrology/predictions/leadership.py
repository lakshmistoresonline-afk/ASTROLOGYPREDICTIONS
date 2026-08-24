from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_leadership_prediction(chart: CanonicalChart, domain_type: str = "Leadership", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Leadership & Authority Analysis: 1st, 5th, 9th, 10th houses and Sun, Mars."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 10th HOUSE (AUTHORITY)
    l10_name = house_lords[10]
    l10 = planets[l10_name]
    if "Exalted" in l10.dignity or l10.dignity == "Own Sign":
        factors.append(EvidenceEngine.create_factor("10th Lord Strength", "lord", "positive", 15, "Strong 10th Lord indicates natural command, authority, and public recognition."))

    # 2. SUN (POWER)
    sun = planets["Sun"]
    if sun.house in [1, 10, 11]:
        factors.append(EvidenceEngine.create_factor("Sun Placement", "planet", "positive", 10, "Sun in a powerful house creates charisma and leadership potential."))

    # 3. MARS (COURAGE)
    mars = planets["Mars"]
    if "Exalted" in mars.dignity:
        factors.append(EvidenceEngine.create_factor("Mars Strength", "planet", "positive", 10, "Exalted Mars provides exceptional courage and administrative power."))

    # Varga Confirmation
    v_conf = False
    if "D10" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Dashamsha (D10) analysis confirms strong leadership and command capabilities."))

    # 3b. Advanced Leadership Indicators
    # A. Ghati Lagna (GL) - Indicator of Power/Command
    gl_lon = chart.special_lagnas.get("Ghati Lagna")
    if gl_lon is not None:
        gl_rashi = int(gl_lon // 30)
        # Check if Sun or Mars sitting in GL
        for p_name, p_info in planets.items():
            if p_info.rashi == gl_rashi and p_name in ["Sun", "Mars"]:
                factors.append(EvidenceEngine.create_factor(
                    "Command Seat", "planet", "positive", 20,
                    f"{p_name} sits on your Ghati Lagna, indicating a natural seat of power and administrative dominance."
                ))

    # B. KP House 10 Significators
    h10_sigs = chart.kp_significators.get(10, {})
    if "Sun" in (h10_sigs.get("A", []) + h10_sigs.get("B", [])):
        factors.append(EvidenceEngine.create_factor(
            "KP Authority Support", "planet", "positive", 15,
            "KP System identifies the Sun as a primary significator for your 10th house, boosting leadership potential."
        ))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Leadership Activation", "transit", "positive", 8, "Current planetary cycles favor assumption of responsibility and display of leadership."))

    summary_template = domain_type + " potential: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
