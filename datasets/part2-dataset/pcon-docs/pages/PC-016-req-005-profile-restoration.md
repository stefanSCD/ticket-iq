# REQ-005 – Restore Supported Bluetooth Profiles

| Field | Value |
|---|---|
| Page ID | PC-016 |
| Requirement | REQ-005 |
| Priority | High |
| Status | Approved |
| Implemented by | COMP-004 Bluetooth Profile Service |
| Verified by | TEST-005 |

## Requirement text

> After reconnection, the system shall restore the supported phone and media audio profiles.

## Profiles in scope

| Profile | Version supported by HU4 | Purpose |
|---|---|---|
| HFP | 1.8 | Phone calls (phone audio) |
| A2DP | 1.3 | Media audio |
| AVRCP | 1.6 | Media control and metadata |
| PBAP | 1.2 | Phonebook (see REQ-014) |
| MAP | 1.4 | Messages (REQ-017, draft) |

"Supported" means supported by both the head unit and the phone, as reported in the phone's SDP record.

## Behavior

- HFP is restored for every connected phone.
- A2DP and AVRCP are restored for the primary phone only (see multi-phone rules, PC-019). AVRCP is always restored together with A2DP.
- If a profile cannot be restored, the phone is shown as "Partially connected" (see PC-027).

## AVRCP features

AVRCP 1.6 offers play/pause/skip, track metadata, cover art and media browsing. Play/pause/skip and track metadata are used by the HMI media widget today. Cover art is shown in the media player screen.

## Acceptance criteria

1. After reconnection, HFP is available for all phones that support it.
2. A2DP and AVRCP are available for the primary phone if supported.
3. Partial restoration is reported to the HMI.
