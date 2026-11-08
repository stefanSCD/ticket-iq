# REQ-018 – REQ-020 – Power Modes and Low Voltage

| Field | Value |
|---|---|
| Page ID | PC-024 |
| Owner | Tobias Kern |
| Implemented by | COMP-010 Power Mode Manager interface, COMP-002 |
| Status | Approved |

## Requirements

**REQ-018** – The system shall suspend automatic reconnection attempts when the vehicle battery voltage drops below **9.0 V**.

**REQ-019** – The system shall disconnect all phones in an orderly way when the infotainment system enters shutdown.

**REQ-020** – The system shall not start reconnection attempts before the Bluetooth subsystem reports BT_READY.

## Low-voltage behavior

Low voltage typically occurs during engine cranking (cold start). While the voltage is below the threshold, COMP-002 enters the `SUSPENDED` state. Ongoing connection attempts are aborted without counting as a failure. When the voltage recovers, reconnection continues from the beginning.

## Vehicle modes

| Mode | Description | PCON behavior |
|---|---|---|
| Ignition ON | KL15 active | Automatic reconnection (REQ-001) |
| Shutdown | Infotainment shutting down | Orderly disconnect (REQ-019) |
| Comfort mode | Infotainment running without KL15, e.g. door opened | **Open point** |
| Transport mode | Logistics/factory mode | Bluetooth stack is started |
| OTA installation | Software update being installed | Infotainment HMI shows the update progress screen |

### Open point: comfort mode

It is not decided whether automatic reconnection shall already start in comfort mode (driver opens the door, infotainment wakes up) or only at KL15 ON. Starting earlier would improve the perceived reconnection time, but increases quiescent current and may connect a phone of a person who is only loading the trunk. Decision owner: Mara Lindqvist.

## Ignition off with active call

When the ignition is switched off, the infotainment system enters its run-on phase. Calls that are active at this moment continue on the vehicle audio during run-on. The run-on duration is defined by the Platform team.
