from datetime import datetime
from typing import Dict, Any, List

class V10TransitNotifier:
    """
    V10.0 Real-Time Planetary Transit Webhook & Notification Engine with deterministic calculation.
    """
    def __init__(self):
        self.version = "V10.0-PROD"

    def check_transit_triggers(self, chart_obj, current_date: datetime) -> List[Dict[str, Any]]:
        alerts = []
        if not chart_obj or not hasattr(chart_obj, 'planets') or not chart_obj.planets:
            return alerts

        for p_name, p_data in chart_obj.planets.items():
            if p_name in ["Jupiter", "Saturn", "Rahu"]:
                is_retro = getattr(p_data, 'is_retrograde', False)
                house = getattr(p_data, 'house', 1)
                alerts.append({
                    "alert_id": f"tr_{p_name.lower()}_h{house}",
                    "planet": p_name,
                    "event_type": "transit_activation",
                    "description": f"{p_name} transits House {house} (Retrograde: {is_retro}) - Active activation window.",
                    "severity": "HIGH" if p_name in ["Jupiter", "Saturn"] else "MODERATE",
                    "timestamp": current_date.isoformat(),
                    "engine_version": self.version
                })
        return alerts

v10_transit_notifier = V10TransitNotifier()
