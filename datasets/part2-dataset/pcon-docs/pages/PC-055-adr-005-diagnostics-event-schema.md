# ADR-005 – Diagnostics Event Schema

| Field | Value |
|---|---|
| Page ID | PC-055 |
| Status | **Accepted** (2026-07-29) |
| Deciders | Elena Rusu, Tobias Kern |

## Context

REQ-006 requires diagnostic events for start, completion, failure and duration of each reconnection attempt. The events are consumed by workshop diagnostics, by test automation (HiL), and potentially by a backend.

## Decision

All events use the following structure:

| Field | Type | Description |
|---|---|---|
| eventType | enum | RECONNECT_START, RECONNECT_COMPLETE, RECONNECT_FAIL, RECONNECT_DURATION, PROFILE_FAIL |
| timestamp | uint64 | ms since epoch (UTC) or since boot if time is not synchronized |
| deviceIdHash | bytes[8] | Truncated SHA-256 of BD_ADDR + vehicle salt |
| attemptId | uint16 | Increments per attempt; same for all events of one attempt |
| durationMs | uint32 | Only for RECONNECT_DURATION |
| resultCode | uint8 | PCON result code (PC-048) |
| swVersion | string[16] | Version of COMP-002 |

## Rationale

- Hashing the BD_ADDR avoids storing personal data in the diagnostic buffer.
- `attemptId` allows correlating events with text traces.

## Consequences

- Test automation reads the events via the diagnostic routine (PC-036).
- Any backend upload (still undecided, see PC-036) would use the same fields.

## Not covered

How future changes to this schema are handled (e.g. adding fields while older readers exist) was not part of this decision.
