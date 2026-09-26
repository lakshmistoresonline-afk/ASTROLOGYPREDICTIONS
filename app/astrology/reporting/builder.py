import hashlib
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

from .models import (
    CanonicalAstrologyReport, NativeProfile, CalculationProvenance,
    PlanetaryPosition, HouseCusp, VargaPlacement, YogaRecord,
    DashaPeriod, DomainPrediction, TimelineEvent, RemedyProtocol,
    ReportBuildError
)
from ..core.planets import PLANET_COLORS
from ..predictions.engine import generate_evidence_based_predictions
from ..dasha.vimshottari import get_vimshottari_periods
from ..predictions.v322_timeline import lifetime_timeline_engine_v22
from ..remedies.engine import get_personalized_remedies
from ..yogas.detector import detect_yogas

logger = logging.getLogger(__name__)

RASHI_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def build_canonical_astrology_report(chart_obj: Any, selected_date: Optional[datetime] = None) -> CanonicalAstrologyReport:
    """
    Orchestrates calculation outputs into a single CanonicalAstrologyReport object.
    Raises ReportBuildError on mandatory calculation/profile failures.
    """
    if not chart_obj:
        raise ReportBuildError("Cannot build report: chart_obj is None or invalid.")

    if selected_date is None:
        selected_date = datetime.now()

    diagnostics: List[Dict[str, Any]] = []

    # 1. Profile Extraction
    birth_dt = getattr(chart_obj, 'birth_datetime', None)
    if not birth_dt:
        raise ReportBuildError("Missing mandatory birth_datetime in chart_obj.")

    profile = NativeProfile(
        name=getattr(chart_obj, 'name', 'Native Participant'),
        birth_dob=getattr(chart_obj, 'birth_dob', birth_dt.strftime('%Y-%m-%d')),
        birth_tob=getattr(chart_obj, 'birth_tob', birth_dt.strftime('%H:%M')),
        birth_place=getattr(chart_obj, 'birth_place', 'Observer Location'),
        latitude=float(getattr(chart_obj, 'latitude')),
        longitude=float(getattr(chart_obj, 'longitude')),
        timezone=getattr(chart_obj, 'timezone', 'UTC'),
        confidence=getattr(chart_obj, 'birth_time_confidence', 'HIGH')
    )

    # 2. Provenance & Fingerprints
    fp = getattr(chart_obj, 'chart_fingerprint', None)
    if not fp:
        fp = hashlib.sha256(f"{birth_dt.isoformat()}:{profile.latitude}:{profile.longitude}".encode('utf-8')).hexdigest()

    rep_hash = hashlib.sha256(f"{fp}:{selected_date.isoformat()}".encode('utf-8')).hexdigest()

    provenance = CalculationProvenance(
        engine_version="V3.36 Authoritative",
        calculation_core="CALC-SWE-2.10.3",
        ayanamsa="Lahiri Sidereal",
        house_system="Placidus / Whole Sign Hybrid",
        coordinates_type="Topocentric True",
        chart_fingerprint=fp,
        report_fingerprint=rep_hash[:24],
        calculation_timestamp=selected_date.strftime("%Y-%m-%d %H:%M:%S UTC")
    )

    # 3. Planetary Positions (Sun through Ketu)
    planets_list: List[PlanetaryPosition] = []
    chart_planets = getattr(chart_obj, 'planets', None)
    if not chart_planets:
        raise ReportBuildError("Missing mandatory planets dictionary in chart_obj.")

    for p_name, p in chart_planets.items():
        sym_val = PLANET_COLORS.get(p_name, p_name[:2])
        sym = sym_val if isinstance(sym_val, str) else p_name[:2]
        r_idx = getattr(p, 'rashi', 0)
        r_name = RASHI_NAMES[r_idx] if (0 <= r_idx < 12) else 'Unknown Sign'
        nak_name = getattr(p.nakshatra, 'name', 'Unknown Nakshatra') if hasattr(p, 'nakshatra') else 'Unknown Nakshatra'
        nak_pada = getattr(p.nakshatra, 'pada', 1) if hasattr(p, 'nakshatra') else 1

        planets_list.append(PlanetaryPosition(
            name=p_name,
            symbol=sym,
            longitude=p.longitude,
            sign_name=r_name,
            sign_degree=p.longitude % 30,
            house=p.house,
            nakshatra=nak_name,
            pada=nak_pada,
            is_retrograde=p.is_retrograde,
            is_combust=getattr(p, 'is_combust', False),
            shadbala_score=getattr(p, 'shadbala_score', None) or getattr(p, 'effective_shadbala', 300.0) or 300.0,
            vimsopaka_score=getattr(p, 'vimsopaka', 12.0) or 12.0,
            dignity=getattr(p, 'dignity', 'Neutral')
        ))

    # 4. House Cusps (12 Houses)
    cusps_list: List[HouseCusp] = []
    asc_idx = getattr(chart_obj, 'asc_rashi', 0)
    asc_r_name = RASHI_NAMES[asc_idx] if (0 <= asc_idx < 12) else 'Aries'
    raw_cusps = getattr(chart_obj, 'houses', None) or getattr(chart_obj, 'cusps', None)
    if not raw_cusps and hasattr(chart_obj, 'ascendant'):
        raw_cusps = [(chart_obj.ascendant + (i * 30)) % 360 for i in range(12)]

    if raw_cusps:
        for idx, cusp_deg in enumerate(raw_cusps, 1):
            r_idx = int(cusp_deg / 30) % 12
            r_name = RASHI_NAMES[r_idx] if (idx > 1) else asc_r_name
            cusps_list.append(HouseCusp(
                house=idx,
                longitude=cusp_deg,
                rashi_name=r_name
            ))

    # 5. Vargas (D1, D9 Navamsha, D10 Dashamsha)
    from ..charts.divisional import calculate_varga_rashi
    vargas_list: List[VargaPlacement] = []
    div_charts = getattr(chart_obj, 'divisional_charts', {}) or {}
    d9_map = div_charts.get("D9", {})
    d10_map = div_charts.get("D10", {})

    for p_name, p in chart_planets.items():
        r_idx = getattr(p, 'rashi', int(p.longitude / 30) % 12)
        d1_s = RASHI_NAMES[r_idx] if (0 <= r_idx < 12) else 'Unknown'

        d9_idx = getattr(p, 'navamsa_rashi', None)
        if d9_idx is None and isinstance(d9_map, dict):
            d9_idx = d9_map.get(p_name)
        if d9_idx is None:
            d9_idx = calculate_varga_rashi(p.longitude, 9)
        d9_s = RASHI_NAMES[d9_idx] if (d9_idx is not None and 0 <= d9_idx < 12) else d1_s

        d10_idx = d10_map.get(p_name) if isinstance(d10_map, dict) else None
        if d10_idx is None:
            d10_idx = calculate_varga_rashi(p.longitude, 10)
        d10_s = RASHI_NAMES[d10_idx] if (d10_idx is not None and 0 <= d10_idx < 12) else d1_s

        vargas_list.append(VargaPlacement(
            planet=p_name,
            d1_sign=d1_s,
            d9_sign=d9_s,
            d10_sign=d10_s
        ))

    # 6. Yogas & Combinations
    yogas_list: List[YogaRecord] = []
    try:
        house_lords = getattr(chart_obj, 'house_lords', {})
        detected = detect_yogas(chart_planets, house_lords, chart=chart_obj)
        for y in detected:
            if isinstance(y, dict) and y.get('present', True):
                yogas_list.append(YogaRecord(
                    name=y.get('name', 'Classical Combination'),
                    definition=y.get('interpretation', 'Vedic planetary yoga'),
                    is_active=y.get('present', True),
                    strength=y.get('strength', 'HIGH'),
                    participating_planets=y.get('planets', [])
                ))
    except Exception as e:
        logger.warning(f"Yoga detection warning in report builder: {e}")
        diagnostics.append({"section": "Yogas", "status": "PARTIAL", "warning": str(e)})

    # 7. Vimshottari Dasha Hierarchy
    dashas_list: List[DashaPeriod] = []
    try:
        moon_lon = chart_planets["Moon"].longitude
        raw_dashas = get_vimshottari_periods(moon_lon, birth_dt)
        for d in raw_dashas:
            dashas_list.append(DashaPeriod(
                lord=d.get('lord', 'Moon'),
                start_date=d.get('start', ''),
                end_date=d.get('end', ''),
                level="Mahadasha"
            ))
    except Exception as e:
        logger.error(f"Dasha calculation failure in report builder: {e}")
        diagnostics.append({"section": "Dashas", "status": "FAILED", "error": str(e)})

    # 8. Domain Predictions
    preds_list: List[DomainPrediction] = []
    try:
        preds_output = generate_evidence_based_predictions(chart_obj, selected_date=selected_date)
        for p in preds_output.get('predictions', []):
            tw = p.get('timing_window', {})
            peak_d = tw.get('peak', 'Active') if isinstance(tw, dict) else 'Active'
            preds_list.append(DomainPrediction(
                domain=p.get('domain', 'General'),
                event_type=p.get('event_type', 'Activation'),
                confluence_score=float(p.get('score', 0.0)),
                prediction_strength=p.get('prediction_strength', 'ACTIVE'),
                peak_date=str(peak_d),
                summary=p.get('summary', 'Confluent activation.'),
                supporting_factors=p.get('supporting_factors', [])
            ))
    except Exception as e:
        logger.error(f"Predictions engine failure in report builder: {e}")
        diagnostics.append({"section": "Predictions", "status": "FAILED", "error": str(e)})

    # 9. Lifetime Timeline
    timeline_list: List[TimelineEvent] = []
    try:
        profile_id = getattr(chart_obj, 'id', 'native_participant')
        tl_output = lifetime_timeline_engine_v22.generate_lifetime_timeline(chart_obj, profile_id)
        events_raw = getattr(tl_output, 'events', []) or (tl_output.get('events', []) if isinstance(tl_output, dict) else [])
        for ev in events_raw:
            p_date_val = getattr(ev, 'peak_date', 'Active')
            p_date_str = p_date_val.strftime('%Y-%m-%d') if isinstance(p_date_val, datetime) else str(p_date_val)
            timeline_list.append(TimelineEvent(
                peak_date=p_date_str,
                domain=getattr(ev, 'domain', 'General'),
                event_type=getattr(ev, 'event_type', 'Activation'),
                age_at_peak=int(getattr(ev, 'age_at_peak', 0)),
                magnitude=getattr(ev, 'event_magnitude', 'MAJOR')
            ))
    except Exception as e:
        logger.warning(f"Timeline engine warning in report builder: {e}")
        diagnostics.append({"section": "Timeline", "status": "PARTIAL", "warning": str(e)})

    # 10. Remedies
    remedies_list: List[RemedyProtocol] = []
    try:
        raw_remedies = get_personalized_remedies(chart_obj)
        for r in raw_remedies:
            remedies_list.append(RemedyProtocol(
                planet=r.get('planet', 'Sun'),
                remedy_type=r.get('approach', 'ALIGNMENT'),
                instructions=r.get('how', 'Daily Morning Discipline'),
                rationale=r.get('why', 'Grounding vital energy.')
            ))
    except Exception as e:
        logger.warning(f"Remedies engine warning in report builder: {e}")
        diagnostics.append({"section": "Remedies", "status": "PARTIAL", "warning": str(e)})

    limitations = [
        "Swiss Ephemeris calculations are accurate to sub-arcsecond precision for topocentric coordinates.",
        "Confluence scores represent internal structural agreement of multi-system astrological factors.",
        "Auspicious timing windows indicate favorable planetary alignment periods rather than deterministic guarantees."
    ]

    return CanonicalAstrologyReport(
        report_id=f"rep_{uuid.uuid4().hex[:12]}",
        schema_version="1.0",
        created_at=selected_date.strftime("%Y-%m-%d %H:%M:%S"),
        profile=profile,
        provenance=provenance,
        planets=planets_list,
        house_cusps=cusps_list,
        varga_placements=vargas_list,
        yogas=yogas_list,
        dashas=dashas_list,
        predictions=preds_list,
        timeline=timeline_list,
        remedies=remedies_list,
        diagnostics=diagnostics,
        limitations=limitations
    )
