# Startup Sequence – Ignition to Connected Phone

| Field | Value |
|---|---|
| Page ID | PC-043 |
| Owner | Radu Ionescu |
| Last updated | 2026-07-03 |

## Sequence

```
Vehicle      COMP-001     COMP-009        COMP-002        COMP-006   COMP-003   COMP-004      COMP-008
  | KL15 ON     |             |               |               |          |          |             |
  |------------>| Ignition    |               |               |          |          |             |
  |             |-------------------------->  |               |          |          |             |
  |             |             | BT_READY      |               |          |          |             |
  |             |             |-------------> |               |          |          |             |
  |             |             |               | getOrder()    |          |          |             |
  |             |             |               |-------------> |          |          |             |
  |             |             |               | GetLinkKey    |          |          |             |
  |             |             |               |------------------------> |          |             |
  |             |             | connect()     |               |          |          |             |
  |             |             | <-------------|               |          |          |             |
  |             |             | ACL + auth ok |               |          |          |             |
  |             |             |-------------> |               |          |          |             |
  |             |             |               | restoreProfiles()                   |             |
  |             |             |               |-------------------------------------> |           |
  |             |             |               |               |          | 1. A2DP  |             |
  |             |             |               |               |          | 2. HFP   |             |
  |             |             |               |               |          | 3. AVRCP |             |
  |             |             |               | StateChanged(CONNECTED)             |------------>|
```

## Notes

1. COMP-002 waits for both events (Ignition ON and BT_READY), in any order.
2. The link key is fetched from COMP-003 and unwrapped by the HSM before the connection request.
3. Profiles are restored by COMP-004 in the order **A2DP, HFP, AVRCP**. Media is restored first because audio playback interruption is the most noticeable effect for the driver.
4. PBAP starts after profile restoration (not shown).

## Typical timings (HiL, SW 2.3.0)

| Step | Duration |
|---|---|
| Service start → BT_READY | 2.4 s |
| BT_READY → connection request sent | 0.1 s |
| Paging + ACL + authentication | 1.5 – 3.0 s |
| HFP SLC | 1.0 – 2.0 s |
| A2DP + AVRCP | 1.5 – 2.5 s |
