from typing import Dict, Any, List

def govern_sample_size(unique_subjects: int, event_count: int) -> Dict[str, Any]:
    """
    V5.5 Sample-Size Governance: Enforces person vs event separation.
    """
    status = "SUFFICIENT"
    if unique_subjects < 10 or event_count < 39:
        status = "INSUFFICIENT_SAMPLE"

    return {
        "unique_subject_count": unique_subjects,
        "event_count": event_count,
        "governance_status": status
    }
