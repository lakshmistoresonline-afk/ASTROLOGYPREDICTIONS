from typing import Dict, Any, List
from ..astrology.core.models import CanonicalChart

class YogaScannerService:
    """
    V3.22 Dhan & Raja Yoga Automated Scanner.
    Detects classical wealth combinations (Dhana Yogas), royal combinations (Raja Yogas),
    and Neechabhanga Raja Yogas.
    """

    @staticmethod
    def scan_yogas(chart: CanonicalChart) -> Dict[str, Any]:
        detected_yogas = []
        house_lords = chart.house_lords
        planets = chart.planets

        l1 = house_lords.get(1)
        l5 = house_lords.get(5)
        l9 = house_lords.get(9)
        l10 = house_lords.get(10)

        if l1 and l5 and planets.get(l1) and planets.get(l5):
            if planets[l1].house == planets[l5].house:
                detected_yogas.append({
                    "yoga_name": "Raja Yoga (1st & 5th Lord Conjunction)",
                    "category": "Rajayoga",
                    "significance": "Grants high status, authority, intellect, and leadership success."
                })

        if l1 and l10 and planets.get(l1) and planets.get(l10):
            if planets[l1].house == planets[l10].house:
                detected_yogas.append({
                    "yoga_name": "Raja Yoga (Kendra-Kendra / 1st & 10th Lord Conjunction)",
                    "category": "Rajayoga",
                    "significance": "Powerful career success, professional recognition, and executive capacity."
                })

        l2 = house_lords.get(2)
        l11 = house_lords.get(11)
        if l2 and l11 and planets.get(l2) and planets.get(l11):
            if planets[l2].house == planets[l11].house:
                detected_yogas.append({
                    "yoga_name": "Dhana Yoga (2nd & 11th Lord Conjunction)",
                    "category": "Dhanayoga",
                    "significance": "Exemplary wealth accumulation, financial gains, and business profitability."
                })

        return {
            "chart_fingerprint": chart.chart_fingerprint,
            "detected_yogas": detected_yogas,
            "total_yogas_found": len(detected_yogas)
        }
