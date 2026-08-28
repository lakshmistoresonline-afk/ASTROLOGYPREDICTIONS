from typing import Dict, Any, List
from .shadbala import calculate_shadbala

class DetailedStrengthEngine:
    """
    Provides a deterministic and transparent breakdown of planetary strength (Phase 10).
    Converts Shadbala Virupas into human-readable evidence.
    """

    @staticmethod
    def get_strength_report(chart_data: Dict[str, Any], is_day: bool, is_shukla: bool, wd_lord: str, hora_lord: str) -> Dict[str, Any]:
        raw_shadbala = calculate_shadbala(chart_data, is_day, is_shukla, wd_lord, hora_lord)

        report = {}
        for p, metrics in raw_shadbala.items():
            total = metrics["total_rupas"]
            label = "STRONG" if total >= 7.0 else "MODERATE" if total >= 5.0 else "WEAK"

            # Identify primary source of strength
            factors = []
            if metrics["dig_bala"] >= 45: factors.append("Excellent Directional Strength (Dig Bala)")
            if metrics["sthana_bala"] >= 120: factors.append("Strong Positional Strength (Sthana Bala)")
            if metrics["cheshta_bala"] >= 50: factors.append("Powerful Movement (Cheshta Bala)")
            if metrics["kala_bala"] >= 200: factors.append("Temporal Dominance (Kala Bala)")

            report[p] = {
                "score": total,
                "label": label,
                "transparent_factors": factors,
                "breakdown": metrics
            }
        return report

strength_engine = DetailedStrengthEngine()
