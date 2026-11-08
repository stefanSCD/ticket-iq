# REQ-014 – REQ-016 – Phonebook Synchronization

| Field | Value |
|---|---|
| Page ID | PC-022 |
| Owner | Ioana Marin |
| Implemented by | COMP-007 Phonebook Sync Service |
| Status | Approved |

## Requirements

**REQ-014** – The system shall download the contacts of the primary phone using PBAP after connection.

**REQ-015** – The system shall download the call history (incoming, outgoing, missed) of the primary phone.

**REQ-016** – Contacts shall be available for search in the HMI as soon as the first 100 contacts have been received.

## Technical basis

- Protocol: PBAP 1.2, vCard 3.0 format.
- Contact photos are downloaded in a second pass at lower priority.
- The phonebook download only starts after HFP and A2DP restoration has completed, so that it does not delay audio availability.
- The user must allow contact sharing on the phone. If the phone denies access, no phonebook is shown and the HMI displays the hint "Allow contact access on your phone".
- The sync strategy (full versus delta) is decided in ADR-004 (PC-054).

## Large phonebooks

Phones with large phonebooks (several thousand contacts) take a long time to deliver all vCards; some phones answer slowly or stop responding during the transfer. The duration of the download depends strongly on the phone model.

## Acceptance criteria

1. Contacts appear in the HMI after a connection without user action.
2. Search is possible after the first 100 contacts.
3. Call history shows the last 50 entries per category.
