"""
Interactive Visual Component Adapter (Module 23 - Task 23.3).
Transforms raw Python analytical outputs into structured JSON component specs ready for React/Next.js/Tailwind rendering.
"""
from typing import Dict, Any, List

class UIComponentAdapter:
    """
    Formats backend AST payloads into frontend UI component specs.
    """

    @staticmethod
    def format_interactive_natal_wheel_spec(chart_obj: Any) -> Dict[str, Any]:
        """
        Formats Interactive Natal Wheel SVG/Canvas specification with planet glyphs, house cusps, and aspect lines.
        """
        planets = getattr(chart_obj, "planets", {})
        houses = getattr(chart_obj, "houses", [i*30.0 for i in range(12)])

        planet_glyphs = []
        for name, p in planets.items():
            planet_glyphs.append({
                "planet": name,
                "longitude": round(getattr(p, "longitude", 0.0), 2),
                "rashi": getattr(p, "rashi", 0),
                "degree_in_rashi": round(getattr(p, "degree", 0.0), 2),
                "house": getattr(p, "house", 1),
                "dignity": getattr(p, "dignity", "Neutral"),
                "is_retrograde": getattr(p, "is_retrograde", False)
            })

        return {
            "component": "InteractiveNatalWheel",
            "ascendant_longitude": round(getattr(chart_obj, "ascendant", 0.0), 2),
            "house_cusps": [round(c, 2) for c in houses[:12]],
            "planet_glyphs": planet_glyphs,
            "render_mode": "SVG_CANVAS_HYBRID"
        }

    @staticmethod
    def format_probability_trend_spec(probability_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Formats 365-Day Probability & Risk Time-Series spec for Chart.js / Recharts.
        """
        return {
            "component": "ProbabilityTrendChart",
            "total_days": len(probability_dataset),
            "time_series_data": probability_dataset,
            "series_keys": ["career_momentum", "financial_liquidity", "vitality_health", "relational_harmony", "relocation_mobility"]
        }

    @staticmethod
    def format_synastry_dual_ring_spec(matchmaking_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formats Synastry/Compatibility Dual Ring spec.
        """
        return {
            "component": "SynastryDualRing",
            "total_score": matchmaking_result.get("total_score", 0.0),
            "max_score": 36.0,
            "verdict": matchmaking_result.get("verdict", "Good"),
            "kutas": matchmaking_result.get("kutas", []),
            "manglik_analysis": matchmaking_result.get("manglik_analysis", {})
        }

ui_component_adapter = UIComponentAdapter()
