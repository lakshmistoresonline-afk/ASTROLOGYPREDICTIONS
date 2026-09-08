# V4 Evidence Architecture

## Evidence Ledger (`EvidenceLedger`)
The V4 evidence architecture separates astrological signals into distinct independent evidence families:
- `NATAL`: House lordship, natal promise, and sthana/dignity.
- `DASHA`: Vimshottari dasha/antar dasha activation.
- `TRANSIT`: Planetary ingress, aspect, and transit triggers.
- `VARGA`: Divisional chart confirmation (D9, D10, etc.).
- `YOGA`: Classical yoga formations.

## Confirmation Gate & Abstention
A prediction is only surfaced as strong when:
1. Net evidence score exceeds established thresholds.
2. At least two independent evidence families converge (e.g. Natal Promise + Dasha Activation + Transit Trigger).
3. Contradictions do not outweigh support.

If criteria are not met, the engine abstains and returns `INSUFFICIENT EVIDENCE` or `CONFLICTING SIGNALS`.
