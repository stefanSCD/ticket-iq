# COMP-002 – Bluetooth Connection Manager

| Field | Value |
|---|---|
| Page ID | PC-033 |
| Component | COMP-002 |
| Version | 2.3.0 (2.3.1 in review) |
| Owner | Radu Ionescu |
| Implements | REQ-001, REQ-002, REQ-004, REQ-007 (draft), REQ-011 – REQ-013 |

## Responsibility

Controls automatic Bluetooth reconnection attempts, retry behavior, connection timing, and cancellation.

## Main functions

- Starts automatic reconnection when both `IgnitionChanged(ON)` and `BT_READY` have been received.
- Requests the ordered device list from COMP-006.
- Sends connection requests to COMP-009 and supervises them.
- Performs the retry according to REQ-004: after a transient failure, a second attempt is made after **1.5 seconds**.
- Gives up the automatic reconnection **30 seconds** after it was started if the phone could not be connected, and moves to `FAILED`.
- Handles manual connection requests from COMP-008.
- Reports state changes to COMP-008 and diagnostic events to COMP-005.

## Connection queue

COMP-009 processes connection-related requests in a queue. In 2.3.0 the reconnection request is queued in FIFO order together with other requests (PBAP leftovers, SDP queries, inquiry). This caused DEF-001 (PC-084). In 2.3.1 COMP-002 marks reconnection requests with priority `HIGH`, and COMP-009 serves them first.

## Phones that refuse the connection

When a phone has removed the vehicle from its own device list, every connection attempt ends with an authentication failure. COMP-002 treats this as a non-transient failure and stops the attempt for the current ignition cycle. The phone stays in the pairing list.

## Concurrency

COMP-002 runs one automatic connection attempt at a time. The connection request for the secondary candidate from COMP-006 is handled after the attempt for the primary candidate has finished or failed.

## Configuration

See PC-046 for all parameters.
