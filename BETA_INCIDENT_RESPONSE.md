# BETA INCIDENT RESPONSE (V1.0.0)

## 1. CALCULATION FAILURE
- **Trigger**: `ASTROLOGY_CALCULATION_UNAVAILABLE` error.
- **Action**: Check `jyotish-calc-service` Docker logs. Restart container.
- **Rule**: Do NOT serve mock data during outage.

## 2. DATA CORRUPTION
- **Trigger**: Database integrity check fails.
- **Action**: Run `python scripts/db_recovery.py`. Restore from last 24h backup.

## 3. SECURITY INCIDENT
- **Trigger**: Suspicious API patterns or credential exposure.
- **Action**: Rotate `FLASK_SECRET_KEY` immediately. Notify beta group.

## 4. ANDROID CRASH
- **Trigger**: Multiple reports in Group 1.
- **Action**: Verify API version parity. Deploy hotfix build.
