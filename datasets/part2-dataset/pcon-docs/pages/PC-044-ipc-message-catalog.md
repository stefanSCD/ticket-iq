# Internal IPC Message Catalog

| Field | Value |
|---|---|
| Page ID | PC-044 |
| Owner | Andrei Popescu |
| Last updated | 2026-08-01 |

All connectivity components communicate over the platform IPC bus. Messages are defined in `pcon-connectivity/interfaces/pcon.proto`.

| Message | Producer | Consumers | Content |
|---|---|---|---|
| IgnitionChanged | COMP-001 | COMP-002 | state, timestamp |
| PowerModeChanged | COMP-001 | COMP-002, COMP-010 | mode, timestamp |
| VehicleStationary | COMP-001 | COMP-008 | bool |
| BtReady | COMP-009 | COMP-002 | timestamp |
| ConnectRequest | COMP-002 | COMP-009 | deviceId, priority |
| ConnectResult | COMP-009 | COMP-002 | deviceId, result, hciError |
| DeviceOrder | COMP-006 | COMP-002 | ordered deviceIds |
| RestoreProfiles | COMP-002 | COMP-004 | deviceId, role |
| ProfileStatus | COMP-004 | COMP-002, COMP-008 | deviceId, profile, status |
| HfpIndicators | COMP-004 | – (published, no subscriber yet) | signal, battery, roaming, service |
| PhonebookStatus | COMP-007 | COMP-008 | deviceId, status, count |
| ConnectionStateChanged | COMP-002 | COMP-008, COMP-005 | deviceId, state |
| DiagEvent | COMP-002, COMP-004 | COMP-005 | see ADR-005 |
| LowVoltage | COMP-010 | COMP-002 | bool |
| ShutdownPrepare | COMP-010 | all | deadline |

## Versioning

The proto file follows backward-compatible evolution: fields are only added, never renamed or removed. Field numbers are never reused.
