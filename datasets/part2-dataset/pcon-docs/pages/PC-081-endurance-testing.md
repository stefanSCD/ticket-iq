# Endurance and Soak Testing

| Field | Value |
|---|---|
| Page ID | PC-081 |
| Owner | Daniel Szabo |
| Last updated | 2026-09-05 |

## Goal

Find failures that only appear after many ignition cycles or long uptime: memory leaks, file system growth, stack resource exhaustion, timing drift.

## HiL soak setup

- Bench: HIL-BT-01 (needs transport mode off, normal voltage).
- Phones: RP-01 and RP-07, permanently charged.
- Cycle: KL15 ON → wait for connection → play media 60 s → place automated call 30 s → KL15 OFF → wait 90 s.
- One cycle takes about 4 minutes, so roughly 15 cycles per hour.
- Monitored: RSS of all PCON processes, size of `/persist/bt/`, reconnection time per cycle, error events.

## Pass criteria

- No crash or restart of a PCON process.
- RSS growth less than 1 MB over the whole run.
- No reconnection above 20 s.

## Duration

The run duration for the R1 soak test has not been fixed. Sofia proposed 72 hours, Daniel pointed out that a 72-hour run blocks HIL-BT-01 for three days and conflicts with the Audio team booking.

## Vehicle endurance

Vehicle endurance for the reconnection KPI is described in the acceptance criteria (PC-077).
