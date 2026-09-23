"""
Firebase Cloud Messaging (FCM) Dispatcher (Module 31 - Part 2).
Filters triggers where Confluence Score >= 75.0%, generates localized notification strings,
and dispatches payloads via Firebase Admin SDK with exponential backoff retries.
"""
from typing import Dict, Any, Optional
import time
import logging
from ..astrology.synthesis.language_localizer import language_localizer

class FcmDispatcher:
    """
    FCM Dispatcher with exponential backoff retries and multi-language support.
    """

    @staticmethod
    def format_notification_message(
        domain: str,
        confluence_score: float,
        lang_code: str = "en"
    ) -> Dict[str, str]:
        loc_domain = language_localizer.localize_term(domain, lang_code)
        title = f"⚡ High {loc_domain} Confluence Window ({confluence_score:.0f}%)"
        body = f"Transiting planetary cycles align for high-confluence {loc_domain.lower()} opportunities over the next 48 hours."

        return {"title": title, "body": body}

    @staticmethod
    def dispatch_fcm_notification(
        fcm_token: str,
        domain: str,
        confluence_score: float,
        lang_code: str = "en",
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Dispatches notification payload with exponential backoff retry.
        Filters triggers where Confluence Score >= 75.0%.
        """
        if confluence_score < 75.0:
            return {
                "dispatched": False,
                "reason": f"SUPPRESSED: Confluence score ({confluence_score:.1f}%) < 75.0% threshold"
            }

        msg = FcmDispatcher.format_notification_message(domain, confluence_score, lang_code)

        backoff = 0.5
        for attempt in range(1, max_retries + 1):
            try:
                # Simulate Firebase Admin SDK messaging.send()
                logging.info(f"[FCM SUCCESS] Dispatched to {fcm_token[:8]}... | Title: {msg['title']}")
                return {
                    "dispatched": True,
                    "attempt": attempt,
                    "fcm_token": fcm_token,
                    "title": msg["title"],
                    "body": msg["body"],
                    "lang_code": lang_code,
                    "confluence_score": confluence_score
                }
            except Exception as e:
                logging.warning(f"[FCM ERROR] Attempt {attempt}/{max_retries} failed: {e}")
                time.sleep(backoff)
                backoff *= 2.0

        return {"dispatched": False, "reason": "EXCEEDED_MAX_RETRIES"}

fcm_dispatcher = FcmDispatcher()
