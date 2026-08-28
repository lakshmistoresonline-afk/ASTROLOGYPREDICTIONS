# MASTER PENDING IMPLEMENTATIONS

## P0: RELEASE BLOCKERS

| Item | Location | Current State | Impact | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Broken Predictions** | `app/astrology/predictions/*.py` | Incorrect `synthesize` signature. | Runtime error on Marriage, Health, etc. | Refactor and migrate to `engines/`. |
| **Missing Snapshots** | `app/routes.py` | Dashboard doesn't save snapshots on view. | Calibration loop requires snapshot existence. | Implement auto-snapshotting for dashboard predictions. |

## P1: REQUIRED FOR CONTROLLED BETA

| Item | Location | Current State | Impact | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Android Prediction Detail** | `android/MainActivity.kt` | No detail screen. | User can't see 'Why' or 'Evidence'. | Implement Detail Screen with Evidence Chain. |
| **Android Outcome Logic** | `android/MainViewModel.kt` | Shallow outcome reporting. | Only 'OCCURRED' status supported in UI. | Add full status support (Partial, Did not occur). |
| **Dasha Integrity** | `app/astrology/dasha/` | Multiple dasha scripts (Shattrimsha vs Vimshottari). | Conflicting logic paths. | Consolidate to Vimshottari as primary beta standard. |

## P2: POST-BETA ENHANCEMENTS

| Item | Location | Current State | Impact | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Public History Purge** | Git History | Compromised key in old commit. | Potential future risk if public. | Run `git-filter-repo` before public launch. |
| **Lightweight Monitoring** | `app/` | No structured API logging. | Debugging production issues is manual. | Implement basic telemetry. |

---
**Status**: AUDIT COMPLETE. COMMENCING IMPLEMENTATION.
