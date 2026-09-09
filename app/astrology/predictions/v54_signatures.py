from typing import Dict, Any, List

EVENT_SIGNATURE_LIBRARY: Dict[str, Dict[str, Any]] = {
    "promotion": {
        "domain": "CAREER",
        "primary_houses": [10, 1, 6],
        "primary_significators": ["Sun", "Saturn", "Mars"],
        "topical_vargas": ["D1", "D10"],
        "specificity_threshold": 0.75,
        "allowed_precision": "MONTH"
    },
    "property_purchase": {
        "domain": "PROPERTY",
        "primary_houses": [4, 2, 11],
        "primary_significators": ["Mars", "Venus", "Moon"],
        "topical_vargas": ["D1", "D4"],
        "specificity_threshold": 0.80,
        "allowed_precision": "MONTH"
    },
    "marriage": {
        "domain": "MARRIAGE",
        "primary_houses": [7, 2, 11],
        "primary_significators": ["Venus", "Jupiter"],
        "topical_vargas": ["D1", "D9"],
        "specificity_threshold": 0.80,
        "allowed_precision": "MONTH"
    }
}

def get_event_signature(event_type: str) -> Dict[str, Any]:
    return EVENT_SIGNATURE_LIBRARY.get(event_type, {
        "domain": "GENERAL",
        "primary_houses": [1],
        "primary_significators": ["Sun"],
        "topical_vargas": ["D1"],
        "specificity_threshold": 0.50,
        "allowed_precision": "YEAR"
    })
