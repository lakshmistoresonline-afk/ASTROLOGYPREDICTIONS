# Implementation Plan: Fix Cloud 500 Internal Server Error

The application is returning a 500 error because it is still attempting to import from `app/astrology/calculator.py`, which was deleted during the modular upgrade.

## User Review Required

> [!IMPORTANT]
> This fix removes the last remaining reference to the legacy `calculator.py` file and completes the transition to the 2.0 engine.

## Proposed Changes

### 1. Route Cleanup

#### [MODIFY] [routes.py](file:///G:/Astrology%20Prediction/app/routes.py)
- Remove `from .astrology.calculator import ...`
- Implement the missing `rahu_kaal` logic directly in the compatibility helper or move it to `app/astrology/panchang/`.

### 2. Rahu Kaal Logic Porting

#### [MODIFY] [panchang/sky.py](file:///G:/Astrology%20Prediction/app/astrology/panchang/sky.py)
- Add `get_kaal_timings` to calculate Rahu Kaal, Gulika Kaal, and Yamaghanta using precise sunrise/sunset times.

## Verification Plan

### Automated Tests
- Run `ruff check` and `mypy` to ensure no more missing imports exist.

### Manual Verification
- Redeploy and verify the home page loads correctly.
