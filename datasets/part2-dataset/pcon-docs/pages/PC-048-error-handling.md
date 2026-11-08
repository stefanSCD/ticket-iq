# Error Handling and Error Codes

| Field | Value |
|---|---|
| Page ID | PC-048 |
| Owner | Radu Ionescu |
| Last updated | 2026-08-12 |

## PCON result codes

| Code | Name | Meaning |
|---|---|---|
| 0 | OK | Success |
| 1 | E_TRANSIENT | Transient communication error – eligible for retry (REQ-004) |
| 2 | E_AUTH | Authentication failed (key missing or rejected) |
| 3 | E_NOT_REACHABLE | Page timeout after retry |
| 4 | E_PROFILE | Profile could not be restored |
| 5 | E_INTERNAL | Internal error in PCON or stack |
| 6 | E_CANCELLED | Attempt cancelled (ignition off, low voltage) |

## Mapping of HCI errors

| HCI error | Name | PCON code | Transient? |
|---|---|---|---|
| 0x04 | Page timeout | E_TRANSIENT | Yes |
| 0x08 | Connection timeout | E_TRANSIENT | Yes |
| 0x22 | LMP response timeout | E_TRANSIENT | Yes |
| 0x05 | Authentication failure | E_AUTH | No |
| 0x06 | PIN or key missing | E_AUTH | No |
| 0x0D–0x0F | Connection rejected (resources/security/address) | E_INTERNAL | No |

## Errors observed but not yet classified

The following HCI errors have been seen in HiL and vehicle traces during connection setup but are not yet mapped:

- 0x0B – ACL connection already exists
- 0x0C – Command disallowed

Until they are classified, COMP-009 maps them to E_INTERNAL.

## Logging

Every error is logged with the HCI code and the PCON code (PC-049).
