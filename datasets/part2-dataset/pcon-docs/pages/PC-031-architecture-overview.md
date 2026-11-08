# Architecture Overview

| Field | Value |
|---|---|
| Page ID | PC-031 |
| Owner | Tobias Kern |
| Last updated | 2026-08-20 |

## Layering

The connectivity domain is organized in three layers:

1. **Adapter layer** – isolates PCON from external systems: Vehicle State Adapter (vehicle network), BT Stack Adapter (Nimbus BT Stack), Power Mode Manager interface (platform power management).
2. **Service layer** – implements the connectivity logic: Bluetooth Connection Manager, Device Priority Manager, Bluetooth Profile Service, Phonebook Sync Service, Pairing Data Store, Connectivity Diagnostics Service.
3. **Presentation layer** – HMI Connectivity Presenter, which offers a stable API to the HMI Platform.

## Components

| ID | Name | Version (R1 baseline) | Owner | Page |
|---|---|---|---|---|
| COMP-001 | Vehicle State Adapter | 1.2.0 | Felix Wagner | PC-032 |
| COMP-002 | Bluetooth Connection Manager | 2.3.0 | Radu Ionescu | PC-033 |
| COMP-003 | Pairing Data Store | 1.4.1 | Felix Wagner | PC-034 |
| COMP-004 | Bluetooth Profile Service | 3.1.0 | Nina Hoffmann | PC-035 |
| COMP-005 | Connectivity Diagnostics Service | 1.2.0 | Elena Rusu | PC-036 |
| COMP-006 | Device Priority Manager | 1.0.2 | Radu Ionescu | PC-037 |
| COMP-007 | Phonebook Sync Service | 1.1.0 | Ioana Marin | PC-038 |
| COMP-008 | HMI Connectivity Presenter | 1.3.0 | Jonas Weber / Andrei Popescu | PC-039 |
| COMP-009 | BT Stack Adapter | 2.0.4 | Andrei Popescu | PC-040 |
| COMP-010 | Power Mode Manager interface | 1.0.0 | Felix Wagner | PC-041 |

## Main data flow at startup

`KL15 ON → COMP-001 → COMP-002`; `BT_READY (COMP-009) → COMP-002`; `COMP-002 → COMP-006 (priority list) → COMP-003 (keys) → COMP-009 (connect) → COMP-004 (profiles) → COMP-007 (phonebook)`; status changes go to COMP-008 and diagnostic events to COMP-005.

The detailed sequence is shown in PC-043, the state machine of COMP-002 in PC-042.

## Communication

- Components communicate over the internal IPC bus (message catalog: PC-044).
- External vehicle signals arrive via SOME/IP (PC-045).
- No component except COMP-009 calls the Nimbus BT Stack API directly.

## Design principles

- One owner per component; interfaces documented on the component page.
- Configuration through coded parameters (PC-046), not through compile-time constants.
- Every state transition of COMP-002 is traced (PC-049).
