"""
Locust Production Load Test Script (Task 3).
Simulates 50+ concurrent POST /api/v1/report/generate requests with mixed chart payloads.
"""
from locust import HttpUser, task, between
import random

class AstroEngineLoadUser(HttpUser):
    wait_time = between(0.5, 2.0)

    # Mixed synthetic birth chart payloads
    TEST_PAYLOADS = [
        {"name": "Subramanian T S", "dob": "1986-09-28", "tob": "16:30", "latitude": 10.7867, "longitude": 76.6548, "timezone": "Asia/Kolkata"},
        {"name": "Polar Birth Sample", "dob": "1992-06-21", "tob": "00:05", "latitude": 64.1466, "longitude": -21.9426, "timezone": "Atlantic/Reykjavik"},
        {"name": "Southern Hemisphere", "dob": "1988-12-15", "tob": "08:45", "latitude": -33.8688, "longitude": 151.2093, "timezone": "Australia/Sydney"},
        {"name": "Equatorial Sample", "dob": "2000-01-01", "tob": "12:00", "latitude": 1.3521, "longitude": 103.8198, "timezone": "Asia/Singapore"},
    ]

    @task(3)
    def generate_report(self):
        payload = random.choice(self.TEST_PAYLOADS)
        headers = {"Content-Type": "application/json"}

        with self.client.post("/api/v1/report/generate", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 202:
                data = response.json()
                job_id = data.get("job_id")
                if job_id:
                    response.success()
                    # Poll status once
                    self.client.get(f"/api/v1/report/status/{job_id}", name="/api/v1/report/status/[job_id]")
                else:
                    response.failure("Missing job_id in response")
            else:
                response.failure(f"Failed with status code {response.status_code}")
