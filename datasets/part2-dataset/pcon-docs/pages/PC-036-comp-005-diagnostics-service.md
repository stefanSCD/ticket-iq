# COMP-005 – Connectivity Diagnostics Service

| Field | Value |
|---|---|
| Page ID | PC-036 |
| Component | COMP-005 |
| Version | 1.2.0 (1.2.1 planned) |
| Owner | Elena Rusu |
| Implements | REQ-006 |

## Responsibility

Records diagnostic events and timing information for Bluetooth connection attempts.

## Event storage

- Events are stored in a persistent **ring buffer of 500 events**.
- When the buffer is full, the oldest events are overwritten.
- The buffer can be read by the workshop tester through the diagnostic routine `ReadConnectivityEvents` (0x31 01 F2 10).

## DTC handling

COMP-005 evaluates events and sets DTCs through the Diagnostics Platform API (see DTC catalog PC-089).

## Backend upload

The Telematics team offered to upload the reconnection events to the vehicle backend for fleet analytics. This would allow monitoring reconnection times in the field after SOP. **Open point:** whether reconnection events are uploaded, and if yes which fields, has not been decided. Privacy review would be required (Karim Haddad).

## Known issue

DEF-002 – the completion event is not always recorded (PC-085). Fix planned in 1.2.1.
