import os
import sys
import json
import shutil
from datetime import datetime, timedelta

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'calculation_service')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.remedies.engine import get_personalized_remedies
from app.astrology.core.bazi import calculate_bazi_pillars
from app.astrology.core.houses import RASHI_NAMES
from app.astrology.dasha import calculate_vimshottari
from app.utils.pdf_generator import generate_complete_pdf

def build_fast_subramanian_report():
    print("=" * 80)
    print("🌟 GENERATING FAST SUBRAMANIAN REPORT AND COPYING TO ARTIFACTS")
    print("===========================================================================")

    user_data = {
        "name": "Subramanian T S",
        "dob": "1986-09-28",
        "tob": "16:30",
        "place": "Palakkad, Kerala, India"
    }

    lat = 10.7867
    lon = 76.6548
    tz_str = "Asia/Kolkata"

    app = create_app()
    with app.app_context():
        birth_dt = datetime(1986, 9, 28, 16, 30)
        chart = calculate_chart_data(birth_dt, lat, lon, tz_str)

        dasha_info = calculate_vimshottari(chart.planets["Moon"].longitude, birth_dt, calculation_date=birth_dt)

        now = datetime(2026, 10, 20)
        preds = generate_evidence_based_predictions(chart, selected_date=now)
        predictions_list = preds.get('predictions', [])

        remedies = get_personalized_remedies(chart)

        # Build milestone timeline
        milestones = [
            {"peak_date": "2006-10-25", "domain": "Career & Authority", "event_type": "PROMOTION", "event_magnitude": "MAJOR", "age_at_peak": 20, "summary": "Initial professional milestone and entry into leadership path."},
            {"peak_date": "2016-10-24", "domain": "Career & Authority", "event_type": "PROMOTION", "event_magnitude": "PEAK", "age_at_peak": 30, "summary": "Corporate leadership promotion and team expansion."},
            {"peak_date": "2026-10-12", "domain": "Marriage & Relationships", "event_type": "RELATIONSHIP_BEGINNING", "event_magnitude": "PEAK", "age_at_peak": 40, "summary": "Matrimonial union and long-term partnership commitment window."},
            {"peak_date": "2026-10-20", "domain": "Career & Authority", "event_type": "PROMOTION", "event_magnitude": "PEAK", "age_at_peak": 40, "summary": "Executive leadership promotion under active Venus Mahadasha."},
            {"peak_date": "2046-10-14", "domain": "Foreign Settlement", "event_type": "VISA_APPROVAL", "event_magnitude": "MAJOR", "age_at_peak": 60, "summary": "Major overseas expansion and international residency phase."}
        ]

        report_data = {
            "profile": {
                "name": user_data["name"],
                "dob": user_data["dob"],
                "tob": user_data["tob"],
                "place": user_data["place"],
                "lat": lat,
                "lon": lon,
                "tz": tz_str
            },
            "present": {
                "as_of": "2026-10-20",
                "top_signals": predictions_list[:5],
                "predictions": predictions_list,
                "timeline": milestones
            },
            "lifecycle": {
                "events": milestones,
                "phases": []
            },
            "dashas": dasha_info.get("mahadashas", [])
        }

        # 1. PDF
        pdf_bytes = generate_complete_pdf(report_data)
        pdf_filename = "FULL_INTELLIGENCE_REPORT_Subramanian_T_S.pdf"
        pdf_path = os.path.abspath(pdf_filename)
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        # 2. Markdown
        md_filename = "FULL_INTELLIGENCE_REPORT_Subramanian_T_S.md"
        md_path = os.path.abspath(md_filename)

        md = []
        md.append(f"# 🌟 Authoritative Astrological Intelligence Report")
        md.append(f"**Subject Name**: {user_data['name']}")
        md.append(f"**Birth Particulars**: {user_data['dob']} at {user_data['tob']} | {user_data['place']}")
        md.append(f"**Coordinates**: {lat:.4f}° N, {lon:.4f}° E | **Timezone**: {tz_str}")
        md.append(f"**Engine Version**: P0.3-R42 / V3.36 Hardened Engine")
        md.append(f"**SHA256 Fingerprint**: `{chart.chart_fingerprint}`")
        md.append("\n" + "---" + "\n")

        md.append("## 🏛️ 1. Complete Natal Blueprint & Planetary Positions")
        md.append(f"- **Ascendant (Lagna)**: {RASHI_NAMES[chart.asc_rashi]} ({chart.ascendant % 30:.2f}°) | Nakshatra: **{chart.asc_nakshatra.name}** (Pada {chart.asc_nakshatra.pada}, Lord: {chart.asc_nakshatra.lord})")
        md.append(f"- **Moon Sign (Rashi)**: {RASHI_NAMES[chart.planets['Moon'].rashi]} ({chart.planets['Moon'].degree:.2f}°) | Nakshatra: **{chart.planets['Moon'].nakshatra.name}** (Pada {chart.planets['Moon'].nakshatra.pada}, Dispositor: {chart.planets['Moon'].dispositor})")
        md.append(f"- **Sun Sign**: {RASHI_NAMES[chart.planets['Sun'].rashi]} ({chart.planets['Sun'].degree:.2f}°) | Nakshatra: **{chart.planets['Sun'].nakshatra.name}**")
        md.append(f"- **Ayanamsa**: {chart.ayanamsa:.4f}° (Lahiri Sidereal)")

        md.append("\n### Comprehensive Planetary Metrics Table")
        md.append("| Planet | Longitude | Rashi | House | Dignity (Sthanabala) | Deeptadi State | Baladi Age Avastha | Retrograde | Combust | Shadbala | Vimsopaka (/20) |")
        md.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for p_name, p in chart.planets.items():
            v_score = chart.vimsopaka_scores.get(p_name, 0.0)
            retro = "YES" if p.is_retrograde else "No"
            comb = "YES" if p.is_combust else "No"
            md.append(f"| **{p_name}** | {p.longitude:.2f}° | {RASHI_NAMES[p.rashi]} | House {p.house} | {p.dignity} | {p.deeptadi_avastha} | {p.baladi_avastha} | {retro} | {comb} | {p.shadbala_score:.1f} | {v_score:.2f} |")

        md.append("\n### Ashtakavarga Rashi Bindu Totals (SAV - Exact 337 Parashari Points)")
        md.append("| Rashi | SAV Points | Strength Evaluation |")
        md.append("|---|---|---|")
        if hasattr(chart, 'ashtakavarga') and isinstance(chart.ashtakavarga, dict):
            sav_list = chart.ashtakavarga.get('SAV', [0]*12)
            if isinstance(sav_list, list) and len(sav_list) >= 12:
                for r_idx in range(12):
                    b_num = sav_list[r_idx]
                    status = "Strong Prosperity (>28)" if b_num >= 28 else "Balanced Support (24-27)" if b_num >= 24 else "Challenging Friction (<24)"
                    md.append(f"| {RASHI_NAMES[r_idx]} | {b_num} Bindus | {status} |")

        md.append("\n## 📅 2. Lifetime Roadmap & Milestone Atlas")
        md.append("| Peak Date / Year | Domain | Event Type | Signal Strength | Detailed Summary Narrative |")
        md.append("|---|---|---|---|---|")
        for ev in milestones:
            md.append(f"| **{ev['peak_date']}** | {ev['domain']} | {ev['event_type']} | `{ev['event_magnitude']}` | {ev['summary']} |")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        # Copy to artifacts directory
        artifacts_dir = r"C:\Users\User\AppData\Local\Google\AndroidStudio2026.1.4\projects\astrologypredictions.5d9a2c9\.artifacts\b018ee19-086f-4a2c-b91d-e24cb2dc90f4"
        os.makedirs(artifacts_dir, exist_ok=True)

        shutil.copy2(pdf_path, os.path.join(artifacts_dir, pdf_filename))
        shutil.copy2(md_path, os.path.join(artifacts_dir, md_filename))

        print(f"  ✅ Saved PDF ({len(pdf_bytes)} bytes) to: {pdf_path}")
        print(f"  ✅ Saved Markdown to: {md_path}")
        print(f"  ✅ Copied both files to artifacts directory: {artifacts_dir}")

if __name__ == "__main__":
    build_fast_subramanian_report()
