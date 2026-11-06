# Audit records and data retention — Architecture decision

Document ID: `TN-AUD-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The audit trail explains sensitive actions without becoming a second copy of all borrower content. Operational retention and account deletion must preserve required transaction references while limiting unnecessary personal data.

## Requirements and guidance

### TN-AUD-ADR-01

Audit event storage is separate from editable application notes and uses append-only writer permissions.

### TN-AUD-ADR-02

An audit_reader grant does not imply incident_reader access to photographs or private incident notes.

### TN-AUD-ADR-03

Ordinary audit retention is independent of operational backup rotation.
