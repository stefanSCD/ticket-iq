# Test Catalog – Reconnection (TEST-001 … TEST-010)

| Field | Value |
|---|---|
| Page ID | PC-070 |
| Owner | Sofia Brandt |
| Last updated | 2026-07-01 |

| Test | Title | Verifies | Expected result |
|---|---|---|---|
| TEST-001 | Automatic reconnection after ignition | REQ-001 | Phone reconnects automatically without user interaction |
| TEST-002 | Reconnection time verification | REQ-002 | Phone reconnects within 10 s |
| TEST-003 | Stored pairing reuse | REQ-003 | No new pairing confirmation |
| TEST-004 | Transient failure retry | REQ-004 | One retry, then successful reconnection |
| TEST-005 | Bluetooth profile restoration | REQ-005 | Phone audio and media audio available |
| TEST-006 | Reconnection diagnostic logging | REQ-006 | Start, completion, result and duration events recorded |
| TEST-007 | Repeated ignition cycle reconnection | REQ-001, REQ-002 | Reconnection within 10 s in each of 5 cycles |
| TEST-008 | Weak-signal reconnection retry | REQ-002, REQ-004 | Retry if needed, reconnection within 10 s |
| TEST-009 | Delayed phone availability | REQ-001, REQ-004 | Phone available 3 s after ignition is detected and reconnected |
| TEST-010 | Cold-start reconnection performance | REQ-002 | Reconnection within 10 s after Bluetooth becomes available |

## Pass/fail rules

- For tests verifying REQ-002, a single execution is **FAIL** when the measured reconnection time exceeds 10 s, even if all other checks pass.
- TEST-007 is FAIL when any of the five cycles fails.
- TEST-006 is FAIL when any of the expected events is missing.

## Planned extensions

- TEST-011 … TEST-013: link-loss reconnection (REQ-011, REQ-012), HiL with link-loss attenuation profile.
- TEST-014: manual reconnection (REQ-013).
