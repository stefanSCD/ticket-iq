# REQ-026 – REQ-027 – HMI Status Information

| Field | Value |
|---|---|
| Page ID | PC-027 |
| Owner | Jonas Weber (HMI), Mara Lindqvist |
| Implemented by | COMP-008 HMI Connectivity Presenter |
| Status | Approved |

## Requirements

**REQ-026** – The system shall provide the connection state of every paired phone to the HMI.

**REQ-027** – The system shall indicate a failed automatic reconnection **only through the status icon** in the status bar. No popup or toast shall be shown for a failed automatic reconnection, to avoid distracting the driver.

## Connection states

| State | Meaning | Status bar icon |
|---|---|---|
| Disconnected | Phone paired, not connected | Phone icon, grey |
| Connecting | Connection attempt running | Phone icon, animated |
| Connected | Connected with all supported profiles | Phone icon, white |
| Partially connected | Connected, but at least one supported profile missing | Phone icon with small warning dot |

UI texts are maintained in English by PCON; translations are delivered by the HMI Platform localization process.

## Notifications

- After a successful automatic reconnection a toast **"Connected to <device name>"** is shown for **3 seconds**.
- After a successful manual connection, the same toast is shown.

## Device name

The device name is the name reported by the phone. Users often personalize the name of their phone ("Anna's phone ❤️"). The name is passed to the HMI unchanged.

## Phone information

Over HFP, phones also report indicators such as signal strength, battery level and roaming status. These indicators are available in COMP-004.
