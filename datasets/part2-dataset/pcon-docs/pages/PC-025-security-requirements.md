# REQ-021 – REQ-023 – Security

| Field | Value |
|---|---|
| Page ID | PC-025 |
| Owner | Karim Haddad |
| Implemented by | COMP-003 Pairing Data Store, COMP-009 BT Stack Adapter |
| Status | Approved |

## Requirements

**REQ-021** – The system shall pair phones only with Secure Simple Pairing using the Numeric Comparison association model.

**REQ-022** – The system shall store link keys only in encrypted form, protected by a key held in the HSM.

**REQ-023** – The system shall reject connection requests from unpaired devices for HFP, A2DP, AVRCP, PBAP and MAP.

## Details

- Legacy PIN pairing (Bluetooth 2.0 and earlier) is **not supported**.
- "Just Works" pairing is not allowed for phones.
- Link keys are wrapped with AES-256-GCM using a device-unique key that never leaves the HSM (see ADR-003, PC-053).
- Connection requests from unknown devices are rejected at the stack level; no HMI notification is shown.
- Pairing is only possible while the vehicle is stationary (speed < 3 km/h); this rule is enforced by the HMI Platform.

## Threat references

The requirements are derived from the TARA summarized in PC-095. Relevant threats: link-key extraction from flash, impersonation of a paired phone, and denial of service by repeated connection requests.

## Older phones

A small share of customers still uses phones that only support Bluetooth versions before 2.1. These phones cannot complete pairing with HU4.
