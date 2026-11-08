# REQ-002 – Reconnection within Ten Seconds

| Field | Value |
|---|---|
| Page ID | PC-013 |
| Requirement | REQ-002 |
| Priority | Critical |
| Status | Approved |
| Implemented by | COMP-002 Bluetooth Connection Manager |
| Verified by | TEST-002, TEST-007, TEST-008, TEST-010 |

## Requirement text

> The system shall complete Bluetooth phone reconnection within 10 seconds after the Bluetooth subsystem becomes available.

## Definition of the measured interval

- **Start (t0):** the moment the Bluetooth subsystem becomes available, i.e. the `BT_READY` event emitted by the BT Stack Adapter (COMP-009). This event is visible in traces with the message "Bluetooth subsystem available; reconnection request submitted."
- **End (t1):** the moment the ACL link and the HFP service level connection are established and COMP-002 reports `CONNECTED`.
- **Reconnection time** = t1 − t0.

Profile restoration of A2DP/AVRCP is **not** part of the 10-second interval; it is governed by REQ-005.

## Rationale

The time between ignition ON and BT_READY depends on the boot time of the head unit, which is owned by the Platform team and not by PCON. Measuring from BT_READY makes the requirement testable for the component that implements it.

## Pass/fail rule

A single test execution verifying REQ-002 is **FAIL** if the measured reconnection time exceeds 10.0 seconds. The release KPI over many cycles is defined in PC-077.

## Notes on phone behavior

Some phones (observed with several Android devices) try to connect to the vehicle themselves when they detect the vehicle, sometimes before the head unit starts its own attempt. In traces, such connections appear as incoming connection requests. The requirement text does not distinguish between connections initiated by the head unit and connections initiated by the phone.

## History

| Date | Change |
|---|---|
| 2026-05-29 | Baselined |
| 2026-07-15 | Clarified that A2DP restoration is outside the interval |
