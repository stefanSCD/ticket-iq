# REQ-013 – Manual Reconnection

| Field | Value |
|---|---|
| Page ID | PC-021 |
| Requirement | REQ-013 |
| Priority | Medium |
| Status | Approved |
| Implemented by | COMP-008 HMI Connectivity Presenter, COMP-002 |

## Requirement text

> The system shall allow the driver to connect a paired phone manually from the device list.

## Behavior

- The device list (rendered by the HMI Platform) shows all paired phones with their state.
- Selecting a phone that is not connected sends a `ConnectRequest(deviceId)` to COMP-002 via COMP-008.
- A manual connection request has a higher priority than background activities like phonebook synchronization.
- If two phones are already connected, a manual connection to a third phone disconnects the secondary phone first (REQ-008 limit of two phones).
- A manual connection makes the selected phone the primary phone and updates the MRU timestamp.

## Interaction with automatic reconnection

Automatic reconnection after ignition can take several seconds, especially when the primary candidate is out of range and the page procedure runs into its timeout. During this time the device list is already usable, so a driver can select a different phone while COMP-002 is still busy with the automatic attempt for another phone.

## Acceptance criteria

1. A paired, available phone selected in the device list is connected within 10 seconds.
2. The HMI shows "Connecting" during the attempt.
3. If the connection fails, the phone stays in the list with state "Disconnected".
