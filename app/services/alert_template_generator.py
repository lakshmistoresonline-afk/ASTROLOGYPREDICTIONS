"""
Contextual Alert Template Generator (Module 12 - Task 12.2).
Generates concise, hyper-personalized push/email notification alert payloads.
"""
from typing import Dict, Any

class AlertTemplateGenerator:
    """
    Generates actionable notification payloads for FCM/APNs/Email delivery.
    """

    @staticmethod
    def generate_push_alert(
        domain: str,
        event_type: str,
        confluence_score: float,
        transiting_planet: str,
        target_house: int
    ) -> Dict[str, Any]:
        title = f"⚡ High {domain} Confluence Window ({confluence_score:.0f}%)"
        body = f"Transiting {transiting_planet} enters your House {target_house} Kakshya. Optimal window for strategic {event_type.lower().replace('_', ' ')} decisions."

        return {
            "title": title,
            "body": body,
            "data": {
                "domain": domain,
                "event_type": event_type,
                "confluence_score": confluence_score,
                "channel": "FCM_PUSH"
            }
        }

alert_template_generator = AlertTemplateGenerator()
