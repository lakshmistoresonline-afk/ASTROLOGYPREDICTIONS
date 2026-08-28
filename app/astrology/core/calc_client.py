import requests
import os
from typing import Dict, Any, List, Optional

class CalculationClient:
    def __init__(self):
        self.base_url = os.getenv("CALC_SERVICE_URL", "http://localhost:8000")
        self.timeout = 10.0

    def get_natal_chart(self, year: int, month: int, day: int, hour: float, lat: float, lon: float, ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        url = f"{self.base_url}/v1/natal-chart"
        payload = {"year": year, "month": month, "day": day, "hour": hour, "lat": lat, "lon": lon, "ayanamsa": ayanamsa}
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception: raise RuntimeError("ASTROLOGY_CALCULATION_UNAVAILABLE")

    def get_transit_range(self, start: str, end: str, lat: float, lon: float) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/v1/transits/range"
        payload = {"start_date": start, "end_date": end, "lat": lat, "lon": lon}
        try:
            resp = requests.post(url, json=payload, timeout=20.0)
            resp.raise_for_status()
            return resp.json()
        except Exception: return []

    def check_health(self) -> bool:
        try: return requests.get(f"{self.base_url}/health", timeout=2.0).status_code == 200
        except: return False

calc_client = CalculationClient()
