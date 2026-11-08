# Functional Safety Classification

| Field | Value |
|---|---|
| Page ID | PC-096 |
| Owner | Tobias Kern |
| Last updated | 2026-06-02 |

## Classification

All PCON functions are classified as **QM** (quality managed, no ASIL) according to the item definition of the infotainment system.

## Rationale

- Phone connectivity does not influence vehicle dynamics or any safety-relevant actuator.
- Emergency calls (eCall) are handled by the telematics unit with its own audio path and are out of scope for PCON.
- Driver distraction is addressed by HMI guidelines (e.g. no popups for failed reconnection, REQ-027), not by functional safety.

## Consequences

- Standard QM development process (ASPICE level 2 target) applies.
- No safety requirements are allocated to PCON components.
