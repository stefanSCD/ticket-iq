# REQ-007 – Handle Bluetooth-Disabled Phones

| Field | Value |
|---|---|
| Page ID | PC-018 |
| Requirement | REQ-007 |
| Priority | Low |
| Status | **Draft** |
| Implemented by | COMP-002 (planned) |
| Verified by | – (no test yet) |

## Requirement text (draft)

> The system shall stop automatic reconnection attempts when Bluetooth is disabled on the paired phone.

## Problem

When Bluetooth is disabled on the phone, the head unit cannot distinguish this case from "phone out of range": in both cases the page procedure times out. Repeated paging consumes radio time and can delay reconnection of other phones.

## Open points

- **Detection method not decided.** Options discussed: (a) stop after the give-up timer as for any unreachable phone, (b) use the "last seen" information from BLE advertising, (c) rely on the phone sending a disconnect reason before switching Bluetooth off. None of them has been selected.
- **Release assignment not decided.** It is open whether REQ-007 becomes part of R1 or moves to R2.

Until these points are decided, REQ-007 remains in Draft and is excluded from release verification.
