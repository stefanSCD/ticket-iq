# Persistence and Storage Layout

| Field | Value |
|---|---|
| Page ID | PC-047 |
| Owner | Felix Wagner |
| Last updated | 2026-07-09 |

All persistent connectivity data is stored in the encrypted partition **`/persist/bt/`** (dm-crypt, key bound to the HU4 hardware).

```
/persist/bt/
  pairing/            COMP-003 records (protobuf), one file per device
  phonebook/          COMP-007 SQLite DBs, one per device (<deviceIdHash>.db)
  diag/               COMP-005 ring buffer file
  settings.json       Connectivity settings (per vehicle)
  stack/              Nimbus stack internal files (do not edit)
```

## Rules

- Only the owning component writes to its folder.
- Writes are atomic (temp file + rename) for pairing and settings.
- The SQLite DBs use WAL mode.
- The budget for the whole partition is 64 MB (REQ-029).

## Backup

There is no backup of `/persist/bt/`. After a head unit replacement in the workshop, phones must be paired again.

## Factory reset

`FactoryReset()` of COMP-003 removes `pairing/`, `phonebook/` and `settings.json`, and clears the ring buffer in `diag/`.
