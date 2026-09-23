"""
Webhook Notification Engine (Task 4).
Delivers 'report.completed' or 'report.failed' event payloads to client-registered endpoints with exponential retries.
"""
from typing import Dict, Any, Optional
import requests
import time
import logging

class WebhookDispatcher:
    """
    Reliable Webhook Dispatcher delivering report events with exponential backoff retries (3 attempts).
    """

    @staticmethod
    def dispatch_webhook(
        webhook_url: str,
        event_type: str,
        job_id: str,
        payload: Dict[str, Any],
        max_retries: int = 3
    ) -> bool:
        event_body = {
            "event": event_type, # 'report.completed' or 'report.failed'
            "job_id": job_id,
            "timestamp": time.time(),
            "data": payload
        }

        backoff = 0.5
        for attempt in range(1, max_retries + 1):
            try:
                res = requests.post(webhook_url, json=event_body, timeout=5.0)
                if res.status_code in [200, 201, 202, 204]:
                    logging.info(f"[WEBHOOK] Successfully dispatched '{event_type}' for job {job_id} to {webhook_url}")
                    return True
                logging.warning(f"[WEBHOOK] Delivery attempt {attempt}/{max_retries} returned status {res.status_code}")
            except Exception as e:
                logging.warning(f"[WEBHOOK] Delivery attempt {attempt}/{max_retries} error: {e}")

            if attempt < max_retries:
                time.sleep(backoff)
                backoff *= 2.0

        logging.error(f"[WEBHOOK FAILED] Failed to deliver webhook '{event_type}' for job {job_id} after {max_retries} retries")
        return False

webhook_dispatcher = WebhookDispatcher()
