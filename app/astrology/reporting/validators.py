from typing import Tuple, List
from .models import CanonicalAstrologyReport

def validate_canonical_report(report: CanonicalAstrologyReport) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    if not report.report_id:
        errors.append("Missing report_id in canonical report.")

    if not report.profile or not report.profile.name:
        errors.append("Missing or invalid native profile in canonical report.")

    if not report.provenance or not report.provenance.chart_fingerprint:
        errors.append("Missing or invalid calculation provenance fingerprint.")

    if not report.planets or len(report.planets) < 7:
        errors.append(f"Incomplete planetary positions count: {len(report.planets)} planets found (min 7 required).")

    if not report.house_cusps or len(report.house_cusps) < 12:
        errors.append(f"Incomplete house cusps count: {len(report.house_cusps)} cusps found (12 required).")

    is_valid = len(errors) == 0
    return is_valid, errors
