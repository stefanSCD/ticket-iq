# Meeting Notes – Architecture Sync 2026-06-03

| Field | Value |
|---|---|
| Page ID | PC-058 |
| Participants | Tobias Kern, Andrei Popescu, Radu Ionescu, Felix Wagner, Nina Hoffmann |

## Agenda

1. Component split for R1
2. Retry strategy (preparation of ADR-001)
3. Stack adapter queue

## Notes

**1. Component split** – Agreed to separate the Device Priority Manager (COMP-006) from the Connection Manager, but to run both in the same process. COMP-010 will be a thin interface, power policy stays with the platform.

**2. Retry strategy** – Radu presented measurements: page timeout 5.12 s. Exponential backoff with three retries cannot fit into 10 s. Tobias will write ADR-001 with a single retry.

**3. Stack adapter queue** – Andrei explained that the Nimbus stack accepts only one connection-related operation at a time; COMP-009 therefore queues requests. Queue is FIFO today. Nobody saw a problem at this point.

## Action items

| Action | Owner | Due |
|---|---|---|
| Draft ADR-001 | Tobias Kern | 2026-06-17 |
| Create COMP-006 repository folder | Radu Ionescu | 2026-06-10 |
| Clarify HSM API availability on B-Sample | Felix Wagner | 2026-06-17 |
