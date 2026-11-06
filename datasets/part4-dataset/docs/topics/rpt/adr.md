# Reports, calendars, and exports — Architecture decision

Document ID: `TN-RPT-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Managers use operational reports to understand completed loans and missed pickups. Reports preserve the distinction between a UTC event instant and a local calendar date, especially when the university changes daylight-saving offset.

## Requirements and guidance

### TN-RPT-ADR-01

Completed-loan reporting uses receivedAt rather than inspection completion time.

### TN-RPT-ADR-02

Report workers operate on committed source records; a cached chart is not an authoritative loan record.

### TN-RPT-ADR-03

Each report job stores the normalized UTC boundaries and the input lab time zone for reproducibility.
