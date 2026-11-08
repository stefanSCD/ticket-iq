# Risk Register

| Field | Value |
|---|---|
| Page ID | PC-008 |
| Owner | Mara Lindqvist |
| Last updated | 2026-09-10 |

| ID | Risk | Probability | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| RSK-01 | Reconnection time above 10 s in vehicle due to stack queueing | High | High | DEF-001 fix (priority queue) in COMP-002 2.3.1 | Radu Ionescu |
| RSK-02 | Supplier response for stack defects too slow for C-Sample | Medium | High | Weekly supplier sync, early reporting | Tobias Kern |
| RSK-03 | New phone OS releases change reconnection behavior | High | Medium | Reference phone list review each quarter | Sofia Brandt |
| RSK-04 | Only two HiL benches available for the whole connectivity domain | Medium | Medium | Night runs, bench booking discipline | Daniel Szabo |
| RSK-05 | Bluetooth SIG qualification delayed | Low | High | Start qualification preparation in Q4 2026 | Tobias Kern |
| RSK-06 | HSM key handling issues on early HU4 hardware | Medium | High | Early integration tests with Security team | Felix Wagner |
| RSK-07 | Phonebook sync memory consumption for very large phonebooks | Medium | Medium | Delta sync (ADR-004), memory profiling | Ioana Marin |
| RSK-08 | Diagnostic event loss at shutdown | Medium | Low | DEF-002 investigation | Elena Rusu |

Risks are reviewed in the sprint review every second sprint.
