# COMP-003 – Pairing Data Store

| Field | Value |
|---|---|
| Page ID | PC-034 |
| Component | COMP-003 |
| Version | 1.4.1 |
| Owner | Felix Wagner |
| Implements | REQ-003, REQ-022, REQ-024, REQ-025 |

## Responsibility

Stores and retrieves pairing credentials and metadata for previously paired Bluetooth devices.

## Capacity

- The store holds **up to 10 paired devices**.
- When an eleventh device is paired, the **least recently used** device (oldest last-connection timestamp) is removed automatically together with its phonebook data.

## Storage

- Location: encrypted partition `/persist/bt/pairing/`.
- Format: one record per device, protobuf-encoded.
- Link keys are stored only in wrapped form; unwrapping is done by the HSM at connection time (ADR-003, PC-053).
- Writes are atomic (write to temp file + rename).

## API (IPC)

| Message | Description |
|---|---|
| `GetPairedDevices()` | Returns all records without keys |
| `GetLinkKey(deviceId)` | Returns the unwrapped key to COMP-009 only |
| `UpdateLastConnected(deviceId, ts)` | Called by COMP-002 after successful connection |
| `RemoveDevice(deviceId)` | Unpair; triggers deletion in COMP-007 |
| `FactoryReset()` | Deletes all records and all connectivity settings |

## Data lifecycle

| Event | Effect |
|---|---|
| Unpair from HMI | Record and phonebook of that phone deleted |
| Factory reset | All records, phonebooks and settings deleted |
| Pairing list full | LRU device removed |
| Vehicle owner change | **Not defined** – see open point in PC-026 |

## Synchronization with user accounts

The HMI Platform introduces user profiles for Meridian. The pairing list is currently stored per vehicle, not per user profile.
