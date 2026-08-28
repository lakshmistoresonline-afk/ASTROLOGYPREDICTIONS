# RUN LOCAL JYOTISH OS (V1.0.0)

Follow these steps to run the complete Trademind Jyotish AI locally.

## 1. PREREQUISITES
- **Python**: 3.12+ (Required for the Backend)
- **Docker**: (Required for the isolated Calculation Service)
- **Node.js**: (Required for the Web Interface)
- **Android Studio**: (Required to build/run the Android App)

## 2. ENVIRONMENT SETUP
1.  **Clone the Repository**.
2.  **Configuration**:
    ```bash
    cp .env.example .env
    # Edit .env and set FLASK_SECRET_KEY to a random string.
    ```
3.  **Virtual Environment**:
    ```bash
    python -m venv venv
    ./venv/Scripts/activate  # Windows
    source venv/bin/activate # Linux/Mac
    pip install -r requirements.txt
    ```

## 3. START SERVICES
### A. Calculation Service
**Option 1: Docker (Preferred)**
```bash
docker-compose up -d jyotish-calc-service
```

**Option 2: Local (if Docker is missing)**
```bash
# Install consolidated requirements
pip install -r consolidated_requirements.txt
# Run service
./scripts/start_calc_service.ps1  # Windows
# Or manually:
# export PYTHONPATH=calculation_service
# uvicorn app.main:app --port 8000
```

### B. Backend (Python/Flask)
Start the primary intelligence and data layer:
```bash
# Windows
./start.ps1
# Linux/Mac
./start.sh
```

### C. Android App (Compose)
1. Open the `android/` directory in Android Studio.
2. Ensure your emulator or device is connected.
3. **Run**: The app will sync with the backend at `http://10.0.2.2:5001`.

## 4. VERIFICATION
1. Open `http://localhost:5001` in your browser.
2. Create a new birth profile.
3. Verify that Dasha and Predictions appear (Deterministic).
4. Run the test suite:
   ```bash
   pytest tests/test_jyotish_os.py
   ```

## 5. REPOSITORY CLEANUP (Public Release Only)
If you intend to make this repository public, you must purge the history of a previously exposed credential:
```bash
# Requires git-filter-repo
git filter-repo --invert-paths --path scripts/deploy.sh
```
*Note: Credential rotation has already been performed in the current worktree.*

## 6. SHUTDOWN
```bash
# Stop calculation service
docker-compose stop jyotish-calc-service
# Or stop local runners (Ctrl+C)
```

---
**Lead Architect**: [Jyotish AI OS]
