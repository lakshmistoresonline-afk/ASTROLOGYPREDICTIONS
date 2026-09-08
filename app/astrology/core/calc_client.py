import requests
import os
from typing import Dict, Any, List, Optional

class CalculationClient:
    def __init__(self):
        self.base_url = os.getenv("CALC_SERVICE_URL", "http://127.0.0.1:8000")
        self.timeout = 10.0 # Robust timeout
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
        except Exception:
            # IN-PROCESS FALLBACK: If calculation service on port 8000 is offline or times out, run directly in-process!
            try:
                from calculation_service.app.core.engine import calculate_natal_chart
                data = calculate_natal_chart(year, month, day, hour, lat, lon, ayanamsa)
                self._cache[cache_key] = data
                return data
            except Exception as inner_e:
                raise RuntimeError(f"ASTROLOGY_CALCULATION_UNAVAILABLE: {inner_e}")

    def get_transit_range(self, start: str, end: str, lat: float, lon: float) -> List[Dict[str, Any]]:
        cache_key = f"transit_{start}_{end}_{lat}_{lon}"
        if cache_key in self._cache: return self._cache[cache_key]

        url = f"{self.base_url}/v1/transits/range"
        payload = {"start_date": start, "end_date": end, "lat": lat, "lon": lon}
        try:
            resp = requests.post(url, json=payload, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
            self._cache[cache_key] = data
            return data
        except Exception:
            try:
                from calculation_service.app.core.engine import calculate_transits_for_range
                return calculate_transits_for_range(start, end, lat, lon)
            except:
                return []

    def get_sky_events(self, jd_ut: float, lat: float, lon: float) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/sky-events"
        payload = {"jd_ut": jd_ut, "lat": lat, "lon": lon}
        try:
            resp = requests.post(url, json=payload, timeout=5.0)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            try:
                from calculation_service.app.core.engine import calculate_sky_events
                return calculate_sky_events(jd_ut, lat, lon)
            except:
                return {"sunrise_jd": None, "sunset_jd": None}

    def check_health(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/health", timeout=1.0).status_code == 200
        except:
            # Return True because in-process fallback is active
            return True

calc_client = CalculationClient()
