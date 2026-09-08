# Astro Predictions (Jyotish OS)

A professional-grade Vedic Astrology Prediction & Remedy system built on deterministic astronomical calculations.

---

## 🏛️ Core Philosophy

1.  **Deterministic Calculations**: We never ask AI to calculate planetary positions. Every degree is computed using the Swiss Ephemeris.
2.  **Multi-Factor Corroboration**: No major prediction is made from a single factor. We corroborate D1, Varga, Dasha, and Transits.
3.  **Explainability**: Every insight includes the "Why", "When", and "How Strong".
4.  **Personalized Remedies**: Prioritized traditional remedies linked to specific chart issues.
5.  **Prediction Tracking**: Feedback loop for continuous accuracy improvement.

## ✨ High-Precision Vedic Features

| Feature | Description |
|---|---|
| **Deterministic Engine** | Real planetary longitudes, retrograde status, and combustion. |
| **Vimshottari Dasha** | Multi-level period calculation for precise timing. |
| **16 Divisional Charts** | D1 to D60 support for specialized domain analysis (Career, Marriage, etc.). |
| **Yoga Detection** | 100+ rule-based classical combinations (Raja, Dhana, Nabhasa). |
| **Evidence Synthesis** | Corroboration of natal potential with current dasha and transits. |

## 🛠️ Requirements

-   **Python 3.10+**
-   **Swiss Ephemeris (pyswisseph)**: Mandatory for core calculations. 
    -   *Windows*: Requires Visual C++ Build Tools.
    -   *Linux*: `apt-get install libswe-dev`
-   **Local AI (Optional)**: Support for Ollama/Llama3 for natural language explanations.

## 🚀 Getting Started

1.  Install dependencies: `pip install -r requirements.txt`
2.  Ensure `swisseph` is properly installed. If you encounter build errors, ensure your C++ compiler is configured.
3.  Run the server: `python run.py`
