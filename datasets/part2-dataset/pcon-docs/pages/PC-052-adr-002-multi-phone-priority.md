# ADR-002 – Most-Recently-Used Priority for Multiple Phones

| Field | Value |
|---|---|
| Page ID | PC-052 |
| Status | **Accepted** (2026-06-26) |
| Deciders | Tobias Kern, Mara Lindqvist, Radu Ionescu, Jonas Weber |

## Context

With REQ-008 the system supports up to two connected phones. When several paired phones are in range after ignition, the system must decide which phone becomes the primary phone (HFP + A2DP + PBAP) and which one becomes secondary (HFP only).

## Options

1. **Most-Recently-Used (MRU):** the phone with the latest successful connection is primary.
2. **Pairing order:** the first paired phone is primary.
3. **Signal strength:** the phone with the strongest RSSI is primary.
4. **Driver identification:** use the key fob / user profile to select the phone.

## Decision

Option 1: **MRU** based on the timestamp of the last successful connection stored in COMP-003. Maximum **two** phones are connected simultaneously.

## Rationale

- MRU matches the behavior of HU3 and of most competitor systems.
- Signal strength is unreliable: a passenger's phone near the head unit could win.
- Driver identification depends on the user-profile feature of the HMI Platform, which is not stable for R1.

## Consequences

- The driver can change the primary phone manually; the change updates the MRU order.
- COMP-006 implements the sorting (PC-037).

## Open point: favourite phone

Product Management (Mara Lindqvist) asked for a "favourite phone" setting: the driver marks one phone as favourite, and this phone shall always become primary when it is in range. It is **not decided** whether a favourite overrides MRU in all cases, only when both phones are in range, or whether the feature is postponed. To be discussed with the HMI Platform team.
