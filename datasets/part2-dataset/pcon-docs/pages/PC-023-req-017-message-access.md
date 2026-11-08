# REQ-017 – Message Access (MAP)

| Field | Value |
|---|---|
| Page ID | PC-023 |
| Requirement | REQ-017 |
| Priority | Low |
| Status | Draft |
| Implemented by | COMP-004 (profile), HMI Messaging app (HMI Platform) |

## Requirement text (draft)

> The system shall allow the driver to read incoming text messages of the primary phone through MAP 1.4.

## Context

Message access requires support from the HMI Platform (message list, text-to-speech). The HMI Platform team has confirmed that a message list screen exists in their R1 baseline, but text-to-speech is planned for later.

## Technical notes

- MAP 1.4 is supported by Nimbus BT Stack 5.2.
- iOS phones only expose notifications for messages after the user enables "Show Notifications" for the vehicle in the phone's Bluetooth settings.
- MAP is connected after PBAP to avoid congestion on the link during startup.

## Release

MAP is shown as a candidate in the release plan (PC-005). The requirement stays in draft until the release assignment is clarified.
