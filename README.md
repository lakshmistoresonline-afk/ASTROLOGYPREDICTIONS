# 🔮 ASTROLOGYPREDICTIONS — Comprehensive Vedic Intelligence Engine

An evidence-based, professional-grade Vedic Astrology (Jyotish) prediction platform utilizing a deterministic inference chain.

---

## ✨ Features

| Category | Mathematical Precision |
|---|---|
| **Core Engine** | Swiss Ephemeris (Topocentric) · 16 Parashari Vargas (D1-D60) · Lahiri Ayanamsa |
| **Strength (Bala)** | Full Shadbala · Bhava Bala · Vimsopaka (16-Varga) · Harsha Bala · Patyayini · Vaisheshikamsha |
| **Dashas (Timing)** | Vimshottari (4 levels) · Yogini · Chara · Kala Chakra · Narayan · Mandook |
| **Jaimini System** | 7/8 Charakarakas · Arudha Padas (AL-A12) · Upapada · Karakamsha · Swamsha · Rajayogas |
| **Advanced Systems** | KP System (SSL, Significators A-D, Ruling Planets) · Tajika (Ithasala, Varsheshwar, Sahams) |
| **Destiny Points** | Bhrigu Bindu · BCP Activation · Pushkar Navamsha · 64th Navamsha · 150 Nadi Amshas |
| **Bio-Rhythms** | Panchapakshi (5-Bird Activities) · Tatva (Elemental Cycles) · Baladi & Deeptadi Avasthas |
| **Inference Framework** | **Deterministic Evidence Engine** · Contradiction Detection · Multi-system Confidence Scoring |

---

## 🏗️ Architecture: The Deterministic Inference Chain

Unlike generic horoscope generators, this application follows a strictly tiered analytical pipeline:

`CALCULATION → ASTROLOGICAL FACTS → STRENGTH ANALYSIS → YOGAS → VARGAS → DASHA → TRANSITS → DOMAIN ANALYSIS → EVENT DETECTION → TIMING → CONTRADICTION ANALYSIS → CONFIDENCE → EXPLANATION`

Every life insight is derived from calculated evidence. If the engine finds conflicting signals (e.g., strong D1 potential but weak D9 fruit), the **Contradiction Engine** alerts the user and adjusts the **Confidence Score**.

---

## 🚀 Key Modules

- **[framework.py](file:///D:/ASTROLOGYPREDICTIONS/app/astrology/predictions/framework.py)**: Centralized inference logic that cross-validates 60+ data layers.
- **[chart.py](file:///D:/ASTROLOGYPREDICTIONS/app/astrology/core/chart.py)**: The "Master Engine" that synthesizes global astrological data into a canonical model.
- **[engine.py](file:///D:/ASTROLOGYPREDICTIONS/app/astrology/predictions/engine.py)**: Aggregates 32+ domain-specific predictions (Career, Wealth, Moksha, etc.).
- **[muhurta.py](file:///D:/ASTROLOGYPREDICTIONS/app/astrology/panchang/muhurta.py)**: Precision timing for surgery, litigation, and financial ventures.

---

## 🤖 AI Explainer (Optional)

The system includes an optional **AI Consultation** layer. The AI *never* replaces deterministic logic; instead, it receives structured astrological facts and "Cosmic Evidence" to provide natural language explanations, acting as a bridge between high-math Jyotish and the user.

---

## 🛠️ Setup & Deployment

### Local Run
```bash
bash install.sh
./start.sh
```

### Docker
```bash
docker-compose up -d
```

### Cloud (Firebase + Cloud Run)
```powershell
.\scripts\deploy.ps1
```

---

## 🛡️ Security & Privacy

All calculations are performed **locally** or within your private cloud instance. Sensitive birth data is stored in encrypted local vaults. The application enforces `FLASK_SECRET_KEY` and utilizes secure production headers (HSTS, CSP) to ensure your cosmic data remains private.

---

## 📜 License
MIT — Professional Jyotish for everyone.
