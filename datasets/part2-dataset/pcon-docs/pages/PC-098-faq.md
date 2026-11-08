# FAQ

| Field | Value |
|---|---|
| Page ID | PC-098 |
| Owner | Andrei Popescu |
| Last updated | 2026-09-25 |

**Why only one retry?**
Because a second retry cannot finish within 10 s (page timeout 5.12 s). See ADR-001.

**Why does the secondary phone not play music?**
REQ-010: the secondary phone is connected with HFP only.

**Can I use a phone that is not on the reference list for tests?**
For exploratory tests yes; for release evidence only reference phones count.

**What happens if I enter the car while I am already on a call?**
This scenario was collected in the requirements clarification (PC-059) and is part of the exploratory test charter.

**Where are the traces of a vehicle execution?**
In the TraceRepository, searchable by execution ID.

**Who decides about requirement changes?**
The Product Owner, Mara Lindqvist (PC-004).

**Why are there two different HiL benches?**
HIL-BT-01 supports transport-mode simulation, HIL-BT-02 does not (PC-068).

**How do I get the Sylvan portal access?**
Ask Tobias Kern (PC-097).
