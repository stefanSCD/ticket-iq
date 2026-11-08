# REQ-003 – Reuse Stored Pairing Information

| Field | Value |
|---|---|
| Page ID | PC-014 |
| Requirement | REQ-003 |
| Priority | High |
| Status | Approved |
| Implemented by | COMP-003 Pairing Data Store |
| Verified by | TEST-003 |

## Requirement text

> The system shall use stored pairing information to reconnect the phone without requiring the user to repeat the pairing process.

## Stored information

For every paired phone the Pairing Data Store keeps:

- Bluetooth device address (BD_ADDR);
- device name as reported by the phone at pairing time;
- link key (encrypted, see PC-053);
- link key type (authenticated / unauthenticated);
- supported profiles discovered at pairing time (SDP record cache);
- timestamp of the last successful connection (used by the MRU rule);
- user settings per phone (e.g. phonebook sync enabled).

## Behavior

- On reconnection, the stored link key is used for authentication; no numeric comparison is shown.
- If the phone reports that the key is missing (the user deleted the vehicle on the phone), authentication fails with "PIN or key missing" (HCI error 0x06). In this case the pairing entry is **not** deleted automatically; the HMI shows the phone as "Not available".
- The SDP cache is refreshed after each successful connection.

## Acceptance criteria

1. After an ignition cycle, the phone reconnects without any pairing confirmation on the phone or in the vehicle.
2. Pairing information survives a complete power-down of the head unit (cold start, see TEST-010).
