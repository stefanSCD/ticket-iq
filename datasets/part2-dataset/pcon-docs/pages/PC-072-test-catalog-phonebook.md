# Test Catalog – Phonebook

| Field | Value |
|---|---|
| Page ID | PC-072 |
| Owner | Ioana Marin, Sofia Brandt |
| Last updated | 2026-08-22 |

| Test | Title | Verifies | Expected result |
|---|---|---|---|
| TEST-019 | Contacts available after connection | REQ-014 | Contacts shown without user action |
| TEST-020 | Call history download | REQ-015 | Last 50 entries per category shown |
| TEST-021 | Search after first batch | REQ-016 | Search possible after 100 contacts |
| TEST-022 | Delta sync with unchanged phonebook | ADR-004 | No vCard download when counters unchanged |
| TEST-023 | Phonebook deleted on unpair | REQ-024 | DB file of phone removed |
| TEST-024 | Access denied on phone | REQ-014 | Hint "Allow contact access on your phone" |

## Test data

- RP-05: 200 contacts.
- RP-01, RP-07: 1,200 contacts each (synthetic test phonebook "PB-M").
- RP-09: 5,000 contacts (synthetic test phonebook "PB-XL").

## Notes

- TEST-022 requires phones supporting PBAP 1.2 folder version counters (RP-01, RP-02, RP-07, RP-08 confirmed).
- SiL uses the BT Peer Simulator with configurable phonebook sizes.
