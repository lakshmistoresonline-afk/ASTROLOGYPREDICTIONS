# 🔮 Jyotish Dashboard 2.0 — Local Run Guide

This guide explains how to set up and run the Jyotish Dashboard locally on your computer for testing and personal use.

## 🛠️ 1. Prerequisites
- **Python 3.10** or higher.
- A terminal (PowerShell, Command Prompt, or Bash).

## 📦 2. Installation
1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/lakshmistoresonline-afk/ASTROLOGYPREDICTIONS.git
    cd ASTROLOGYPREDICTIONS
    ```
2.  **Create and activate a virtual environment**:
    ```powershell
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Linux / Mac
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ 3. Configuration
Ensure your `.env` file exists in the root directory and contains the following settings for local operation:

```ini
FLASK_SECRET_KEY=a7f03eedd2a10e739cd43152ee574b7d821b412f2f37b1202af8a7035305f9bc
USE_FIREBASE=false
SE_EPHE_PATH=./ephe
PORT=5001
FLASK_ENV=development
```
> [!NOTE]
> Setting `USE_FIREBASE=false` forces the app to use the local **SQLite** database (`data/app.db`) instead of the cloud.

## 🧪 4. Verification (Recommended)
Before running the full dashboard, verify that the core astrology engine and data files are correctly set up:
```bash
python scripts/test_run.py
```
If you see **"🎉 ALL LOCAL CORE TESTS PASSED"**, you are ready to go.

## 🚀 5. Start the Dashboard
Run the following command to launch the web server:
```bash
python run.py
```
The application will automatically attempt to open in your browser at:
👉 **[http://localhost:5001](http://localhost:5001)**

## 🏁 Stopping the app
Press `Ctrl+C` in your terminal to shut down the server.

---
*Note: This mode stores all your saved charts locally in the `data/` folder. If you move the project to another computer, make sure to copy the `data/` folder to keep your charts.*
