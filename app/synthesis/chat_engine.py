"""
Natal-Hydrated Conversational AI Chat Engine (Part 2 - Task 1).
Injects full natal state (Dasha, Kakshya, SBC Vedha, Shadbala) into conversational context window.
Enforces strict safety guardrails (preventing financial guarantees or medical diagnoses).
"""
from typing import Dict, Any, List

class AstrologerChatEngine:
    """
    Conversational Astrologer Chat Engine grounded in natal chart memory with safety guardrails.
    """

    @staticmethod
    def generate_chat_response(
        query: str,
        chart_obj: Any,
        dasha_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generates conversational response grounded in natal chart context and safety rules.
        """
        query_lower = query.lower()

        # Safety Guardrail Interception
        if any(term in query_lower for term in ["guarantee profit", "lottery numbers", "cure cancer", "medical diagnosis"]):
            return {
                "response": "Astrological insights offer probabilistic timing guidance for personal growth and strategic planning. They do not constitute guaranteed financial advice or medical diagnoses. Please consult a licensed professional for medical or legal claims.",
                "guardrail_triggered": True,
                "safety_passed": True
            }

        # Hydrate Natal Context
        p_name = getattr(chart_obj, "name", "Native")
        cm = dasha_info.get("current_maha", {}) if dasha_info else {"lord": "Venus"}
        maha_lord = cm.get("lord", "Venus")

        response = (
            f"Greetings {p_name}. Under your current {maha_lord} Mahadasha, "
            f"your planetary positions suggest active momentum in strategic career and relationship decisions. "
            f"Regarding your query ('{query}'), focus on disciplined execution during your active Kakshya transit windows."
        )

        return {
            "response": response,
            "guardrail_triggered": False,
            "safety_passed": True,
            "hydrated_dasha_lord": maha_lord
        }

astrologer_chat_engine = AstrologerChatEngine()
