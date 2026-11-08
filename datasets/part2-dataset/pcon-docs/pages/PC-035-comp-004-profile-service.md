# COMP-004 – Bluetooth Profile Service

| Field | Value |
|---|---|
| Page ID | PC-035 |
| Component | COMP-004 |
| Version | 3.1.0 (3.1.1 delivered with DEF-003 fix) |
| Owner | Nina Hoffmann |
| Implements | REQ-005, REQ-010, REQ-028 |

## Responsibility

Restores supported Bluetooth profiles such as phone audio and media audio after a connection is established.

## Restoration order

After COMP-002 reports `CONNECTED` (ACL + HFP SLC), COMP-004 restores profiles in this order:

1. **HFP** – service level connection completion is confirmed;
2. **A2DP** – only after the HFP SLC is fully established;
3. **AVRCP** – directly after A2DP;
4. PBAP is handed over to COMP-007.

The order HFP → A2DP is mandatory since 3.1.1. Starting A2DP while the HFP SLC is still in setup caused DEF-003 (PC-086).

## Timeouts

- Each profile has a restoration timeout of **5 seconds** (parameter `BT_PROFILE_TIMEOUT_MS`).
- If a profile does not connect within its timeout, it is marked as not restored and COMP-008 shows "Partially connected".

Whether a profile that timed out should be attempted again later in the same ignition cycle is under discussion; REQ-004 does not cover profile-level failures.

## HFP indicators

COMP-004 receives HFP indicators from the phone (service, call status, signal, roaming, battery charge) and publishes them as `HfpIndicators` on the IPC bus.

## Projection

When a phone is marked `projection active`, COMP-004 does not restore A2DP/AVRCP (REQ-028).
