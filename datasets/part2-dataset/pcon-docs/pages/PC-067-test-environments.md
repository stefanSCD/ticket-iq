# Test Environments – SiL, HiL, Vehicle

| Field | Value |
|---|---|
| Page ID | PC-067 |
| Owner | Sofia Brandt |
| Last updated | 2026-07-06 |

## SiL

- PCON components built for x86-64 Linux.
- Nimbus stack replaced by the **BT Peer Simulator**, which simulates phones and their responses (including configurable delays and errors).
- Vehicle signals from a restbus simulation.
- Used for: nightly regression, failure injection (e.g. transient error for TEST-004).
- Limitation: radio timing is not realistic.

## HiL

- Real HU4 B-Sample on bench HIL-BT-01 or HIL-BT-02.
- Real phones in a shielded RF box with programmable attenuator.
- Restbus simulation for vehicle signals; power supply programmable for voltage profiles.
- Used for: system tests, performance, timing.

## Vehicle

- Prototype vehicles of the Meridian program (MER-P01 … MER-P08); PCON has access mainly to MER-P03 and MER-P05.
- Real phones from the reference list.
- Used for: timing in real environment, user scenarios, endurance.

## Result reporting

All environments report to the TestManagementSystem with environment, software version, result and measured reconnection time.
