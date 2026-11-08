# Threading and Timing Model

| Field | Value |
|---|---|
| Page ID | PC-050 |
| Owner | Andrei Popescu |
| Last updated | 2026-07-28 |

## Processes

Each component runs in its own process, except COMP-002 and COMP-006, which share the process `pcon-connmgr`.

| Process | Components | Scheduling |
|---|---|---|
| pcon-connmgr | COMP-002, COMP-006 | SCHED_OTHER, nice −5 |
| pcon-stack | COMP-009 + Nimbus stack | SCHED_FIFO, prio 20 |
| pcon-profiles | COMP-004 | SCHED_OTHER |
| pcon-pbap | COMP-007 | SCHED_OTHER, nice 5 |
| pcon-diag | COMP-005 | SCHED_OTHER, nice 5 |
| pcon-store | COMP-003 | SCHED_OTHER |
| pcon-vehicle | COMP-001, COMP-010 | SCHED_OTHER |
| pcon-hmi | COMP-008 | SCHED_OTHER |

## Event loop

Every process uses a single-threaded event loop (libuv). Blocking operations (file I/O, HSM calls) are executed in a worker pool of 2 threads per process.

## Timers

- All timers use the monotonic clock.
- Timestamps in diagnostic events use the system clock (UTC), synchronized by the platform; before time synchronization, timestamps are relative to boot.

## Timing budget at startup

| Phase | Budget |
|---|---|
| Connectivity components started | ≤ 1.5 s (REQ-030) |
| BT_READY | ≤ 3 s after component start (assumption A2) |
| Reconnection | ≤ 10 s after BT_READY (REQ-002) |
