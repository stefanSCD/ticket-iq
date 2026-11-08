# COMP-001 – Vehicle State Adapter

| Field | Value |
|---|---|
| Page ID | PC-032 |
| Component | COMP-001 |
| Version | 1.2.0 |
| Owner | Felix Wagner |
| Implements | REQ-001 |

## Responsibility

Receives vehicle ignition and power-state events and makes them available to the connectivity software.

## Inputs

| Signal | Source | Values |
|---|---|---|
| `KL15_Status` | SOME/IP service `VehicleStateSrv` | OFF, ON |
| `PowerMode` | SOME/IP service `VehicleStateSrv` | OFF, COMFORT, ON, CRANKING, TRANSPORT |
| `VehicleSpeed` | SOME/IP service `VehicleStateSrv` | km/h |

## Outputs (IPC)

| Message | Content |
|---|---|
| `IgnitionChanged` | new KL15 state, timestamp |
| `PowerModeChanged` | new power mode, timestamp |
| `VehicleStationary` | true when speed < 3 km/h |

## Behavior

- Debounces KL15 for 100 ms to avoid toggling during cranking.
- On startup, requests the current values from `VehicleStateSrv` instead of waiting for the next change event.
- If `VehicleStateSrv` is not available within 2 s after startup, COMP-001 assumes `KL15 = ON` and logs a warning. This fallback ensures that reconnection is not blocked by a missing vehicle service on test benches.

## Known limitations

- On HiL bench HIL-BT-02 the `VehicleStateSrv` is simulated by the restbus simulation; `PowerMode = TRANSPORT` is not simulated there.
