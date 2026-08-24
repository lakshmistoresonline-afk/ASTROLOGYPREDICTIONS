# 🔮 Jyotish Dashboard 2.0 — Local Run Guide

This guide explains how to set up and run the Unified Astrology Engine locally for professional-grade predictive analysis.

## 🛠️ 1. Prerequisites
- **Python 3.10** to **3.12** (Python 3.13 may require build tools for some libraries).
- A terminal (PowerShell, Command Prompt, or Bash).
- **C++ Build Tools** (Required for `pyswisseph` and `numpy` if wheels are not available).

## 📦 2. Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/lakshmistoresonline-afk/ASTROLOGYPREDICTIONS.git
    cd ASTROLOGYPREDICTIONS
    ```
2.  **Run the Supreme Doctor**:
    This script will automatically detect and fix most environment issues.
    ```bash
    python scripts/doctor.py
    ```
    > [!IMPORTANT]
    > If `pyswisseph` fails, you **MUST** install **Visual Studio C++ Build Tools** from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

## ⚙️ 3. Configuration
Ensure your `.env` file exists in the root directory:

```ini
FLASK_SECRET_KEY=your_secret_key_here
USE_FIREBASE=false
SE_EPHE_PATH=./ephe
PORT=5001
FLASK_ENV=development
```

## 🧪 4. Verification
Verify the multi-disciplinary engine:
```bash
python scripts/test_run.py
```
This script checks the integration of Vedic, Western, Hellenistic, and East Asian modules.

## 🚀 5. Start the Engine
```bash
python run.py
```
Access the dashboard at: **[http://localhost:5001](http://localhost:5001)**

## 🌟 6. Accessing Advanced Metrics
Once the app is running, use the API or the "Advanced Metrics" section in the UI to see:
- **KP 4-Step Theory** & **Nadi D-150 Amshas**.
- **Human Design Gates** & **Gene Keys**.
- **Bazi Pillars** & **Zi Wei Dou Shu** Palaces.
- **AstroCartoGraphy** Power Longitudes.
- **Zodiacal Releasing** Chapters.
