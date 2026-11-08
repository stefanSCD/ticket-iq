# Meeting Notes – Supplier Sync with Sylvan Wireless 2026-08-05

| Field | Value |
|---|---|
| Page ID | PC-062 |
| Participants | Tobias Kern, Andrei Popescu, Liam O'Connor (Sylvan Wireless) |

## Agenda

1. Status of open stack tickets
2. Nimbus BT Stack 5.3 roadmap
3. Queue behavior in the stack

## Notes

**1. Open tickets** – SYL-2291 (A2DP stream start latency) is fixed in patch 5.2.4. SYL-2307 (SDP response handling with certain Android phones) is under analysis.

**2. Stack 5.3** – Liam presented 5.3: release planned for 2026-11, includes LE Audio groundwork, improved SDP caching and a native priority queue for connection requests. Sylvan recommends 5.3 for all new programs. For Meridian, upgrading would mean a stack change shortly before the C-Sample. Tobias and Andrei see the benefit (native priority queue) but also the integration risk. **No decision** on whether Meridian R1 moves to 5.3 or stays on 5.2.x. Decision needed before the R1 code freeze.

**3. Queue** – Confirmed that 5.2 processes one connection-related operation at a time. The priority handling must therefore be implemented in COMP-009 (done in 2.0.4).

## Action items

| Action | Owner | Due |
|---|---|---|
| Provide 5.3 release notes and migration guide | Liam O'Connor | 2026-08-19 |
| Integrate patch 5.2.4 | Andrei Popescu | 2026-08-26 |
| Prepare 5.3 risk assessment | Tobias Kern | 2026-09-09 |
