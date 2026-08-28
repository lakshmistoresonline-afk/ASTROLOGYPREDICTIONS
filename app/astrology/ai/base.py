from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class AIProvider(ABC):
    """
    Base interface for all AI interpretation providers (Phase 46).
    Ensures the app can continue calculating facts if AI is unavailable.
    """

    @abstractmethod
    def explain_prediction(self, facts: Dict[str, Any]) -> str:
        """Translates deterministic astrological facts into natural language."""
        pass

    @abstractmethod
    def chat_consultation(self, user_msg: str, chart_context: Dict[str, Any]) -> str:
        """Handles context-aware user questions about their chart."""
        pass

    @abstractmethod
    def get_status(self) -> bool:
        """Returns True if the provider is reachable and active."""
        pass
