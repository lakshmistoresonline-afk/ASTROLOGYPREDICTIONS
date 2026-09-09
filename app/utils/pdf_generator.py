from fpdf import FPDF
from datetime import datetime
import json

class JyotishReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, 'Astro Predictions - V3.22 Premium Intelligence Audit', border=0, align='R')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Confidential | Deterministic Jyotish Architecture V3.22', align='C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(245, 158, 11) # Gold
        self.cell(0, 15, title, ln=True, align='L')
        self.ln(5)

    def section_title(self, title):
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(2)

def sanitize_text(text):
    if not text: return ""
    mapping = {"\u2014": "-", "\u2013": "-", "\u2022": "-", "\u0950": "OM"}
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
    pdf.set_fill_color(5, 5, 8) # Midnight Blue
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_y(100)
    pdf.set_font('helvetica', 'B', 32)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, 'ASTRO PREDICTIONS', ln=True, align='C')

    pdf.set_font('helvetica', 'B', 18)
    pdf.set_text_color(245, 158, 11) # Gold
    pdf.cell(0, 15, 'PREMIUM PERSONAL INTELLIGENCE AUDIT', ln=True, align='C')

    pdf.set_y(160)
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 10, 'Complete Lifetime Lifecycle Analysis', ln=True, align='C')

    pdf.set_y(240)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(150, 150, 150)
    p = data.get('profile', {})
    if not isinstance(p, dict): p = {}
    profile_name = sanitize_text(p.get('name') or 'Native')
    pdf.cell(0, 6, f"Participant: {profile_name}", ln=True, align='C')
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M %Z')}", ln=True, align='C')
    pdf.cell(0, 6, f"Governance: V3.22 Premium Specification", ln=True, align='C')

    # --- 2. EXECUTIVE SUMMARY ---
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.chapter_title('1. Intelligence Overview')

    pdf.section_title('Birth Identity & Foundation')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 8, 'Name:', border=0)
    pdf.cell(0, 8, profile_name, ln=True)
    pdf.cell(50, 8, 'Birth Data:', border=0)
    pdf.cell(0, 8, f"{p.get('dob', 'N/A')} {p.get('tob', 'N/A')} ({p.get('place', 'N/A')})", ln=True)
    pdf.ln(5)

    pdf.section_title('Primary Active Signals')
    present_data = data.get('present', {})
    if not isinstance(present_data, dict): present_data = {}
    for sig in present_data.get('top_signals', []):
        if not isinstance(sig, dict): continue
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(60, 8, f" {sig.get('domain', 'Signal')}:", border=0)
        pdf.set_font('helvetica', '', 10)
        pdf.cell(0, 8, f"{sig.get('prediction_strength', 'ACTIVE')} (Signal Strength: {int(sig.get('score', 50))}/100)", ln=True)

    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 10, 'METHODOLOGICAL NOTE', ln=True)
    pdf.set_font('helvetica', 'I', 9)
    pdf.multi_cell(w=pdf.epw, h=5, txt="Signal scores represent deterministic confluence of planetary cycles (V3.15 Engine), not statistical probability. No 100% certainty is implied.")

    # --- 3. TIMELINE SNAPSHOTS (V3.23) ---
    pdf.add_page()
    pdf.chapter_title('2. Horizon Roadmaps')

    pdf.section_title('12-Month Professional & Personal Roadmap')
    # Table Header
    pdf.set_fill_color(245, 158, 11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 10, 'Peak Date', border=1, fill=True, align='C')
    pdf.cell(60, 10, 'Intelligence Sector', border=1, fill=True, align='C')
    pdf.cell(90, 10, 'Primary Development', border=1, fill=True, align='C')
    pdf.ln()

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('helvetica', '', 9)
    # Using 12-month timeline data from dashboard
    for item in present_data.get('timeline', [])[:10]:
        if not isinstance(item, dict): continue
        if pdf.get_y() > 260: pdf.add_page()
        peak = str(item.get('peak') or item.get('peak_date') or 'N/A')
        domain = str(item.get('domain') or 'General')
        event_txt = sanitize_text(str(item.get('event') or item.get('description') or 'Active Phase')[:45])
        pdf.cell(40, 8, peak, border=1, align='C')
        pdf.cell(60, 8, domain, border=1, align='C')
        pdf.cell(90, 8, event_txt, border=1, align='L')
        pdf.ln()

    # --- 4. LIFETIME ROADMAP ---
    pdf.add_page()
    pdf.chapter_title('3. Lifetime Developmental Roadmap')
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(w=pdf.epw, h=6, txt="Chronological reconstruction and prospective forecast of significant life chapters.")
    pdf.ln(5)

    lifecycle_data = data.get('lifecycle', {})
    if not isinstance(lifecycle_data, dict): lifecycle_data = {}
    for event in lifecycle_data.get('events', []):
        if not isinstance(event, dict): continue
        if pdf.get_y() > 250: pdf.add_page()
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(30, 8, f"Age {int(event.get('age_at_peak', 30))}:", border=0)
        pdf.set_text_color(245, 158, 11)
        pdf.cell(60, 8, str(event.get('domain', 'General')), border=0)
        pdf.set_text_color(0,0,0)
        pdf.set_font('helvetica', 'I', 9)
        pdf.cell(0, 8, f"({event.get('peak_date', 'N/A')})", ln=True)

        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(0, 5, f"Temporal Status: {event.get('status', 'ACTIVE')} | Precision: {event.get('timing_precision', 'MONTH')}", ln=True)

        pdf.set_font('helvetica', '', 9)
        pdf.multi_cell(w=pdf.epw, h=5, txt=sanitize_text(event.get('why_now', 'Active planetary transit activation.')))
        pdf.ln(2)

    # --- 5. DETAILED DOMAIN AUDIT ---
    pdf.add_page()
    pdf.chapter_title('4. 16-Domain Comprehensive Audit')
    for p_item in present_data.get('predictions', []):
        if not isinstance(p_item, dict): continue
        if pdf.get_y() > 230: pdf.add_page()
        pdf.set_fill_color(245, 245, 245)
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, f"{p_item.get('domain', 'Domain')}", ln=True, fill=True)

        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(60, 8, f"Signal Strength: {int(p_item.get('score', 50))}/100", border=0)
        pdf.cell(0, 8, f"Confidence Class: {p_item.get('confidence', 'MODERATE')}", ln=True)

        pdf.set_font('helvetica', '', 10)
        pdf.multi_cell(w=pdf.epw, h=6, txt=sanitize_text(p_item.get('summary', '')))

        if p_item.get('manifestations'):
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(0, 8, "Potential Manifestations:", ln=True)
            pdf.set_font('helvetica', '', 10)
            for m in p_item['manifestations']:
                pdf.cell(0, 6, f"- {sanitize_text(str(m))}", ln=True)

        pdf.ln(4)

    # --- 6. TECHNICAL APPENDIX ---
    pdf.add_page()
    pdf.chapter_title('Appendix A: Dasha Cycles (Vimshottari)')
    pdf.set_font('helvetica', '', 9)
    # Header
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(50, 8, 'Planet Lord', border=1, fill=True)
    pdf.cell(70, 8, 'Start Date', border=1, fill=True)
    pdf.cell(70, 8, 'End Date', border=1, fill=True)
    pdf.ln()
    for d in data.get('dashas', [])[:20]: # Limit for brevity
        if not isinstance(d, dict): continue
        pdf.cell(50, 7, str(d.get('lord', '')), border=1)
        pdf.cell(70, 7, str(d.get('start', '')), border=1)
        pdf.cell(70, 7, str(d.get('end', '')), border=1)
        pdf.ln()

    pdf.add_page()
    pdf.chapter_title('Appendix B: Technical Evidence Audit')
    pdf.set_font('helvetica', '', 8)
    pdf.set_text_color(100, 100, 100)
    for p_item in present_data.get('predictions', []):
        if not isinstance(p_item, dict): continue
        if pdf.get_y() > 260: pdf.add_page()
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(0, 8, f"Evidence: {p_item.get('domain', 'Domain')}", ln=True)
        for node in p_item.get('evidence_chain', []):
            if not isinstance(node, dict): continue
            src = node.get('source', 'Unknown')
            pdf.multi_cell(w=pdf.epw, h=4, txt=f"  [{sanitize_text(str(src))}] {sanitize_text(str(node.get('description', '')))}")
        pdf.ln(2)

    return bytes(pdf.output())
