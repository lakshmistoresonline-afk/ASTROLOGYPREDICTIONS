import os
from .ollama import LocalAIProvider
from .base import AIProvider

def get_active_provider() -> AIProvider:
    """
    Factory to return the selected AI provider based on ENV.
    Defaults to Local/Offline mode.
    """
    provider_type = os.getenv("AI_PROVIDER", "LOCAL").upper()

    if provider_type == "OPENAI":
        # Placeholder for OpenAIProvider
        return LocalAIProvider()
    elif provider_type == "GEMINI":
        # Placeholder for GeminiProvider
        return LocalAIProvider()
    else:
        return LocalAIProvider()

# Global instance
ai_engine = get_active_provider()
