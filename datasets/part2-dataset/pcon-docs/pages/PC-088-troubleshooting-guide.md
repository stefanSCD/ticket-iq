# Troubleshooting Guide for Testers

| Field | Value |
|---|---|
| Page ID | PC-088 |
| Owner | Sofia Brandt |
| Last updated | 2026-09-10 |

## Phone does not reconnect after ignition

1. Check the status icon: grey = disconnected, animated = still trying.
2. Check that Bluetooth is enabled on the phone and the phone is not connected to another device.
3. Check in the trace whether `BT_READY` was reached.
4. If the trace shows authentication failure (HCI 0x05/0x06), the phone has probably deleted the vehicle. Remove the vehicle on the phone and the phone in the vehicle, then pair again.
5. If the trace shows long queue waits, attach the trace to DEF-001 (if SW < 2.3.1).

## Phone connected but no media audio

- Check the HMI shows "Partially connected".
- On SW with COMP-004 3.1.0, this is DEF-003; update to 3.1.1.
- If the phone is used with CarPlay/Android Auto, A2DP is intentionally not used (REQ-028).

## No contacts

- Check contact sharing permission on the phone.
- Check PhonebookStatus in the trace.

## Reconnection takes long only on one bench

- Check the attenuator setting; after link-loss tests it may still be at a high value.
- Check for other phones in the room (LIM-03).

## Collecting data for a bug

Software version, environment, execution ID, phone model and OS, trace file, diagnostic events (`ReadConnectivityEvents`).
