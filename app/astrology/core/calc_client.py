import requests
import os
from typing import Dict, Any, List, Optional

class CalculationClient:
    def __init__(self):
        self.base_url = os.getenv("CALC_SERVICE_URL", "http://127.0.0.1:8000")
        self.timeout = 30.0 # Increased for V3.22 performance
        self._cache = {}

    def get_natal_chart(self, year: int, month: int, day: int, hour: float, lat: float, lon: float, ayanamsa: str = "LAHIRI") -> Dict[str, Any]:
        cache_key = f"natal_{year}_{month}_{day}_{hour}_{lat}_{lon}_{ayanamsa}"
        if cache_key in self._cache: return self._cache[cache_key]

        url = f"{self.base_url}/v1/natal-chart"
        payload = {"year": year, "month": month, "day": day, "hour": hour, "lat": lat, "lon": lon, "ayanamsa": ayanamsa}
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            self._cache[cache_key] = data
            return data
        except Exception: raise RuntimeError("ASTROLOGY_CALCULATION_UNAVAILABLE")

    def get_transit_range(self, start: str, end: str, lat: float, lon: float) -> List[Dict[str, Any]]:
        cache_key = f"transit_{start}_{end}_{lat}_{lon}"
        if cache_key in self._cache: return self._cache[cache_key]

        url = f"{self.base_url}/v1/transits/range"
        payload = {"start_date": start, "end_date": end, "lat": lat, "lon": lon}
        try:
            resp = requests.post(url, json=payload, timeout=20.0)
            resp.raise_for_status()
            data = resp.json()
            self._cache[cache_key] = data
            return data
        except Exception: return []

    def get_sky_events(self, jd_ut: float, lat: float, lon: float) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/sky-events"
        payload = {"jd_ut": jd_ut, "lat": lat, "lon": lon}
        try:
            resp = requests.post(url, json=payload, timeout=5.0)
            resp.raise_for_status()
            return resp.json()
        except Exception: return {"sunrise_jd": None, "sunset_jd": None}

    def check_health(self) -> bool:
        try: return requests.get(f"{self.base_url}/health", timeout=2.0).status_code == 200
        except: return False

calc_client = CalculationClient()
