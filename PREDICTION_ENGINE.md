# Prediction Engine Guide

The ASTROLOGYPREDICTIONS platform uses a **Tiered Inference Architecture** to provide professional-grade Vedic insights.

## 🔮 Supported Domains (38+)
The engine provides deep analysis across 38 life areas, including:
- **Essence**: Personality, Life Purpose, Dharma, Creativity, Mental Stability.
- **Material**: Career, Business, Finance, Wealth, Property, Vehicles, Government Authority.
- **Social**: Marriage, Relationships, Children, Family, Parents, Siblings, social Status.
- **Survival**: Health, Longevity, Foreign Travel/Settlement, Legal, Debt, Risk Tolerance.

## ⚙️ How it Works

### 1. Evidence Collection
Every domain predictor (e.g., `career.py`) gathers multiple factors:
- **House Lordship**: Placement and dignity of the primary house lord.
- **Varga Confirmation**: Verification in the relevant divisional chart (e.g., D10 for Career).
- **Ashtakavarga**: Energetic capacity of the house (SAV points).
- **Yogas**: Presence of specific planetary combinations.

### 2. Contradiction Analysis
The engine automatically detects "Mixed Signals":
- **Natal vs. Varga**: e.g., strong H10 in D1 but weak D10 chart.
- **Lord vs. Strength**: e.g., favorable placement but low Shadbala.

### 3. Confidence Scoring
Confidence levels (**LOW**, **MEDIUM**, **HIGH**) are assigned based on the depth and alignment of evidence across various charts.

## ⏳ Timing Integration
Every prediction is cross-referenced with the current **Vimshottari Dasha** and **Transit Support** to indicate if the birth promise is currently "activated".

## 🤖 AI Narrative (Optional)
Optional Large Language Model (LLM) support is used only for **Explanation**. The AI interprets the calculated facts and evidence into human-friendly language without altering the underlying data.
