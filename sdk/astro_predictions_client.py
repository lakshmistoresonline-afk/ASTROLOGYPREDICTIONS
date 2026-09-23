"""
Astro Predictions Python Client SDK (Task 4).
Lightweight SDK wrapper for API authentication, async report generation, status polling, and payload fetching.
"""
from typing import Dict, Any, Optional
import requests
import time

class AstroPredictionsClient:
    """
    Python SDK Client for Astro Predictions API (V3.36).
    """

    def __init__(self, base_url: str = "http://localhost:5000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def generate_report(self, name: str, dob: str, tob: str, latitude: float, longitude: float, timezone: str = "Asia/Kolkata") -> str:
        """Triggers asynchronous report generation and returns job_id."""
        url = f"{self.base_url}/api/v1/report/generate"
        payload = {
            "name": name,
            "dob": dob,
            "tob": tob,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone
        }
        res = self.session.post(url, json=payload, timeout=10.0)
        res.raise_for_status()
        return res.json().get("job_id")

    def get_status(self, job_id: str) -> Dict[str, Any]:
        """Polls current job execution status."""
        url = f"{self.base_url}/api/v1/report/status/{job_id}"
        res = self.session.get(url, timeout=5.0)
        res.raise_for_status()
        return res.json()

    def fetch_report(self, job_id: str) -> Dict[str, Any]:
        """Fetches final completed report payload."""
        url = f"{self.base_url}/api/v1/report/fetch/{job_id}"
        res = self.session.get(url, timeout=10.0)
        res.raise_for_status()
        return res.json().get("payload", {})

    def generate_and_poll(self, name: str, dob: str, tob: str, latitude: float, longitude: float, timezone: str = "Asia/Kolkata", poll_interval: float = 1.0, timeout_sec: float = 30.0) -> Dict[str, Any]:
        """Convenience method: triggers report generation, polls until complete, and returns report payload."""
        job_id = self.generate_report(name, dob, tob, latitude, longitude, timezone)
        start_time = time.time()

        while time.time() - start_time < timeout_sec:
            status_data = self.get_status(job_id)
            state = status_data.get("status")

            if state == "COMPLETED":
                return self.fetch_report(job_id)
            elif state == "FAILED":
                raise RuntimeError(f"Report generation failed for job {job_id}: {status_data.get('error')}")

            time.sleep(poll_interval)

        raise TimeoutError(f"Report generation job {job_id} timed out after {timeout_sec} seconds")
