# DEF-003 – Media Audio Profile not Restored – Analysis

| Field | Value |
|---|---|
| Page ID | PC-086 |
| Defect | DEF-003 |
| Severity | High |
| Status | Resolved |
| Created | 2026-07-24 |
| Affected component | COMP-004 Bluetooth Profile Service |
| Assignee | Nina Hoffmann |

## Symptom

The phone reconnects successfully but the media audio profile is not restored in some vehicle executions. Found in EXEC-014 (Vehicle, TEST-005), trace TRACE-010.

## Root cause

COMP-004 3.1.0 started the A2DP connection while the HFP service level connection was still being set up. Some phones (RP-03, RP-09) reject the A2DP connection in this situation, and COMP-004 did not retry it.

## Fix

COMP-004 3.1.1 waits for the HFP SLC to be completely established before starting A2DP. The fix was verified in HiL (TEST-005, all reference phones, 3 runs each) and in the vehicle on MER-P05.

## Notes

The startup sequence page (PC-043) was created before this fix.
