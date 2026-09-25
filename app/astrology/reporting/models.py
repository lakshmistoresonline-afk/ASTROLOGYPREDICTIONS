from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class NativeProfile:
    name: str
    birth_dob: str
    birth_tob: str
    birth_place: str
    latitude: float
    longitude: float
    timezone: str
    confidence: str = "HIGH"

@dataclass
class CalculationProvenance:
    engine_version: str = "V3.36 Authoritative"
    calculation_core: str = "CALC-SWE-2.10.3"
    ayanamsa: str = "Lahiri Sidereal"
    house_system: str = "Placidus / Whole Sign Hybrid"
    coordinates_type: str = "Topocentric True"
    chart_fingerprint: str = ""
    report_fingerprint: str = ""
    calculation_timestamp: str = ""

@dataclass
class PlanetaryPosition:
    name: str
    symbol: str
    longitude: float
    sign_name: str
    sign_degree: float
    house: int
    nakshatra: str
    pada: int
    is_retrograde: bool
    is_combust: bool = False
    shadbala_score: float = 300.0
    vimsopaka_score: float = 12.0
    dignity: str = "Neutral"

@dataclass
class HouseCusp:
    house: int
    longitude: float
    rashi_name: str

@dataclass
class VargaPlacement:
    planet: str
    d1_sign: str
    d9_sign: str
    d10_sign: str

@dataclass
class YogaRecord:
    name: str
    definition: str
    is_active: bool
    strength: str
    participating_planets: List[str] = field(default_factory=list)

@dataclass
class DashaPeriod:
    lord: str
    start_date: str
    end_date: str
    level: str = "Mahadasha"

@dataclass
class DomainPrediction:
    domain: str
    event_type: str
    confluence_score: float
    prediction_strength: str
    peak_date: str
    summary: str
    supporting_factors: List[str] = field(default_factory=list)

@dataclass
class TimelineEvent:
    peak_date: str
    domain: str
    event_type: str
    age_at_peak: int
    magnitude: str

@dataclass
class RemedyProtocol:
    planet: str
    remedy_type: str
    instructions: str
    rationale: str

@dataclass
class CanonicalAstrologyReport:
    report_id: str
    schema_version: str
    created_at: str
    profile: NativeProfile
    provenance: CalculationProvenance
    planets: List[PlanetaryPosition] = field(default_factory=list)
    house_cusps: List[HouseCusp] = field(default_factory=list)
    varga_placements: List[VargaPlacement] = field(default_factory=list)
    yogas: List[YogaRecord] = field(default_factory=list)
    dashas: List[DashaPeriod] = field(default_factory=list)
    predictions: List[DomainPrediction] = field(default_factory=list)
    timeline: List[TimelineEvent] = field(default_factory=list)
    remedies: List[RemedyProtocol] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
