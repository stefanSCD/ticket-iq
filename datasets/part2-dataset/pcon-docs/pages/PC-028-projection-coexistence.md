# REQ-028 – Coexistence with CarPlay and Android Auto

| Field | Value |
|---|---|
| Page ID | PC-028 |
| Owner | Tobias Kern |
| Status | Approved |

## Requirement

**REQ-028** – When a phone is used with wireless Apple CarPlay or wireless Android Auto, the system shall keep the Bluetooth HFP connection to that phone established, and shall not start A2DP for that phone.

## Background

CarPlay and Android Auto are delivered by the Projection team and are out of scope for PCON. Wireless projection uses Bluetooth for the initial discovery and for call signaling; media is streamed over Wi-Fi. If PCON connected A2DP in parallel, audio could be played twice or the phone could switch audio routing unexpectedly.

## Behavior

1. COMP-002 reconnects the phone as usual after ignition.
2. When the projection session starts, the phone is marked as `projection active`.
3. A2DP and AVRCP are not restored (or are disconnected if already established).
4. HFP remains connected.
5. When the projection session ends, A2DP restoration is triggered.

## Handover

The exact handover between the Projection stack and PCON (who sends the `projection active` information, and which component on PCON side consumes it) is still being aligned with the Projection team. Candidates on PCON side are COMP-002 and COMP-004.
