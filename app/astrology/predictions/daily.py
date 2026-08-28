from typing import Dict, Any, List
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import CorroborationEngine
from ..dasha import calculate_vimshottari

def get_daily_forecast(chart: CanonicalChart, target_date: datetime) -> Dict[str, Any]:
    """
    Personalized Daily Forecast (Phase 35).
    Synthesizes Dasha, Transit Moon, and House Activation.
    """
    # 1. Current Dasha Context
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
    antar_lord = dasha.get("current_antar", {}).get("lord", "Unknown")

    # 2. Transit Moon Position (Fact-based)
    from ..core.calc_client import calc_client
    transit_facts = calc_client.get_natal_chart(
        target_date.year, target_date.month, target_date.day,
        target_date.hour + target_date.minute/60.0,
        chart.latitude, chart.longitude
    )
    moon_transit_rashi = int(transit_facts["planets"]["Moon"]["longitude"] // 30)

    # 3. Personal Theme
    # Theme is driven by the Antardasha Lord's House ownership and placement
    antar_p = chart.planets.get(antar_lord)
    house_activated = antar_p.house if antar_p else 1

    themes = {
        1: "Personal growth and physical vitality.",
        2: "Financial stability and family matters.",
        3: "Communication, courage, and short journeys.",
        4: "Emotional peace, home, and property.",
        5: "Intelligence, creativity, and children.",
        6: "Daily routine, health, and overcoming hurdles.",
        7: "Partnerships, public dealings, and relationships.",
        8: "Deep transformation and research.",
        9: "Higher wisdom, philosophy, and long journeys.",
        10: "Professional authority and career focus.",
        11: "Social gains and achievement of goals.",
        12: "Introspection, expenditures, and spiritual depth."
    }

    strongest_theme = themes.get(house_activated, "General life balance.")

    return {
        "date": target_date.strftime("%Y-%m-%d"),
        "strongest_theme": strongest_theme,
        "current_dasha": f"{dasha.get('current_maha', {}).get('lord')} - {antar_lord}",
        "opportunities": [f"Activation of House {house_activated} favors focusing on {strongest_theme.lower()}"],
        "caution": "Avoid impulsive decisions in matters unrelated to your current support cycle.",
        "recommended_remedy": f"Traditional {antar_lord}-oriented practice to align with current activation."
    }
