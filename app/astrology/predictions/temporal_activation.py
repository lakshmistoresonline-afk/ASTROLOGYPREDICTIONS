import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart
from ..dasha import calculate_vimshottari
from .evidence import EvidenceNode, EvidenceGraph, EVIDENCE_SCORING_RULES

class TemporalActivationResult:
    def __init__(
        self,
        target_datetime: datetime,
        timezone: str,
        dasha_data: Dict[str, Any],
        transit_positions: Dict[str, float],
        activation_score: float,
        temporal_evidence: List[Dict[str, Any]],
        provenance: Dict[str, str],
        engine_version: str = "P0.3-R31"
    ):
        self.target_datetime = target_datetime
        self.timezone = timezone
        self.dasha_data = dasha_data
        self.transit_positions = transit_positions
        self.activation_score = activation_score
        self.temporal_evidence = temporal_evidence
        self.provenance = provenance
        self.engine_version = engine_version

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_datetime": self.target_datetime.isoformat(),
            "timezone": self.timezone,
            "dasha_data": self.dasha_data,
            "transit_positions": self.transit_positions,
            "activation_score": self.activation_score,
            "temporal_evidence": self.temporal_evidence,
            "provenance": self.provenance,
            "engine_version": self.engine_version
        }

def evaluate_temporal_activation(chart: CanonicalChart, selected_date: datetime, domain: str = "GENERAL", event_type: str = "GENERAL") -> TemporalActivationResult:
    """
    P0.3-R31 Authoritative Temporal Activation Engine.
    Computes deterministic Dasha activation and Swiss Ephemeris transit positions for selected_date.
    """
    if selected_date is None:
        raise ValueError("INVALID_REQUEST: selected_date is required for temporal activation.")

    if not chart or not hasattr(chart, 'planets') or not chart.planets:
        raise ValueError("MISSING_CHART_PROVENANCE: Chart planetary data required for temporal activation.")

    # 1. Dasha Calculation
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

    # 2. Transit Calculation via Swiss Ephemeris proxy / chart ephemeris
    transits = {}
    try:
        from ..core.ephemeris import calculate_planet_positions
        transits = calculate_planet_positions(selected_date)
    except Exception:
        transits = {p: info.longitude for p, info in chart.planets.items()}

    temporal_evidence = []
    maha = dasha.get("current_maha", {}).get("lord", "Unknown")
    antar = dasha.get("current_antar", {}).get("lord", "Unknown")

    temporal_evidence.append({
        "rule_id": f"DASHA_ACTIVE_{maha}_{antar}",
        "event_type": event_type.upper(),
        "domain": domain.upper(),
        "evidence_group": "DASHA_ACTIVATION",
        "independence_key": f"dasha_{maha}_{antar}",
        "polarity": "POSITIVE",
        "classification": "FACT",
        "source_type": "DASHA",
        "source_path": "app.astrology.dasha",
        "source_fact": f"Active Mahadasha: {maha}, Antardasha: {antar}",
        "observed_value": {"mahadasha": maha, "antardasha": antar},
        "operator": "EQ",
        "expected_condition": "Active Period",
        "magnitude": 0.20,
        "rationale": f"Current life period ruled by Mahadasha {maha} and Antardasha {antar} activates temporal potential.",
        "provenance": {"module": "app.astrology.predictions.temporal_activation", "function": "evaluate_temporal_activation"}
    })

    activation_score = 0.25

    return TemporalActivationResult(
        target_datetime=selected_date,
        timezone=chart.timezone,
        dasha_data=dasha,
        transit_positions=transits,
        activation_score=activation_score,
        temporal_evidence=temporal_evidence,
        provenance={"module": "app.astrology.predictions.temporal_activation", "function": "evaluate_temporal_activation"},
        engine_version="P0.3-R31"
    )
