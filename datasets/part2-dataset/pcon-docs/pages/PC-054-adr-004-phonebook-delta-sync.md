# ADR-004 – Delta Synchronization of the Phonebook

| Field | Value |
|---|---|
| Page ID | PC-054 |
| Status | **Accepted** (2026-07-22) |
| Deciders | Ioana Marin, Tobias Kern, Andrei Popescu |

## Context

Downloading the complete phonebook on each connection takes up to several minutes for large phonebooks, creates load on the Bluetooth link during startup, and consumes memory (RSK-07). PBAP 1.2 provides a database identifier and folder version counters that allow a client to detect changes.

## Decision

COMP-007 uses **delta synchronization**:

1. On connection, read the PBAP *database identifier* and the *primary/secondary folder version counters*.
2. If the database identifier is unchanged and the counters are unchanged, keep the local copy – no download.
3. If counters changed, download only the vCard listing with handles and download vCards that are new or changed.
4. If the database identifier changed, or the phone does not support PBAP 1.2 features, fall back to a full download.

Call history is always downloaded completely, because the lists are short.

## Consequences

- Typical reconnection with an unchanged phonebook needs no phonebook transfer.
- COMP-007 must store the database identifier and counters per phone.
- Memory profiling was done with a reference phonebook of 5,000 contacts.

## Not covered

The ADR does not define how many contacts the vehicle stores at most.
