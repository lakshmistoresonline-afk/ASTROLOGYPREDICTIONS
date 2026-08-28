# PHASE 7 SECURITY AUDIT

## 1. AUTHENTICATION & ACCESS
- **Status**: **CAUTION**
- **Findings**: Deployment scripts (`deploy.ps1`, `deploy.sh`) contain a hardcoded `SECRET_KEY`.
- **Risk**: Potential exposure of session signing keys in source control.
- **Fix**: Move `SECRET_KEY` to environment variables or a `.env` file excluded from Git.

## 2. API SECURITY
- **Status**: **VALIDATED**
- **Findings**: Flask is configured with `ALLOWED_ORIGINS` in production mode.
- **Findings**: Security headers (HSTS, CSP, X-Frame-Options) are enforced in `app/__init__.py`.

## 3. INPUT VALIDATION
- **Status**: **VALIDATED**
- **Findings**: Birth coordinates and dates are validated in `external.py` and `datetime.py`.
- **Findings**: Prediction snapshots use UUID-like identifiers in database lookups.

## 4. SECRETS LEAKAGE
- **Status**: **CAUTION**
- **Findings**: Insecure fallback for `secret_key` in `app/__init__.py` ("insecure-dev-only-key").
- **Fix**: Require `FLASK_SECRET_KEY` to be present in ALL environments or fail fast.

## 5. PRIVACY (AI GROUNDING)
- **Status**: **VALIDATED**
- **Findings**: AI layer (Ollama) receives only `evidence_chain` objects containing house/planet indices and generic descriptions.
- **Findings**: No PII (Name, Email, etc.) is sent to AI consultation or explanation endpoints.

**Lead Architect Signature**: [Jyotish AI OS]
