from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

class NakshatraInfo(BaseModel):
    name: str
    index: int
    pada: int
    lord: str
    deity: Optional[str] = None
    symbol: Optional[str] = None
    gana: Optional[str] = None
    yoni: Optional[str] = None
    nadi: Optional[int] = None # 0=Adi, 1=Madhya, 2=Antya
    degree_range: Optional[tuple] = None # (start, end)

class PlanetInfo(BaseModel):
    name: str
    longitude: float
    latitude: float
    speed: float
    is_retrograde: bool
    is_combust: bool
    rashi: int
    degree: float
    house: int
    dignity: str
    nakshatra: NakshatraInfo
    dispositor: str
    functional_status: Optional[str] = None
    shadbala_score: Optional[float] = None
    baladi_avastha: Optional[str] = None
    deeptadi_avastha: Optional[str] = None
    navamsa_rashi: Optional[int] = None

class CanonicalChart(BaseModel):
    birth_datetime: datetime
    timezone: str
    latitude: float
    longitude: float
    ayanamsa: float
    ayanamsa_name: str = "Lahiri"
    house_system: str = "Whole Sign"

    ascendant: float
    asc_rashi: int
    asc_nakshatra: NakshatraInfo

    birth_time_confidence: str = "HIGH"

    planets: Dict[str, PlanetInfo]
    houses: List[float] # Cusps
    house_lords: Dict[int, str]

    calculation_config: Optional[Dict[str, Any]] = None
    calculation_provenance: Optional[Dict[str, Any]] = None
    chart_fingerprint: Optional[str] = None
    calculation_config_fingerprint: Optional[str] = None

    divisional_charts: Dict[str, Dict[str, int]] = {}

    ashtakavarga: Dict[str, Any] = {}
    yogas: List[Dict[str, Any]] = []

    jaimini_karakas: Dict[str, str] = {}
    special_lagnas: Dict[str, float] = {}
    arudha_padas: Dict[str, int] = {}
    yogi_details: Dict[str, str] = {}
    rashi_drishti: Dict[int, List[int]] = {}
    karakamsha_swamsha: Dict[str, Any] = {}

    chara_dasha: Any = {}
    kalachakra_dasha: Dict[str, Any] = {}
    shattrimsha_dasha: Dict[str, Any] = {}
    pindayu: Dict[str, float] = {}

class CorroborationEvidence(BaseModel):
    source: str # NATAL_PROMISE, DASHA_ACTIVATION, etc.
    level: str = "PRIMARY" # PRIMARY, SECONDARY, MITIGATING
    planet_involved: Optional[str] = None
    house_involved: Optional[int] = None
    strength_score: float # Weighted impact
    description: str
    rationale: Optional[str] = None # Technical explanation

    # V3.22 Independence Layer
    evidence_type: str = "SUPPORTING" # INDEPENDENT, SHARED_TRIGGER, DERIVED, CONFLICT
    source_layer: str = "NATAL" # NATAL, DASHA, TRANSIT, VARGA
    independence_group: Optional[str] = None # e.g. "Mars-Trigger"

class DomainPrediction(BaseModel):
    domain: str
    headline: str = ""
    score: float # Confluence Score
    quality_score: float = 0.0 # V3 Quality Metric
    confidence: str # VERY STRONG, STRONG, etc.
    prediction_strength: str
    event_type: Optional[str] = None
    event_magnitude: Optional[str] = "MODERATE"
    what_may_develop: Optional[str] = None # V3.15 Event Class
    summary: str
    manifestations: List[str] = [] # How it appears in life
    confirmation_criteria: List[str] = [] # Specific success markers
    supporting_factors: List[str] = []
    contradicting_factors: List[str] = []
    validation_status: str = "PRELIMINARY"

    # IMMUTABLE SNAPSHOT (V2.0.0)
    version_snapshot: Dict[str, str] = {
        "calculation": "CALC-SWE-2.10.3",
        "engine": "PREDICT-V2-CONFLUENCE",
        "dasha": "DASHA-VIM-365.2425",
        "evidence": "EVIDENCE-HIERARCHY-9L"
    }

    evidence_chain: List[CorroborationEvidence] = []

    timing_window: Dict[str, Any] = {
        "phase": "SCANNING", # BUILD_UP, PEAK_ACTIVE, DECLINE
        "activation": None,
        "build": None,
        "peak": None,
        "manifestation": None,
        "decline": None,
        "description": "",
        "timing_confidence": "LOW"
    }

    remedies: List[Dict[str, Any]] = []
    practical_actions: List[str] = [] # Actionable steps
    limitations: Optional[str] = None

class TimelineEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    profile_id: Optional[str] = None
    domain: str
    event_type: str
    event_magnitude: str # LOW, MODERATE, SIGNIFICANT, MAJOR

    start_date: str
    peak_date: str
    end_date: str

    age_at_start: float
    age_at_peak: float
    age_at_end: float

    signal_strength: str
    confidence: str
    timing_precision: str = "MODERATE" # NARROW, MODERATE, BROAD

    evidence_count: int = 0
    independent_evidence_count: int = 0
    conflict_count: int = 0

    status: str # PAST_RECONSTRUCTION, PRESENT_ACTIVE, FUTURE_FORECAST, VERIFIED_OUTCOME
    provenance: str = "GENERATED"
    engine_version: str = "V3.17"

    evidence_summary: str
    why_now: Optional[str] = None
    evidence_chain: List[CorroborationEvidence] = []
    conflicts: List[str] = []

    # Validation Fields
    actual_event_date: Optional[str] = None
    matching_status: str = "UNKNOWN" # MATCH, PARTIAL_MATCH, NO_MATCH, UNKNOWN
    timing_error_days: Optional[int] = None

class LifeTimeline(BaseModel):
    profile_id: str
    birth_datetime: datetime
    events: List[TimelineEvent] = []
    phases: List[Dict[str, Any]] = [] # V3.16 Phases
    generated_at: datetime = Field(default_factory=datetime.now)
    engine_version: str = "V3.17"
