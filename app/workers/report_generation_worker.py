"""
Asynchronous PDF & Multi-Format Report Worker (Module 23 - Task 23.2).
Generates multi-page PDF reports and exports iCal (.ics) calendar files for high-confluence transit timing windows.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from ..utils.pdf_generator import generate_complete_pdf

class ReportGenerationWorker:
    """
    Asynchronous Report Worker rendering downloadable PDF reports and .ics iCal calendars.
    """

    @staticmethod
    def generate_ical_calendar(
        events: List[Dict[str, Any]],
        profile_name: str = "Native"
    ) -> str:
        """
        Generates standard RFC 5545 iCalendar (.ics) format string for high-confluence transit windows.
        """
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Astro Predictions V3.36//NONSGML Transit Calendar//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH"
        ]

        for idx, ev in enumerate(events, 1):
            peak_date = ev.get("peak_date") or ev.get("peak", "2026-10-20")
            try:
                dt_start = datetime.strptime(peak_date, "%Y-%m-%d")
            except Exception:
                dt_start = datetime(2026, 10, 20)

            dt_end = dt_start + timedelta(days=1)
            summary = f"🌟 {ev.get('domain', 'Astro')}: {ev.get('event_type', 'Peak Window')}"
            desc = ev.get("summary_narrative", ev.get("summary", "High-confluence planetary alignment."))

            lines.extend([
                "BEGIN:VEVENT",
                f"UID:astro-event-{idx}-{dt_start.strftime('%Y%m%d')}@astropredictions.com",
                f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M00Z')}",
                f"DTSTART;VALUE=DATE:{dt_start.strftime('%Y%m%d')}",
                f"DTEND;VALUE=DATE:{dt_end.strftime('%Y%m%d')}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{desc}",
                "STATUS:CONFIRMED",
                "END:VEVENT"
            ])

        lines.append("END:VCALENDAR")
        return "\r\n".join(lines)

    @staticmethod
    def process_async_pdf_and_ical_export(
        report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processes asynchronous report rendering and outputs PDF bytes and .ics iCal content.
        """
        pdf_bytes = generate_complete_pdf(report_data)

        profile_name = report_data.get("profile", {}).get("name", "Native")
        predictions = report_data.get("present", {}).get("predictions", [])

        # Filter high-confluence events for calendar export
        high_events = [p for p in predictions if p.get("score", 0) >= 50.0]
        if not high_events:
            high_events = predictions[:3]

        ical_str = ReportGenerationWorker.generate_ical_calendar(high_events, profile_name)

        return {
            "pdf_bytes": pdf_bytes,
            "pdf_size_bytes": len(pdf_bytes),
            "ical_content": ical_str,
            "ical_size_bytes": len(ical_str),
            "status": "SUCCESS"
        }

report_generation_worker = ReportGenerationWorker()
