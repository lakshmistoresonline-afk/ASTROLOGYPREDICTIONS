# PHASE 6 UI AUDIT

## 1. CURRENT SCREENS (WEB)
- **Home (`index.html`)**: Landing page with profile vault and basic sky intelligence.
- **Dashboard (`dashboard.html`)**: Summary view with resonance score, domain forecasts, and immediate timing.
- **Predictions (`predictions.html`)**: Detailed domain-specific audits with hierarchical evidence and remedies.
- **Kundli (`kundli.html`)**: Classic chart visualization.
- **Dasha (`dasha.html`)**: Timeline of life periods.
- **Transit (`transit.html`)**: Live planetary positions.

## 2. NAVIGATION
- Sidebar/Header based navigation.
- Category-based switching in predictions view.

## 3. BIRTH PROFILE FLOW
- Current flow collects Name, Date, Time, and Location.
- **Gap**: Missing "Birth-Time Confidence" selection (HIGH/MEDIUM/LOW/UNKNOWN).

## 4. DASHBOARD ANALYSIS
- Displays resonance score and categorized forecasts.
- **Gap**: Needs clearer prioritization: TOP PREDICTION, NEXT IMPORTANT WINDOW, TOP REMEDY.
- **Gap**: Missing 7-day, 30-day, and 12-month outlook blocks.

## 5. PREDICTION DISPLAY
- Shows resonance % and summary text.
- **Gap**: Every card must explicitly show WHAT, WHEN (PEAK), WHY (Evidence), STRENGTH, and WHAT TO DO.

## 6. REMEDY SYSTEM
- Displays Mantra, Charity, and Lifestyle.
- **Gap**: Missing priority ranking (HIGH/MEDIUM/SUPPORTIVE/OPTIONAL).
- **Gap**: No tracking mechanism for Start/Complete/Streak.

## 7. ANDROID STATUS
- Native Kotlin/Compose shell initialized.
- **Gap**: Lacks real API integration and deep features (Tracking, Why?, Quality Dashboard).

## 8. ERROR & LOADING STATES
- Basic loading spinners.
- **Gap**: Missing explicit "Calculation Service Unavailable" (Determinism failure) UI state.

---
**Audit Conclusion**: The UI is aesthetically strong but requires a "Decision-System" refactor to match the high-precision backend capabilities.
