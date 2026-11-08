# ADR-006 – Block Inquiry during Startup

| Field | Value |
|---|---|
| Page ID | PC-056 |
| Status | **Accepted** (2026-08-07) |
| Deciders | Andrei Popescu, Tobias Kern |

## Context

During the analysis of DEF-001, traces showed that inquiry (device discovery) started by the HMI device list screen at startup occupied the radio and the request queue of COMP-009 while COMP-002 tried to reconnect the phone.

## Decision

Inquiry is blocked for **20 seconds** after BT_READY (parameter `BT_INQUIRY_BLOCK_S`). Inquiry requests during this time are delayed, not rejected. If the driver explicitly opens the "Add device" screen, the block is lifted immediately.

## Consequences

- The "Add device" screen may need up to a few seconds longer to show devices if opened early – accepted by HMI (Jonas Weber).
- This decision complements, but does not replace, the priority queue (DEF-001 fix).
