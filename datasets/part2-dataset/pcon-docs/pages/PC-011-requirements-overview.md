# Requirements Overview and Traceability Rules

| Field | Value |
|---|---|
| Page ID | PC-011 |
| Owner | Mara Lindqvist |
| Last updated | 2026-07-15 |

## Source of requirements

Requirements are maintained in the RequirementsSystem and mirrored to this space for readability. In case of doubt, the RequirementsSystem export is the formal baseline. Each requirement has an ID (REQ-xxx), a title, a description, a priority (Critical, High, Medium, Low) and a status (Draft, Approved, Rejected, Obsolete).

## Requirement list R1

| ID | Title | Priority | Status | Page |
|---|---|---|---|---|
| REQ-001 | Automatic reconnection after ignition | High | Approved | PC-012 |
| REQ-002 | Reconnection within ten seconds | Critical | Approved | PC-013 |
| REQ-003 | Reuse stored pairing information | High | Approved | PC-014 |
| REQ-004 | Transient reconnection retry | Medium | Approved | PC-015 |
| REQ-005 | Restore supported Bluetooth profiles | High | Approved | PC-016 |
| REQ-006 | Record reconnection diagnostics | Medium | Approved | PC-017 |
| REQ-007 | Handle Bluetooth-disabled phones | Low | Draft | PC-018 |
| REQ-008 – REQ-010 | Multi-phone handling | High | Approved | PC-019 |
| REQ-011 – REQ-012 | Link-loss reconnection | High | Approved | PC-020 |
| REQ-013 | Manual reconnection | Medium | Approved | PC-021 |
| REQ-014 – REQ-016 | Phonebook synchronization | Medium | Approved | PC-022 |
| REQ-017 | Message access | Low | Draft | PC-023 |
| REQ-018 – REQ-020 | Power modes | High | Approved | PC-024 |
| REQ-021 – REQ-023 | Security | High | Approved | PC-025 |
| REQ-024 – REQ-025 | Privacy | High | Approved | PC-026 |
| REQ-026 – REQ-027 | HMI status | Medium | Approved | PC-027 |
| REQ-028 | Projection coexistence | Medium | Approved | PC-028 |
| REQ-029 – REQ-030 | Non-functional | High | Approved | PC-029 |

## Traceability rules

1. Every approved requirement is implemented by at least one software component (relationship *IMPLEMENTS*).
2. Every approved requirement is verified by at least one test (relationship *VERIFIES*).
3. Every test execution belongs to exactly one test; every trace belongs to exactly one execution.
4. Every defect is linked to at least one failed execution and to at least one affected component.
5. Draft requirements may be implemented, but they are not part of the release verification.

These rules are checked automatically by the data-quality validation before the traceability graph is rebuilt.

## Coverage status

For REQ-001 … REQ-007 the coverage is as follows: REQ-001 to REQ-006 are verified by TEST-001 … TEST-010. **REQ-007 has no test** because it is still in draft. Test coverage for REQ-008 … REQ-030 is tracked in the test catalogs PC-071 – PC-073.
