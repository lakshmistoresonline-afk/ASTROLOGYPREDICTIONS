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
        self.cell(0, 10, f'Page {self.page_no()} | Confidential | deterministic Jyotish Architecture V3.22', align='C')

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
    pdf.cell(0, 6, f"Participant: {sanitize_text(data['profile']['name'])}", ln=True, align='C')
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M %Z')}", ln=True, align='C')
    pdf.cell(0, 6, f"Governance: V3.22 Premium Specification", ln=True, align='C')

    # --- 2. EXECUTIVE SUMMARY ---
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.chapter_title('1. Intelligence Overview')

    pdf.section_title('Birth Identity & Foundation')
    pdf.set_font('helvetica', '', 10)
    p = data['profile']
    pdf.cell(50, 8, 'Name:', border=0)
    pdf.cell(0, 8, sanitize_text(p['name']), ln=True)
    pdf.cell(50, 8, 'Birth Data:', border=0)
    pdf.cell(0, 8, f"{p['dob']} {p['tob']} ({p['place']})", ln=True)
    pdf.ln(5)

    pdf.section_title('Primary Active Signals')
    for sig in data['present']['top_signals']:
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(60, 8, f" {sig['domain']}:", border=0)
        pdf.set_font('helvetica', '', 10)
        pdf.cell(0, 8, f"{sig['prediction_strength']} (Signal Strength: {int(sig['score'])}/100)", ln=True)

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
    for item in data['present'].get('timeline', [])[:10]:
        if pdf.get_y() > 260: pdf.add_page()
        pdf.cell(40, 8, item['peak'], border=1, align='C')
        pdf.cell(60, 8, item['domain'], border=1, align='C')
        pdf.cell(90, 8, sanitize_text(item['event'][:45]), border=1, align='L')
        pdf.ln()

    # --- 4. EVENT CLUSTERS ---

    # --- 4. LIFETIME ROADMAP ---
    pdf.add_page()
    pdf.chapter_title('3. Lifetime Developmental Roadmap')
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(w=pdf.epw, h=6, txt="Chronological reconstruction and prospective forecast of significant life chapters.")
    pdf.ln(5)

    for event in data['lifecycle']['events']:
        if pdf.get_y() > 250: pdf.add_page()
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(30, 8, f"Age {int(event['age_at_peak'])}:", border=0)
        pdf.set_text_color(245, 158, 11)
        pdf.cell(60, 8, event['domain'], border=0)
        pdf.set_text_color(0,0,0)
        pdf.set_font('helvetica', 'I', 9)
        pdf.cell(0, 8, f"({event['peak_date']})", ln=True)

        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(0, 5, f"Temporal Status: {event['status']} | Precision: {event['timing_precision']}", ln=True)

        pdf.set_font('helvetica', '', 9)
        pdf.multi_cell(w=pdf.epw, h=5, txt=sanitize_text(event['why_now']))
        pdf.ln(2)

    # --- 5. DETAILED DOMAIN AUDIT ---
    pdf.add_page()
    pdf.chapter_title('4. 16-Domain Comprehensive Audit')
    for p in data['present']['predictions']:
        if pdf.get_y() > 230: pdf.add_page()
        pdf.set_fill_color(245, 245, 245)
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, f"{p['domain']}", ln=True, fill=True)

        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(60, 8, f"Signal Strength: {int(p['score'])}/100", border=0)
        pdf.cell(0, 8, f"Confidence Class: {p['confidence']}", ln=True)

        pdf.set_font('helvetica', '', 10)
        pdf.multi_cell(w=pdf.epw, h=6, txt=sanitize_text(p['summary']))

        if p.get('manifestations'):
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(0, 8, "Potential Manifestations:", ln=True)
            pdf.set_font('helvetica', '', 10)
            for m in p['manifestations']:
                pdf.cell(0, 6, f"- {sanitize_text(m)}", ln=True)

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
        pdf.cell(50, 7, d['lord'], border=1)
        pdf.cell(70, 7, d['start'], border=1)
        pdf.cell(70, 7, d['end'], border=1)
        pdf.ln()

    pdf.add_page()
    pdf.chapter_title('Appendix B: Technical Evidence Audit')
    pdf.set_font('helvetica', '', 8)
    pdf.set_text_color(100, 100, 100)
    for p in data['present']['predictions']:
        if pdf.get_y() > 260: pdf.add_page()
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(0, 8, f"Evidence: {p['domain']}", ln=True)
        for node in p.get('evidence_chain', []):
            src = node.get('source', 'Unknown')
            pdf.multi_cell(w=pdf.epw, h=4, txt=f"  [{sanitize_text(src)}] {sanitize_text(node.get('description'))}")
        pdf.ln(2)

    return bytes(pdf.output())
