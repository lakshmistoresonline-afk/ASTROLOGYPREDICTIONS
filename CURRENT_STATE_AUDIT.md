# Astro Predictions — Comprehensive Repository Audit (P0.5 / P0.6)

**Current HEAD**: `b9d789c74a46f58724e5b2a166d9d43576ebb1f3`  
**Target Branch**: `main`  
**Protected Calculation Core**: V3.15 (`chart.py`, `swe_proxy.py`, `ephemeris.py` verified byte-for-byte identical).

---

## 1. Architecture Audit Summary
- **Backend Framework**: Flask with SQLAlchemy ORM and Flask-CORS.
- **Authentication**: Firebase Admin SDK (`firebase-admin`) token verification (`check_revoked=True`), session-based identity caching, `@login_required` decorator, and centralized `@require_admin` role validation.
- **Data Ownership**: Strict owner-scoping (`owner_uid`) across SQLite/Firestore data layers (`store.py`, `firebase_store.py`) and durable report records (`ReportRecord`).
- **Payment & Commerce**: Admin-controlled UPI/QR payment model (`PaymentSettings`), canonical product catalog (`CANONICAL_PRODUCTS`), secure order creation, UTR & screenshot payment proof submission, and idempotent admin verification (`/admin/payments`).
- **Mobile APIs**: JSON REST endpoints under `/api/v1/mobile/` covering dashboard, charts, reports, and profile management.
- **Consumer vs Admin UX**: Consumer dashboard (`dashboard.html`) focused on life timing and daily insights; admin business dashboard (`/admin/business`, `/admin/payments`) dedicated to operational revenue and payment approvals.
- **Testing**: 439 regression, marketing, commercial, security, and authentication tests passing (100% success rate).
