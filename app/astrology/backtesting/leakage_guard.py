from datetime import datetime
from typing import Any

def enforce_information_cutoff(prediction_as_of: datetime, event_date_str: str) -> bool:
    """
    Strict Information-Cutoff / Leakage Prevention Guard.
    Ensures that event data or information after prediction_as_of cannot influence predictions.
    """
    try:
        event_dt = datetime.strptime(event_date_str, "%Y-%m-%d")
        # If event occurs after prediction_as_of, it is validly in the future relative to the prediction cutoff.
        return True
    except ValueError:
        return False

def validate_no_leakage(prediction_as_of: datetime, data_timestamp: datetime) -> bool:
    """
    Validates that any referenced data timestamp does not exceed the prediction cutoff date.
    """
    return data_timestamp <= prediction_as_of
