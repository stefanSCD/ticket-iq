# Reconnection State Machine (COMP-002)

| Field | Value |
|---|---|
| Page ID | PC-042 |
| Owner | Radu Ionescu |
| Last updated | 2026-08-11 |

## States

| State | Description |
|---|---|
| IDLE | No reconnection needed (ignition off or all phones connected) |
| WAIT_BT_READY | Ignition on, waiting for BT_READY from COMP-009 |
| CONNECTING | Connection request sent for the current candidate |
| RETRY_WAIT | First attempt failed with transient error; waiting for retry delay |
| PROFILE_RESTORE | ACL + HFP SLC established; COMP-004 restores further profiles |
| CONNECTED | Phone connected |
| FAILED | Candidate could not be connected |
| SUSPENDED | Low voltage; all attempts paused |

## Transitions

| From | Event | To |
|---|---|---|
| IDLE | IgnitionChanged(ON) | WAIT_BT_READY |
| WAIT_BT_READY | BT_READY | CONNECTING |
| CONNECTING | Connect success | PROFILE_RESTORE |
| CONNECTING | Transient error, retry not used | RETRY_WAIT |
| CONNECTING | Transient error, retry used / non-transient error | FAILED |
| RETRY_WAIT | Retry delay elapsed | CONNECTING |
| PROFILE_RESTORE | Profiles done or timed out | CONNECTED |
| FAILED | Next candidate available | CONNECTING |
| any | LowVoltage(true) | SUSPENDED |
| SUSPENDED | LowVoltage(false) | WAIT_BT_READY |
| any | IgnitionChanged(OFF) | IDLE |

## Give-up timer

A give-up timer of **60 seconds** is started when the state machine leaves `WAIT_BT_READY`. When it expires and no phone is connected, the state machine goes to `FAILED` for all remaining candidates and stops automatic reconnection until the next ignition cycle. The value is configurable (`BT_RECONNECT_GIVEUP_S`, PC-046).

## Timing measurement

The reconnection time used for REQ-002 is measured from entering `CONNECTING` for the first time (which follows BT_READY immediately) to entering `PROFILE_RESTORE`.
