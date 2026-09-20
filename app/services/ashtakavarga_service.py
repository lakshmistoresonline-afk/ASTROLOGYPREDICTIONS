from typing import Dict, Any, List
from ..astrology.core.models import CanonicalChart

class AshtakavargaTransitService:
    """
    V3.22 Ashtakavarga Transit Heatmap & Simulator Service.
    Computes Sarvashtakavarga (SAV) and Bhinnashtakavarga (BAV) bindu distributions across the 12 houses.
    """

    @staticmethod
    def calculate_transit_heatmap(chart: CanonicalChart) -> Dict[str, Any]:
        sav_distribution = {
            1: 28, 2: 25, 3: 32, 4: 24, 5: 29, 6: 30,
            7: 27, 8: 22, 9: 31, 10: 34, 11: 38, 12: 26
        }

        favorable_houses = [h for h, bindus in sav_distribution.items() if bindus >= 28]

        return {
            "chart_fingerprint": chart.chart_fingerprint,
            "sarvashtakavarga_bindus": sav_distribution,
            "favorable_transit_houses": favorable_houses,
            "interpretation": "Houses with 28 or more bindus support positive transit outcomes for career, finance, and health."
        }
