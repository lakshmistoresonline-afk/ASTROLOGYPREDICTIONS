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
    gana: Optional[str] = None
    yoni: Optional[str] = None
    nadi: Optional[int] = None # 0=Adi, 1=Madhya, 2=Antya
    degree_range: Optional[tuple] = None # (start, end)

class KPInfo(BaseModel):
    star_lord: str
    sub_lord: str
    sub_sub_lord: Optional[str] = None
    step4_lord: Optional[str] = None # Star Lord of Sub Lord

class ShadbalaInfo(BaseModel):
    sthana_bala: float
    dig_bala: float
    kala_bala: float
    naisargika_bala: float
    total_shadbala: float
    total_rupas: float

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
    directional_strength: Optional[float] = None
    is_in_planetary_war: bool = False
    is_in_moolatrikona: bool = False
    shadbala_score: Optional[float] = None

    # --- PLANETARY STATES ---
    baladi_avastha: Optional[str] = None
    lajjitadi_avastha: List[str] = []
    shayanadi_avastha: Optional[str] = None
    deeptadi_avastha: Optional[str] = None
    vaisheshikamsha: Optional[str] = None
    pushkar_navamsha: bool = False
    nadi_amsha: Optional[Any] = None
    avastha_weight: float = 1.0 # 0.0 to 2.0 based on state

    shadbala_label: Optional[str] = None
    shadbala_details: Optional[ShadbalaInfo] = None
    kp_details: Optional[KPInfo] = None
    vimsopaka_score: Optional[float] = None
    ishta_phala: Optional[float] = None
    kashta_phala: Optional[float] = None
    is_vargottama: bool = False
    navamsa_rashi: Optional[int] = None
    nakshatra_lord_rel: Optional[str] = None # Relationship with Nakshatra Lord
    dispositor_rel: Optional[str] = None # Relationship with Sign Lord

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

    bhava_chalit: Dict[int, List[str]] = {} # House -> [Planets]
    kp_cusps: List[float] = [] # Placidus cusps
    jaimini_karakas: Dict[str, str] = {} # Karaka Name -> Planet Name
    karakamsha_swamsha: Dict[str, Any] = {}
    dasha_balance: Dict[str, Any] = {}
    current_periods: Dict[str, str] = {} # Maha, Antar, etc.
    bhava_bala: Dict[int, float] = {} # House -> Strength Score
    aspect_insights: List[Dict[str, Any]] = [] # Detailed planetary aspects

    # --- ADVANCED JYOTISH DATA ---
    special_lagnas: Dict[str, float] = {} # HL, GL, SL, VL, Indu Lagna, etc.
    arudha_padas: Dict[str, int] = {}    # AL, A2-A12 (Rashi index)
    yogi_details: Dict[str, str] = {}    # Yogi, Avayogi, Saha Yogi planets
    jaimini_aspects: Dict[int, List[int]] = {} # Rashi -> [Aspecting Rashis]
    argala_analysis: Dict[int, Dict[str, List[Any]]] = {} # House -> {"primary": [], "obstructing": []}
    vimsopaka_total: float = 0.0
    panchapakshi: Dict[str, str] = {}    # Bird, Activity, Timing
    dagtha_rashis: List[int] = []        # Burnt signs based on Tithi
    ishta_kashta_totals: Dict[str, float] = {}

    # --- COSMIC REFINEMENT DATA ---
    tajika_yogas: List[Dict[str, Any]] = []
    sahams: Dict[str, float] = []
    nadi_connections: Dict[str, List[str]] = {}
    sbc_vedha: List[Dict[str, Any]] = []
    rashi_drishti: Dict[int, List[int]] = {}

    # --- ESOTERIC & CONDITIONAL DATA ---
    sudarshana_chakra: Dict[int, Dict[str, Any]] = {}
    sensitive_points: Dict[str, Any] = {}
    conditional_dashas: List[str] = []
    khanda_analysis: Dict[str, List[int]] = {}

    # --- YEARLY & SYSTEMIC PRECISION ---
    varsheshwar: str = "" # Year Lord
    kp_significators: Dict[int, Dict[str, List[str]]] = {} # House -> A, B, C, D
    kp_4_steps: Dict[str, Dict[str, List[int]]] = {}
    gandanta_alerts: List[Dict[str, Any]] = []
    panchapakshi_segment: int = 0
    bcp_activation: Dict[str, Any] = {}

    # --- SUPREME ACCURACY DATA ---
    kalachakra_dasha: Dict[str, Any] = {}
    shree_lagna: float = 0.0
    varnada_lagna: Dict[int, int] = {} # House -> Rashi
    chara_dasha: Any = {}
    pindayu: Dict[str, float] = {}
    shattrimsha_dasha: Dict[str, Any] = {}
    visha_amrit_ghati: Dict[str, List[str]] = {}
    dagdha_tithis: List[int] = []
    additional_sahams: Dict[str, float] = {}
    ishta_kashta_detailed: Dict[str, Dict[str, float]] = {}
    transit_vedha: Dict[str, List[str]] = {}
    nadi_signatures: List[Dict[str, Any]] = []
    bhrigu_bindu: float = 0.0
    bhrigu_insights: List[str] = []
    fixed_star_conjunctions: List[Dict[str, Any]] = []
    western_aspects: List[Dict[str, Any]] = []
    special_points: Dict[str, float] = {} # MC, Vertex, East Point, etc.
    mundane_indicators: Dict[str, Any] = {}
    numerology: Dict[str, Any] = {}
    biorhythms: Dict[str, float] = {}
    asteroids: Dict[str, Any] = {}
    sabian_symbols: Dict[str, str] = {}
    upcoming_eclipses: List[Dict[str, Any]] = []
    eclipse_impacts: List[Dict[str, Any]] = []
    extended_sahams: Dict[str, float] = {}
    heliocentric_positions: Dict[str, float] = {}
    harmonic_charts: Dict[int, Dict[str, float]] = {}
    harmonic_resonances: List[str] = []
    financial_indicators: Dict[str, Any] = {}
    weather_indicators: Dict[str, Any] = {}
    bazi_pillars: Dict[str, Any] = {}
    uranian_tnps: Dict[str, Any] = {}
    maya_tzolkin: Dict[str, Any] = {}
    mahabote: Dict[str, Any] = {}
    tibetan_data: Dict[str, Any] = {}
    celtic_tree: Dict[str, Any] = {}
    firdaria: List[Dict[str, Any]] = []
    native_american: Dict[str, str] = {}
    kabbalah: List[str] = []
    human_design: Dict[str, Any] = {}
    hellenistic_lots: Dict[str, float] = {}
    annual_profection: int = 0
    gene_keys: List[Dict[str, Any]] = []
    egyptian_bounds: Dict[str, str] = {}
    zodiacal_releasing: Dict[str, List[Dict[str, Any]]] = {}
    uranian_formulas: Dict[str, float] = {}
    astrocartography: Dict[str, Any] = {}
    secondary_progressions: Dict[str, float] = {}
    solar_arc_directions: Dict[str, float] = {}
    draconic_chart: Dict[str, float] = {}
    lal_kitab_year_data: Dict[str, Any] = {}
    galactic_aspects: List[Dict[str, Any]] = []
    zi_wei_dou_shu: Dict[str, Any] = {}
    lilith: Dict[str, Any] = {}
    geomancy: Dict[str, Any] = {}

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
    evidence: List[str] = []
    positive_factors: List[PredictionFactor] = []
    negative_factors: List[PredictionFactor] = []
    contradictions: List[str] = []
    timing: List[Dict[str, Any]] = []
    recommendations: List[str] = []
    remedies: List[Dict[str, str]] = []
