# COMP-007 – Phonebook Sync Service

| Field | Value |
|---|---|
| Page ID | PC-038 |
| Component | COMP-007 |
| Version | 1.1.0 |
| Owner | Ioana Marin |
| Implements | REQ-014, REQ-015, REQ-016, REQ-024 |

## Responsibility

Downloads contacts and call history of the primary phone through PBAP and provides them to the HMI.

## Synchronization

On each connection of the primary phone, COMP-007 performs a **full synchronization**: the complete phonebook (`telecom/pb.vcf`) and the call history lists (`ich`, `och`, `mch`) are downloaded, and the local copy is replaced after the download completed successfully.

## Progressive availability

Contacts are written to the local database in batches of 100 so that search is available after the first batch (REQ-016).

## Storage

- SQLite database in `/persist/bt/phonebook/<deviceIdHash>.db`.
- Photos are stored as JPEG thumbnails (96×96).

## Failure handling

- If the phone denies access, COMP-007 reports `ACCESS_DENIED` to COMP-008.
- If the PBAP session is closed by the phone, the previous local copy is kept.
- Some phones stop responding during long transfers; COMP-007 then waits for the PBAP session to be closed.

## Deletion

On `RemoveDevice` from COMP-003, the database file of that phone is deleted.
