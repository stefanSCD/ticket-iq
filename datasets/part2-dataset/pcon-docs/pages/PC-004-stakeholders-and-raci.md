# Stakeholders and RACI

| Field | Value |
|---|---|
| Page ID | PC-004 |
| Owner | Mara Lindqvist |
| Last updated | 2026-07-01 |

## Core team

| Name | Role | Main responsibility |
|---|---|---|
| Mara Lindqvist | Product Owner | Backlog, scope, feature acceptance; owner of FEAT-001 |
| Tobias Kern | System Architect | Architecture, ADRs, Bluetooth SIG qualification |
| Andrei Popescu | Tech Lead | Technical direction, code reviews, integration |
| Radu Ionescu | Developer | COMP-002 Bluetooth Connection Manager, COMP-006 Device Priority Manager |
| Nina Hoffmann | Developer | COMP-004 Bluetooth Profile Service |
| Felix Wagner | Developer | COMP-003 Pairing Data Store, COMP-001 Vehicle State Adapter |
| Ioana Marin | Developer | COMP-007 Phonebook Sync Service |
| Elena Rusu | Developer / Diagnostics owner | COMP-005 Connectivity Diagnostics Service, DTCs |
| Sofia Brandt | Test Lead | Test strategy, HiL and vehicle test planning |
| Daniel Szabo | HiL bench engineer (50%) | Bench setup and maintenance |
| Lukas Becker | Vehicle test engineer | Vehicle executions, field test |

## External stakeholders

| Name | Organization | Topic |
|---|---|---|
| Jonas Weber | HMI Platform team | HMI rendering of connectivity information, COMP-008 interface |
| Karim Haddad | Cybersecurity | TARA, pairing security, key storage |
| Petra Novak | Release Management | Milestones, release notes, freeze dates |
| Liam O'Connor | Sylvan Wireless | Nimbus BT Stack support |

## RACI

| Activity | Mara | Tobias | Andrei | Sofia | Petra | Karim |
|---|---|---|---|---|---|---|
| Requirement approval | A | C | C | C | I | C |
| Architecture decisions (ADR) | I | A | R | C | I | C |
| Test strategy | C | C | C | A/R | I | I |
| Release sign-off | A | C | R | R | R | C |
| Security concept | I | C | C | I | I | A/R |
| Defect triage | A | C | R | R | I | I |
| Supplier communication | I | A | R | I | I | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed.
