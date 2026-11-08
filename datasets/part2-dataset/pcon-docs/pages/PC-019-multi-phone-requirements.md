# REQ-008 – REQ-010 – Multi-Phone Handling

| Field | Value |
|---|---|
| Page ID | PC-019 |
| Owner | Mara Lindqvist |
| Implemented by | COMP-006 Device Priority Manager, COMP-002 |
| Status | Approved |

## Requirements

**REQ-008** – The system shall support up to two simultaneously connected phones.

**REQ-009** – When more than one paired phone is available, the system shall select one primary phone according to the priority rule defined in ADR-002.

**REQ-010** – The secondary phone shall be connected with the hands-free profile only.

## Roles

| Role | Profiles | Use |
|---|---|---|
| Primary phone | HFP, A2DP, AVRCP, PBAP | Calls, media, phonebook |
| Secondary phone | HFP | Incoming and outgoing calls |

Both phones can receive calls. The phonebook shown in the HMI is the one of the primary phone.

## Reconnection order

After ignition, COMP-006 sorts the paired phones by priority and COMP-002 connects them one after the other: first the primary candidate, then the secondary candidate. REQ-002 applies to the primary phone.

## Phone-side behavior

Phones decide themselves which profiles they offer. A secondary phone may request an A2DP connection from its side, for example when the user starts music playback on it. Several phones do this automatically after connecting to a car.

## Changing the primary phone

The driver can make the secondary phone primary from the device list. The change takes effect immediately and is remembered as the new MRU order.
