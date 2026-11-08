# Jira Workflow and Ticket Conventions

| Field | Value |
|---|---|
| Page ID | PC-007 |
| Owner | Andrei Popescu |
| Last updated | 2026-05-18 |

## Project

All work of the team is tracked in the Jira project **PCON**. Defects found by other teams on connectivity topics are moved into PCON by the triage meeting.

## Issue types

| Type | Use |
|---|---|
| Story | User-visible or requirement-driven change |
| Bug | Defect in delivered software (DEF-xxx in the defect tracking export) |
| Task | Technical work without direct user value |
| Spike | Time-boxed investigation |
| Decision | Scope or architecture decision that needs approval |

## Workflow

`Open → In Progress → In Review → Verification → Closed`

- **Open → In Progress**: assignee starts work.
- **In Progress → In Review**: merge request created.
- **In Review → Verification**: change merged.
- **Verification → Closed**: for Bugs, the developer who fixed the issue closes the ticket after the fix has been verified in the SiL regression run.

## Ticket conventions

- Summary: imperative, max 80 characters, component prefix in square brackets, e.g. `[COMP-002] Prioritize reconnection requests in queue`.
- Every Story and Bug links at least one requirement (REQ-xxx) or explains why none applies.
- Bugs contain: software version, environment (SiL/HiL/Vehicle), execution ID if available, trace excerpt, expected and actual behavior.
- Labels: `reconnection`, `multiphone`, `phonebook`, `diagnostics`, `hmi`, `supplier`.
- Components field in Jira uses the component name, not the COMP ID.

## Priorities

Jira priority mirrors defect severity for Bugs (see PC-083). For Stories, the Product Owner sets priority.
