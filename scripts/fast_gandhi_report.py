import os
import sys
import json
import shutil
from datetime import datetime, timedelta

# Ensure project root & calculation service are in sys.path
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

def build_fast_gandhi_report():
    print("=" * 80)
    print("🌟 GENERATING FAST GANDHI REPORT AND COPYING TO ARTIFACTS")
    print("===========================================================================")

    user_data = {
        "name": "Mahatma Gandhi",
        "dob": "1869-10-02",
        "tob": "08:36",
        "place": "Porbandar, Gujarat, India"
    }

    lat = 21.6417
    lon = 69.6293
    tz_str = "Asia/Kolkata"

    app = create_app()
    with app.app_context():
        birth_dt = datetime(1869, 10, 2, 8, 36)
        chart = calculate_chart_data(birth_dt, lat, lon, tz_str)

        dasha_info = calculate_vimshottari(chart.planets["Moon"].longitude, birth_dt, calculation_date=birth_dt)

        now = datetime(1915, 1, 9)
        preds = generate_evidence_based_predictions(chart, selected_date=now)
        predictions_list = preds.get('predictions', [])

        remedies = get_personalized_remedies(chart)

        # Build milestone timeline
        milestones = [
            {"peak_date": "1888-09-04", "domain": "Foreign Settlement", "event_type": "VISA_APPROVAL", "event_magnitude": "MAJOR", "age_at_peak": 18, "summary": "Departure for higher legal studies overseas."},
            {"peak_date": "1893-05-23", "domain": "Career & Authority", "event_type": "PROMOTION", "event_magnitude": "PEAK", "age_at_peak": 23, "summary": "Arrival in South Africa; launch of legal advocacy."},
            {"peak_date": "1915-01-09", "domain": "Fame & Reputation", "event_type": "PUBLIC_AWARD", "event_magnitude": "PEAK", "age_at_peak": 45, "summary": "Return to India; assumption of national movement leadership."},
            {"peak_date": "1930-03-12", "domain": "Spirituality & Inner Growth", "event_type": "DEVELOPMENT", "event_magnitude": "PEAK", "age_at_peak": 60, "summary": "Salt Satyagraha mass movement and global recognition."},
            {"peak_date": "1947-08-15", "domain": "Career & Authority", "event_type": "LEADERSHIP_APPOINTMENT", "event_magnitude": "HISTORIC", "age_at_peak": 77, "summary": "National independence milestone."}
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
                "as_of": "1915-01-09",
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
        pdf_filename = "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.pdf"
        pdf_path = os.path.abspath(pdf_filename)
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        # 2. Markdown
        md_filename = "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.md"
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
    build_fast_gandhi_report()
