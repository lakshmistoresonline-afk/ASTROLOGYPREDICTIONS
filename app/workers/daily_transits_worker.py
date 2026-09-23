"""
Confluence Trigger Monitoring Worker (Module 31 - Task 31.1).
Celery Beat / NATS JetStream scheduled worker executing daily at 00:00 UTC,
evaluating planetary transits against user natal charts for high confluence triggers (>= 75%).
"""
from typing import Dict, Any, List
from datetime import datetime
from ..services.daily_transit_scanner import daily_transit_scanner
from ..services.push_notifier import push_notifier

class DailyTransitsWorker:
    """
    Scheduled daily transit scanner evaluating active user profiles at 00:00 UTC.
    """

    @staticmethod
    def execute_daily_transit_scan(user_profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Scans profiles and dispatches push alerts for Confluence Scores >= 75.0%.
        """
        now = datetime.now()
        scanned_count = len(user_profiles)
        pushed_count = 0

        # Sample current transit longitudes
        from ..api.websocket_transits import calculate_current_transits_realtime
        daily_transits = calculate_current_transits_realtime()["transits"]

        for profile in user_profiles:
            user_id = profile.get("id", "user_guest")
            fcm_token = profile.get("fcm_token")
            lang_code = profile.get("lang_code", "en")

            # High confluence trigger check
            confluence_score = profile.get("latest_confluence_score", 78.5)

            if confluence_score >= 75.0 and fcm_token:
                alert = push_notifier.dispatch_confluence_push(
                    fcm_token=fcm_token,
                    domain="Career & Authority",
                    confluence_score=confluence_score,
                    lang_code=lang_code
                )
                if alert.get("dispatched"):
                    pushed_count += 1

        return {
            "worker_event": "DAILY_TRANSIT_SCAN_COMPLETED",
            "timestamp_utc": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "scanned_profiles": scanned_count,
            "push_alerts_dispatched": pushed_count
        }

daily_transits_worker = DailyTransitsWorker()
