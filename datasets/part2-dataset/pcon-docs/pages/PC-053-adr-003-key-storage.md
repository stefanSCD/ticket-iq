# ADR-003 – Encrypted Link-Key Storage with HSM Key Wrapping

| Field | Value |
|---|---|
| Page ID | PC-053 |
| Status | **Accepted** (2026-07-08) |
| Deciders | Karim Haddad, Tobias Kern, Felix Wagner |

## Context

Bluetooth link keys allow impersonation of a paired phone if they are extracted from the vehicle. The TARA (PC-095) rated link-key extraction from flash as a relevant threat. REQ-022 requires encrypted storage.

## Options

1. Rely on the encrypted partition `/persist/bt/` only.
2. **Wrap each link key with a key held in the HSM** and store only the wrapped key.
3. Store link keys inside the HSM secure storage.

## Decision

Option 2. Each link key is wrapped with **AES-256-GCM** using a device-unique wrapping key that never leaves the HSM. The wrapped key is stored by COMP-003; unwrapping happens at connection time and the plain key is passed only to COMP-009 in memory.

## Rationale

- Option 1 protects against offline flash reading only if the partition key is safe; defense in depth is required by Cybersecurity.
- Option 3 is limited by HSM secure storage capacity (16 slots) and slow write performance.

## Consequences

- Every reconnection needs an HSM unwrap operation (measured: 4–7 ms).
- COMP-003 depends on the HSM being available during startup.

## Open point

The behavior when the HSM is not available or returns an error during startup (e.g. HSM firmware update in progress, HSM self-test failure) is **not defined**. Options discussed: delay reconnection until the HSM is available, or skip automatic reconnection for this ignition cycle. Owner: Karim Haddad.
