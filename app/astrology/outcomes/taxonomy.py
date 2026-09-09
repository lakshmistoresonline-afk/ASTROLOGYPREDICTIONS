from typing import Dict, Any, Optional

CANONICAL_EVENT_TAXONOMY: Dict[str, list] = {
    "CAREER": ["job_start", "job_change", "promotion", "major_role_change", "business_start", "business_expansion", "business_failure"],
    "FINANCE": ["major_gain", "major_loss", "investment_event", "property_purchase", "property_sale"],
    "RELATIONSHIP": ["marriage", "engagement", "separation", "divorce", "major_relationship_start"],
    "FAMILY": ["child_birth", "major_family_event"],
    "HEALTH": ["major_health_event", "hospitalization", "surgery"],
    "EDUCATION": ["admission", "graduation", "major_exam"],
    "RELOCATION": ["relocation", "foreign_move", "long_distance_move"],
    "LEGAL": ["major_legal_event"],
    "OTHER_MAJOR_LIFE_EVENT": []
}

EVENT_ALIASES: Dict[str, str] = {
    "job_begin": "job_start",
    "new_job": "job_change",
    "wedding": "marriage",
    "baby_born": "child_birth",
    "moved": "relocation",
    "lawsuit": "major_legal_event"
}

def normalize_event_type(raw_event: str) -> str:
    """
    Maps raw or alias event strings into the canonical event taxonomy.
    """
    raw_clean = raw_event.strip().lower().replace(" ", "_")
    if raw_clean in EVENT_ALIASES:
        raw_clean = EVENT_ALIASES[raw_clean]

    for domain, events in CANONICAL_EVENT_TAXONOMY.items():
        if raw_clean in events:
            return raw_clean

    return "other_major_life_event"
