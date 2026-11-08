# REQ-024 – REQ-025 – Privacy and Data Deletion

| Field | Value |
|---|---|
| Page ID | PC-026 |
| Owner | Karim Haddad |
| Implemented by | COMP-003, COMP-007 |
| Status | Approved |

## Requirements

**REQ-024** – When a phone is unpaired (by the driver in the HMI), the system shall delete the pairing information, the downloaded phonebook and the downloaded call history of that phone.

**REQ-025** – A factory reset shall delete all pairing information, all phonebooks and call histories, and all connectivity settings.

## Data stored per phone

| Data | Stored where | Deleted on unpair | Deleted on factory reset |
|---|---|---|---|
| Pairing entry and link key | COMP-003 | Yes | Yes |
| Contacts | COMP-007 | Yes | Yes |
| Call history | COMP-007 | Yes | Yes |
| Per-phone settings | COMP-003 | Yes | Yes |
| Diagnostic events (hashed device ID) | COMP-005 | No | Yes |

## Call history

The call history is downloaded from the phone after every connection and kept in the vehicle so that it is available immediately at the next connection. Entries older than what the phone delivers are kept as long as the phone remains paired.

## Owner change

When a vehicle is sold, the previous owner's phones are still paired unless a factory reset is performed. Whether PCON should offer a dedicated "owner change" behavior (for example, triggered by the backend when the vehicle is transferred to a new account) is an **open point** raised by the Privacy Office. No decision has been made.
