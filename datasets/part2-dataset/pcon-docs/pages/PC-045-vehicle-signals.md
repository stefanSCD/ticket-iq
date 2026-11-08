# Vehicle Signals Used by PCON

| Field | Value |
|---|---|
| Page ID | PC-045 |
| Owner | Felix Wagner |
| Last updated | 2026-06-24 |

| Signal | Service / Event | Cycle | Consumer |
|---|---|---|---|
| KL15_Status | VehicleStateSrv / evKl15 | On change + 1 s cyclic | COMP-001 |
| PowerMode | VehicleStateSrv / evPowerMode | On change | COMP-001 |
| VehicleSpeed | VehicleStateSrv / evSpeed | 100 ms | COMP-001 |
| DriverDoorOpen | BodySrv / evDoors | On change | not used in R1 |
| BatteryVoltage | PlatformPowerSrv | 100 ms | COMP-010 |

## SOME/IP details

- Service `VehicleStateSrv` – service ID 0x4A10, instance 1, major version 2.
- Event group 1 contains KL15_Status and PowerMode.
- COMP-001 subscribes at startup and reads current values via the getter methods.

## Signal quality

If a signal is marked invalid (quality bit), COMP-001 keeps the last valid value and logs a warning. After 5 s with invalid KL15, the fallback described in PC-032 applies.
