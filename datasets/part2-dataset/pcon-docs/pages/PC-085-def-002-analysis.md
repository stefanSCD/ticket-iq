# DEF-002 – Missing Reconnection Completion Diagnostic Event – Analysis

| Field | Value |
|---|---|
| Page ID | PC-085 |
| Defect | DEF-002 |
| Severity | Medium |
| Status | In Progress |
| Created | 2026-07-22 |
| Affected component | COMP-005 Connectivity Diagnostics Service |
| Assignee | Elena Rusu |

## Symptom

The diagnostic service does not always record the completion event for a successful reconnection attempt. Found in EXEC-012 (Vehicle, TEST-006); trace TRACE-009.

## Root cause

COMP-005 buffers events in memory and writes them to the ring buffer file every 500 ms. When the infotainment system shuts down within about **200 ms** after the completion event (short ignition cycle in the test), COMP-010 confirms the shutdown after its 800 ms deadline while COMP-005 is still waiting for the HSM-backed file write. The completion event is lost.

## Fix

COMP-005 1.2.1: write COMPLETE and FAIL events synchronously; flush on `ShutdownPrepare` with priority.

## Release

Target version 1.2.1. Whether 1.2.1 is part of R1 or R2 is **not decided** (see PC-063).
