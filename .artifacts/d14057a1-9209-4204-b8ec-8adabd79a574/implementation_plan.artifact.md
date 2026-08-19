# Implementation Plan: Comprehensive Vedic Astrology Prediction Engine

This plan details the transformation of the Jyotish Dashboard into a professional-grade, evidence-based prediction platform with 32+ domains of life analysis.

## User Review Required

> [!IMPORTANT]
> **Data Model Unification**: We will introduce a `CanonicalChart` model using Pydantic to ensure every prediction module receives consistent, validated astrological facts.
> **Security**: The `.env` file will be moved out of Git tracking to protect your secret keys.

> [!WARNING]
> **Performance**: Calculating D1 through D60, Shadbala, and 100+ Yogas simultaneously is computationally expensive. We will implement a multi-level caching system.

## Proposed Changes

### 1. Foundation & Security
- **Security**: Remove `.env` from Git tracking and update `.gitignore`.
- **Modeling**: Create `app/astrology/core/models.py` with `CanonicalChart` definition.
- **Ephemeris**: Validate Swiss Ephemeris JD calculations and Lahiri ayanamsa implementation.

### 2. Comprehensive Engine Upgrades
- **Nakshatra Engine**: Support for Padas, Lords, Deities, and Symbolism.
- **Strength Engine**: Full Shadbala (all 6 components) and normalized scoring.
- **Varga Engine**: Validation of D1 through D60 divisional charts.
- **Yoga Engine**: Framework for detecting 100+ standard Yogas (Raja, Dhana, Mahapurusha, etc.).
- **Timing Engine**: Unified system for merging Dasha and Transit activation windows.

### 3. Prediction Domain Expansion
We will implement 32+ domain-specific modules in `app/astrology/predictions/`, including:
- **Personality**: Temperament and leadership style.
- **Education**: D24 analysis.
- **Marriage/Relationships**: Deep D9 integration and Upapada Lagna.
- **Career/Business**: D10 analysis and entrepreneurship suitability.
- **Health**: Dusthana analysis (not medical advice).
- **Travel/Foreign**: Rahu and 12th house themes.

### 4. Advanced System Logic
- **Evidence Engine**: Structured JSON output explaining the "Why" behind every score.
- **Contradiction Engine**: Detecting conflicting signals (e.g., strong lord but weak house).
- **Confidence Scoring**: Calculating a reliability index for each domain.

### 5. UI/UX Overhaul
- **Dashboard**: Card-based overview of all life domains.
- **Timelines**: Visual representation of upcoming activation periods.
- **Evidence View**: Expandable sections showing supporting astrological factors.

## Verification Plan

### Automated Tests
- **Golden Charts**: 10 reference charts validated against standard ephemeris (e.g., Jagannatha Hora).
- **Domain Tests**: Verifying that each prediction module returns valid evidence and scores within 0-100.
- **Property-Based Testing**: Using Hypothesis to test coordinate and date boundaries.

### Manual Verification
- Cross-check 5 diverse sample charts to ensure no "hallucinations" or impossible predictions.
- Verify that UI displays "Confidence" levels correctly.
