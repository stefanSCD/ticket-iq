# COMP-009 – BT Stack Adapter

| Field | Value |
|---|---|
| Page ID | PC-040 |
| Component | COMP-009 |
| Version | 2.0.4 |
| Owner | Andrei Popescu |
| Implements | REQ-020, REQ-021, REQ-023 |

## Responsibility

Wraps the **Nimbus BT Stack 5.2** (supplier: Sylvan Wireless) and is the only component allowed to call the stack API.

## Functions

- Initializes the Bluetooth controller and the stack after startup.
- Emits `BT_READY` when the controller and the stack accept connection requests. Typical time from service start to `BT_READY`: 2.1 – 2.8 s on HU4 B-Sample.
- Maintains the **request queue** for connection-related operations (connect, SDP query, inquiry, PBAP session setup).
- Translates HCI error codes into PCON error codes (PC-048).
- Rejects connection requests from unpaired devices (REQ-023).

## Request queue

| Version | Behavior |
|---|---|
| 2.0.3 and earlier | Strict FIFO |
| 2.0.4 | Supports priority flag `HIGH`; requests with `HIGH` are served before `NORMAL` |

COMP-002 2.3.1 sets `HIGH` for reconnection requests (DEF-001 fix).

## Stack configuration

| Item | Value |
|---|---|
| Page timeout | 5.12 s |
| Supervision timeout | 3 s (REQ-012) |
| Inquiry | Disabled during the first 20 s after BT_READY |
| Controller firmware | Sylvan SWC-4421 v7.3 |

## Supplier interface

Defects in the stack are reported to Sylvan Wireless as described in PC-093.
