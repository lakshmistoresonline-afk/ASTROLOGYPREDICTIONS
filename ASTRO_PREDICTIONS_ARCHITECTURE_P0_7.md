# Astro Predictions — Architecture Map (P0.7)

```
                    ASTRO PREDICTIONS
                           │
             ┌─────────────┴─────────────┐
             │                           │
       PUBLIC WEBSITE               MOBILE APP
             │                           │
             └─────────────┬─────────────┘
                           │
                    API V1 / AUTH
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
      USERS             COMMERCE         ASTROLOGY
        │                  │                  │
   Charts/Reports     Orders/Payments    Calculation
   Timeline/Remedies  Subscriptions      Evidence
        │              Entitlements       Dasha
        │                  │              Transit
        └──────────────────┼────────────── Varga
                           │
                           ▼
                   PREDICTION ENGINE
                           │
                           ▼
                    EVIDENCE LEDGER
                           │
                           ▼
                  USER-FACING INSIGHT
                           │
                           ▼
              Optional AI NARRATION ONLY
```

## 1. Subsystems
- **Authentication**: Firebase Admin SDK token verification (`check_revoked=True`), session-based identity, `@login_required`, and centralized `@require_admin`.
- **User Ownership**: Strict owner-scoping (`owner_uid`) across SQLite chart vault, Firestore store, and durable report records (`ReportRecord`).
- **Payment & Commerce**: Admin-controlled UPI/QR payment model (`PaymentSettings`), canonical server-authoritative product catalog (`CANONICAL_PRODUCTS`), UTR proof submission, and idempotent admin verification.
- **Mobile APIs**: JSON REST endpoints under `/api/v1/mobile/` supporting dashboard, charts, reports, and profile management.
- **Astrology Core (V3.15)**: Protected, frozen deterministic calculation core (`chart.py`, `swe_proxy.py`, `ephemeris.py`).
