# COMP-010 – Power Mode Manager Interface

| Field | Value |
|---|---|
| Page ID | PC-041 |
| Component | COMP-010 |
| Version | 1.0.0 |
| Owner | Felix Wagner |
| Implements | REQ-018, REQ-019 |

## Responsibility

Connects PCON to the platform power management. Provides battery voltage information and shutdown notifications to COMP-002, and keeps the shutdown of the connectivity domain within the time granted by the platform.

## Inputs from the platform

| Input | Description |
|---|---|
| `BatteryVoltage` | Measured at the head unit supply, 10 Hz |
| `ShutdownRequest` | Infotainment is going to shut down; PCON has 800 ms to finish |
| `PowerMode` | Forwarded from COMP-001 |

## Low-voltage handling

COMP-010 sends `LowVoltage(true)` to COMP-002 when `BatteryVoltage` falls below **8.5 V** for more than 50 ms. COMP-002 then suspends all connection attempts (`SUSPENDED`).

When the voltage is back in the normal range, COMP-010 sends `LowVoltage(false)`.

## Shutdown handling

1. Receive `ShutdownRequest`.
2. Ask COMP-002 to disconnect all phones (REQ-019).
3. Ask COMP-005 to flush the event buffer.
4. Confirm shutdown to the platform.

If step 2 or 3 is not completed within 800 ms, COMP-010 confirms anyway. This can interrupt the flush of diagnostic events (see DEF-002, PC-085).

## Comfort mode

COMP-010 forwards `PowerMode = COMFORT` to COMP-002. COMP-002 currently ignores it; whether comfort mode should trigger automatic reconnection is an open decision (see PC-024).
