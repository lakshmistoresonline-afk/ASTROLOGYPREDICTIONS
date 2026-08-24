from typing import Dict, Any, List
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine
from ..core.varshaphala import get_varshaphala_data

def get_yearly_prediction(chart: CanonicalChart, target_year: int) -> DomainPrediction:
    """Yearly Forecast Analysis: Muntha, Varshaphala Chart, and Dasha."""
    factors = []

    # Muntha Analysis
    extra = get_varshaphala_data(chart.birth_datetime, chart.asc_rashi, target_year)
    muntha_house = extra["muntha_house"]

    factors.append(EvidenceEngine.create_factor(
        "Muntha Placement", "varshaphala", "positive" if muntha_house in [1, 9, 10, 11, 5, 2] else "negative", 15,
        f"Muntha (Yearly Point) is in House {muntha_house} for your {extra['age']}th year: {get_muntha_meaning(muntha_house)}"
    ))

    # General Theme based on Muntha Lord
    from ..core.houses import RASHI_LORDS
    muntha_lord = RASHI_LORDS[extra["muntha_rashi"]]
    p_info = chart.planets.get(muntha_lord)
    if p_info:
        factors.append(EvidenceEngine.create_factor(
            "Muntha Lord Status", "varshaphala", "positive" if p_info.house not in [6, 8, 12] else "negative", 10,
            f"Muntha Lord {muntha_lord} is in natal House {p_info.house}, directing the year's efforts toward that area."
        ))

    summary_template = f"Forecast for {target_year}: " + "{score}%. Confidence: {confidence}."

    return analyze_domain(
        f"Yearly Forecast ({target_year})",
        factors,
        summary_template,
        chart=chart
    )

def get_muntha_meaning(house: int) -> str:
    meanings = {
        1: "Personal growth, new beginnings, and high vitality.",
        2: "Financial gains, family focus, and wealth accumulation.",
        3: "Travel, courage, sibling support, and effective communication.",
        4: "Domestic happiness, property matters, and emotional peace.",
        5: "Creativity, children, education, and speculative gains.",
        6: "Overcoming challenges, focus on health, and competition.",
        7: "Partnerships, public deals, and relationship growth.",
        8: "Transformation, inheritance, and intense inner research.",
        9: "Higher wisdom, long travels, and divine support (luck).",
        10: "Career success, recognition, and social status.",
        11: "Fulfillment of desires, gains from friends, and networking.",
        12: "Detachment, foreign travels, or higher expenses."
    }
    return meanings.get(house, "General evolutionary phase.")
