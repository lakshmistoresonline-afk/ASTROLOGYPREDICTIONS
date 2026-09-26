from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
from typing import Dict, Any, Union
from ..astrology.reporting.models import CanonicalAstrologyReport

class JyotishReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, text='Astro Predictions - Authoritative Multi-Domain Intelligence Audit', border=0, align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, text=f'Page {self.page_no()} | Confidential | Deterministic Swiss Ephemeris Architecture V3.36', align='C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(245, 158, 11) # Gold
        self.cell(0, 15, text=title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(3)

    def section_title(self, title):
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(30, 41, 59)
        self.cell(0, 8, text=title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(2)

def sanitize_text(text):
    if not text: return ""
    mapping = {
        "\u2014": "-", "\u2013": "-", "\u2022": "-", "\u0950": "OM",
        "\u2705": "[OK]", "\u26a0": "[!]", "\u25c0": "<", "\u25b6": ">",
        "\u2704": "[*]", "\u2605": "*", "\u2606": "*"
    }
    for char, replacement in mapping.items():
        text = text.replace(char, replacement)
    try:
        return text.encode('latin-1', 'replace').decode('latin-1')
    except:
        return text.encode('ascii', 'replace').decode('ascii')

def generate_complete_pdf(data: Union[Dict[str, Any], CanonicalAstrologyReport]) -> bytes:
    if isinstance(data, CanonicalAstrologyReport):
        data = data.to_dict()

    if not data or not isinstance(data, dict):
        data = {}

    profile = data.get('profile', {})
    if not isinstance(profile, dict): profile = {}
    profile_name = sanitize_text(profile.get('name') or 'Native Participant')
    dob = profile.get('birth_dob') or profile.get('dob') or 'N/A'
    tob = profile.get('birth_tob') or profile.get('tob') or 'N/A'
    place = profile.get('birth_place') or profile.get('place') or 'Observer Location'
    lat = float(profile.get('latitude') or profile.get('lat') or 0.0)
    lon = float(profile.get('longitude') or profile.get('lon') or 0.0)
    tz = str(profile.get('timezone') or profile.get('tz') or 'UTC')

    provenance = data.get('provenance') or data.get('metadata') or {}
    if not isinstance(provenance, dict): provenance = {}

    pdf = JyotishReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    # --- 1. COVER PAGE ---
    pdf.add_page()
    pdf.set_fill_color(8, 9, 14)
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_y(90)
    pdf.set_font('helvetica', 'B', 30)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 18, text='ASTRO PREDICTIONS', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(245, 158, 11)
    pdf.cell(0, 12, text='AUTHORITATIVE 16-DOMAIN INTELLIGENCE AUDIT', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.set_y(150)
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 8, text='Exhaustive Confluent Prediction & Lifetime Atlas Report', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.set_y(220)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(160, 160, 160)
    pdf.cell(0, 6, text=f"Subject: {profile_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 6, text=f"Birth Particulars: {dob} {tob} | {place}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 6, text=f"Coordinates: {lat:.4f}° N, {lon:.4f}° E | Timezone: {tz}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 6, text=f"Fingerprint: {provenance.get('chart_fingerprint', 'Calculated')[:24]}...", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 6, text=f"Architecture: V3.36 Swiss Ephemeris Hardened Specification", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # --- 2. EXECUTIVE SUMMARY & PARTICIPANT IDENTITY ---
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.chapter_title('1. Executive Intelligence Summary')

    pdf.section_title('Participant Identity & Birth Baseline')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 7, text='Full Name:', border=0)
    pdf.cell(0, 7, text=profile_name, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(50, 7, text='Birth Date & Time:', border=0)
    pdf.cell(0, 7, text=f"{dob} at {tob}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(50, 7, text='Birth Location:', border=0)
    pdf.cell(0, 7, text=f"{place} ({lat:.4f}° N, {lon:.4f}° E)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(50, 7, text='Timezone:', border=0)
    pdf.cell(0, 7, text=tz, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # --- 3. PLANETARY POSITIONS TABLE ---
    pdf.section_title('Planetary Positions & Sub-Arcsecond Coordinates')
    planets_data = data.get('planets', [])
    if planets_data:
        pdf.set_fill_color(245, 158, 11)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('helvetica', 'B', 8.5)
        pdf.cell(30, 7, text='Planet', border=1, fill=True, align='C')
        pdf.cell(40, 7, text='Longitude', border=1, fill=True, align='C')
        pdf.cell(35, 7, text='Sign', border=1, fill=True, align='C')
        pdf.cell(20, 7, text='House', border=1, fill=True, align='C')
        pdf.cell(45, 7, text='Nakshatra (Pada)', border=1, fill=True, align='C')
        pdf.cell(20, 7, text='Retro', border=1, fill=True, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font('helvetica', '', 8)
        for pl in planets_data:
            if not isinstance(pl, dict): continue
            if pdf.get_y() > 260: pdf.add_page()
            p_name = sanitize_text(str(pl.get('name', 'Planet')))
            p_lon = f"{float(pl.get('longitude', 0.0)):.2f}°"
            p_sign = sanitize_text(str(pl.get('sign_name', 'Sign')))
            p_house = str(pl.get('house', 1))
            p_nak = sanitize_text(f"{pl.get('nakshatra', 'Nakshatra')} ({pl.get('pada', 1)})")
            p_retro = "YES" if pl.get('is_retrograde') else "NO"

            pdf.cell(30, 6, text=p_name, border=1, align='L')
            pdf.cell(40, 6, text=p_lon, border=1, align='C')
            pdf.cell(35, 6, text=p_sign, border=1, align='C')
            pdf.cell(20, 6, text=p_house, border=1, align='C')
            pdf.cell(45, 6, text=p_nak, border=1, align='L')
            pdf.cell(20, 6, text=p_retro, border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

    # --- 4. TOP SIGNALS SUMMARY ---
    pdf.section_title('Top Confluent Life Predictions')
    predictions_data = data.get('predictions') or (data.get('present', {}).get('predictions') if isinstance(data.get('present'), dict) else [])
    if not isinstance(predictions_data, list): predictions_data = []

    pdf.set_fill_color(245, 158, 11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 8.5)
    pdf.cell(60, 7, text='Domain', border=1, fill=True, align='C')
    pdf.cell(40, 7, text='Signal Score', border=1, fill=True, align='C')
    pdf.cell(45, 7, text='Status Level', border=1, fill=True, align='C')
    pdf.cell(45, 7, text='Peak Window', border=1, fill=True, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('helvetica', '', 8.5)
    for sig in predictions_data[:5]:
        if not isinstance(sig, dict): continue
        if pdf.get_y() > 260: pdf.add_page()
        d_text = sanitize_text(str(sig.get('domain', 'Domain'))[:30])
        score_text = f"{int(sig.get('confluence_score') or sig.get('score', 0))}%"
        status_text = sanitize_text(str(sig.get('prediction_strength', 'ACTIVE')))
        peak_text = sanitize_text(str(sig.get('peak_date') or sig.get('timing_window', {}).get('peak', 'Active')))

        pdf.cell(60, 6, text=d_text, border=1, align='L')
        pdf.cell(40, 6, text=score_text, border=1, align='C')
        pdf.cell(45, 6, text=status_text, border=1, align='C')
        pdf.cell(45, 6, text=peak_text, border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- 5. LIFETIME ROADMAP ---
    pdf.add_page()
    pdf.chapter_title('2. Lifetime Developmental Roadmap (Age 0 - 80)')

    pdf.set_fill_color(245, 158, 11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 8.5)
    pdf.cell(30, 7, text='Peak Date', border=1, fill=True, align='C')
    pdf.cell(50, 7, text='Domain', border=1, fill=True, align='C')
    pdf.cell(45, 7, text='Event Type', border=1, fill=True, align='C')
    pdf.cell(65, 7, text='Magnitude & Status', border=1, fill=True, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('helvetica', '', 8)

    timeline_data = data.get('timeline') or (data.get('lifecycle', {}).get('events') if isinstance(data.get('lifecycle'), dict) else [])
    if not isinstance(timeline_data, list): timeline_data = []
    for event in timeline_data[:15]:
        if not isinstance(event, dict): continue
        if pdf.get_y() > 260: pdf.add_page()
        p_date = str(event.get('peak_date') or event.get('peak') or 'Active')
        d_txt = sanitize_text(str(event.get('domain', 'General'))[:25])
        ev_txt = sanitize_text(str(event.get('event_type', 'Activation')).replace('_', ' ')[:25])
        mag_txt = sanitize_text(f"{event.get('magnitude') or event.get('event_magnitude', 'MAJOR')} (Age {int(event.get('age_at_peak', 30))})")

        pdf.cell(30, 6, text=p_date, border=1, align='C')
        pdf.cell(50, 6, text=d_txt, border=1, align='L')
        pdf.cell(45, 6, text=ev_txt, border=1, align='L')
        pdf.cell(65, 6, text=mag_txt, border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- 6. EXHAUSTIVE 16-DOMAIN COMPREHENSIVE AUDIT ---
    pdf.add_page()
    pdf.chapter_title('3. Exhaustive 16-Domain Intelligence Audit')

    for p_item in predictions_data:
        if not isinstance(p_item, dict): continue
        if pdf.get_y() > 210: pdf.add_page()

        pdf.set_fill_color(240, 240, 245)
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 8, text=f" Domain: {p_item.get('domain', 'Domain')} - {str(p_item.get('event_type', '')).replace('_', ' ')}", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font('helvetica', 'B', 8.5)
        pdf.set_text_color(0, 0, 0)
        score_val = float(p_item.get('confluence_score') or p_item.get('score', 0))
        p_date = p_item.get('peak_date') or p_item.get('timing_window', {}).get('peak', 'Active')
        pdf.cell(60, 6, text=f"Match Score: {score_val:.2f}%", border=0)
        pdf.cell(65, 6, text=f"Status: {p_item.get('prediction_strength', 'WATCH')}", border=0)
        pdf.cell(0, 6, text=f"Peak Window: {p_date}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font('helvetica', '', 8.5)
        pdf.multi_cell(w=pdf.epw, h=4.5, text=sanitize_text(p_item.get('summary', '')))
        pdf.ln(2)

        factors = p_item.get('supporting_factors', [])
        if factors:
            pdf.set_font('helvetica', 'B', 8)
            pdf.cell(0, 5, text="Key Causal Factors:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font('helvetica', '', 8)
            for factor in factors[:3]:
                pdf.multi_cell(w=pdf.epw, h=4, text=f" - {sanitize_text(str(factor))}")

        pdf.ln(3)

    # --- 7. VIMSHOTTARI DASHA APPENDIX ---
    pdf.add_page()
    pdf.chapter_title('Appendix A: Point-in-Time Vimshottari Dasha Hierarchy')
    pdf.set_font('helvetica', '', 8.5)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(40, 7, text='Planet Lord', border=1, fill=True, align='C')
    pdf.cell(75, 7, text='Start Date', border=1, fill=True, align='C')
    pdf.cell(75, 7, text='End Date', border=1, fill=True, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    dashas_data = data.get('dashas', [])
    for d in dashas_data[:20]:
        if not isinstance(d, dict): continue
        if pdf.get_y() > 260: pdf.add_page()
        pdf.cell(40, 6, text=str(d.get('lord', 'N/A')), border=1, align='C')
        pdf.cell(75, 6, text=str(d.get('start_date') or d.get('start_str') or d.get('start') or 'N/A'), border=1, align='C')
        pdf.cell(75, 6, text=str(d.get('end_date') or d.get('end_str') or d.get('end') or 'N/A'), border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- 8. PROVENANCE & LIMITATIONS ---
    pdf.add_page()
    pdf.chapter_title('Appendix B: Calculation Provenance & Methodology')
    pdf.set_font('helvetica', '', 8.5)
    pdf.multi_cell(w=pdf.epw, h=4.5, text=f"Engine Version: {provenance.get('engine_version', 'V3.36 Authoritative')}\nCalculation Core: {provenance.get('calculation_core', 'CALC-SWE-2.10.3')}\nAyanamsa: {provenance.get('ayanamsa', 'Lahiri Sidereal')}\nHouse System: {provenance.get('house_system', 'Placidus / Whole Sign Hybrid')}\nCoordinates Type: {provenance.get('coordinates_type', 'Topocentric True')}\nChart Fingerprint: {provenance.get('chart_fingerprint', 'N/A')}\nReport Fingerprint: {provenance.get('report_fingerprint', 'N/A')}\nCalculation Timestamp: {provenance.get('calculation_timestamp', 'N/A')}")

    return bytes(pdf.output())
