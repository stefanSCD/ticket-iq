# Scope and Out-of-Scope

| Field | Value |
|---|---|
| Page ID | PC-002 |
| Owner | Mara Lindqvist |
| Last updated | 2026-06-12 |
| Status | Approved |

## In scope for Release 1

The following capabilities are part of the PCON scope for R1:

- **Automatic reconnection after ignition** of previously paired phones (FEAT-001).
- **Reconnection after link loss** while the vehicle is running, for example when the driver leaves the vehicle briefly with the phone and returns.
- **Multi-phone handling**: up to two phones connected at the same time, with a priority rule that decides which phone becomes the primary phone.
- **Profile restoration** for hands-free (HFP), media audio (A2DP) and media control (AVRCP).
- **Phonebook and call-history synchronization** via PBAP.
- **Diagnostics**: diagnostic events for every reconnection attempt and diagnostic trouble codes for persistent faults.
- **Status information** for the HMI: connection state, device name, and profile availability.
- **Manual reconnection** triggered by the driver from the device list in the HMI.

## Out of scope for PCON

| Topic | Owner |
|---|---|
| First-time pairing user experience (pairing wizard, PIN screens) | HMI Platform team |
| Wi-Fi hotspot and Wi-Fi client | Network Services team |
| Apple CarPlay and Android Auto projection | Projection team |
| Digital key via Bluetooth Low Energy | Access & Security team |
| eCall and emergency call audio routing | Telematics team |
| Bluetooth audio for rear-seat headphones | Rear Seat Entertainment (not on Meridian) |

The PCON team provides interfaces that other teams use. For example, the Projection team relies on PCON to keep the HFP connection of a CarPlay phone alive (see PC-028). Such interfaces are documented on the respective component pages, but the features themselves are not delivered by PCON.

## Vehicle modes considered

The vehicle can be in several modes that influence connectivity behavior:

- **Ignition ON** (terminal KL15 active) – the main trigger for automatic reconnection.
- **Comfort mode** – the infotainment system is running without ignition, e.g. after the driver door is opened.
- **Transport mode** – a factory/logistics mode that restricts many vehicle functions.
- **Guest / valet mode** – a restricted user mode offered by the HMI Platform.
- **OTA installation mode** – the vehicle installs a software update.

How PCON behaves in each of these modes is described in PC-024 (power modes) where decided.

## Boundary of the original proof of concept

The knowledge-graph proof of concept that preceded this space only covered the reconnection of one previously paired phone after one ignition cycle. The R1 scope described above is wider; the PoC data (REQ-001 … REQ-007, TEST-001 … TEST-010, EXEC-001 … EXEC-016) remains valid and is reused on the requirement and test pages.

## Scope changes

Scope changes must be raised as a Jira issue of type *Decision* in PCON and approved by the Product Owner in the sprint review. Accepted changes are recorded in the documentation change log (PC-010).
