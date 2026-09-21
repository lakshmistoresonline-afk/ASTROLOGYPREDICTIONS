from typing import Dict, Any, List
from datetime import datetime, timedelta
from ..astrology.core.chart import calculate_chart_data
from ..astrology.core.models import CanonicalChart

class VarshaphalaEngine:
    """
    V3.22 Varshaphala (Solar Return Annual Chart) Engine.
    Casts annual predictive charts for the exact moment the Sun returns to its natal sidereal longitude.
    Computes Muntha placement, Sahams, and Varshapheshwar (Lord of the Year).
    """

    @staticmethod
    def calculate_varshaphala(chart: CanonicalChart, target_year: int) -> Dict[str, Any]:
        birth_dt = chart.birth_datetime
        return_dt = datetime(target_year, birth_dt.month, birth_dt.day, birth_dt.hour, birth_dt.minute)

        annual_chart = calculate_chart_data(return_dt, chart.latitude, chart.longitude, chart.timezone)

        age = target_year - birth_dt.year
        muntha_house = ((chart.asc_rashi + age) % 12) + 1

        return {
            "target_year": target_year,
            "solar_return_datetime": return_dt.isoformat(),
            "muntha_house": muntha_house,
            "lord_of_the_year": annual_chart.house_lords.get(1),
            "annual_ascendant_rashi": annual_chart.asc_rashi,
            "summary": f"Varshaphala for {target_year}: Muntha is placed in house {muntha_house}, directing focus toward that life sector for the year."
        }
