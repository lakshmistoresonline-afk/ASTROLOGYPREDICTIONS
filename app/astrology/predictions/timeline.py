from typing import List, Dict, Any
from datetime import datetime, timedelta
from ..core.models import CanonicalChart
from ..timing.engine import get_timing_score

def get_life_timeline(chart: CanonicalChart) -> List[Dict[str, Any]]:
    """Generate a horizontal life timeline with peak activation events."""
    from ..dasha import calculate_vimshottari

    moon_lon = chart.planets["Moon"].longitude
    dasha_data = calculate_vimshottari(moon_lon, chart.birth_datetime)

    all_mahas = dasha_data.get("mahadashas", [])
    timeline = []

    # 1. Current Context
    now = datetime.now()

    # 2. Key life domains to monitor for events
    domains = {
        "Career": (["Saturn", "Sun", chart.house_lords[10]], [10, 6, 11]),
        "Wealth": (["Jupiter", chart.house_lords[2], chart.house_lords[11]], [2, 11]),
        "Marriage": (["Venus", "Jupiter", chart.house_lords[7]], [7, 5]),
        "Foreign": (["Rahu", chart.house_lords[12]], [12, 9])
    }

    for m in all_mahas:
        lord = m["lord"]

        # Determine core mahadasha theme
        theme = _get_lord_theme(lord)

        # Check for specific "peaks" within the mahadasha (Simplified for 3-year sub-cycles)
        # In a real engine, we'd check every Antardasha.

        events = []
        for d_name, (planets, houses) in domains.items():
             # Check mahadasha lord support
             if lord in planets:
                  events.append(f"{d_name} Activation")

        timeline.append({
            "period": f"{lord} Cycle",
            "start": m["start"].strftime("%Y"),
            "end": m["end"].strftime("%Y"),
            "theme": theme,
            "status": "Active" if m["start"] <= now <= m["end"] else "Past" if m["end"] < now else "Upcoming",
            "lord": lord,
            "events": events,
            "color": _get_planet_color(lord)
        })

    return timeline

def get_current_micro_timing(chart: CanonicalChart) -> Dict[str, Any]:
    """Calculate the active Sookshma and Prana periods for 'Right Now' accuracy."""
    from ..dasha.vimshottari import calculate_dasha_balance, get_vimshottari_periods

    moon_lon = chart.planets["Moon"].longitude
    mahadashas = get_vimshottari_periods(moon_lon, chart.birth_datetime)

    now = datetime.now()

    current = {"Maha": "", "Antar": "", "Praty": "", "Sookshma": "", "Prana": ""}

    for m in mahadashas:
        if m["start"] <= now <= m["end"]:
            current["Maha"] = m["lord"]
            for a in m["antardashas"]:
                if a["start"] <= now <= a["end"]:
                    current["Antar"] = a["lord"]
                    for p in a["pratyantardashas"]:
                        if p["start"] <= now <= p["end"]:
                            current["Praty"] = p["lord"]
                            for s in p["sookshma"]:
                                if s["start"] <= now <= s["end"]:
                                    current["Sookshma"] = s["lord"]
                                    for pr in s.get("prana", []):
                                        if pr["start"] <= now <= pr["end"]:
                                            current["Prana"] = pr["lord"]
                                            break
    return current

def _get_lord_theme(lord: str) -> str:
    themes = {
        "Sun": "Authority & Self-Expression",
        "Moon": "Emotional Growth & Domesticity",
        "Mars": "Action, Courage & Conflict",
        "Mercury": "Intellect, Skill & Commerce",
        "Jupiter": "Expansion, Wisdom & Prosperity",
        "Venus": "Harmony, Arts & Relationships",
        "Saturn": "Discipline, Structure & Endurance",
        "Rahu": "Ambition & Unconventional Paths",
        "Ketu": "Spirituality & Introspection"
    }
    return themes.get(lord, "General Evolutionary Phase")

def _get_planet_color(p: str) -> str:
    colors = {
        "Sun": "#FF6B35", "Moon": "#C8D8E8", "Mars": "#FF4444",
        "Mercury": "#00CC88", "Jupiter": "#FFD700", "Venus": "#FF69B4",
        "Saturn": "#9CA3AF", "Rahu": "#8B5CF6", "Ketu": "#EC4899"
    }
    return colors.get(p, "#FFFFFF")
