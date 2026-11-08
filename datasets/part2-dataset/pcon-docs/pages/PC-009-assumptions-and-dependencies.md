# Assumptions and Dependencies

| Field | Value |
|---|---|
| Page ID | PC-009 |
| Owner | Tobias Kern |
| Last updated | 2026-06-05 |

## Assumptions

- A1: Phones used by customers support Bluetooth 4.2 or newer and HFP 1.6 or newer.
- A2: The Bluetooth controller of HU4 is ready within 3 seconds after the application processor boots.
- A3: The vehicle provides KL15 and power mode signals over SOME/IP within 200 ms of a change.
- A4: The driver's phone is located inside or within 5 m of the vehicle when the ignition is switched on.
- A5: The HMI Platform renders connection state changes within 300 ms of receiving them.

## Dependencies

| ID | Dependency | Provider | Needed for |
|---|---|---|---|
| D1 | Nimbus BT Stack 5.2 with patches | Sylvan Wireless | All connectivity functions |
| D2 | VehicleStateSrv SOME/IP service | Vehicle Integration team | COMP-001 |
| D3 | HSM key wrapping API | Platform Security team | COMP-003 |
| D4 | HMI device list and status bar | HMI Platform team | COMP-008 |
| D5 | Diagnostics Platform DTC API | Diagnostics Platform team | COMP-005 |
| D6 | Persistent storage partition `/persist/bt/` | Platform team | COMP-003, COMP-007 |
| D7 | HiL benches HIL-BT-01/02 | Test infrastructure | HiL regression |

Changes in any dependency are reported in the architecture sync (see meeting notes PC-058 ff.).
