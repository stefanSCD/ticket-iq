# Performance Measurement Method – Reconnection Time

| Field | Value |
|---|---|
| Page ID | PC-074 |
| Owner | Sofia Brandt |
| Last updated | 2026-08-30 |

## Purpose

This page defines how the reconnection time is measured in HiL and vehicle tests, so that results from different environments and testers are comparable.

## Measurement points

| Point | Definition | Source |
|---|---|---|
| **t0** | **Ignition ON** – rising edge of KL15 as received by COMP-001 (trace "Vehicle ignition event received.") | COMP-001 trace |
| t1 | Phone shown as connected: COMP-002 state `PROFILE_RESTORE` reached (ACL + HFP SLC) | COMP-002 trace |

**Reconnection time = t1 − t0.**

The measurement starts at ignition because this is what the driver experiences. Using the KL15 trace makes the measurement independent of internal events.

## Procedure (HiL)

1. Phone paired and connected; ignition OFF for at least 60 s.
2. Switch KL15 ON via restbus.
3. Read t0 and t1 from the trace (automated parser `reconn_time.py`).
4. Record the value in the TestManagementSystem with 0.1 s resolution.

## Procedure (Vehicle)

1. Driver enters the vehicle with the phone in the pocket, Bluetooth enabled.
2. Switch on ignition.
3. Trace is captured on the head unit; values extracted after the drive.

## Special cases

- If the head unit reboots during the measurement, the execution is invalid and repeated.
