# PRODUCTION BACKUP & RECOVERY PROCEDURES (V1.0.0)

## 1. DATA ASSETS
| Asset | Location | Storage Type |
| :--- | :--- | :--- |
| **User Profiles** | `data/app.db` (SQLite) | Persistent Disk |
| **Prediction Snapshots** | `data/app.db` (SQLite) | Persistent Disk |
| **Outcome Logs** | `data/app.db` (SQLite) | Persistent Disk |
| **Ephemeris Data** | `ephe/` | Static Artifact |

## 2. BACKUP PROCEDURE (LOCAL/DOCKER)
Every 24 hours, perform the following:
1.  **Stop Container**: `docker-compose down` (Ensures data consistency).
2.  **Snapshot SQLite**: `cp data/app.db backups/app_$(date +%F).db`.
3.  **Rotate**: Keep last 30 daily backups.
4.  **Restart**: `docker-compose up -d`.

## 3. RECOVERY PROCEDURE
In the event of database corruption:
1.  **Stop Service**: `systemctl stop jyotish-backend` or `docker-compose down`.
2.  **Restore**: `mv data/app.db data/app.db.corrupt` then `cp backups/app_YYYY-MM-DD.db data/app.db`.
3.  **Verify**: Run `pytest tests/test_jyotish_os.py` to ensure schema integrity.
4.  **Restart**: `docker-compose up -d`.

## 4. PREDICTION SNAPSHOT RECOVERY
Since predictions are immutable:
- Historical predictions can be regenerated from `PredictionOutcome` records using the stored `calculation_version` and `birth_datetime`.
- No data loss occurred if the `raw_data` field in `charts` table is intact.

---
**Lead Architect**: [Jyotish AI OS]
