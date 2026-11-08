# REQ-004 – Transient Reconnection Retry

| Field | Value |
|---|---|
| Page ID | PC-015 |
| Requirement | REQ-004 |
| Priority | Medium |
| Status | Approved |
| Implemented by | COMP-002 Bluetooth Connection Manager |
| Verified by | TEST-004, TEST-008, TEST-009 |

## Requirement text

> The system shall retry the Bluetooth connection once when the first reconnection attempt fails because of a transient communication error.

## Interpretation

- The number of retries is **one** (one initial attempt plus one retry).
- The retry is performed after a delay; the delay value is defined in ADR-001 (PC-051).
- The retry is only performed for errors classified as transient. The classification of HCI error codes is maintained in the error handling page (PC-048).
- For non-transient errors (e.g. authentication failure because the key is missing) no retry is performed.
- The retry is part of the same reconnection attempt and therefore within the REQ-002 time interval.

## Scope

REQ-004 covers the connection establishment (ACL and HFP SLC). It does not specify any behavior for failures that occur later, during restoration of individual profiles.

## Acceptance criteria

1. When the first connection attempt fails with a transient error, exactly one retry is performed.
2. When the retry also fails, COMP-002 reports `FAILED` and a `RECONNECT_FAIL` diagnostic event is recorded.
3. No retry is performed for non-transient errors.
