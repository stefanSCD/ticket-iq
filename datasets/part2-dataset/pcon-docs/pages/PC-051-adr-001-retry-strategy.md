# ADR-001 – Single Retry with Fixed Delay

| Field | Value |
|---|---|
| Page ID | PC-051 |
| Status | **Accepted** (2026-06-19) |
| Deciders | Tobias Kern, Andrei Popescu, Radu Ionescu, Mara Lindqvist |

## Context

REQ-004 requires a retry when the first reconnection attempt fails because of a transient communication error. The number of retries and the delay were not fixed by the requirement. The 10-second limit of REQ-002 limits how much time can be spent on retries: a page timeout alone takes 5.12 s.

## Options

1. **Single retry with a fixed delay.**
2. Up to three retries with exponential backoff (1 s, 2 s, 4 s).
3. Continuous retries until the give-up timer expires.

## Decision

Option 1: **exactly one retry**, after a fixed delay of **2 seconds**.

## Rationale

- With a page timeout of 5.12 s, a second retry can never finish within 10 s.
- The 2-second delay gives the phone time to finish its own Bluetooth activities (e.g. a connection to a headset that is being released) and reduces the chance that the retry fails for the same reason.
- Exponential backoff adds complexity without benefit within the 10-second window.
- Continuous retries would block the radio for the secondary phone.

## Consequences

- REQ-004 is interpreted as "one retry" (PC-015).
- Phones that are not reachable within the first attempt plus one retry are handled by the give-up logic (PC-042).
- The test TEST-004 verifies exactly one retry.
