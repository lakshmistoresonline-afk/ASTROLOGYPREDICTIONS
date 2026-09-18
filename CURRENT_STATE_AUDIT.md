# Astro Predictions — Current State Audit (P0.5 / P0.6)

**Current HEAD**: `ed4448497920a8a32bf983cee7ff8f18d2dffdff`  
**Branch**: `main`  
**Python Version**: Python 3.13.0  
**Database**: SQLite (`app.db`) / SQLAlchemy ORM  

---

## 1. Architecture Audit
- **Calculation Core (V3.15)**: Protected calculation core (`chart.py`, `swe_proxy.py`, `ephemeris.py`) verified byte-for-byte identical to baseline SHA-256 hashes.
- **Authentication & Authorization**: Firebase ID token cryptographic verification (`firebase-admin`), session management, `@login_required`, and centralized `@require_admin`.
- **User Ownership**: Strict owner-scoping (`owner_uid`) enforced across SQLite chart vault (`store.py`), Firestore store (`firebase_store.py`), and durable report records (`ReportRecord`).
- **Payment & Commerce**: Admin-controlled UPI/QR payment model, canonical product catalog (`CANONICAL_PRODUCTS`), order creation, proof submission (UTR + screenshot), and atomic/idempotent admin verification queue (`/admin/payments`).
- **Mobile APIs**: Standardized JSON REST endpoints under `/api/v1/mobile/` for dashboard, charts, reports, and user profile.
- **Consumer vs Admin UX**: Consumer dashboard (`dashboard.html`) structured around intuitive life timing and insights; admin business dashboard (`/admin/business`, `/admin/payments`) dedicated to operational revenue and payment verification.
- **Testing**: 439 regression, marketing, commercial, security, and authentication tests passing (100% success rate).
