# Test Catalog – Multi-Phone and Manual Connection

| Field | Value |
|---|---|
| Page ID | PC-071 |
| Owner | Sofia Brandt |
| Last updated | 2026-08-20 |

| Test | Title | Verifies | Environment | Expected result |
|---|---|---|---|---|
| TEST-015 | Two phones reconnect after ignition | REQ-008 | HiL, Vehicle | Both phones connected; MRU phone primary |
| TEST-016 | MRU order after manual primary change | REQ-009 | HiL | Phone selected manually becomes primary at next ignition |
| TEST-017 | Secondary phone HFP only | REQ-010 | HiL | Secondary phone has HFP, no A2DP |
| TEST-018 | Primary out of range | REQ-009 | HiL | Next phone becomes primary |
| TEST-014 | Manual connection from device list | REQ-013 | HiL | Phone connected within 10 s |

## Test setup

- Two reference phones in the RF box (default: RP-01 and RP-07).
- MRU order prepared by connecting phones in a defined order before the ignition cycle.
- TEST-018 uses the attenuator to put the primary candidate out of range.

## Vehicle sign-off for multi-phone

The vehicle part of TEST-015 is executed in the endurance campaign. **The number of ignition cycles required for multi-phone sign-off is not defined yet.** For single-phone timing, PC-077 defines the release KPI; it is not clear whether the same campaign size applies to two-phone scenarios, which take longer per cycle.

## Status

TEST-014 – TEST-018 are implemented in HiL automation; first executions planned for October 2026.
