from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
import json

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

def generate_complete_pdf(data):
    if not data or not isinstance(data, dict):
        data = {}

    pdf = JyotishReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    # --- 1. COVER PAGE ---
    pdf.add_page()
    pdf.set_fill_color(8, 9, 14) # Midnight Dark
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_y(90)
    pdf.set_font('helvetica', 'B', 30)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 18, text='ASTRO PREDICTIONS', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(245, 158, 11) # Gold
    pdf.cell(0, 12, text='AUTHORITATIVE 16-DOMAIN INTELLIGENCE AUDIT', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.set_y(150)
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 8, text='Exhaustive Confluent Prediction & Lifetime Atlas Report', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.set_y(230)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(160, 160, 160)
    p = data.get('profile', {})
    if not isinstance(p, dict): p = {}
    profile_name = sanitize_text(p.get('name') or 'Native Participant')
    pdf.cell(0, 6, text=f"Subject: {profile_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 6, text=f"Birth Particulars: {p.get('dob', 'N/A')} {p.get('tob', 'N/A')} | {p.get('place', 'N/A')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 6, text=f"Execution Date: {datetime.now().strftime('%d %b %Y, %H:%M %Z')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 6, text=f"Architecture: V3.36 Swiss Ephemeris Hardened Specification", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # --- 2. EXECUTIVE SUMMARY ---
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.chapter_title('1. Executive Intelligence Summary')

    pdf.section_title('Participant Identity & Birth Baseline')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 7, text='Full Name:', border=0)
    pdf.cell(0, 7, text=profile_name, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(50, 7, text='Birth Date & Time:', border=0)
    pdf.cell(0, 7, text=f"{p.get('dob', 'N/A')} at {p.get('tob', 'N/A')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(50, 7, text='Birth Location:', border=0)
    pdf.cell(0, 7, text=f"{p.get('place', 'N/A')} ({p.get('lat', 0):.4f} N, {p.get('lon', 0):.4f} E)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(50, 7, text='Timezone:', border=0)
    pdf.cell(0, 7, text=str(p.get('tz', 'Asia/Kolkata')), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    pdf.section_title('Top Confluent Life Predictions')
    present_data = data.get('present', {})
    if not isinstance(present_data, dict): present_data = {}

    pdf.set_fill_color(245, 158, 11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(60, 8, text='Domain', border=1, fill=True, align='C')
    pdf.cell(40, 8, text='Signal Score', border=1, fill=True, align='C')
    pdf.cell(45, 8, text='Status Level', border=1, fill=True, align='C')
    pdf.cell(45, 8, text='Peak Window', border=1, fill=True, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('helvetica', '', 9)
    for sig in present_data.get('top_signals', []):
        if not isinstance(sig, dict): continue
        if pdf.get_y() > 260: pdf.add_page()
        d_text = sanitize_text(str(sig.get('domain', 'Domain'))[:30])
        score_text = f"{int(sig.get('score', 0))}%"
        status_text = sanitize_text(str(sig.get('prediction_strength', 'ACTIVE')))
        tw = sig.get('timing_window', {})
        peak_text = sanitize_text(str(tw.get('peak', 'Active') if isinstance(tw, dict) else 'Active'))

        pdf.cell(60, 7, text=d_text, border=1, align='L')
        pdf.cell(40, 7, text=score_text, border=1, align='C')
        pdf.cell(45, 7, text=status_text, border=1, align='C')
        pdf.cell(45, 7, text=peak_text, border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(0, 6, text='METHODOLOGICAL NOTE', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', 'I', 8)
    pdf.multi_cell(w=pdf.epw, h=4, text="Signal confluence scores reflect deterministic multi-layer agreement of planetary cycles (Swiss Ephemeris Core V3.36). Scores represent internal structural strength rather than statistical probability.")

    # --- 3. LIFETIME ROADMAP ---
    pdf.add_page()
    pdf.chapter_title('2. Lifetime Developmental Roadmap (Age 0 - 80)')

    pdf.set_fill_color(245, 158, 11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(30, 8, text='Peak Date', border=1, fill=True, align='C')
    pdf.cell(50, 8, text='Domain', border=1, fill=True, align='C')
    pdf.cell(45, 8, text='Event Type', border=1, fill=True, align='C')
    pdf.cell(65, 8, text='Magnitude & Status', border=1, fill=True, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('helvetica', '', 8)

    lifecycle_data = data.get('lifecycle', {})
    if not isinstance(lifecycle_data, dict): lifecycle_data = {}
    for event in lifecycle_data.get('events', []):
        if not isinstance(event, dict): continue
        if pdf.get_y() > 260: pdf.add_page()
        p_date = str(event.get('peak_date') or event.get('peak') or 'Active')
        d_txt = sanitize_text(str(event.get('domain', 'General'))[:25])
        ev_txt = sanitize_text(str(event.get('event_type', 'Activation')).replace('_', ' ')[:25])
        mag_txt = sanitize_text(f"{event.get('event_magnitude', 'MAJOR')} (Age {int(event.get('age_at_peak', 30))})")

        pdf.cell(30, 7, text=p_date, border=1, align='C')
        pdf.cell(50, 7, text=d_txt, border=1, align='L')
        pdf.cell(45, 7, text=ev_txt, border=1, align='L')
        pdf.cell(65, 7, text=mag_txt, border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- 4. EXHAUSTIVE 16-DOMAIN COMPREHENSIVE AUDIT ---
    pdf.add_page()
    pdf.chapter_title('3. Exhaustive 16-Domain Intelligence Audit')

    for p_item in present_data.get('predictions', []):
        if not isinstance(p_item, dict): continue
        if pdf.get_y() > 210: pdf.add_page()

        pdf.set_fill_color(240, 240, 245)
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 8, text=f" Domain: {p_item.get('domain', 'Domain')} - {str(p_item.get('event_type', '')).replace('_', ' ')}", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font('helvetica', 'B', 9)
        pdf.set_text_color(0, 0, 0)
        tw = p_item.get('timing_window', {})
        p_date = tw.get('peak', 'Active') if isinstance(tw, dict) else 'Active'
        pdf.cell(60, 6, text=f"Match Score: {p_item.get('score', 0):.2f}%", border=0)
        pdf.cell(65, 6, text=f"Status: {p_item.get('prediction_strength', 'WATCH')}", border=0)
        pdf.cell(0, 6, text=f"Peak Window: {p_date}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font('helvetica', '', 9)
        pdf.multi_cell(w=pdf.epw, h=4.5, text=sanitize_text(p_item.get('summary', '')))
        pdf.ln(2)

        if p_item.get('supporting_factors'):
            pdf.set_font('helvetica', 'B', 8.5)
            pdf.cell(0, 5, text="Key Causal Factors:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font('helvetica', '', 8.5)
            for factor in p_item['supporting_factors'][:3]:
                pdf.multi_cell(w=pdf.epw, h=4, text=f" - {sanitize_text(str(factor))}")

        if p_item.get('manifestations'):
            pdf.set_font('helvetica', 'B', 8.5)
            pdf.cell(0, 5, text="Real-World Manifestations:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font('helvetica', '', 8.5)
            for m in p_item['manifestations'][:3]:
                pdf.multi_cell(w=pdf.epw, h=4, text=f" - {sanitize_text(str(m))}")

        pdf.ln(3)

    # --- 5. DASHA APPENDIX ---
    pdf.add_page()
    pdf.chapter_title('Appendix A: Point-in-Time Vimshottari Dasha Hierarchy')
    pdf.set_font('helvetica', '', 9)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(40, 8, text='Planet Lord', border=1, fill=True, align='C')
    pdf.cell(75, 8, text='Start Date', border=1, fill=True, align='C')
    pdf.cell(75, 8, text='End Date', border=1, fill=True, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    for d in data.get('dashas', [])[:20]:
        if not isinstance(d, dict): continue
        if pdf.get_y() > 260: pdf.add_page()
        pdf.cell(40, 7, text=str(d.get('lord', 'N/A')), border=1, align='C')
        pdf.cell(75, 7, text=str(d.get('start_str') or d.get('start') or 'N/A'), border=1, align='C')
        pdf.cell(75, 7, text=str(d.get('end_str') or d.get('end') or 'N/A'), border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return bytes(pdf.output())
