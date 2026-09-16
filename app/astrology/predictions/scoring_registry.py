SCORING_REGISTRY_VERSION = "P0.3-R40"

SCORING_RULES = {
    "R40-KARAKA-STRONG": {"magnitude": 0.25, "evidence_group": "SIGNIFICATOR_STRENGTH", "version": "R40"},
    "R40-KARAKA-WEAK": {"magnitude": -0.25, "evidence_group": "SIGNIFICATOR_STRENGTH", "version": "R40"},
    "R40-KARAKA-COMBUST": {"magnitude": -0.20, "evidence_group": "PLANETARY_CONDITION", "version": "R40"},
    "R40-LORD-STRONG": {"magnitude": 0.25, "evidence_group": "LORD_PLACEMENT", "version": "R40"},
    "R40-LORD-WEAK": {"magnitude": -0.20, "evidence_group": "LORD_PLACEMENT", "version": "R40"},
    "R40-HOUSE-OCCUPANCY": {"magnitude": 0.15, "evidence_group": "HOUSE_STRUCTURE", "version": "R40"},
    "R40-YOGA-SUPPORT": {"magnitude": 0.15, "evidence_group": "YOGA_SUPPORT", "version": "R40"},
    "R40-VARGA-CONFIRMATION": {"magnitude": 0.15, "evidence_group": "DIVISIONAL_CONFIRMATION", "version": "R40"},
    "R40-DASHA-ACTIVATION": {"magnitude": 0.15, "evidence_group": "DASHA_ACTIVATION", "version": "R40"},
    "R40-TRANSIT-ASPECT": {"magnitude": 0.15, "evidence_group": "TRANSIT_ACTIVATION", "version": "R40"},
    "R40-SHADBALA-FACTUAL": {"magnitude": 0.0, "evidence_group": "SHADBALA_MODIFIER", "version": "R40"}
}
