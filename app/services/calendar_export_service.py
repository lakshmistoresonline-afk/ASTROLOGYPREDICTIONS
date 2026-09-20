from typing import Dict, Any, List
from datetime import datetime

class AstrologicalCalendarExportService:
    """
    V3.22 Planetary Transit & Dasha iCal / Google Calendar Sync Service.
    Generates standard iCal (.ics) formatted calendar feeds for astrological transit and dasha alerts.
    """

    @staticmethod
    def generate_ical_feed(events: List[Dict[str, Any]]) -> str:
        ical_lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Astro Predictions//Vedic Intelligence//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH"
        ]

        for ev in events:
            summary = ev.get("summary", "Astrological Transit Alert")
            start = ev.get("date", datetime.utcnow().strftime("%Y%m%dT%H%M00Z"))
            description = ev.get("description", "Astro Predictions Timing Alert")

            ical_lines.extend([
                "BEGIN:VEVENT",
                f"SUMMARY:{summary}",
                f"DTSTART:{start.replace('-', '').replace(':', '')}",
                f"DESCRIPTION:{description}",
                "END:VEVENT"
            ])

        ical_lines.append("END:VCALENDAR")
        return "\r\n".join(ical_lines)
