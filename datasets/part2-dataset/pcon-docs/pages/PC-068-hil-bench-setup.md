# HiL Bench Setup

| Field | Value |
|---|---|
| Page ID | PC-068 |
| Owner | Daniel Szabo |
| Last updated | 2026-08-28 |

## Benches

| Bench | Location | HU4 sample | Special features |
|---|---|---|---|
| HIL-BT-01 | Lab 2.14 | B-Sample #117 | Full restbus incl. transport mode |
| HIL-BT-02 | Lab 2.14 | B-Sample #121 | No transport mode simulation |

A third bench (HIL-BT-03) has been requested (see retrospective PC-064); procurement is not approved.

## RF setup

- Each bench has a shielded RF box with up to 4 phone holders.
- Programmable attenuator 0–90 dB between head unit antenna and box.
- Weak-signal profile for TEST-008: attenuation step to reach about **−80 dBm** RSSI at the phone, held for 15 s.
- Link-loss profile: attenuation 90 dB for 30 s, then back to 20 dB.

## Power supply

Programmable supply, voltage profiles for cranking (dip to 6 V), low voltage (8.0 V for 5 s), normal (13.5 V).

## Booking

Benches are booked in **BenchBooker** in slots of 2 hours. Weekly full regression runs are booked by Daniel. The Audio team uses the benches Thursday and Friday afternoons.

## Phone automation

Android phones via ADB, iOS phones via a robotic finger for actions that cannot be automated (e.g. accepting a pairing). Phones are charged continuously.

## Unattended runs

The full regression takes about 9 hours, so it is started in the evening and runs overnight.
