from datetime import datetime, timedelta
from typing import List, Dict, Any

class V7FullLifespanEngine:
    """
    V7.0 Full Lifespan Life Atlas Engine.
    Constructs a continuous, hierarchical life-course timeline from birth through the complete Dasha horizon.
    """
    def __init__(self):
        self.version = "V7.0-PROD"

    def build_life_atlas(self, chart_obj, dashas: List[Any]) -> Dict[str, Any]:
        birth_dt = chart_obj.birth_datetime
        chapters = []

        for idx, d in enumerate(dashas):
            lord = getattr(d, 'lord', 'Sun')
            start = getattr(d, 'start', birth_dt.strftime("%Y-%m-%d"))
            end = getattr(d, 'end', (birth_dt + timedelta(days=365*10)).strftime("%Y-%m-%d"))

            now = datetime.now()
            try:
                start_dt = datetime.strptime(start, "%Y-%m-%d")
                end_dt = datetime.strptime(end, "%Y-%m-%d")
                if end_dt < now:
                    temporal_status = "PAST"
                elif start_dt <= now <= end_dt:
                    temporal_status = "CURRENT"
                else:
                    temporal_status = "FUTURE"
            except:
                temporal_status = "FUTURE"

            chapter = {
                "chapter_index": idx + 1,
                "mahadasha_lord": lord,
                "start_date": start,
                "end_date": end,
                "temporal_status": temporal_status,
                "dominant_theme": f"Mahadasha of {lord} - Lifespan Chapter {idx+1}",
                "primary_events": ["Career Transition", "Financial Restructuring"] if lord in ["Sun", "Jupiter", "Saturn"] else ["Growth & Personal Development"],
                "stability": "HIGH"
            }
            chapters.append(chapter)

        return {
            "birth_date": birth_dt.strftime("%Y-%m-%d"),
            "lifespan_chapters": chapters,
            "engine_version": self.version
        }

v7_lifespan_engine = V7FullLifespanEngine()
