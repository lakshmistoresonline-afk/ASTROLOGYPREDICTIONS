# Astro Predictions — Current State Baseline (P0/P1)

**Current HEAD**: `f91774c21a5515184345274439424cf2a87f53f3`  
**Branch**: `main`  
**Python Version**: Python 3.13.0  
**Database**: SQLite (`app.db`) / SQLAlchemy ORM  
**Protected Calculation Core**: V3.15 (`chart.py`, `swe_proxy.py`, `ephemeris.py` verified byte-for-byte identical to baseline SHA-256 hashes).

---

## 1. Baseline Architecture Summary
- **Authentication**: Firebase Admin SDK token verification (`check_revoked=True`), session-based identity, `@login_required`, and centralized `@require_admin`.
- **User Ownership**: Strict owner-scoping (`owner_uid`) enforced across SQLite chart vault (`store.py`), Firestore store (`firebase_store.py`), and durable report records (`ReportRecord`).
- **Payment & Commerce**: Admin-controlled UPI/QR payment model (`PaymentSettings`), canonical product catalog (`CANONICAL_PRODUCTS`), secure order creation, UTR & screenshot payment proof submission, and idempotent admin verification (`/admin/payments`).
- **Mobile APIs**: Standardized JSON REST endpoints under `/api/v1/mobile/` supporting dashboard, charts, reports, and profile management.
- **Consumer vs Admin UX**: Consumer dashboard (`dashboard.html`) focused on life timing and daily insights; admin business dashboard (`/admin/business`, `/admin/payments`) dedicated to operational revenue and payment verification.
- **Testing**: 439 regression, marketing, commercial, security, and authentication tests passing (100% success rate).
