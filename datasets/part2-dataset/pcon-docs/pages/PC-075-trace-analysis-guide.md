# Test Data and Trace Analysis Guide

| Field | Value |
|---|---|
| Page ID | PC-075 |
| Owner | Elena Rusu |
| Last updated | 2026-08-25 |

## Where to find traces

- HiL and vehicle traces: TraceRepository, searchable by execution ID (EXEC-xxx) and trace ID (TRACE-xxx).
- SiL traces: GitLab CI job artifacts, kept for 14 days.

## Reading a reconnection trace

Look for these lines in order:

1. `Vehicle ignition event received.` (COMP-001)
2. `Bluetooth subsystem available; reconnection request submitted.` (COMP-002)
3. Queue wait warnings from COMP-009, e.g. `Reconnection request remained in the connection queue for X seconds.`
4. `Reconnection completed in X seconds` (INFO if ≤ 10 s, WARN/ERROR if > 10 s)
5. Profile messages from COMP-004.

## Typical patterns

| Pattern | Likely cause | Reference |
|---|---|---|
| Long gap between 2 and the connect request | Queue wait in COMP-009 | DEF-001 |
| "Device service discovery response was delayed." | Slow SDP response by phone | TRACE-004 |
| Completion missing in diagnostic events but present in text trace | Shutdown race | DEF-002 |
| "Media audio profile restoration failed" | A2DP/HFP race | DEF-003 |

## Correlation

Use the `attemptId` (4 hex digits in the trace line) to correlate text traces with diagnostic events from COMP-005.

## Example: EXEC-010

TRACE-006 (ignition event, 08:45:03) → TRACE-007 (queue wait 8.9 s) → TRACE-008 (reconnected after 18.0 s). Classified as DEF-001.
