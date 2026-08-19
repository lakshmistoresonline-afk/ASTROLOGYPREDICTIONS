from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class NakshatraInfo(BaseModel):
    name: str
    index: int
    pada: int
    lord: str
    deity: Optional[str] = None
    symbol: Optional[str] = None

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
    shadbala_label: Optional[str] = None

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

    planets: Dict[str, PlanetInfo]
    houses: List[float] # Cusps
    house_lords: Dict[int, str]

    divisional_charts: Dict[str, Dict[str, int]] = {} # e.g., {"D9": {"Sun": 4, ...}}

    ashtakavarga: Dict[str, Any] = {}
    yogas: List[Dict[str, Any]] = []

    dasha_balance: Dict[str, Any] = {}
    current_periods: Dict[str, str] = {} # Maha, Antar, etc.

class PredictionFactor(BaseModel):
    factor: str
    type: str # house, lord, planet, yoga, dasha, transit, varga, ashtakavarga
    direction: str # positive, negative, neutral
    weight: float
    explanation: str

class DomainPrediction(BaseModel):
    domain: str
    score: float
    confidence: str # LOW, MEDIUM, HIGH
    summary: str
    positive_factors: List[PredictionFactor]
    negative_factors: List[PredictionFactor]
    contradictions: List[str]
    timing: List[Dict[str, Any]]
    recommendations: List[str]
