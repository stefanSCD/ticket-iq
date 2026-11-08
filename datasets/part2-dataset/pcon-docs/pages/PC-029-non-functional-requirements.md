# REQ-029 – REQ-030 – Non-Functional Requirements

| Field | Value |
|---|---|
| Page ID | PC-029 |
| Owner | Andrei Popescu |
| Status | Approved |

## REQ-029 – Resource budgets

| Resource | Budget |
|---|---|
| Memory (RSS) of all connectivity components together | ≤ 12 MB |
| CPU load of COMP-002 during startup (first 30 s after BT_READY) | ≤ 5 % average |
| CPU load of all connectivity components in steady state | ≤ 2 % average |
| Persistent storage `/persist/bt/` | ≤ 64 MB |

## REQ-030 – Startup robustness

The connectivity components shall start within 1.5 seconds after the application processor has started the service manager, independently of the number of paired phones.

## Measurement

- Memory and CPU are measured on HiL with the performance tracing build.
- The measurement is part of the weekly HiL performance run.
- Violations are reported as Bugs with label `performance`.

## Current values (SW 2.3.0, HiL)

| Metric | Value |
|---|---|
| RSS connectivity components | 9.8 MB |
| COMP-002 CPU startup | 3.1 % |
| Steady-state CPU | 0.9 % |
