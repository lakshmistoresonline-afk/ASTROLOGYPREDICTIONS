# PRODUCTION ENVIRONMENT REFERENCE (V1.0.0)

## 1. MANDATORY VARIABLES
The application will refuse to start if these are not configured.

| Variable | Purpose | Recommended Source |
| :--- | :--- | :--- |
| `FLASK_SECRET_KEY` | Session signing & security | Hardware Random Hex (64 char) |
| `CALC_SERVICE_URL` | Microservice endpoint | Docker Service Name or Static IP |
| `DATABASE_URL` | Persistent storage | Local Disk (SQLite) or Cloud SQL |
| `LLM_BASE_URL` | Narrative generation (Optional) | Local Ollama or API Gateway |

## 2. INFRASTRUCTURE TARGETS
- **Calculation**: Isolated Docker container (Deterministic).
- **Backend**: Python 3.12+ (Hardened Flask).
- **Frontend**: Compose Multiplatform / Jinja2.

## 3. SECURITY DEFAULTS
- `CORS_ORIGINS`: Restricted to production domains.
- `HSTS`: Enabled (Max-Age 31536000).
- `FAIL_FAST`: Enabled for missing credentials.

---
**Lead Architect**: [Jyotish AI OS]
