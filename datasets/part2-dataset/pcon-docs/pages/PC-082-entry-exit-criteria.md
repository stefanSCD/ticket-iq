# Entry and Exit Criteria per Test Environment

| Field | Value |
|---|---|
| Page ID | PC-082 |
| Owner | Sofia Brandt |
| Last updated | 2026-07-06 |

## SiL

| Entry | Exit |
|---|---|
| Build green, unit tests passed | All SiL regression cases executed, no new failures |

## HiL

| Entry | Exit |
|---|---|
| SiL nightly green on the same build | All HiL cases for changed requirements executed |
| Bench booked, phones charged and on reference OS | Traces uploaded to TraceRepository |
| Software flashed and version verified | Results in TestManagementSystem |

## Vehicle

| Entry | Exit |
|---|---|
| HiL regression passed for the build | All planned vehicle executions done |
| Vehicle booked and released by the workshop | Traces and measured times recorded |
| Reference phones with test phonebooks | Defects created for every failure |

## Requirement verification evidence

A requirement is counted as verified when at least one execution on HiL or Vehicle has passed. Whether a SiL execution can count as verification evidence for requirements without radio dependency is under discussion (see PC-066).
