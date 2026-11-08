# Bluetooth Stack Supplier Interface – Sylvan Wireless

| Field | Value |
|---|---|
| Page ID | PC-093 |
| Owner | Tobias Kern |
| Last updated | 2026-08-08 |

## Supplier

- Company: **Sylvan Wireless**
- Product: **Nimbus BT Stack 5.2** (current patch 5.2.4) and controller firmware SWC-4421
- Contact: Liam O'Connor (Technical Account Manager)

## Reporting defects

1. Reproduce the issue with stack debug logging enabled (`nimbus_log_level=4`).
2. Create a ticket in the Sylvan support portal (project SYL) with logs, HCI snoop file and stack version.
3. Link the SYL ticket in the PCON Bug.

## Service levels

| Item | Commitment |
|---|---|
| First response to a bug report | **10 business days** |
| Patch releases | Quarterly, or on agreement |
| Security fixes | Communicated via security advisory |

## Meetings

Supplier sync every 4 weeks (Tobias Kern, Andrei Popescu, Liam O'Connor). Minutes are stored in this space (e.g. PC-062).

## Critical issues

The 10-business-day response time is too long for issues that block a sample release. The contract mentions "priority handling for critical issues" but does not define what that means in practice or whom to contact beyond the support portal.

## Stack version for R1

Meridian R1 is currently planned on 5.2.x. The option to move to 5.3 is discussed in PC-062.
