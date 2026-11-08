# COMP-006 – Device Priority Manager

| Field | Value |
|---|---|
| Page ID | PC-037 |
| Component | COMP-006 |
| Version | 1.0.2 |
| Owner | Radu Ionescu |
| Implements | REQ-008, REQ-009 |

## Responsibility

Calculates the order in which paired phones are reconnected and determines the primary and secondary phone.

## Algorithm

1. Read all paired devices from COMP-003.
2. Sort by `lastConnected` timestamp, newest first (MRU, ADR-002).
3. The first entry is the primary candidate, the second the secondary candidate.
4. Return the ordered list to COMP-002.

If the primary candidate cannot be connected, the next device in the list becomes the primary candidate.

## Edge cases

- Phones that have never been connected after pairing have no `lastConnected` timestamp.
- Two phones can have very close timestamps, for example when both were connected during the same drive.

How the algorithm orders devices in these cases is not specified in ADR-002.

## Favourite phone

Product Management requested a "favourite phone" setting that the driver can set in the device list. See open point in ADR-002 (PC-052).
