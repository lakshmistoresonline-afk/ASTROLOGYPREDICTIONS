# AI GROUNDING VALIDATION

## 1. DATA CONSTRAINTS
- **AI Access**: The AI Provider (Ollama/Llama3) only receives structured **Facts** from the Deterministic Calculation Engine.
- **Strict Forbidden Actions**: 
  - AI cannot calculate longitudes.
  - AI cannot determine Dasha dates.
  - AI cannot invent Yogas.

## 2. OUTPUT VALIDATION
- Every AI-generated explanation is prefixed by the raw facts to ensure transparency.
- The UI separates "Astronomical Facts" from "AI Insights".

## 3. PROMPT SAFETY
- Prompts are restricted to "interpretation and explanation".
- System prompt enforces a Master Jyotishi persona that refers back to specific chart placements (D1/D9).

**Status**: **VERIFIED**
