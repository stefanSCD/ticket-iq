# Test Results Summary – July 2026 Campaign (SW 2.3.0)

| Field | Value |
|---|---|
| Page ID | PC-078 |
| Owner | Sofia Brandt |
| Last updated | 2026-08-03 |

## Overview

| Environment | Executions | PASS | FAIL |
|---|---|---|---|
| SiL | 5 | 4 | 1 |
| HiL | 4 | 2 | 2 |
| Vehicle | 7 | 3 | 4 |
| **Total** | **16** | **9** | **7** |

## Executions

| Execution | Date | Env | Test | Result | Time (s) | Defect |
|---|---|---|---|---|---|---|
| EXEC-001 | 07-14 | SiL | TEST-001 | PASS | 6.8 | |
| EXEC-002 | 07-14 | SiL | TEST-002 | PASS | 7.4 | |
| EXEC-003 | 07-15 | SiL | TEST-002 | FAIL | 12.1 | DEF-001 |
| EXEC-004 | 07-15 | SiL | TEST-003 | PASS | 5.9 | |
| EXEC-005 | 07-16 | SiL | TEST-004 | PASS | 9.6 | |
| EXEC-006 | 07-17 | HiL | TEST-002 | FAIL | 15.4 | DEF-001 |
| EXEC-007 | 07-18 | HiL | TEST-007 | PASS | 9.3 | |
| EXEC-008 | 07-18 | HiL | TEST-008 | FAIL | 13.8 | DEF-001 |
| EXEC-009 | 07-19 | HiL | TEST-005 | PASS | 8.7 | |
| EXEC-010 | 07-21 | Vehicle | TEST-002 | FAIL | 18.0 | DEF-001 |
| EXEC-011 | 07-21 | Vehicle | TEST-001 | PASS | 7.9 | |
| EXEC-012 | 07-22 | Vehicle | TEST-006 | FAIL | 8.1 | DEF-002 |
| EXEC-013 | 07-23 | Vehicle | TEST-009 | PASS | 9.8 | |
| EXEC-014 | 07-24 | Vehicle | TEST-005 | FAIL | 8.6 | DEF-003 |
| EXEC-015 | 07-25 | Vehicle | TEST-010 | PASS | 9.7 | |
| EXEC-016 | 07-26 | Vehicle | TEST-007 | FAIL | 11.6 | DEF-001 |

## Observations

- DEF-001 (delayed reconnection) appears in all three environments: SiL, HiL and Vehicle.
- EXEC-012 and EXEC-014 failed for functional reasons although the reconnection time was below 10 s.
- Several passed executions are close to the limit (EXEC-005 9.6 s, EXEC-013 9.8 s, EXEC-015 9.7 s).

## Requirements without coverage

REQ-007 (draft) has no test.
