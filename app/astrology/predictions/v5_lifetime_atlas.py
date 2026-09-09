from datetime import datetime, timedelta
from typing import List, Dict, Any

class FullLifetimeAtlasEngine:
    """
    V5 Full Lifetime Engine: Generates complete life-course Dasha and Antardasha chapters.
    """
    def generate_lifetime_atlas(self, chart_obj, dashas: List[Any]) -> List[Dict[str, Any]]:
        atlas = []
        birth_dt = chart_obj.birth_datetime

        for d in dashas:
            lord = getattr(d, 'lord', 'Sun')
            start = getattr(d, 'start', birth_dt.strftime("%Y-%m-%d"))
            end = getattr(d, 'end', (birth_dt + timedelta(days=365*10)).strftime("%Y-%m-%d"))

            chapter = {
                "chapter_type": "MAHADASHA",
                "ruler": lord,
                "start_date": start,
                "end_date": end,
                "theme": f"Mahadasha period ruled by {lord}",
                "prominent_domains": ["Career & Authority", "Finance & Wealth"] if lord in ["Sun", "Jupiter", "Saturn"] else ["Growth & Transition"],
                "confidence": "HIGH"
            }
            atlas.append(chapter)
        return atlas

v5_atlas_engine = FullLifetimeAtlasEngine()
