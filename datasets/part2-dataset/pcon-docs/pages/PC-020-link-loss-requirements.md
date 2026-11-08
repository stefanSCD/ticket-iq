# REQ-011 – REQ-012 – Link-Loss Reconnection

| Field | Value |
|---|---|
| Page ID | PC-020 |
| Owner | Mara Lindqvist |
| Implemented by | COMP-002 Bluetooth Connection Manager |
| Status | Approved |

## Requirements

**REQ-011** – When the connection to a phone is lost unintentionally while the ignition is on, the system shall attempt to reconnect the phone automatically.

**REQ-012** – The system shall detect a link loss within 3 seconds, using the supervision timeout of the ACL link.

## Distinguishing link loss from intended disconnection

| Disconnect reason (HCI) | Classification |
|---|---|
| 0x08 Connection timeout | Link loss |
| 0x13 Remote user terminated connection | Intended (user) |
| 0x16 Connection terminated by local host | Intended (vehicle) |
| 0x15 Remote device terminated due to power off | Intended (phone) |

Only link loss triggers REQ-011.

## Example

The driver stops at a gas station, leaves the vehicle with the phone while the engine is running, and returns after 4 minutes. The connection is lost after the phone leaves the range; when the driver returns, the phone shall reconnect without user interaction.

## Open point

The number of reconnection attempts after a link loss and the total time after which the system stops trying are **not yet defined**. The ignition-based give-up timer (PC-042) was designed for the startup case and was not intended for link loss. To be decided by Tobias Kern and Mara Lindqvist.

## Verification

Link-loss tests are planned in HiL using the RF attenuator to simulate the phone leaving the range (see PC-068).
