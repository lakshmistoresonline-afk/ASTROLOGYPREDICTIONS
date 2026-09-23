"""
Dynamic System Prompt Matrix & Persona Router (Module 3 - Task 3.1).
Matches domain context tags to domain-specific narrative personas to eliminate repetitive prose.
"""
from typing import Dict, Any

DOMAIN_PERSONA_PROMPTS = {
    "EXECUTIVE": """You are an Executive Astrological Analyst specializing in Corporate Strategy, Financial Risk, and Career Trajectories.
Your tone is risk-adjusted, quantitative, precise, and executive-focused. Avoid vague spiritual metaphors. Focus on institutional power, market positioning, revenue timing, and strategic execution.""",

    "PSYCHOLOGICAL": """You are a Depth Psychological Astrologer specializing in Core Identity, Mind Structures, and Evolutionary Shifts.
Your tone is introspective, analytical, strategically deep, and self-actualizing. Focus on internal motivations, mental resilience, identity evolution, and cognitive patterns.""",

    "RELATIONAL": """You are an Interpersonal Dynamics Systems Specialist.
Your tone is empathetic, systems-oriented, clear-bordered, and constructive. Focus on interpersonal communication, shared long-term values, emotional maturity, and mutual boundaries.""",

    "REMEDIAL": """You are a Behavioral Remediation & Habit Optimization Specialist.
Your tone is practical, non-superstitious, actionable, and habit-forming. Focus on psychological self-discipline, routine optimization, and practical behavioral alignment."""
}

DOMAIN_CATEGORY_MAP = {
    "Career": "EXECUTIVE",
    "Career & Authority": "EXECUTIVE",
    "Finance": "EXECUTIVE",
    "Finance & Wealth": "EXECUTIVE",
    "Wealth & Finance": "EXECUTIVE",
    "Business": "EXECUTIVE",
    "Business & Enterprise": "EXECUTIVE",
    "Fame": "EXECUTIVE",
    "Fame & Reputation": "EXECUTIVE",

    "Personality": "PSYCHOLOGICAL",
    "Personality & Essence": "PSYCHOLOGICAL",
    "Spirituality": "PSYCHOLOGICAL",
    "Spirituality & Inner Growth": "PSYCHOLOGICAL",
    "Education": "PSYCHOLOGICAL",
    "Education & Knowledge": "PSYCHOLOGICAL",

    "Marriage": "RELATIONAL",
    "Marriage & Relationships": "RELATIONAL",
    "Family": "RELATIONAL",
    "Family & Roots": "RELATIONAL",
    "Children": "RELATIONAL",
    "Children & Creativity": "RELATIONAL",

    "Health": "REMEDIAL",
    "Health & Vitality": "REMEDIAL",
    "Property": "EXECUTIVE",
    "Property & Assets": "EXECUTIVE",
    "Travel": "PSYCHOLOGICAL",
    "Travel & Horizons": "PSYCHOLOGICAL",
    "Foreign": "EXECUTIVE",
    "Foreign Settlement": "EXECUTIVE",
    "Legal": "EXECUTIVE",
    "Legal & Disputes": "EXECUTIVE",
    "Vehicles": "EXECUTIVE",
    "Vehicles & Mobility": "EXECUTIVE"
}

class SystemPromptRouter:
    """
    Matches domain tags to specialized system prompt personas.
    """

    @staticmethod
    def get_system_prompt(domain: str) -> str:
        persona_key = DOMAIN_CATEGORY_MAP.get(domain, "PSYCHOLOGICAL")
        return DOMAIN_PERSONA_PROMPTS.get(persona_key, DOMAIN_PERSONA_PROMPTS["PSYCHOLOGICAL"])

    @staticmethod
    def get_persona_type(domain: str) -> str:
        return DOMAIN_CATEGORY_MAP.get(domain, "PSYCHOLOGICAL")

system_prompt_router = SystemPromptRouter()
