# Regression Suite and Continuous Integration

| Field | Value |
|---|---|
| Page ID | PC-076 |
| Owner | Andrei Popescu |
| Last updated | 2026-08-15 |

## Suites

| Suite | Content | Trigger | Duration |
|---|---|---|---|
| Unit | All component unit tests | Every push | ~4 min |
| SiL smoke | 25 key scenarios | Every merge request | ~12 min |
| SiL nightly | Full SiL regression (~420 cases) | Daily **02:00 CET** | ~95 min |
| HiL nightly | TEST-001 … TEST-010 with RP-01 and RP-07 | Daily 22:00 on HIL-BT-01 | ~3 h |
| HiL weekly | Full HiL regression, all reference phones | Saturday | ~9 h |

## CI system

- GitLab CI in the repository `pcon-connectivity`.
- SiL jobs run in Docker containers on the shared runner pool.
- HiL jobs are triggered via the bench controller API; results are pushed to the TestManagementSystem.

## Rules

- A red SiL nightly is the first topic in the daily.
- Flaky tests are quarantined with label `flaky` and must be fixed within one sprint.
- Merges to `release/r1.x` require a green SiL nightly from the same day.
