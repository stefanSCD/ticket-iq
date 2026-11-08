# DEF-001 – Delayed Bluetooth Reconnection after Ignition – Analysis

| Field | Value |
|---|---|
| Page ID | PC-084 |
| Defect | DEF-001 |
| Severity | **Critical** |
| Status | Open (fix in review) |
| Created | 2026-07-17 |
| Affected component | COMP-002 Bluetooth Connection Manager |
| Assignee | Radu Ionescu |

## Symptom

Bluetooth reconnection sometimes exceeds the 10-second requirement because the connection request remains queued longer than expected.

## Affected executions

| Execution | Env | Time (s) |
|---|---|---|
| EXEC-003 | SiL | 12.1 |
| EXEC-006 | HiL | 15.4 |
| EXEC-008 | HiL | 13.8 |
| EXEC-010 | Vehicle | 18.0 |
| EXEC-016 | Vehicle | 11.6 |

## Root cause

COMP-009 processed connection-related requests in strict FIFO order. At startup, the queue already contained:

- SDP queries left from the previous session's service discovery,
- an inquiry started by the HMI device list screen,
- PBAP session setup requests for a phone that was not in range.

The reconnection request of COMP-002 was placed behind them. TRACE-007 shows 8.9 s queue wait in EXEC-010.

## Fix

1. COMP-009 2.0.4: priority flag for queue entries.
2. COMP-002 2.3.1: reconnection requests sent with priority `HIGH`.
3. ADR-006: inquiry blocked for 20 s after BT_READY.

## Verification plan

- HiL: TEST-002, TEST-007, TEST-008 with all reference phones.
- Vehicle: TEST-002 and TEST-007 on MER-P03 and MER-P05.

## Severity

The defect violates REQ-002 (priority Critical) in normal use and was observed in every environment. Severity Critical as reported.
