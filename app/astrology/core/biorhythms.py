import math
from datetime import datetime
from typing import Dict

def calculate_biorhythms(birth_date: datetime, target_date: datetime) -> Dict[str, float]:
    """
    Calculate Physical (23 days), Emotional (28 days), and Intellectual (33 days) cycles.
    Returns value from -1.0 to 1.0.
    """
    diff = (target_date - birth_date).days

    def get_val(cycle_days):
        return math.sin(2 * math.pi * diff / cycle_days)

    return {
        "physical": round(get_val(23), 3),
        "emotional": round(get_val(28), 3),
        "intellectual": round(get_val(33), 3),
        "total_vitality": round((get_val(23) + get_val(28) + get_val(33)) / 3, 3)
    }
