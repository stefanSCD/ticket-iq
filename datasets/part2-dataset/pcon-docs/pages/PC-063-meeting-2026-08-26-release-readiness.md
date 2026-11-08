# Meeting Notes – Release Readiness Review 2026-08-26

| Field | Value |
|---|---|
| Page ID | PC-063 |
| Participants | Petra Novak, Mara Lindqvist, Andrei Popescu, Sofia Brandt, Elena Rusu |

## Agenda

1. R1 dates
2. Release KPI for reconnection time
3. Defect status
4. Diagnostics topics

## Notes

**1. R1 dates** – Petra informed that the program moved the R1 code freeze by one week: new date **2026-11-27**. C-Sample date unchanged (2026-12-15).

**2. Release KPI** – For release sign-off, the reconnection time KPI over the vehicle endurance campaign is: **at least 95 % of ignition cycles reconnect within 10 s**, and no cycle above 20 s.

**3. Defects**

| Defect | Status | Comment |
|---|---|---|
| DEF-001 | Open | Fix in review (COMP-002 2.3.1 + COMP-009 2.0.4) |
| DEF-002 | In Progress | Root cause known; fix planned in COMP-005 1.2.1 |
| DEF-003 | Resolved | COMP-004 3.1.1 |

For DEF-002, it is **not decided** whether the fix is required for R1 or can be delivered with R2; Elena estimates two sprints including HiL verification. Mara will decide after the next sprint review.

**4. Diagnostics** – The Telematics request to upload reconnection events was mentioned again; still open, waiting for privacy review.

## Action items

| Action | Owner | Due |
|---|---|---|
| Update release plan page | Petra Novak | 2026-09-04 |
| DEF-002 R1/R2 decision | Mara Lindqvist | 2026-09-09 |
