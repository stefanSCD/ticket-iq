# Cybersecurity Concept – Summary for Connectivity

| Field | Value |
|---|---|
| Page ID | PC-095 |
| Owner | Karim Haddad |
| Last updated | 2026-07-14 |

## TARA result

A Threat Analysis and Risk Assessment was performed for the Bluetooth interface of HU4. The Bluetooth attack surface is rated **"medium"**.

| Threat | Risk | Measure |
|---|---|---|
| Extraction of link keys from flash | High | HSM key wrapping (ADR-003, REQ-022) |
| Impersonation of a paired phone | Medium | SSP Numeric Comparison only (REQ-021) |
| Connection flooding / DoS | Medium | Reject unpaired devices at stack level (REQ-023) |
| Malformed vCards from phone | Medium | Fuzz testing of COMP-007 parser |
| Personal data leakage via logs | Medium | Hashed device IDs in diagnostic events (ADR-005) |

## Residual topics

- Text traces still contain device names and Bluetooth addresses (see PC-049). Whether pseudonymization is required for traces in production builds is open.
- Startup behavior when the HSM is unavailable is open (see ADR-003).

## Security testing

- Fuzzing of PBAP/vCard parser (weekly, SiL).
- Penetration test of the Bluetooth interface by an external lab, planned for C-Sample.
