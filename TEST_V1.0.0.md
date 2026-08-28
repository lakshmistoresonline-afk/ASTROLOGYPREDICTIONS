# TEST JYOTISH OS (V1.0.0)

This guide outlines the verification protocol for the V1.0.0 release.

## 1. SMOKE TEST (QUICK)
Run the core regression suite:
```bash
$env:FLASK_SECRET_KEY="test-secret"; $env:PYTHONPATH="."; pytest tests/test_jyotish_os.py
```

## 2. DETERMINISTIC CALCULATION
Verify Sun position for a known date:
1. Create profile: 1990-01-01 12:00 Delhi.
2. Verify **Sun in Sagittarius (Dhanu)**.
3. Verify **Ayanamsa ~23.7** (Lahiri).

## 3. PLATFORM SYNC
1. View a prediction on the **Web Dashboard**.
2. Open the **Android App**.
3. Verify the **Match Rate** and **Dasha** are identical.

## 4. FAILURE MODES
### Calculation Service Offline
1. Stop the Docker container.
2. Refresh the dashboard.
3. Result: **"Astrological calculation service unavailable"** shown. No mock data.

### AI Unavailable
1. Disable Ollama or remove `LLM_BASE_URL`.
2. Open a prediction detail.
3. Result: **Evidence chain visible**; narrative explanation shows "AI unavailable".

## 5. OUTCOME TRACKING
1. Generate a prediction.
2. Click **REPORT MATCH**.
3. Select **OCCURRED** and set a date.
4. Verify the **Admin Dashboard** reflects the new case.

---
**Lead Architect**: [Jyotish AI OS]
