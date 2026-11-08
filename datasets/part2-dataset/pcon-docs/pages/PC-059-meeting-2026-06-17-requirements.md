# Meeting Notes – Requirements Clarification 2026-06-17

| Field | Value |
|---|---|
| Page ID | PC-059 |
| Participants | Mara Lindqvist, Tobias Kern, Sofia Brandt, Jonas Weber, Andrei Popescu |

## Agenda

1. REQ-002 measurement interval
2. Comfort mode
3. REQ-007 Bluetooth-disabled phones
4. Scenarios around REQ-001

## Notes

**1. REQ-002** – Sofia asked for a precise start event. Agreed: BT_READY, as written in the requirement. Tobias will add the clarification to the requirement page.

**2. Comfort mode** – Jonas reported that the HMI is already visible in comfort mode and customers might expect the phone to be connected at that time. Mara is concerned about quiescent current and about connecting phones of people who only open the trunk. No decision; Mara will check with Product Management and the Energy Management team.

**3. REQ-007** – Discussion of detection methods (give-up timer, BLE advertising, disconnect reason). No method could be confirmed as reliable across iOS and Android. REQ-007 stays in draft; R1 or R2 assignment open.

**4. Scenarios around REQ-001** – Collected: phone already in a call when entering the vehicle; phone connected to another car or headset; phone in power-saving mode. Sofia will consider them for exploratory testing.

## Action items

| Action | Owner | Due |
|---|---|---|
| Add t0 clarification to REQ-002 page | Tobias Kern | 2026-06-24 |
| Ask Energy Management about comfort mode | Mara Lindqvist | 2026-07-01 |
| Exploratory test charter for REQ-001 scenarios | Sofia Brandt | 2026-07-08 |
