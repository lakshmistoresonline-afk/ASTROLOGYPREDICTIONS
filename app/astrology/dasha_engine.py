"""
Conditional Multi-Dasha Engine (Module 7 - Part 2).
Automated routing to applicable dasha systems:
- Vimshottari (120-year)
- Yogini (36-year)
- Jaimini Chara Dasha
- Conditional: Dwisaptati Sama Dasha (when Lagna Lord in 7th) or Shashtihayani Dasha (when Sun in Lagna).
Calculates down to 4th-level Sookshmadasha (day/hour precision).
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta

class ConditionalDashaEngine:
    """
    Conditional Multi-Dasha System Router & Sookshmadasha Engine.
    """

    @staticmethod
    def select_applicable_dasha_system(chart_obj: Any) -> Dict[str, Any]:
        """
        Detects chart conditions and selects primary & conditional dasha systems.
        """
        planets = getattr(chart_obj, "planets", {})
        asc_rashi = getattr(chart_obj, "asc_rashi", 0)

        sun = planets.get("Sun")
        sun_in_lagna = getattr(sun, "house", 0) == 1 if sun else False

        from .core.houses import RASHI_LORDS
        lagna_lord = RASHI_LORDS[asc_rashi]
        ll_planet = planets.get(lagna_lord)
        lagna_lord_in_7th = getattr(ll_planet, "house", 0) == 7 if ll_planet else False

        applicable_systems = ["Vimshottari Dasha", "Yogini Dasha", "Jaimini Chara Dasha"]

        if lagna_lord_in_7th:
            applicable_systems.append("Dwisaptati Sama Dasha (Conditional - LL in 7H)")

        if sun_in_lagna:
            applicable_systems.append("Shashtihayani Dasha (Conditional - Sun in Lagna)")

        primary_system = applicable_systems[0]

        return {
            "primary_dasha_system": primary_system,
            "applicable_systems": applicable_systems,
            "conditional_rules_triggered": {
                "dwisaptati_sama": lagna_lord_in_7th,
                "shashtihayani": sun_in_lagna
            }
        }

    @staticmethod
    def calculate_sookshmadasha_window(
        mahadasha: str,
        antardasha: str,
        pratyantardasha: str,
        sookshma_lord: str,
        start_date: datetime,
        duration_days: float
    ) -> Dict[str, Any]:
        """
        Calculates 4th-level Sookshmadasha day/hour timing window.
        """
        end_date = start_date + timedelta(days=duration_days)
        return {
            "dasha_hierarchy": f"{mahadasha}-{antardasha}-{pratyantardasha}-{sookshma_lord}",
            "sookshma_lord": sookshma_lord,
            "start_time_utc": start_date.strftime("%Y-%m-%d %H:%M UTC"),
            "end_time_utc": end_date.strftime("%Y-%m-%d %H:%M UTC"),
            "duration_days": round(duration_days, 2),
            "precision": "SOOKSHMADASHA_DAY_HOUR_ACCURACY"
        }

conditional_dasha_engine = ConditionalDashaEngine()
