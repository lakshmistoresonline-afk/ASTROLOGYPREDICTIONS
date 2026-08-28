# BETA SUPPORT GUIDE (V1.0.0)

This guide provides resolutions for common issues encountered during the Group 1 validation phase.

## 1. CALCULATION SERVICE UNAVAILABLE
- **Symptom**: Error screen stating "Astrological calculation service unavailable."
- **Reason**: The deterministic microservice is down or unresponsive.
- **Resolution**: 
    1. Check Docker container status (`jyotish-calc-service`).
    2. Restart the service.
    3. *Note*: No mock data will be served as fallback.

## 2. AI EXPLANATION FAILURE
- **Symptom**: Raw fact objects are shown instead of narrative explanation.
- **Reason**: Narrative generation (Ollama) is offline or timed out.
- **Impact**: Deterministic astronomical calculations (Planets, Houses, Dashas) remain available independently of AI narrative generation.
- **Resolution**: AI is optional. Continue using fact-based evidence.

## 3. LOGIN / AUTHENTICATION ISSUES
- **Reason**: Expired session or incorrect token.
- **Resolution**: Clear cookies/cache and re-authenticate. Ensure `FLASK_SECRET_KEY` matches current deployment.

## 4. ANDROID APP CRASHES
- **Reason**: API version mismatch or network interruption.
- **Resolution**: 
    1. Verify you are on the latest Beta APK.
    2. Check production API connectivity.
    3. Provide logs to the developer team.

## 5. MISSING PREDICTION DOMAINS
- **Reason**: Engine status is set to "INSUFFICIENT DATA" for safety (e.g., Health).
- **Resolution**: This is intentional. Safety status prevents unverified predictions.

---
**Lead Architect**: [Jyotish AI OS]
