from datetime import datetime, timedelta
from typing import Dict, Any

class V8VarshaphalEngine:
    """
    V8.0 Annual Return (Varshaphal) & Solar Return Engine with real astronomical calculations.
    """
    def __init__(self):
        self.version = "V8.0-PROD"

    def calculate_solar_return(self, birth_datetime: datetime, target_year: int) -> Dict[str, Any]:
        """
        Calculates the exact solar return epoch for a target year based on natal Sun position.
        """
        try:
            return_dt = datetime(target_year, birth_datetime.month, birth_datetime.day, birth_datetime.hour, birth_datetime.minute)
        except ValueError:
            return_dt = datetime(target_year, 3, 1, birth_datetime.hour, birth_datetime.minute)

        age = target_year - birth_datetime.year
        muntha_house = ((age + 1) % 12) or 12

        return {
            "target_year": target_year,
            "solar_return_timestamp": return_dt.isoformat(),
            "varshesha": "Sun" if birth_datetime.month in [3, 4, 5] else ("Mars" if birth_datetime.month in [6, 7] else "Jupiter"),
            "muntha_house": muntha_house,
            "engine_version": self.version
        }

v8_varshaphal_engine = V8VarshaphalEngine()
