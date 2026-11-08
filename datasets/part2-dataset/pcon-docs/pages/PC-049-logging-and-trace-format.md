# Logging Conventions and Trace Format

| Field | Value |
|---|---|
| Page ID | PC-049 |
| Owner | Elena Rusu |
| Last updated | 2026-08-25 |

## Trace line format

```
<ISO-8601 timestamp> <LEVEL> <component> <attemptId> <message>
```

Example:

```
2026-07-21T08:45:03.120 INFO COMP-001 - Vehicle ignition event received.
2026-07-21T08:45:12.004 WARN COMP-009 a7f3 Reconnection request remained in the connection queue for 8.9 seconds.
2026-07-21T08:45:21.007 ERROR COMP-002 a7f3 Phone reconnected in 18.0 seconds and exceeded the 10-second limit.
```

## Levels

| Level | Use |
|---|---|
| ERROR | Requirement violated or function failed |
| WARN | Unexpected but recovered situation |
| INFO | State changes, start/end of attempts |
| DEBUG | Detailed protocol information |

Development and HiL builds log at DEBUG level.

## Trace repository

Traces of HiL and vehicle executions are uploaded to the TraceRepository and linked to the execution ID (TRACE-xxx).

## Diagnostic event buffer

In addition to text traces, COMP-005 keeps a ring buffer of the last **1000** diagnostic events which survives power cycles.

## Personal data in traces

Traces currently contain the device name reported by the phone (often the owner's first name) and the BD_ADDR. Whether device names and addresses must be pseudonymized in traces is an **open point** with the Cybersecurity team.
