# REQ-001 – Automatic Reconnection after Ignition

| Field | Value |
|---|---|
| Page ID | PC-012 |
| Requirement | REQ-001 |
| Priority | High |
| Status | Approved |
| Implemented by | COMP-001 Vehicle State Adapter, COMP-002 Bluetooth Connection Manager |
| Verified by | TEST-001, TEST-007, TEST-009 |

## Requirement text

> The system shall automatically reconnect a previously paired phone after the vehicle ignition is switched on.

## Clarifications

- "Automatically" means without any interaction by the driver, either in the vehicle HMI or on the phone.
- "Previously paired" means the phone is present in the pairing list stored by the Pairing Data Store (COMP-003) and the stored link key is valid.
- The trigger is the transition of KL15 from OFF to ON as reported by the Vehicle State Adapter.
- If several paired phones are in range, the multi-phone priority rules in PC-019 apply.
- If the phone becomes available only after the vehicle has started (e.g. the driver enables Bluetooth later), the reconnection shall still happen. This is covered by TEST-009 (phone available three seconds after ignition).

## Preconditions

- The phone was paired with the vehicle before the ignition was switched off.
- Bluetooth is enabled on the phone.
- The phone is inside or close to the vehicle.
- Pairing information is still stored by the infotainment system.

## Acceptance criteria

1. After KL15 ON and BT_READY, COMP-002 starts a connection attempt to the highest-priority paired phone.
2. The phone is shown as connected in the HMI without any user action.
3. The driver is not asked to confirm the connection.

## Related scenarios raised in review

During the requirements review on 2026-06-17 (PC-059) the following situations were mentioned as relevant to REQ-001:

- the driver enters the vehicle while already in a phone call on the phone;
- the phone is connected to another vehicle or a headset at the time of ignition;
- the phone has Bluetooth enabled but is in a low-power mode.

These situations are listed for completeness; the requirement text above applies unchanged.
