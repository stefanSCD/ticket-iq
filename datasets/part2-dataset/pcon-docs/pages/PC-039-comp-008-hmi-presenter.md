# COMP-008 – HMI Connectivity Presenter

| Field | Value |
|---|---|
| Page ID | PC-039 |
| Component | COMP-008 |
| Version | 1.3.0 |
| Owner | Andrei Popescu (PCON side), Jonas Weber (HMI side) |
| Implements | REQ-013, REQ-026, REQ-027 |

## Responsibility

Offers a stable API to the HMI Platform for all connectivity information and forwards user actions to the service layer.

## API towards HMI

| Method / Event | Description |
|---|---|
| `getDeviceList()` | Up to **8** paired devices with name, state, role |
| `connect(deviceId)` | Manual connection (REQ-013) |
| `setPrimary(deviceId)` | Make phone primary |
| `unpair(deviceId)` | Unpair phone |
| `onStateChanged` | Connection state event |
| `onNotification` | Toast/popup request |

## Notifications

| Situation | Notification |
|---|---|
| Successful automatic or manual connection | Toast "Connected to <name>", 3 s |
| Automatic reconnection failed (give-up reached) | Popup "<name> could not be connected. Check that Bluetooth is enabled on your phone." with button "OK" |
| Phonebook access denied | Hint in phonebook screen |

## Device names

COMP-008 passes the name reported by the phone. The HMI Platform font supports Latin, Cyrillic, Greek, CJK and Arabic scripts.
