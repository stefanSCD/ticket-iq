# Release Notes – Connectivity SW 2.3.0

| Field | Value |
|---|---|
| Page ID | PC-091 |
| Owner | Petra Novak |
| Release date | 2026-07-10 |

## Component versions

| Component | Version |
|---|---|
| COMP-001 Vehicle State Adapter | 1.2.0 |
| COMP-002 Bluetooth Connection Manager | 2.3.0 |
| COMP-003 Pairing Data Store | 1.4.1 |
| COMP-004 Bluetooth Profile Service | 3.1.0 |
| COMP-005 Connectivity Diagnostics Service | 1.2.0 |
| COMP-006 Device Priority Manager | 1.0.2 |
| COMP-007 Phonebook Sync Service | 1.1.0 |
| COMP-008 HMI Connectivity Presenter | 1.3.0 |
| COMP-009 BT Stack Adapter | 2.0.3 |
| COMP-010 Power Mode Manager interface | 1.0.0 |
| Nimbus BT Stack | 5.2.3 |

## New

- Automatic reconnection after ignition with single retry (REQ-001 … REQ-004, ADR-001).
- Profile restoration HFP, A2DP, AVRCP (REQ-005).
- Diagnostic events for reconnection (REQ-006, ADR-005).
- MRU-based multi-phone handling (ADR-002).
- Encrypted link-key storage with HSM wrapping (ADR-003).

## Known issues

- Reconnection time can exceed 10 s (later reported as DEF-001).
- See known issues list PC-087.

## Not included

- Delta phonebook sync (ADR-004) – planned for COMP-007 1.2.0.
- Inquiry blocking (ADR-006).
