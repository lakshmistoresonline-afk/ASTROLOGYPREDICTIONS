# Trademind Jyotish AI V2 — Baseline Audit Report

## 1. CURRENT STATE (V1.0.2)
- **Engine**: Reliable Swiss Ephemeris (Deterministic) + Pydantic models.
- **Predictions**: 16 life domains implemented using a hierarchical evidence chain.
- **UI**: Clean but "developer-centric" layout. Functional sidebar and bento-style dashboard.
- **Mobile**: Responsive but basic single-column fallback.
- **Tracking**: Preliminary outcome reporting system implemented.

## 2. CORE PROBLEMS IDENTIFIED
### A. Prediction Quality (The "Intelligence" Gap)
- **Single-Threaded Evidence**: While hierarchical, it doesn't elegantly handle **Confluence** (multiple factors agreeing to amplify strength) or **Contradictions** (limiting factors reducing confidence).
- **Weak Explanation**: Predictions are often one-paragraph summaries. Users can't see the "Why" node-by-node (Planet -> House -> Aspect).
- **Static Timing**: "Timing Windows" are calculated but often lack specific "Peak" vs "Build-up" nuances in the UI.
- **Remedy Disconnect**: Remedies are listed but not deeply linked to the specific evidence node that triggered them.

### B. User Experience (The "Premium" Gap)
- **Data Overload**: Technical terms like "Shadbala" or "Varga Confirm" are shown without progressive disclosure.
- **Navigation Clutter**: Sidebar is growing too long. Needs better information architecture (Groups for Chart, Predictions, Tools).
- **Visual Noise**: Heavy reliance on plain Bootstrap-looking components in some areas.
- **Missing Visualization**: No visual Dasha timeline, no Transit impact graph, and no Evidence Chain diagram.
- **Onboarding**: "New Profile" is a single long form. Needs a stepped, premium experience.

## 3. MISSING FEATURES (Requirements for V2)
- [ ] **Unified Evidence Graph**: A data structure that links every prediction to its astronomical root.
- [ ] **Contradiction Engine**: Logic to explicitly deduct score if malefics aspect a benefic promise.
- [ ] **Peak Activation Logic**: Distinguishing between Mahadasha vs Transit triggers for specific peak dates.
- [ ] **Visual Dasha Explorer**: Interactive horizontal timeline.
- [ ] **Transit Impact Map**: Personalized view of "Current Sky vs My Chart."
- [ ] **V2 Home Dashboard**: Polished hero section, Today's Cosmic Status, and Priority Insights.
- [ ] **Stepped Profile Creation**: Multi-step "Ritual" for entering birth data.

## 4. TECHNICAL DEBT
- **Encoding Issues**: Some files recently had encoding conflicts (UTF-16 vs UTF-8).
- **Duplicate Logic**: Varga logic is repeated in several engines. Needs a unified utility.
- **Process Management**: Double-tab opening on start and orphan Python processes.

---
**Verdict**: The system has a strong deterministic foundation but lacks the "Intelligence Layer" and "Premium Polish" required to compete with professional Jyotish platforms.
