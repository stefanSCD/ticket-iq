# REQ-006 – Record Reconnection Diagnostics

| Field | Value |
|---|---|
| Page ID | PC-017 |
| Requirement | REQ-006 |
| Priority | Medium |
| Status | Approved |
| Implemented by | COMP-005 Connectivity Diagnostics Service |
| Verified by | TEST-006 |

## Requirement text

> The system shall record diagnostic events for the start, completion, failure, and duration of each reconnection attempt.

## Events

| Event | Emitted when |
|---|---|
| RECONNECT_START | COMP-002 starts a reconnection attempt |
| RECONNECT_COMPLETE | COMP-002 reaches `CONNECTED` |
| RECONNECT_FAIL | COMP-002 reaches `FAILED` |
| RECONNECT_DURATION | Together with COMPLETE or FAIL; contains the duration in ms |

The full event schema is defined in ADR-005 (PC-055).

## Known issue

DEF-002: the completion event is not always recorded (see PC-085).

## Acceptance criteria

1. For every reconnection attempt exactly one START and exactly one COMPLETE or FAIL event is recorded.
2. The DURATION event contains the same value as the reconnection time measured according to REQ-002.
