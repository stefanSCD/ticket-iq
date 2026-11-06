# Audit records and data retention — Workflow

Document ID: `TN-AUD-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The audit trail explains sensitive actions without becoming a second copy of all borrower content. Operational retention and account deletion must preserve required transaction references while limiting unnecessary personal data.

## Requirements and guidance

### TN-AUD-WF-01

The audit viewer filters by lab, action, resource ID, and UTC time interval.

### TN-AUD-WF-02

A correction to a sensitive record produces a new audit event rather than modifying the earlier audit event.

### TN-AUD-WF-03

The account deletion screen lists blocking transaction references visible to the requesting borrower.

### TN-AUD-WF-04

A legal-hold process is proposed, but who can place a hold and which records it covers are not agreed.
