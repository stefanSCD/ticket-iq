# Diagnostic Trouble Code Catalog – Connectivity

| Field | Value |
|---|---|
| Page ID | PC-089 |
| Owner | Elena Rusu |
| Last updated | 2026-09-01 |

| DTC | Name | Set condition | Component |
|---|---|---|---|
| B1A10 | Bluetooth module not responding | BT_READY not received within 10 s after component start in 3 consecutive power cycles | COMP-009 / COMP-005 |
| B1A11 | Pairing storage corrupted | COMP-003 cannot read pairing records (CRC error) at startup | COMP-003 / COMP-005 |
| B1A12 | Repeated reconnection failure | Automatic reconnection failed in N consecutive ignition cycles although a paired phone was reachable | COMP-002 / COMP-005 |

## B1A12 – open point

The value of **N is not decided**. Diagnostics Platform guidelines recommend 3 or 5. The team needs to agree how "phone was reachable" is determined (e.g. phone seen during inquiry later in the cycle).

## Freeze frame data

All DTCs store: SW version, power mode, battery voltage, number of paired devices, last PCON result code.

## Workshop

DTCs are readable with the standard workshop tester; the event buffer with `ReadConnectivityEvents` (PC-036).
