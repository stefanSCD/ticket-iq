# Movement between university labs — Architecture decision

Document ID: `TN-XFR-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The multi-lab release tracks physical custody separately from ownership. Moving an asset between labs must not lose the source and destination acknowledgements or silently move a borrower's confirmed pickup location.

## Requirements and guidance

### TN-XFR-ADR-01

Current location, owning department, and reservation pickup lab are distinct fields.

### TN-XFR-ADR-02

Transfer custody events are append-only and reference immutable asset UUIDs.

### TN-XFR-ADR-03

A transfer is not treated as a borrower loan and creates no borrower overdue record.
