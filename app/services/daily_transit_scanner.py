"""
Daily Transit Scanner & Event Trigger Daemon (Module 12 - Task 12.1).
Scans daily planetary transits against user birth charts at 00:00 UTC and dispatches proactive alert payloads.
"""
from typing import Dict, Any, List
from datetime import datetime
from ..astrology.timing.kakshya import kakshya_evaluator
from ..services.alert_template_generator import alert_template_generator
from ..services.webhook_dispatcher import webhook_dispatcher

class DailyTransitScanner:
    """
    Background worker evaluating daily transit coordinates against user charts.
    """

    @staticmethod
    def scan_user_chart_for_daily_alerts(
        user_id: str,
        chart_obj: Any,
        daily_transits: Dict[str, float],
        webhook_url: str = None
    ) -> List[Dict[str, Any]]:
        alerts = []
        bav_matrix = getattr(chart_obj, "ashtakavarga", {}).get("BAV", {})
        natal_rashis = {n: getattr(p, "rashi", 0) for n, p in getattr(chart_obj, "planets", {}).items()}

        for p_name, t_lon in daily_transits.items():
            if p_name in ["Sun", "Mars", "Mercury", "Venus", "Jupiter", "Saturn"]:
                k_eval = kakshya_evaluator.evaluate_transit_kakshya(p_name, t_lon, bav_matrix, natal_rashis)
                if k_eval["activation_status"] == "HIGH_ACTIVATION":
                    target_house = (k_eval["rashi"] - getattr(chart_obj, "asc_rashi", 0) + 12) % 12 + 1
                    alert_payload = alert_template_generator.generate_push_alert(
                        domain="Career & Authority" if target_house == 10 else "Wealth & Finance" if target_house in [2, 11] else "General Strategy",
                        event_type="HIGH_ACTIVATION_TRANSIT",
                        confluence_score=88.0,
                        transiting_planet=p_name,
                        target_house=target_house
                    )
                    alerts.append(alert_payload)

                    if webhook_url:
                        webhook_dispatcher.dispatch_webhook(
                            webhook_url=webhook_url,
                            event_type="report.alert",
                            job_id=f"alert-{user_id}",
                            payload=alert_payload
                        )

        return alerts

daily_transit_scanner = DailyTransitScanner()
